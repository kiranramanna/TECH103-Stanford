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
3. Example searches for different scenarios:
   - Luxury beachfront hotels
   - Family-friendly hotels
   - Budget hotels with specific amenities

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
- Raw response (when available)

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

The system includes performance monitoring through the `@timeit` decorator, which logs execution time for each search operation. Error handling is implemented through the `@log_errors` decorator, ensuring robust operation and proper error reporting.

## Future Improvements

- Add more search engines
- Implement result caching
- Add support for more metadata fields
- Improve error handling and recovery
- Add unit tests
- Implement result ranking and filtering
- Add support for more data sources 