"""
Generic search engine implementation using local embeddings.
"""
import os
from typing import List, Dict, Any
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from .base import StockSearchEngine, StockResult, SearchError
from utils.logger import timeit, log_errors
from utils.storage import save_embeddings, load_embeddings

class GenericSearchEngine(StockSearchEngine):
    """Generic search engine using local embeddings."""
    
    def __init__(self, data_path: str = "../data/miami_hotels.csv"):
        """Initialize the generic search engine.
        
        Args:
            data_path: Path to the CSV file containing hotel data
        """
        try:
            # Initialize model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Try to load existing embeddings
            loaded_data = load_embeddings('generic')
            if loaded_data is not None:
                self.embeddings, self.stocks_df = loaded_data
                print("Loaded existing embeddings from storage")
            else:
                # Load and process data
                self.stocks_df = self._load_data(data_path)
                self.embeddings = self._compute_embeddings()
                
                # Save embeddings for future use
                save_embeddings('generic', self.embeddings, self.stocks_df)
                print("Computed and saved new embeddings")
                
        except Exception as e:
            raise SearchError(f"Failed to initialize search engine: {str(e)}")
    
    def _load_data(self, data_path: str) -> pd.DataFrame:
        """Load hotel data from CSV file.
        
        Args:
            data_path: Path to the CSV file
            
        Returns:
            DataFrame containing hotel data
        """
        try:
            return pd.read_csv(data_path)
        except Exception as e:
            raise SearchError(f"Failed to load data: {str(e)}")
    
    def _compute_embeddings(self) -> np.ndarray:
        """Compute embeddings for all hotels.
        
        Returns:
            Numpy array of embeddings
        """
        try:
            # Combine text fields for embedding
            texts = []
            for _, row in self.stocks_df.iterrows():
                text = self._get_text_for_embedding(row)
                texts.append(text)
            
            # Compute embeddings
            return self.model.encode(texts)
        except Exception as e:
            raise SearchError(f"Failed to compute embeddings: {str(e)}")
    
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
        if 'market_cap' in row and pd.notna(row['market_cap']):
            text_parts.append(str(row['market_cap']))
        # Filter out 'nan' strings and join
        text_parts = [part for part in text_parts if part.lower() != 'nan']
        return " ".join(text_parts)
    
    @timeit
    @log_errors
    def search(self, query: str, top_k: int = 5) -> List[StockResult]:
        """Search for stocks using cosine similarity.
        
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
            
            # Compute similarities
            similarities = cosine_similarity([query_embedding], self.embeddings)[0]
            
            # Get top k results
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            # Create results
            results = []
            for idx in top_indices:
                row = self.stocks_df.iloc[idx]
                results.append(StockResult(
                    title=row['name'],
                    url='',
                    snippet='',
                    score=float(similarities[idx]),
                    source='generic',
                    metadata={
                        'symbol': row['symbol'],
                        'name': row['name'],
                        'sector': row['sector'] if pd.notna(row['sector']) else None,
                        'industry': row['industry'] if pd.notna(row['industry']) else None,
                        'market_cap': row['market_cap'] if pd.notna(row['market_cap']) else None
                    }
                ))
            
            return results
            
        except Exception as e:
            raise SearchError(f"Search failed: {str(e)}")

    def add_hotel(self, hotel_data: Dict[str, Any]):
        """Add a new hotel to the search engine.
        
        Args:
            hotel_data: Dictionary containing hotel information
        """
        try:
            new_hotel_df = pd.DataFrame([hotel_data])
            self.stocks_df = pd.concat([self.stocks_df, new_hotel_df], ignore_index=True)
            self._compute_embeddings()  # Recompute embeddings
        except Exception as e:
            raise SearchError(f"Error adding hotel: {str(e)}")

    def save_data(self, data_path: str):
        """Save the current hotel data to a CSV file.
        
        Args:
            data_path: Path where to save the CSV file
        """
        try:
            self.stocks_df.to_csv(data_path, index=False)
        except Exception as e:
            raise SearchError(f"Error saving data: {str(e)}") 