import os
from search_engines.traversaal import TraversaalSearchEngine

def get_momentum_signal(symbol: str) -> dict:
    """Fetch momentum signal (RSI or MACD) for the given stock symbol using Traversaal API."""
    engine = TraversaalSearchEngine()
    # Example: Use a query for RSI or MACD
    query = f"{symbol} RSI MACD momentum signal"
    results = engine.search(query, top_k=1)
    if results:
        return {
            "indicator": "Momentum Signal",
            "result": results[0].snippet,
            "raw": results[0].raw_response
        }
    return {"indicator": "Momentum Signal", "result": "No data found."} 