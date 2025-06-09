#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Install required packages if they don't exist
pip install requests beautifulsoup4 pillow

# Step 1: Download hair care products and images from neutriherbs.com
echo "Step 1: Downloading hair care products and images from neutriherbs.com..."
python download_neutriherbs_global.py

# Step 2: Check if images were successfully downloaded
echo "Step 2: Checking downloaded images and creating placeholders if needed..."
python check_images.py

# Step 3: Import hair care products into the Django database
echo "Step 3: Importing hair care products into the Django database..."
python import_haircare_products.py

echo "Import process completed." 