"""
Create a Jupyter notebook for hotel search engine demo.
"""
import os
import nbformat as nbf
from pathlib import Path
import json
import numpy as np

def create_notebook():
    """Create a Jupyter notebook with hotel search engine demo."""
    # Create notebook
    nb = nbf.v4.new_notebook()
    
    # Add cells
    cells = [
        nbf.v4.new_markdown_cell("""# Miami Hotel Search Engine Demo

This notebook demonstrates four different hotel search engines:
1. Generic Search Engine API
2. DuckDuckGo Search
3. Traversaal Search
4. Local Qdrant Vector Search

Each engine has its own strengths and use cases:
- Generic Search: Broad web search with customizable parameters
- DuckDuckGo: Privacy-focused search with real-time results
- Traversaal: Specialized hotel search with rich metadata
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

# Add src to path
sys.path.append('..')

# Load environment variables
load_dotenv()

# Import base module first
import src.search_engines.base as base
importlib.reload(base)

# Import and reload search engine modules
import src.search_engines.generic as generic
import src.search_engines.duckduckgo as duckduckgo
import src.search_engines.traversaal as traversaal
import src.search_engines.qdrant_local as qdrant_local
import src.llm as llm

# Reload all modules in reverse dependency order
importlib.reload(llm)
importlib.reload(qdrant_local)
importlib.reload(traversaal)
importlib.reload(duckduckgo)
importlib.reload(generic)

# Import search engines after reload
from src.search_engines.generic import GenericSearchEngine
from src.search_engines.duckduckgo import DuckDuckGoSearchEngine
from src.search_engines.traversaal import TraversaalSearchEngine
from src.search_engines.qdrant_local import QdrantLocalSearchEngine
from src.llm import OpenRouterLLM"""),
        
        nbf.v4.new_markdown_cell("""## Initialize Search Engines and LLM

Each search engine requires different initialization parameters:
- Generic Search: Path to hotel data CSV
- DuckDuckGo: No API key needed
- Traversaal: API key
- Qdrant Local: Path to hotel data CSV
- OpenRouter LLM: API key for text generation"""),
        
        nbf.v4.new_code_cell("""# Initialize search engines
engines = {}

# Generic Search Engine
try:
    engines['generic'] = GenericSearchEngine(data_path="../../004-module/data/miami_hotels.csv")
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
    engines['qdrant'] = QdrantLocalSearchEngine(data_path="../../004-module/data/miami_hotels.csv")
    print("✓ Qdrant Local Search Engine initialized")
except Exception as e:
    print(f"✗ Qdrant Local Search Engine failed: {str(e)}")

# Initialize OpenRouter LLM
try:
    llm = OpenRouterLLM()
    print("✓ OpenRouter LLM initialized")
except Exception as e:
    print(f"✗ OpenRouter LLM failed: {str(e)}")"""),
        
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

def search_hotels(query: str, top_k: int = 2):
    \"\"\"Search for hotels using all available engines.
    
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
    for name, hotels in results.items():
        display(Markdown(f"### {name.upper()} Results"))
        
        for i, hotel in enumerate(hotels, 1):
            display(Markdown(f"#### {i}. {hotel.title}"))
            display(Markdown(f"**Score:** {hotel.score:.2f}"))
            display(Markdown(f"**URL:** {hotel.url}"))
            display(Markdown(f"**Snippet:** {hotel.snippet}"))
            
            if hotel.metadata:
                display(Markdown("**Metadata:**"))
                for key, value in hotel.metadata.items():
                    if value:  # Only show non-empty values
                        display(Markdown(f"- {key}: {value}"))
            
            # Display raw response if available
            if hotel.raw_response:
                display(Markdown("**Raw Response:**"))
                from IPython.display import JSON
                display(JSON(hotel.raw_response))
            
            # Get LLM analysis for this hotel
            try:
                context = {
                    "query": query,
                    "engine": name,
                    "hotel": {
                        "title": hotel.title,
                        "score": hotel.score,
                        "url": hotel.url,
                        "snippet": hotel.snippet,
                        "metadata": hotel.metadata,
                        "raw_response": hotel.raw_response
                    }
                }
                
                llm_response = llm.generate(
                    prompt="Analyze these hotel search results and provide insights about:",
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
        
        nbf.v4.new_code_cell("""# Search for luxury beachfront hotels
search_hotels("luxury beachfront hotels with ocean view and spa facilities")"""),
    ]
    
    nb['cells'] = cells
    
    # Set notebook metadata
    nb['metadata'] = {
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
    notebooks_dir = Path("../notebooks")
    notebooks_dir.mkdir(exist_ok=True)
    
    # Write notebook
    nbf.write(nb, "../notebooks/005-hotel_search.ipynb")
    print("Notebook created at ../notebooks/005-hotel_search.ipynb")

if __name__ == "__main__":
    create_notebook() 