import os
import requests
import json
import time
from urllib.parse import urljoin

# Create directories if they don't exist
if not os.path.exists('products'):
    os.makedirs('products')

# Base URL for the Neutriherbs Nigeria Shopify store
BASE_URL = "https://neutriherbs.ng"
PRODUCTS_API = "/products.json"
COLLECTIONS_API = "/collections.json"

def download_image(url, folder, filename=None):
    """Download an image from URL and save to the specified folder"""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # If no filename provided, use the last part of the URL
            if filename is None:
                filename = url.split('/')[-1].split('?')[0]  # Remove query parameters
            
            # Save the image
            filepath = os.path.join(folder, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {filepath}")
            return filepath
        else:
            print(f"Failed to download {url}: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def fetch_shopify_products():
    """Fetch products directly from Shopify API"""
    products_data = []
    
    try:
        # Fetch products from Shopify API
        print(f"Fetching products from {BASE_URL}{PRODUCTS_API}")
        response = requests.get(f"{BASE_URL}{PRODUCTS_API}")
        
        if response.status_code != 200:
            print(f"Failed to fetch products: HTTP {response.status_code}")
            return products_data
        
        data = response.json()
        products = data.get('products', [])
        
        print(f"Found {len(products)} products")
        
        for product in products:
            product_id = product.get('id')
            title = product.get('title', '')
            description = product.get('body_html', '')
            
            # Extract price from variants
            price = 0
            variants = product.get('variants', [])
            if variants:
                price = float(variants[0].get('price', 0))
            
            # Get product collections/categories
            product_type = product.get('product_type', '')
            tags = product.get('tags', '').split(', ')
            
            # Determine product line and skin concern from tags
            product_line = ""
            skin_concern = ""
            
            for tag in tags:
                tag_lower = tag.lower()
                if "vitamin c" in tag_lower:
                    product_line = "Vitamin C"
                elif "retinol" in tag_lower:
                    product_line = "Retinol"
                elif "acne" in tag_lower:
                    skin_concern = "Acne Skin"
                elif "dry" in tag_lower:
                    skin_concern = "Dry Skin"
            
            # Get product images
            images = product.get('images', [])
            
            # Download product images
            downloaded_images = []
            for idx, image in enumerate(images):
                image_url = image.get('src', '')
                
                if image_url:
                    # Sanitize product name to use as filename
                    sanitized_name = title.replace(' ', '_').replace('/', '_').replace('\\', '_')
                    sanitized_name = ''.join(c for c in sanitized_name if c.isalnum() or c in '_-.')
                    
                    # Create filename
                    filename = f"{sanitized_name}_{idx}.jpg"
                    
                    # Download the image
                    filepath = download_image(image_url, 'products', filename)
                    if filepath:
                        downloaded_images.append(filepath)
            
            # Add product to list
            products_data.append({
                'name': title,
                'url': f"{BASE_URL}/products/{product.get('handle', '')}",
                'description': description,
                'price': price,
                'product_line': product_line,
                'skin_concern': skin_concern,
                'images': downloaded_images
            })
            
            # Be nice to the server
            time.sleep(0.5)
    
    except Exception as e:
        print(f"Error fetching Shopify products: {e}")
    
    return products_data

def main():
    print("Starting to download product images from Neutriherbs Shopify store")
    
    # Fetch products from Shopify API
    products = fetch_shopify_products()
    
    # Save products to JSON file
    with open('products.json', 'w') as f:
        json.dump(products, f, indent=4)
    
    print(f"Downloaded information for {len(products)} products")
    print(f"Product data saved to products.json")

if __name__ == "__main__":
    main() 