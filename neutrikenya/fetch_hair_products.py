import requests
from bs4 import BeautifulSoup
import json

# Base URL for the Neutriherbs Global website
BASE_URL = "https://neutriherbs.com"
HAIR_CARE_URL = "/collections/hair-care"

def fetch_product_data(product_url):
    """Extract basic product details from a product page"""
    product_data = {}
    
    try:
        print(f"Fetching product page: {product_url}")
        response = requests.get(product_url)
        
        if response.status_code != 200:
            print(f"Failed to access product page. Status code: {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract product name
        name_tag = soup.select_one('h1.product__title')
        if name_tag:
            product_data['name'] = name_tag.text.strip()
            print(f"Product name: {product_data['name']}")
        
        # Extract price
        price_tag = soup.select_one('span.product__price')
        if price_tag:
            price_text = price_tag.text.strip()
            product_data['price'] = price_text
            print(f"Product price: {price_text}")
        
        # Extract image URL of first image
        image_tag = soup.select_one('div.product-gallery__slide img')
        if image_tag:
            img_url = image_tag.get('src')
            if img_url and img_url.startswith('//'):
                img_url = 'https:' + img_url
            product_data['image_url'] = img_url
            print(f"Product image: {img_url}")
        
        return product_data
    
    except Exception as e:
        print(f"Error fetching product data: {e}")
        return None

def list_hair_products():
    """List hair care products from neutriherbs.com"""
    print(f"Fetching hair care products from {BASE_URL}{HAIR_CARE_URL}")
    
    try:
        response = requests.get(f"{BASE_URL}{HAIR_CARE_URL}")
        
        if response.status_code != 200:
            print(f"Failed to fetch hair care page. Status code: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all product cards
        product_cards = soup.select('div.product-grid-item')
        
        print(f"Found {len(product_cards)} products")
        
        products = []
        
        for idx, card in enumerate(product_cards[:3]):  # Process just the first 3 for a quick test
            print(f"\nProduct #{idx+1}:")
            
            # Get product name
            name_tag = card.select_one('.product-grid-item__title')
            if name_tag:
                print(f"- Name: {name_tag.text.strip()}")
            
            # Get product price
            price_tag = card.select_one('.product-grid-item__price')
            if price_tag:
                print(f"- Price: {price_tag.text.strip()}")
            
            # Get product link
            link_tag = card.select_one('a.product-grid-item__link')
            if link_tag:
                product_url = link_tag.get('href')
                if product_url and not product_url.startswith('http'):
                    product_url = BASE_URL + product_url
                print(f"- URL: {product_url}")
                
                # Get detailed product data
                product_data = fetch_product_data(product_url)
                if product_data:
                    products.append(product_data)
        
        # Save product data to file for reference
        with open('hair_product_examples.json', 'w') as f:
            json.dump(products, f, indent=2)
        
        print(f"\nSaved {len(products)} product examples to hair_product_examples.json")
    
    except Exception as e:
        print(f"Error listing hair products: {e}")

if __name__ == "__main__":
    list_hair_products() 