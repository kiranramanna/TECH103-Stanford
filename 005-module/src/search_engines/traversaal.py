"""
Traversaal search engine implementation.
"""
import os
from typing import List, Dict, Any
import requests
from .base import HotelSearchEngine, HotelResult, SearchError
from ..utils.logger import timeit, log_errors

class TraversaalSearchEngine(HotelSearchEngine):
    """Traversaal API-based hotel search engine."""
    
    def __init__(self):
        """Initialize the Traversaal search engine."""
        self.api_key = os.getenv("TRAVERSAAL_API_KEY")
        if not self.api_key:
            raise SearchError("TRAVERSAAL_API_KEY environment variable not set")
        
        self.api_url = "https://api-ares.traversaal.ai/live/predict"
        self.headers = {
            "x-api-key": self.api_key,
            "content-type": "application/json"
        }
    
    @timeit
    @log_errors
    def search(self, query: str, top_k: int = 2) -> List[HotelResult]:
        """Search for hotels using Traversaal API.
        
        Args:
            query: Search query string
            top_k: Number of results to return
            
        Returns:
            List of HotelResult objects
            
        Raises:
            SearchError: If the search fails
        """
        try:
            # Prepare request payload
            payload = {
                "query": [query]
            }
            
            # Make API request
            response = requests.post(
                self.api_url,
                json=payload,
                headers=self.headers
            )
            
            # Check response
            response.raise_for_status()
            data = response.json()
            
            # Store raw response for debugging
            raw_response = data
            
            # Process results
            results = []
            
            # Extract response text and web URLs
            response_text = data.get("data", {}).get("response_text", "")
            web_urls = data.get("data", {}).get("web_url", [])
            
            # Create a single result with the complete response
            result = HotelResult(
                title="Traversaal Search Results",
                url=web_urls[0] if web_urls else "",
                snippet=response_text,
                score=1.0,  # Since this is a single comprehensive result
                source="traversaal",
                metadata={
                    "web_urls": web_urls,
                    "query": query
                },
                raw_response=data  # Store the complete raw response
            )
            results.append(result)
            
            return results
            
        except requests.exceptions.RequestException as e:
            raise SearchError(f"Traversaal API request failed: {str(e)}")
        except Exception as e:
            raise SearchError(f"Failed to process Traversaal results: {str(e)}") 