import os
from search_engines.traversaal import TraversaalSearchEngine

def get_trend_confirmation(symbol: str) -> dict:
    """Fetch trend confirmation for the given stock symbol using Traversaal API."""
    engine = TraversaalSearchEngine()
    # Example: Use a query for moving average crossover
    query = f"{symbol} moving average crossover trend confirmation"
    results = engine.search(query, top_k=1)
    if results:
        return {
            "indicator": "Trend Confirmation",
            "result": results[0].snippet,
            "raw": results[0].raw_response
        }
    return {"indicator": "Trend Confirmation", "result": "No data found."} 