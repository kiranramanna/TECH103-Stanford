"""
Generic search engine implementation using local embeddings.
"""
import os
from typing import List, Dict, Any
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from .base import HotelSearchEngine, HotelResult, SearchError
from ..utils.logger import timeit, log_errors
from ..utils.storage import save_embeddings, load_embeddings

class GenericSearchEngine(HotelSearchEngine):
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
                self.embeddings, self.hotels_df = loaded_data
                print("Loaded existing embeddings from storage")
            else:
                # Load and process data
                self.hotels_df = self._load_data(data_path)
                self.embeddings = self._compute_embeddings()
                
                # Save embeddings for future use
                save_embeddings('generic', self.embeddings, self.hotels_df)
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
            for _, row in self.hotels_df.iterrows():
                text = self._get_text_for_embedding(row)
                texts.append(text)
            
            # Compute embeddings
            return self.model.encode(texts)
        except Exception as e:
            raise SearchError(f"Failed to compute embeddings: {str(e)}")
    
    def _get_text_for_embedding(self, row: pd.Series) -> str:
        """Combine available text fields for embedding.
        
        Args:
            row: DataFrame row containing hotel data
            
        Returns:
            Combined text string
        """
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
    
    @timeit
    @log_errors
    def search(self, query: str, top_k: int = 5) -> List[HotelResult]:
        """Search for hotels using cosine similarity.
        
        Args:
            query: Search query string
            top_k: Number of results to return
            
        Returns:
            List of HotelResult objects
            
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
                row = self.hotels_df.iloc[idx]
                results.append(HotelResult(
                    title=row['name'],
                    url=row['website'] if pd.notna(row['website']) else '',
                    snippet=row['review'] if pd.notna(row['review']) else '',
                    score=float(similarities[idx]),
                    source='generic',
                    metadata={
                        'type': row['type'],
                        'rating': row['rating'] if pd.notna(row['rating']) else None,
                        'hotel_class': row['hotelClass'] if pd.notna(row['hotelClass']) else None,
                        'price_level': row['priceLevel'] if pd.notna(row['priceLevel']) else None,
                        'price_range': row['priceRange'] if pd.notna(row['priceRange']) else None,
                        'address': row['address'] if pd.notna(row['address']) else None,
                        'amenities': row['amenities'] if pd.notna(row['amenities']) else None,
                        'number_of_reviews': row['numberOfReviews'] if pd.notna(row['numberOfReviews']) else None,
                        'ranking': row['rankingString'] if pd.notna(row['rankingString']) else None,
                        'phone': row['phone'] if pd.notna(row['phone']) else None
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
            self.hotels_df = pd.concat([self.hotels_df, new_hotel_df], ignore_index=True)
            self._compute_embeddings()  # Recompute embeddings
        except Exception as e:
            raise SearchError(f"Error adding hotel: {str(e)}")

    def save_data(self, data_path: str):
        """Save the current hotel data to a CSV file.
        
        Args:
            data_path: Path where to save the CSV file
        """
        try:
            self.hotels_df.to_csv(data_path, index=False)
        except Exception as e:
            raise SearchError(f"Error saving data: {str(e)}") 