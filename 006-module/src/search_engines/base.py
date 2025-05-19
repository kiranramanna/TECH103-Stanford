"""
Base interface for stock market search engines.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from dataclasses import dataclass

@dataclass
class StockResult:
    """Stock market search result."""
    title: str
    url: str
    snippet: str
    score: float
    source: str
    metadata: Dict[str, Any]
    raw_response: Optional[Dict[str, Any]] = None  # Raw response from the API

class SearchError(Exception):
    """Custom exception for search engine errors."""
    pass

class StockSearchEngine(ABC):
    """Abstract base class for stock market search engines."""
    
    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> List[StockResult]:
        """Search for stocks based on the query.
        
        Args:
            query: Search query string
            top_k: Number of results to return
            
        Returns:
            List of StockResult objects
            
        Raises:
            SearchError: If the search fails
        """
        pass
    
    def pretty_demo(self, query: str, k: int = 5) -> None:
        """Run a demo search and display results in a formatted way.
        
        Args:
            query: Search query string
            k: Number of results to return
        """
        try:
            results = self.search(query, top_k=k)
            print(f"\n🔍 Search Results for: '{query}'\n")
            print(f"Found {len(results)} results from {self.__class__.__name__}\n")
            
            for i, result in enumerate(results, 1):
                print(f"{i}. {result.title}")
                print(f"   URL: {result.url}")
                print(f"   Score: {result.score:.2f}")
                print(f"   {result.snippet[:200]}...")
                print()
                
        except SearchError as e:
            print(f"❌ Search failed: {str(e)}")
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}") 