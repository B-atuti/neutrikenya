import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Create a directory to store images if it doesn't exist
if not os.path.exists('product_images'):
    os.makedirs('product_images')

# Product URLs and their details from the screenshot
products = [
    {
        'name': 'Super_Booster_Vitamin_C_Plus_Brightening_Serum',
        'price': '38.00',
        'image_url': 'https://neutriherbs.com/cdn/shop/products/neutriherbs-20-vitamin-c-serum.jpg'
    },
    {
        'name': 'Vitamin_C_Serum_Helps_Lighten_And_Brighten',
        'price': '29.00',
        'image_url': 'https://neutriherbs.com/cdn/shop/products/neutriherbs-best-20-vitamin-c-serum.jpg'
    },
    {
        'name': 'Vitamin_C_Brightening_and_Glow_Cream',
        'price': '32.00',
        'image_url': 'https://neutriherbs.com/cdn/shop/products/neutriherbs-anti-aging-vitamin-c-cream.jpg'
    },
    {
        'name': 'Vitamin_C_Sunscreen_SPF50',
        'price': '33.00',
        'image_url': 'https://neutriherbs.com/cdn/shop/products/neutriherbs-vitamin-c-sunscreen-spf50.jpg'
    }
]

def download_image(url, product_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Get the file extension from the URL
            file_extension = os.path.splitext(url)[1] or '.jpg'
            filename = f"product_images/{product_name}{file_extension}"
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Successfully downloaded: {product_name}")
            return filename
        else:
            print(f"Failed to download {product_name}: Status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading {product_name}: {str(e)}")
        return None

def main():
    print("Starting to download product images...")
    downloaded_files = []
    
    for product in products:
        filename = download_image(product['image_url'], product['name'])
        if filename:
            downloaded_files.append({
                'filename': filename,
                'name': product['name'],
                'price': product['price']
            })
    
    print("\nDownload Summary:")
    print(f"Total products processed: {len(products)}")
    print(f"Successfully downloaded: {len(downloaded_files)}")
    
    # Print details of downloaded files
    if downloaded_files:
        print("\nDownloaded Products:")
        for file in downloaded_files:
            print(f"- {file['name']}: {file['filename']} (Price: ${file['price']})")

if __name__ == "__main__":
    main() 