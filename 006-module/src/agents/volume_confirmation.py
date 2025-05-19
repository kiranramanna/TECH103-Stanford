import os
from search_engines.traversaal import TraversaalSearchEngine

def get_volume_confirmation(symbol: str) -> dict:
    """Fetch volume confirmation for the given stock symbol using Traversaal API."""
    engine = TraversaalSearchEngine()
    query = f"{symbol} volume confirmation analysis"
    results = engine.search(query, top_k=1)
    if results:
        return {
            "indicator": "Volume Confirmation",
            "result": results[0].snippet,
            "raw": results[0].raw_response
        }
    return {"indicator": "Volume Confirmation", "result": "No data found."} 