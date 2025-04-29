"""
Miami Hotel Search Engine - Search Module
"""
import pandas as pd
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class HotelSearchEngine:
    def __init__(self, data_path: str = "../data/miami_hotels.csv"):
        """Initialize the search engine with hotel data.
        
        Args:
            data_path: Path to the CSV file containing hotel data
        """
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.hotels_df = self._load_data(data_path)
        self.embeddings = None
        if not self.hotels_df.empty:
            self._compute_embeddings()

    def _load_data(self, data_path: str) -> pd.DataFrame:
        """Load hotel data from CSV file."""
        try:
            df = pd.read_csv(data_path)
            print("Available columns in CSV:", df.columns.tolist())
            return df
        except FileNotFoundError:
            print(f"Warning: Hotel data file not found at {data_path}")
            return pd.DataFrame()
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return pd.DataFrame()

    def _get_text_for_embedding(self, row):
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

    def _compute_embeddings(self):
        """Compute embeddings for all hotel descriptions."""
        descriptions = self.hotels_df.apply(self._get_text_for_embedding, axis=1).tolist()
        self.embeddings = self.model.encode(descriptions)

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for hotels based on the query.
        
        Args:
            query: Search query string
            top_k: Number of results to return
            
        Returns:
            List of top_k most relevant hotels
        """
        if self.hotels_df.empty or self.embeddings is None:
            return []

        # Encode the query
        query_embedding = self.model.encode([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top_k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Return results with scores
        results = []
        for idx in top_indices:
            hotel_dict = {}
            row = self.hotels_df.iloc[idx]
            
            # Add basic info
            hotel_dict['name'] = row['name']
            hotel_dict['type'] = row['type']
            hotel_dict['similarity_score'] = float(similarities[idx])
            
            # Add rating and class info if available
            if pd.notna(row['rating']):
                hotel_dict['rating'] = row['rating']
            if pd.notna(row['hotelClass']):
                hotel_dict['hotel_class'] = row['hotelClass']
            
            # Add price info
            if pd.notna(row['priceLevel']):
                hotel_dict['price_level'] = row['priceLevel']
            if pd.notna(row['priceRange']):
                hotel_dict['price_range'] = row['priceRange']
            
            # Add location
            if pd.notna(row['address']):
                hotel_dict['address'] = row['address']
            
            # Add amenities
            if pd.notna(row['amenities']):
                hotel_dict['amenities'] = row['amenities']
            
            # Add review info
            if pd.notna(row['review']):
                hotel_dict['review'] = row['review']
            if pd.notna(row['numberOfReviews']):
                hotel_dict['number_of_reviews'] = row['numberOfReviews']
            
            # Add ranking info
            if pd.notna(row['rankingPosition']) and pd.notna(row['rankingDenominator']):
                hotel_dict['ranking'] = f"#{row['rankingPosition']} of {row['rankingDenominator']}"
            
            # Add contact info
            if pd.notna(row['phone']):
                hotel_dict['phone'] = row['phone']
            if pd.notna(row['website']):
                hotel_dict['website'] = row['website']
            
            results.append(hotel_dict)
        
        return results

    def add_hotel(self, hotel_data: Dict[str, Any]):
        """Add a new hotel to the search engine.
        
        Args:
            hotel_data: Dictionary containing hotel information
        """
        new_hotel_df = pd.DataFrame([hotel_data])
        self.hotels_df = pd.concat([self.hotels_df, new_hotel_df], ignore_index=True)
        self._compute_embeddings()  # Recompute embeddings

    def save_data(self, data_path: str):
        """Save the current hotel data to a CSV file.
        
        Args:
            data_path: Path where to save the CSV file
        """
        self.hotels_df.to_csv(data_path, index=False) 