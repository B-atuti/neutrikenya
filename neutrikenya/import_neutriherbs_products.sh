#!/bin/bash

# Activate virtual environment
source venv/Scripts/activate

# Install required packages if they don't exist
pip install requests beautifulsoup4

# Step 1: Download images and product data
echo "Step 1: Downloading images and product data from neutriherbs.ng..."
python download_images.py

# Step 2: Import products into the Django database
echo "Step 2: Importing products into the Django database..."
python import_products.py

echo "Import process completed." 