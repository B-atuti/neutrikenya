# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install required packages if they don't exist
pip install requests beautifulsoup4 pillow

# Step 1: Download images and product data
Write-Host "Step 1: Downloading images and product data from neutriherbs.ng..."
Write-Host "Using Shopify API method for more reliable downloads..."
python download_shopify_images.py

# Step 2: Check if images were successfully downloaded
Write-Host "Step 2: Checking downloaded images and creating placeholders if needed..."
python check_images.py

# Step 3: Import products into the Django database
Write-Host "Step 3: Importing products into the Django database..."
python import_products.py

Write-Host "Import process completed." 