import os
from search_engines.traversaal import TraversaalSearchEngine

def get_support_resistance(symbol: str) -> dict:
    """Fetch support and resistance levels for the given stock symbol using Traversaal API."""
    engine = TraversaalSearchEngine()
    query = f"{symbol} support and resistance levels"
    results = engine.search(query, top_k=1)
    if results:
        return {
            "indicator": "Support and Resistance Levels",
            "result": results[0].snippet,
            "raw": results[0].raw_response
        }
    return {"indicator": "Support and Resistance Levels", "result": "No data found."} 