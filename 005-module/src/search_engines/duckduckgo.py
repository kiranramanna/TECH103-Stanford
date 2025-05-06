"""
DuckDuckGo search engine implementation.
"""
from typing import List
from duckduckgo_search import DDGS
from .base import HotelSearchEngine, HotelResult, SearchError
from ..utils.logger import timeit, log_errors

class DuckDuckGoSearchEngine(HotelSearchEngine):
    """DuckDuckGo-based hotel search engine."""
    
    def __init__(self):
        """Initialize the DuckDuckGo search engine."""
        self.ddgs = DDGS()
    
    @timeit
    @log_errors
    def search(self, query: str, top_k: int = 5) -> List[HotelResult]:
        """Search for hotels using DuckDuckGo.
        
        Args:
            query: Search query string
            top_k: Number of results to return
            
        Returns:
            List of HotelResult objects
            
        Raises:
            SearchError: If the search fails
        """
        try:
            # Add hotel-specific context to query
            hotel_query = f"{query} hotel site:booking.com OR site:tripadvisor.com"
            
            # Get search results
            results = list(self.ddgs.text(
                hotel_query,
                region='us-en',
                max_results=top_k
            ))
            
            # Convert to HotelResult objects
            hotel_results = []
            for result in results:
                hotel_results.append(HotelResult(
                    title=result['title'],
                    url=result.get('href', ''),
                    snippet=result.get('body', ''),
                    score=1.0,  # DuckDuckGo doesn't provide scores
                    source='duckduckgo',
                    metadata={
                        'source_url': result.get('href', ''),
                        'raw_result': result
                    }
                ))
            
            return hotel_results
            
        except Exception as e:
            raise SearchError(f"DuckDuckGo search failed: {str(e)}") 