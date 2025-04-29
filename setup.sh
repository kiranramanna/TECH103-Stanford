#!/bin/bash

# Activate conda environment
echo "Activating ais_ml1 conda environment..."
conda activate ais_ml1

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Check if jupyter is installed
if ! command -v jupyter &> /dev/null; then
    echo "Installing Jupyter..."
    pip install jupyter
fi

echo "Setup complete! You can now run the hotel search engine:"
echo "1. Start Jupyter: jupyter lab"
echo "2. Navigate to notebooks/hotel_search.ipynb"
echo "3. Follow the notebook instructions to search for hotels" 