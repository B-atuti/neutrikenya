import os
import requests
from bs4 import BeautifulSoup
import time
import random
import json
import re
from urllib.parse import urljoin, urlparse

# Create directories if they don't exist
if not os.path.exists('products'):
    os.makedirs('products')

# URL of the website to scrape
base_url = 'https://neutriherbs.ng'

def download_image(url, folder, filename=None):
    """Download an image from a URL and save it to the specified folder"""
    # Properly join URLs to avoid double slashes
    if not url.startswith(('http://', 'https://')):
        url = urljoin(base_url, url.lstrip('/'))
    
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # If no filename is provided, use the last part of the URL
            if filename is None:
                filename = os.path.basename(urlparse(url).path)
            
            # Clean up filename
            filename = filename.split('?')[0]  # Remove query parameters
            
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

def extract_price(text):
    """Extract price from text"""
    if not text:
        return 0
    
    # Try to find price pattern ₦XX,XXX.XX
    price_match = re.search(r'₦([\d,]+\.?\d*)', text)
    if price_match:
        # Remove commas and convert to float
        price_str = price_match.group(1).replace(',', '')
        try:
            return float(price_str)
        except ValueError:
            pass
    
    return 0

def clean_url(url):
    """Clean and normalize URL"""
    if not url.startswith(('http://', 'https://')):
        return urljoin(base_url, url.lstrip('/'))
    return url

def scrape_product_images():
    """Scrape product images from the website"""
    try:
        # Get the home page
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find product links
        product_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Look for product links
            if '/products/' in href:
                product_links.append(href)
        
        # Also check shop pages for more products
        shop_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Look for shop/collection links
            if '/collections/' in href:
                shop_links.append(href)
        
        # Process product pages
        products = []
        for link in product_links:
            full_url = clean_url(link)
            try:
                print(f"Scraping product page: {full_url}")
                product_response = requests.get(full_url)
                product_soup = BeautifulSoup(product_response.text, 'html.parser')
                
                # Find product name
                product_name = product_soup.find('h1', class_='product__title')
                if product_name:
                    product_name = product_name.text.strip()
                else:
                    product_name = "Product_" + str(random.randint(1000, 9999))
                
                # Find product description
                product_description = ""
                description_div = product_soup.find('div', class_='product__description')
                if description_div:
                    product_description = description_div.text.strip()
                
                # Find product price
                product_price = 0
                price_div = product_soup.find('div', class_='product__price')
                if price_div:
                    product_price = extract_price(price_div.text.strip())
                
                # Try to find product categories or tags
                product_line = ""
                skin_concern = ""
                
                # Look for tags or categories in the breadcrumbs
                breadcrumbs = product_soup.find('nav', class_='breadcrumbs')
                if breadcrumbs:
                    links = breadcrumbs.find_all('a')
                    for link in links:
                        link_text = link.text.strip()
                        if "vitamin c" in link_text.lower():
                            product_line = "Vitamin C"
                        elif "retinol" in link_text.lower():
                            product_line = "Retinol"
                        elif "acne" in link_text.lower():
                            skin_concern = "Acne Skin"
                        elif "dry" in link_text.lower():
                            skin_concern = "Dry Skin"
                
                # Find product images
                product_images = []
                for img in product_soup.find_all('img'):
                    src = img.get('src', '')
                    srcset = img.get('srcset', '')
                    data_src = img.get('data-src', '')
                    
                    # Get the highest resolution image available
                    if srcset:
                        # Parse srcset attribute for highest resolution image
                        srcset_urls = srcset.split(',')
                        highest_res_url = srcset_urls[-1].strip().split(' ')[0]
                        # Clean the URL
                        if highest_res_url and not highest_res_url.startswith(('data:', 'javascript:')):
                            product_images.append(highest_res_url)
                    elif data_src:
                        if data_src and not data_src.startswith(('data:', 'javascript:')):
                            product_images.append(data_src)
                    elif src and (src.endswith('.jpg') or src.endswith('.png') or src.endswith('.jpeg')) and not src.startswith(('data:', 'javascript:')):
                        product_images.append(src)
                
                # Download product images
                downloaded_images = []
                for idx, img_url in enumerate(product_images):
                    # Clean up the URL
                    img_url = clean_url(img_url)
                    
                    sanitized_name = product_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
                    sanitized_name = re.sub(r'[^\w\-_.]', '', sanitized_name)  # Remove any other invalid chars
                    filename = f"{sanitized_name}_{idx}.jpg"
                    filepath = download_image(img_url, 'products', filename)
                    if filepath:
                        downloaded_images.append(filepath)
                
                # Add product info with downloaded images
                products.append({
                    'name': product_name,
                    'url': full_url,
                    'description': product_description,
                    'price': product_price,
                    'product_line': product_line,
                    'skin_concern': skin_concern,
                    'images': downloaded_images
                })
                
                # Be nice to the server
                time.sleep(1)
                
            except Exception as e:
                print(f"Error processing product {link}: {e}")
        
        # Process shop/collection pages to find more products
        for link in shop_links:
            full_url = clean_url(link)
            try:
                print(f"Scraping collection page: {full_url}")
                collection_response = requests.get(full_url)
                collection_soup = BeautifulSoup(collection_response.text, 'html.parser')
                
                # Find product links within the collection
                for product_link in collection_soup.find_all('a', class_='product-card'):
                    href = product_link.get('href')
                    if href and '/products/' in href:
                        if href not in product_links:
                            product_links.append(href)
                
                # Be nice to the server
                time.sleep(1)
                
            except Exception as e:
                print(f"Error processing collection {link}: {e}")
        
        print(f"Total products found: {len(products)}")
        print(f"Total product links found: {len(product_links)}")
        
        # Save products data to JSON file
        with open('products.json', 'w') as f:
            json.dump(products, f, indent=4)
        
        print(f"Product data saved to products.json")
        
        return products
    
    except Exception as e:
        print(f"Error scraping website: {e}")
        return []

if __name__ == "__main__":
    print("Starting to scrape product images...")
    products = scrape_product_images()
    print(f"Completed scraping. Downloaded information for {len(products)} products.") 