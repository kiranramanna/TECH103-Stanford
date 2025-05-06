# Hotel Search Engine Module

This module implements a comprehensive hotel search system that combines multiple search engines to provide diverse and relevant hotel recommendations. The system is designed to be modular, extensible, and capable of handling various types of hotel searches.

## Features

- Multiple search engine integration:
  - Generic Search Engine (local embedding-based)
  - DuckDuckGo Search
  - Traversaal Search
  - Qdrant Local Vector Search
- Semantic search capabilities
- Rich metadata handling
- Configurable search parameters
- Error handling and logging
- Performance monitoring

## Components

### Search Engines

1. **Generic Search Engine**
   - Uses local embeddings for semantic search
   - Processes hotel data from CSV files
   - Provides basic hotel information and metadata

2. **DuckDuckGo Search Engine**
   - Privacy-focused web search
   - Real-time results
   - No API key required

3. **Traversaal Search Engine**
   - Specialized hotel search
   - Rich metadata support
   - API-based integration

4. **Qdrant Local Search Engine**
   - Fast semantic search using local vector database
   - Efficient similarity matching
   - Persistent storage of embeddings

### Core Components

- `base.py`: Base classes and interfaces
- `generic.py`: Generic search implementation
- `duckduckgo.py`: DuckDuckGo search integration
- `traversaal.py`: Traversaal API integration
- `qdrant_local.py`: Local vector search implementation
- `utils.py`: Utility functions and helpers

## Usage

The module provides a Jupyter notebook (`005-hotel_search.ipynb`) that demonstrates the functionality of all search engines. The notebook includes:

1. Environment setup and package installation
2. Search engine initialization
3. A single example search for:
   - Luxury beachfront hotels

### Example Search

```python
# Initialize search engines
engines = {
    'generic': GenericSearchEngine(data_path="path/to/hotels.csv"),
    'duckduckgo': DuckDuckGoSearchEngine(),
    'traversaal': TraversaalSearchEngine(),
    'qdrant': QdrantLocalSearchEngine(data_path="path/to/hotels.csv")
}

# Perform a search
results = search_hotels("luxury beachfront hotels with ocean view and spa facilities")
```

## Search Results

Each search engine returns results in a standardized format, including:

- Hotel title
- Relevance score
- URL
- Snippet/description
- Metadata (rating, price, amenities, etc.)
- Raw response (when available, now displayed using `IPython.display.JSON` for clarity)

## LLM Analysis with OpenRouter

The module integrates an OpenRouter LLM (Large Language Model) for advanced analysis of search results. After each search, the notebook calls the `OpenRouterLLM` class, which sends a prompt and context to the OpenRouter API. The context includes the raw response and metadata from each search engine result, allowing the LLM to provide:

- Insights about how well each hotel matches the query
- Key features and amenities
- Potential concerns or limitations

This LLM analysis is displayed directly below each search result in the notebook, leveraging the actual search engine response as context for more relevant and insightful feedback.

## Requirements

- Python 3.12+
- pandas
- sentence-transformers
- qdrant-client
- duckduckgo-search
- requests
- python-dotenv
- pydantic
- tqdm

## Setup

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   - Create a `.env` file
   - Add necessary API keys (e.g., Traversaal API key)

3. Prepare data:
   - Place hotel data CSV file in the appropriate directory
   - Ensure data format matches expected schema

## Performance

The system includes performance monitoring through the `@timeit` decorator, which now logs execution time for each search operation along with the engine (class) name. For example:

```
2025-05-06 02:11:50 - INFO - [GenericSearchEngine] search took 0.03 seconds
2025-05-06 02:11:50 - INFO - [QdrantLocalSearchEngine] search took 0.44 seconds
```

Error handling is implemented through the `@log_errors` decorator, ensuring robust operation and proper error reporting.

## Changelog

- Only one example search is included in the generated notebook for clarity.
- Raw JSON responses are now displayed using `IPython.display.JSON` for better readability in Jupyter.
- The `@timeit` decorator now logs the engine (class) name in timing logs, e.g., `[GenericSearchEngine] search took 0.03 seconds`.
- Added OpenRouter LLM integration: after each search, the LLM is called with the search engine's raw response as context to provide analysis and insights in the notebook.

## Future Improvements

- Add more search engines
- Implement result caching
- Add support for more metadata fields
- Improve error handling and recovery
- Add unit tests
- Implement result ranking and filtering
- Add support for more data sources 