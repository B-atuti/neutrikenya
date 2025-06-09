import os
import requests
from urllib.parse import urljoin, urlparse
import json

# Product image URLs from current Neutriherbs.com
PRODUCT_IMAGES = {
    'vitamin_c': {
        'super_booster': 'https://cdn.shopify.com/s/files/1/0648/1955/files/Super-Booster-Vitamin-C-Plus-Brightening-Serum-20-VC.jpg',
        'serum': 'https://cdn.shopify.com/s/files/1/0648/1955/files/Vitamin-C-Serum-Helps-Lighten-And-Brighten-Your-Skin.jpg',
        'cream': 'https://cdn.shopify.com/s/files/1/0648/1955/files/Vitamin-C-Brightening-and-Glow-Cream-For-Antioxidant-And-Skin-Radiant.jpg',
        'sunscreen': 'https://cdn.shopify.com/s/files/1/0648/1955/files/Vitamin-C-Sunscreen-SPF50-With-Double-UV-Protection.jpg',
        'cleanser': 'https://cdn.shopify.com/s/files/1/0648/1955/files/Vitamin-C-Face-Cleanser-Soothes-And-Purifies-For-Super-Clean.jpg',
        'toner': 'https://cdn.shopify.com/s/files/1/0648/1955/files/Vitamin-C-Brightening-Glowing-Skin-Toner.jpg'
    },
    'snail_mucin': {
        'cream': 'https://cdn.shopify.com/s/files/1/0648/1955/files/The-Best-All-In-One-Snail-Mucin-Cream-For-Anti-Aging-And-Skin-Repair.jpg',
        'serum': 'https://cdn.shopify.com/s/files/1/0648/1955/files/The-Best-All-In-One-Snail-Mucin-Serum-For-Anti-Aging-And-Skin-Soothing.jpg'
    },
    'lightening': {
        'cream': 'https://cdn.shopify.com/s/files/1/0648/1955/files/Brightening-And-Lightening-Skin-Face-Cream-For-Dark-Skin.jpg',
        'face_wash': 'https://cdn.shopify.com/s/files/1/0648/1955/files/Neutriherbs-Best-Face-Wash-For-Lightening-Skin.jpg',
        'serum': 'https://cdn.shopify.com/s/files/1/0648/1955/files/Skin-Lightening-Serum-For-Dark-Uneven-Tone-Skin.jpg',
        'soap': 'https://cdn.shopify.com/s/files/1/0648/1955/files/Best-Skin-Lightening-Soap-For-Glowing-Skin.jpg',
        'body_lotion': 'https://cdn.shopify.com/s/files/1/0648/1955/files/Skin-Whitening-Body-Lotion-For-Dark-Skin.jpg'
    }
}

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)

def download_image(url, save_path):
    """Download image from URL and save to specified path"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded: {save_path}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False

def main():
    # Base directory for product images
    base_dir = os.path.join('static', 'images', 'products')
    
    # Create category directories
    for category in PRODUCT_IMAGES.keys():
        category_dir = os.path.join(base_dir, category)
        create_directory(category_dir)
        
        # Download images for each product in category
        for product, url in PRODUCT_IMAGES[category].items():
            # Get file extension from URL
            ext = os.path.splitext(urlparse(url).path)[1]
            if not ext:
                ext = '.jpg'  # Default to .jpg if no extension found
                
            # Create filename
            filename = f"{product}{ext}"
            save_path = os.path.join(category_dir, filename)
            
            # Download image
            download_image(url, save_path)

if __name__ == "__main__":
    main() 