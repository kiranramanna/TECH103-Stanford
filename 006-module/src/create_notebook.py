"""
Create a Jupyter notebook for stock market search engine demo.
"""
import os
import nbformat as nbf
from pathlib import Path
import json
import numpy as np
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_notebook():
    """Create a Jupyter notebook with stock market search engine demo."""
    # Create notebook
    nb = nbf.v4.new_notebook()
    
    # Add cells
    cells = [
        nbf.v4.new_code_cell("""# Ensure src/ is in sys.path for imports
import sys
import os
sys.path.insert(0, os.path.abspath('../src'))
"""),
        nbf.v4.new_markdown_cell("""# Stock Market Search Engine Demo

This notebook demonstrates four different stock market search engines:
1. Generic Search Engine API
2. DuckDuckGo Search
3. Traversaal Search
4. Local Qdrant Vector Search

Each engine has its own strengths and use cases:
- Generic Search: Broad web search with customizable parameters
- DuckDuckGo: Privacy-focused search with real-time results
- Traversaal: Specialized stock market search with rich metadata
- Qdrant Local: Fast semantic search with local data"""),
        nbf.v4.new_code_cell("""# Install required packages
!pip install -r ../requirements.txt"""),
        nbf.v4.new_code_cell("""import os
import sys
import importlib
import pandas as pd
from dotenv import load_dotenv
from IPython.display import display, Markdown
import json

# Load environment variables
load_dotenv()

# Import base module first
from search_engines import base
importlib.reload(base)

# Import and reload search engine modules
import search_engines.generic as generic
import search_engines.duckduckgo as duckduckgo
import search_engines.traversaal as traversaal
import search_engines.qdrant_local as qdrant_local
import llm

# Reload all modules in reverse dependency order
importlib.reload(llm)
importlib.reload(qdrant_local)
importlib.reload(traversaal)
importlib.reload(duckduckgo)
importlib.reload(generic)

# Import search engines after reload
from search_engines.generic import GenericSearchEngine
from search_engines.duckduckgo import DuckDuckGoSearchEngine
from search_engines.traversaal import TraversaalSearchEngine
from search_engines.qdrant_local import QdrantLocalSearchEngine
from llm import OpenRouterLLM"""),
        nbf.v4.new_markdown_cell("""## Initialize Search Engines and LLM

Each search engine requires different initialization parameters:
- Generic Search: Path to stock market data CSV
- DuckDuckGo: No API key needed
- Traversaal: API key
- Qdrant Local: Path to stock market data CSV
- OpenRouter LLM: API key for text generation"""),
        nbf.v4.new_code_cell("""# Initialize search engines
engines = {}

# Generic Search Engine
try:
    engines['generic'] = GenericSearchEngine(data_path="../data/2022_03_17_02_06_nasdaq.csv")
    print("✓ Generic Search Engine initialized")
except Exception as e:
    print(f"✗ Generic Search Engine failed: {str(e)}")

# DuckDuckGo Search Engine
try:
    engines['duckduckgo'] = DuckDuckGoSearchEngine()
    print("✓ DuckDuckGo Search Engine initialized")
except Exception as e:
    print(f"✗ DuckDuckGo Search Engine failed: {str(e)}")

# Traversaal Search Engine
try:
    engines['traversaal'] = TraversaalSearchEngine()
    print("✓ Traversaal Search Engine initialized")
except Exception as e:
    print(f"✗ Traversaal Search Engine failed: {str(e)}")

# Qdrant Local Search Engine
try:
    engines['qdrant'] = QdrantLocalSearchEngine(data_path="../data/2022_03_17_02_06_nasdaq.csv")
    print("✓ Qdrant Local Search Engine initialized")
except Exception as e:
    print(f"✗ Qdrant Local Search Engine failed: {str(e)}")

# Initialize OpenRouter LLM
try:
    llm_client = llm.OpenRouterLLM()
    print("✓ OpenRouter LLM initialized")
except Exception as e:
    print(f"✗ OpenRouter LLM failed: {str(e)}")
"""),
        nbf.v4.new_markdown_cell("""## Search Function

This function will run a search query across all initialized engines, display the raw results, and then show an LLM-processed summary of the results."""),
        nbf.v4.new_code_cell("""import numpy as np
# Helper to convert numpy types to native Python types
def convert_np(obj):
    if isinstance(obj, dict):
        return {k: convert_np(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_np(i) for i in obj]
    elif isinstance(obj, np.generic):
        return obj.item()
    else:
        return obj

def search_stocks(query: str, top_k: int = 1):
    \"\"\"Search for stocks using all available engines.
    
    Args:
        query: Search query string
        top_k: Number of results to return per engine
    \"\"\"
    results = {}
    
    # Run search on each engine
    for name, engine in engines.items():
        try:
            results[name] = engine.search(query, top_k=top_k)
        except Exception as e:
            print(f"Error with {name} engine: {str(e)}")
    
    # Display results
    for name, stocks in results.items():
        display(Markdown(f"### {name.upper()} Results"))
        
        for i, stock in enumerate(stocks, 1):
            display(Markdown(f"#### {i}. {stock.title}"))
            display(Markdown(f"**Score:** {stock.score:.2f}"))
            display(Markdown(f"**URL:** {stock.url}"))
            display(Markdown(f"**Snippet:** {stock.snippet}"))
            
            if stock.metadata:
                display(Markdown("**Metadata:**"))
                for key, value in stock.metadata.items():
                    if value:  # Only show non-empty values
                        display(Markdown(f"- {key}: {value}"))
            
            # Display raw response if available
            if stock.raw_response:
                display(Markdown("**Raw Response:**"))
                from IPython.display import JSON
                display(JSON(stock.raw_response))
            
            # Get LLM analysis for this stock
            try:
                context = {
                    "query": query,
                    "engine": name,
                    "stock": {
                        "title": stock.title,
                        "score": stock.score,
                        "url": stock.url,
                        "snippet": stock.snippet,
                        "metadata": stock.metadata,
                        "raw_response": stock.raw_response
                    }
                }
                
                llm_response = llm_client.generate(
                    prompt="Analyze these stock search results and provide insights about:",
                    context=convert_np(context)
                )
                
                # Add a dotted line for clear demarcation before LLM analysis
                display(Markdown('<hr style="border-top: 1px dotted #bbb;">'))
                # Underline the LLM Analysis heading
                display(Markdown('<u>**LLM Analysis:**</u>'))
                display(Markdown(llm_response))
            except Exception as e:
                display(Markdown(f"*Error getting LLM analysis: {str(e)}*"))
            
            display(Markdown("---"))"""),
        nbf.v4.new_markdown_cell("""## Example Searches

Let's try an example search to see how each engine performs and how the LLM analyzes the results."""),
        nbf.v4.new_code_cell("""# Search for high-growth technology stocks
search_stocks("Apple stock")"""),
        nbf.v4.new_code_cell(
            """import importlib\nimport gradio_app\nimportlib.reload(gradio_app)\nfrom gradio_app import launch_gradio_app\nlaunch_gradio_app(engines, llm_client)"""
        )
    ]
    
    nb['cells'] = cells
    
    # Set notebook metadata
    nb['metadata'] = {
        'title': 'Stock Market Search Engine Demo',
        'authors': [
            {'name': 'Your Name or Team'}
        ],
        'description': 'A demo notebook for comparing multiple stock market search engines and LLM-based analysis.',
        'created': datetime.now().isoformat(),
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'codemirror_mode': {
                'name': 'ipython',
                'version': 3
            },
            'file_extension': '.py',
            'mimetype': 'text/x-python',
            'name': 'python',
            'nbconvert_exporter': 'python',
            'pygments_lexer': 'ipython3',
            'version': '3.12.9'
        }
    }
    
    # Create notebooks directory if it doesn't exist
    notebooks_dir = Path("notebooks")
    notebooks_dir.mkdir(exist_ok=True)
    
    # Write notebook
    nbf.write(nb, "notebooks/005-stock_search.ipynb")
    print("Notebook created at notebooks/005-stock_search.ipynb")

if __name__ == "__main__":
    create_notebook() 