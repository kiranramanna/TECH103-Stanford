# Miami Hotel Search Engine

A semantic search engine for finding hotels in Miami based on user queries.

## Project Structure
```
.
├── data/               # Hotel data and summaries
├── notebooks/          # Jupyter notebooks for development and demonstration
├── src/               # Source code modules
└── requirements.txt   # Project dependencies
```

## Setup and Usage

### Environment Setup

This project uses the `ais_ml1` conda environment. Follow these steps to set up and run:

1. Activate the conda environment:
```bash
conda activate ais_ml1
```

2. Install additional required packages if not already present:
```bash
pip install -r requirements.txt
```

### Running the Search Engine

1. Start Jupyter Lab/Notebook:
```bash
jupyter lab
```

2. Navigate to `notebooks/hotel_search.ipynb`
3. Run the notebook cells to interact with the search engine

### Features

- Semantic search for Miami hotels using natural language queries
- Detailed hotel information including:
  - Name and location
  - Amenities and features
  - Price range and ratings
  - Reviews and descriptions
- Natural language query processing
- Similarity scoring for search results

### Data Source

The hotel data is stored in `data/miami_hotels.csv`, which contains comprehensive information about Miami hotels including their amenities, locations, and reviews.

### Example Queries

Try searching with natural language queries like:
- "luxury beachfront hotels with ocean view"
- "family friendly hotels with swimming pools"
- "spa resorts with yoga classes"
- "affordable hotels near downtown Miami" 