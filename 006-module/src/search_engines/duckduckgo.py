"""
DuckDuckGo search engine implementation.
"""
from typing import List
from duckduckgo_search import DDGS
from .base import StockSearchEngine, StockResult, SearchError
from utils.logger import timeit, log_errors

class DuckDuckGoSearchEngine(StockSearchEngine):
    """DuckDuckGo-based stock market search engine."""
    
    def __init__(self):
        """Initialize the DuckDuckGo search engine."""
        self.ddgs = DDGS()
    
    @timeit
    @log_errors
    def search(self, query: str, top_k: int = 5) -> List[StockResult]:
        """Search for stocks using DuckDuckGo.
        
        Args:
            query: Search query string
            top_k: Number of results to return
            
        Returns:
            List of StockResult objects
            
        Raises:
            SearchError: If the search fails
        """
        try:
            # Remove hotel-specific context, just use query
            search_query = query
            
            # Get search results
            results = list(self.ddgs.text(
                search_query,
                region='us-en',
                max_results=top_k
            ))
            
            # Convert to StockResult objects
            stock_results = []
            for result in results:
                stock_results.append(StockResult(
                    title=result.get('title', ''),
                    url=result.get('href', ''),
                    snippet=result.get('body', ''),
                    score=1.0,  # DDGS does not provide a score, so use a default
                    source='duckduckgo',
                    metadata=result
                ))
            
            return stock_results
            
        except Exception as e:
            raise SearchError(f"DuckDuckGo search failed: {str(e)}") 