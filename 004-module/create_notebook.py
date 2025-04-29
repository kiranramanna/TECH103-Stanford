import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

# Create the notebook content
cells = [
    nbf.v4.new_markdown_cell("""# Miami Hotel Search Engine Demo

This notebook demonstrates the semantic search functionality for finding Miami hotels based on natural language queries, enhanced with real-time internet search results."""),
    
    nbf.v4.new_code_cell("""# Import required libraries
import sys
sys.path.append('../src')
import importlib
import search
importlib.reload(search)  # Reload the module to get latest changes
from search import HotelSearchEngine
import pandas as pd
from IPython.display import display, Markdown

# Install and import DuckDuckGo search
!pip install -q duckduckgo-search
from duckduckgo_search import DDGS"""),
    
    nbf.v4.new_markdown_cell("""## Initialize the Search Engine

First, let's create an instance of our search engine and load the hotel data."""),
    
    nbf.v4.new_code_cell("""# Initialize the search engine
search_engine = HotelSearchEngine('../data/miami_hotels.csv')

# Display basic statistics about our dataset
print(f"Total number of hotels: {len(search_engine.hotels_df)}\\n")
print("Available columns in the dataset:")
print(search_engine.hotels_df.columns.tolist())
print("\\nSample of available hotels:")
display(search_engine.hotels_df[['name', 'type', 'rating', 'priceRange', 'category']].head())"""),
    
    nbf.v4.new_markdown_cell("""## Search Results with Internet Information"""),
    
    nbf.v4.new_code_cell('''def render_hotel_markdown(hotel, news, reviews):
    """Format hotel information and search results as markdown"""
    # Hotel info as markdown table
    hotel_md = "### 🏨 Hotel Data\\n\\n"
    hotel_md += "| Field | Value |\\n|---|---|\\n"
    for k, v in hotel.items():
        hotel_md += f"| {k} | {str(v).replace('|', '\\|')} |\\n"

    # News section
    news_md = "\\n### 📰 News\\n"
    if news:
        for n in news:
            link = f"[{n['title']}]({n.get('url', '')})" if n.get('url') else n['title']
            date = n.get('date', '')
            body = n.get('body', '')
            news_md += f"- **{date}**: {link}\\n  \\n  {body}\\n"
    else:
        news_md += "_No news found._\\n"

    # Reviews/info section
    reviews_md = "\\n### 💬 Reviews / Info\\n"
    if reviews:
        for r in reviews:
            link = f"[{r['title']}]({r.get('href', '')})" if r.get('href') else r['title']
            body = r.get('body', '')
            reviews_md += f"- {link}\\n  \\n  {body}\\n"
    else:
        reviews_md += "_No reviews/info found._\\n"
    
    reviews_md += "\\n---\\n"  # Add separator between hotels
    
    display(Markdown(hotel_md + news_md + reviews_md))

def search_hotels(query, top_k=3):
    """Search for hotels and get internet information"""
    print(f"🔍 Search Query: '{query}'\\n")
    
    # Get local search results
    results = search_engine.search(query, top_k=top_k)
    if not results:
        print("No results found.")
        return
        
    # Display results with internet information
    for hotel in results:
        with DDGS() as ddgs:
            news = list(ddgs.news(
                f'"{hotel["name"]}" Miami hotel',
                region='us-en',
                max_results=2
            ))
            reviews = list(ddgs.text(
                f'"{hotel["name"]}" Miami hotel reviews site:tripadvisor.com OR site:booking.com',
                region='us-en',
                max_results=2
            ))
        render_hotel_markdown(hotel, news, reviews)'''),
    
    nbf.v4.new_markdown_cell("""## Try Some Example Searches"""),
    
    nbf.v4.new_code_cell("""# Example 1: Search for luxury beachfront hotels
search_hotels("luxury beachfront hotels with ocean view", top_k=2)"""),
    
    nbf.v4.new_code_cell("""# Example 2: Search for family-friendly hotels with pools
search_hotels("family friendly hotels with swimming pools and activities for kids", top_k=2)"""),
    
    nbf.v4.new_markdown_cell("""## Interactive Search

Use the cell below to try your own search queries!"""),
    
    nbf.v4.new_code_cell("""# Enter your search query
your_query = ""  # Replace with your search query
search_hotels(your_query)""")
]

nb.cells = cells

# Create notebooks directory if it doesn't exist
os.makedirs('notebooks', exist_ok=True)

# Write the notebook
with open('notebooks/hotel_search.ipynb', 'w') as f:
    nbf.write(nb, f) 