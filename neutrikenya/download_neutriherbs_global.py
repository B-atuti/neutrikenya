import os
import requests
import json
import time
from bs4 import BeautifulSoup

# Create directories if they don't exist
if not os.path.exists('products'):
    os.makedirs('products')

# Base URL for the Neutriherbs Global website
BASE_URL = "https://neutriherbs.com"
HAIR_CARE_URL = "/collections/hair-care"

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

def extract_product_data(product_url):
    """Extract product details from a product page"""
    try:
        response = requests.get(product_url)
        if response.status_code != 200:
            print(f"Failed to access product page {product_url}: HTTP {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract product name
        product_name = None
        name_tag = soup.select_one('h1.product__title')
        if name_tag:
            product_name = name_tag.text.strip()
        
        # Extract price
        price = 0
        price_tag = soup.select_one('span.product__price')
        if price_tag:
            price_text = price_tag.text.strip().replace('$', '').replace('USD', '').strip()
            try:
                price = float(price_text)
            except ValueError:
                print(f"Could not parse price from '{price_text}'")
        
        # Extract description
        description = ""
        desc_tag = soup.select_one('div.product__description')
        if desc_tag:
            description = desc_tag.text.strip()
        
        # Extract product images
        image_urls = []
        image_tags = soup.select('div.product-gallery__slide img')
        for img in image_tags:
            img_url = img.get('src')
            if img_url:
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                image_urls.append(img_url)
        
        # Extract product tags/categories
        product_line = "Hair Care"
        
        return {
            'name': product_name,
            'url': product_url,
            'description': description,
            'price': price,
            'product_line': product_line,
            'image_urls': image_urls
        }
    
    except Exception as e:
        print(f"Error extracting product data from {product_url}: {e}")
        return None

def fetch_neutriherbs_haircare_products():
    """Fetch hair care products from neutriherbs.com"""
    products_data = []
    
    try:
        # Fetch hair care collection page
        print(f"Fetching hair care products from {BASE_URL}{HAIR_CARE_URL}")
        response = requests.get(f"{BASE_URL}{HAIR_CARE_URL}")
        
        if response.status_code != 200:
            print(f"Failed to fetch hair care page: HTTP {response.status_code}")
            return products_data
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all product links on the collection page
        product_links = []
        product_cards = soup.select('div.product-grid-item a.product-grid-item__link')
        
        for card in product_cards:
            product_url = card.get('href')
            if product_url:
                if not product_url.startswith('http'):
                    product_url = BASE_URL + product_url
                product_links.append(product_url)
        
        print(f"Found {len(product_links)} product links")
        
        # Extract data from each product page
        for product_url in product_links:
            print(f"Processing {product_url}")
            product_data = extract_product_data(product_url)
            
            if product_data:
                # Download product images
                downloaded_images = []
                for idx, image_url in enumerate(product_data['image_urls']):
                    if product_data['name']:
                        # Sanitize product name to use as filename
                        sanitized_name = product_data['name'].replace(' ', '_').replace('/', '_').replace('\\', '_')
                        sanitized_name = ''.join(c for c in sanitized_name if c.isalnum() or c in '_-.')
                        
                        # Create filename
                        filename = f"{sanitized_name}_{idx}.jpg"
                        
                        # Download the image
                        filepath = download_image(image_url, 'products', filename)
                        if filepath:
                            downloaded_images.append(filepath)
                
                # Add downloaded image paths to product data
                product_data['images'] = downloaded_images
                del product_data['image_urls']
                
                # Add product to list
                products_data.append(product_data)
                
                # Be nice to the server
                time.sleep(1)
    
    except Exception as e:
        print(f"Error fetching hair care products: {e}")
    
    return products_data

def main():
    print("Starting to download hair care product images from Neutriherbs.com")
    
    # Fetch products from website
    products = fetch_neutriherbs_haircare_products()
    
    # Save products to JSON file
    with open('haircare_products.json', 'w') as f:
        json.dump(products, f, indent=4)
    
    print(f"Downloaded information for {len(products)} hair care products")
    print(f"Product data saved to haircare_products.json")

if __name__ == "__main__":
    main() 