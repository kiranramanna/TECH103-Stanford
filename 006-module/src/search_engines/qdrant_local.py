"""
Local Qdrant vector search engine implementation.
"""
import os
import uuid
from typing import List, Dict, Any
import pandas as pd
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from .base import StockSearchEngine, StockResult, SearchError
from utils.logger import timeit, log_errors
from utils.storage import get_qdrant_path

class QdrantLocalSearchEngine(StockSearchEngine):
    """Local Qdrant-based stock market search engine."""
    
    def __init__(self, data_path: str = "data/2022_03_17_02_06_nasdaq.csv"):
        """Initialize the Qdrant local search engine.
        
        Args:
            data_path: Path to the CSV file containing stock market data
        """
        try:
            # Initialize model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.vector_size = self.model.get_sentence_embedding_dimension()
            
            # Initialize Qdrant client with persistent storage
            qdrant_path = get_qdrant_path()
            self.qdrant_client = QdrantClient(path=str(qdrant_path))
            self.collection_name = "stock_chunks"
            
            # Check if collection exists
            collections = self.qdrant_client.get_collections().collections
            collection_names = [collection.name for collection in collections]
            
            if self.collection_name not in collection_names:
                # Create collection if it doesn't exist
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )
                # Load and index data
                self._load_and_index_data(data_path)
                print("Created new Qdrant collection and indexed data")
            else:
                print("Using existing Qdrant collection")
                
        except Exception as e:
            raise SearchError(f"Failed to initialize search engine: {str(e)}")
    
    def _load_and_index_data(self, data_path: str) -> None:
        """Load stock market data and index it in Qdrant.
        
        Args:
            data_path: Path to the CSV file
        """
        try:
            # Load data
            self.stocks_df = pd.read_csv(data_path)
            
            # Index each stock
            for idx, row in self.stocks_df.iterrows():
                # Get text for embedding
                text = self._get_text_for_embedding(row)
                
                # Compute embedding
                embedding = self.model.encode(text)
                
                # Create metadata
                metadata = {
                    'symbol': row['symbol'],
                    'name': row['name'],
                    'sector': row['sector'] if 'sector' in row and pd.notna(row['sector']) else None,
                    'industry': row['industry'] if 'industry' in row and pd.notna(row['industry']) else None,
                    'market_cap': row['market_cap'] if 'market_cap' in row and pd.notna(row['market_cap']) else None
                }
                
                # Generate UUID for point ID
                point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{row['symbol']}_{idx}"))
                
                # Add to Qdrant
                self.qdrant_client.upsert(
                    collection_name=self.collection_name,
                    points=[
                        models.PointStruct(
                            id=point_id,
                            vector=embedding.tolist(),
                            payload=metadata
                        )
                    ]
                )
                
        except Exception as e:
            raise SearchError(f"Failed to load and index data: {str(e)}")
    
    def _get_text_for_embedding(self, row: pd.Series) -> str:
        """Combine available text fields for embedding.
        
        Args:
            row: DataFrame row containing stock data
            
        Returns:
            Combined text string
        """
        text_parts = []
        text_parts.append(str(row['symbol']))
        text_parts.append(str(row['name']))
        if 'sector' in row and pd.notna(row['sector']):
            text_parts.append(str(row['sector']))
        if 'industry' in row and pd.notna(row['industry']):
            text_parts.append(str(row['industry']))
        if 'description' in row and pd.notna(row['description']):
            text_parts.append(str(row['description']))
        return " ".join([part for part in text_parts if part.lower() != 'nan'])
    
    @timeit
    @log_errors
    def search(self, query: str, top_k: int = 5) -> List[StockResult]:
        """Search for stocks using local Qdrant.
        
        Args:
            query: Search query string
            top_k: Number of results to return
            
        Returns:
            List of StockResult objects
            
        Raises:
            SearchError: If the search fails
        """
        try:
            # Encode query
            query_embedding = self.model.encode(query)
            
            # Search in Qdrant
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding.tolist(),
                limit=top_k
            )
            
            # Convert to StockResult objects
            stock_results = []
            for result in search_results:
                payload = result.payload
                stock_results.append(StockResult(
                    title=payload['name'],
                    url=payload.get('website', ''),
                    snippet=payload.get('description', ''),
                    score=result.score,
                    source='qdrant_local',
                    metadata=payload
                ))
            
            return stock_results
            
        except Exception as e:
            raise SearchError(f"Qdrant search failed: {str(e)}") 