"""
Stock Market Search Engine - Search Module
"""
import pandas as pd
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
from dataclasses import dataclass
from tqdm import tqdm
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
import os
import json
import requests
from datetime import datetime
import uuid

@dataclass
class TextChunk:
    """Represents a chunk of text with metadata."""
    text: str
    doc_id: str  # Stock ID
    chunk_id: int  # Position in document
    metadata: Dict[str, Any]  # Additional metadata

class OpenRouterClient:
    """Client for OpenRouter API."""
    
    def __init__(self, api_key: str = None):
        """Initialize OpenRouter client.
        
        Args:
            api_key: OpenRouter API key. If None, tries to get from environment.
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key not provided and not found in environment")
        
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(self, messages: List[Dict[str, str]], model: str = "openai/gpt-3.5-turbo") -> str:
        """Get chat completion from OpenRouter.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use for completion
            
        Returns:
            Generated text response
        """
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": model,
                    "messages": messages
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error getting chat completion: {str(e)}")
            return ""

class TextChunker:
    """Handles text chunking with overlap and metadata preservation."""
    
    def __init__(self, chunk_size: int = 512, overlap: float = 0.2):
        """Initialize chunker with size and overlap parameters.
        
        Args:
            chunk_size: Maximum number of tokens per chunk
            overlap: Fraction of overlap between chunks (0-1)
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences using regex."""
        # Simple sentence splitting - can be improved with NLP libraries
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def chunk_text(self, text: str, doc_id: str, metadata: Dict[str, Any]) -> List[TextChunk]:
        """Split text into overlapping chunks with metadata.
        
        Args:
            text: Input text to chunk
            doc_id: Unique identifier for the document
            metadata: Additional metadata to store with chunks
            
        Returns:
            List of TextChunk objects
        """
        sentences = self._split_into_sentences(text)
        chunks = []
        current_chunk = []
        current_size = 0
        chunk_id = 0
        
        for sentence in sentences:
            # Rough token count (words + punctuation)
            sentence_size = len(sentence.split())
            
            if current_size + sentence_size > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_text = " ".join(current_chunk)
                chunks.append(TextChunk(
                    text=chunk_text,
                    doc_id=doc_id,
                    chunk_id=chunk_id,
                    metadata=metadata
                ))
                
                # Start new chunk with overlap
                overlap_size = int(self.chunk_size * self.overlap)
                current_chunk = current_chunk[-overlap_size:] if overlap_size > 0 else []
                current_size = sum(len(s.split()) for s in current_chunk)
                chunk_id += 1
            
            current_chunk.append(sentence)
            current_size += sentence_size
        
        # Add final chunk if any
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append(TextChunk(
                text=chunk_text,
                doc_id=doc_id,
                chunk_id=chunk_id,
                metadata=metadata
            ))
        
        return chunks

class StockSearchEngine:
    def __init__(self, data_path: str = "../data/2022_03_17_02_06_nasdaq.csv", openrouter_api_key: str = None):
        """Initialize the search engine with stock market data.
        
        Args:
            data_path: Path to the CSV file containing stock market data
            openrouter_api_key: OpenRouter API key for LLM features
        """
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunker = TextChunker(chunk_size=512, overlap=0.2)
        self.stocks_df = self._load_data(data_path)
        
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(":memory:")  # In-memory storage
        self.collection_name = "stock_chunks"
        self.vector_size = self.model.get_sentence_embedding_dimension()
        
        # Initialize OpenRouter client
        try:
            self.llm_client = OpenRouterClient(api_key=openrouter_api_key)
            self.llm_enabled = True
        except ValueError:
            print("Warning: OpenRouter API key not found. LLM features will be disabled.")
            self.llm_enabled = False
        
        # Create collection if it doesn't exist
        self._init_qdrant_collection()
        
        if not self.stocks_df.empty:
            self._prepare_and_index_chunks()

    def _init_qdrant_collection(self):
        """Initialize Qdrant collection for stock chunks."""
        try:
            # Check if collection exists
            collections = self.qdrant_client.get_collections().collections
            collection_names = [collection.name for collection in collections]
            
            if self.collection_name not in collection_names:
                # Create new collection
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )
                print(f"Created new collection: {self.collection_name}")
        except Exception as e:
            print(f"Error initializing Qdrant collection: {str(e)}")
            raise

    def _load_data(self, data_path: str) -> pd.DataFrame:
        """Load stock market data from CSV file."""
        try:
            df = pd.read_csv(data_path)
            print("Available columns in CSV:", df.columns.tolist())
            return df
        except FileNotFoundError:
            print(f"Warning: Stock market data file not found at {data_path}")
            return pd.DataFrame()
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return pd.DataFrame()

    def _get_text_for_embedding(self, row) -> str:
        """Combine available text fields for embedding."""
        text_parts = []
        
        # Add name and type
        text_parts.append(str(row['name']))
        text_parts.append(str(row['type']))
        
        # Add category if available
        if pd.notna(row['category']):
            text_parts.append(str(row['category']))
        
        # Add amenities
        if pd.notna(row['amenities']):
            text_parts.append(str(row['amenities']))
        
        # Add review and title
        if pd.notna(row['review']):
            text_parts.append(str(row['review']))
        if pd.notna(row['title']):
            text_parts.append(str(row['title']))
        
        # Add location info
        if pd.notna(row['address']):
            text_parts.append(str(row['address']))
        
        # Add awards info
        if pd.notna(row['awards']):
            text_parts.append(str(row['awards']))
        
        # Filter out 'nan' strings and join
        text_parts = [part for part in text_parts if part.lower() != 'nan']
        return " ".join(text_parts)

    def _prepare_and_index_chunks(self):
        """Prepare text chunks and index them in Qdrant."""
        print("Preparing text chunks and indexing in Qdrant...")
        
        # Process each stock
        for idx, row in tqdm(self.stocks_df.iterrows(), total=len(self.stocks_df)):
            # Create metadata for the stock
            metadata = {
                'name': row['name'],
                'type': row['type'],
                'rating': row['rating'],
                'stock_class': row['stockClass'],
                'price_level': row['priceLevel'],
                'price_range': row['priceRange'],
                'address': row['address'],
                'amenities': row['amenities'],
                'review': row['review'],
                'number_of_reviews': row['numberOfReviews'],
                'ranking': row['rankingString'],
                'phone': row['phone'],
                'website': row['website']
            }
            
            # Get text for embedding
            text = self._get_text_for_embedding(row)
            
            # Create chunks
            chunks = self.chunker.chunk_text(text, doc_id=str(idx), metadata=metadata)
            
            # Compute embeddings and index in Qdrant
            for chunk in chunks:
                # Compute embedding
                embedding = self.model.encode(chunk.text)
                
                # Generate a UUID for the point ID
                point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{chunk.doc_id}_{chunk.chunk_id}"))
                
                # Add to Qdrant
                self.qdrant_client.upsert(
                    collection_name=self.collection_name,
                    points=[
                        models.PointStruct(
                            id=point_id,
                            vector=embedding.tolist(),
                            payload={
                                'text': chunk.text,
                                'doc_id': chunk.doc_id,
                                'chunk_id': chunk.chunk_id,
                                **chunk.metadata
                            }
                        )
                    ]
                )
        
        print(f"Indexed chunks from {len(self.stocks_df)} stocks in Qdrant")

    def _enhance_search_with_llm(self, query: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhance search results using LLM.
        
        Args:
            query: Original search query
            results: Initial search results
            
        Returns:
            Enhanced search results
        """
        if not self.llm_enabled or not results:
            return results
            
        try:
            # Prepare context from results
            context = []
            for result in results[:3]:  # Use top 3 results for context
                context.append(f"Stock: {result['name']}")
                if result.get('review'):
                    context.append(f"Review: {result['review']}")
                if result.get('amenities'):
                    context.append(f"Amenities: {result['amenities']}")
                context.append("---")
            
            # Create prompt for LLM
            messages = [
                {
                    "role": "system",
                    "content": """You are a stock search assistant. Analyze the search results and provide insights about:
1. How well each stock matches the user's query
2. Key features and amenities that might interest the user
3. Any potential concerns or limitations
Keep your analysis concise and focused on the user's needs."""
                },
                {
                    "role": "user",
                    "content": f"""Search Query: {query}

Search Results:
{chr(10).join(context)}

Please analyze these results and provide insights."""
                }
            ]
            
            # Get LLM analysis
            analysis = self.llm_client.chat_completion(messages)
            
            # Add analysis to results
            for result in results:
                result['llm_analysis'] = analysis
                
            return results
            
        except Exception as e:
            print(f"Error enhancing search with LLM: {str(e)}")
            return results

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for stocks based on the query.
        
        Args:
            query: Search query string
            top_k: Number of results to return
            
        Returns:
            List of top_k most relevant stocks
        """
        if self.stocks_df.empty:
            return []

        # Encode the query
        query_embedding = self.model.encode(query)
        
        # Search in Qdrant
        search_results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding.tolist(),
            limit=top_k * 2  # Get more results to filter by stock
        )
        
        # Group results by stock and get best chunk for each
        stock_scores = {}
        for result in search_results:
            doc_id = result.payload['doc_id']
            score = result.score
            
            if doc_id not in stock_scores or score > stock_scores[doc_id][0]:
                stock_scores[doc_id] = (score, result.payload)
        
        # Return results
        results = []
        for doc_id, (score, payload) in sorted(stock_scores.items(), key=lambda x: x[1][0], reverse=True):
            result = {k: v for k, v in payload.items() if k not in ['text', 'doc_id', 'chunk_id']}
            result['similarity_score'] = score
            results.append(result)
        
        # Enhance results with LLM
        results = self._enhance_search_with_llm(query, results[:top_k])
        
        return results

    def add_stock(self, stock_data: Dict[str, Any]):
        """Add a new stock to the search engine.
        
        Args:
            stock_data: Dictionary containing stock information
        """
        new_stock_df = pd.DataFrame([stock_data])
        self.stocks_df = pd.concat([self.stocks_df, new_stock_df], ignore_index=True)
        self._prepare_and_index_chunks()  # Reprocess all chunks

    def save_data(self, data_path: str):
        """Save the current stock data to a CSV file.
        
        Args:
            data_path: Path where to save the CSV file
        """
        self.stocks_df.to_csv(data_path, index=False) 