import os
import json
import shutil
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap

def check_downloads():
    """Check if any images were successfully downloaded, create placeholders if needed"""
    # Check if products.json exists
    if not os.path.exists('products.json'):
        print("No products.json file found. Checking for sample products...")
        if os.path.exists('sample_products.json'):
            print("Using sample_products.json as fallback...")
            shutil.copy('sample_products.json', 'products.json')
        else:
            print("No sample_products.json file found. Please run download scripts first.")
            return False
    
    # Load products data
    with open('products.json', 'r') as f:
        products = json.load(f)
    
    # Check if we have any products
    if not products:
        print("No products found in products.json.")
        if os.path.exists('sample_products.json'):
            print("Using sample_products.json as fallback...")
            with open('sample_products.json', 'r') as f:
                products = json.load(f)
            
            # Save to products.json
            with open('products.json', 'w') as f:
                json.dump(products, f, indent=4)
    
    # Check if we have products with images
    products_with_images = [p for p in products if p.get('images')]
    products_without_images = [p for p in products if not p.get('images')]
    
    print(f"Total products: {len(products)}")
    print(f"Products with images: {len(products_with_images)}")
    print(f"Products without images: {len(products_without_images)}")
    
    # If we have no products with images, we need to create placeholders
    if not products_with_images:
        print("No products with images found. Creating placeholder images...")
        create_placeholder_images(products)
        return False
    
    # Check if products directory exists and has files
    if not os.path.exists('products') or not os.listdir('products'):
        print("No images found in products directory. Creating placeholder images...")
        create_placeholder_images(products)
        return False
    
    return True

def create_placeholder_image(product, index, output_dir='products'):
    """Create a placeholder image for a product"""
    # Create a 600x600 image with the product name
    width, height = 600, 600
    
    # Choose background color based on product line
    bg_color = (255, 255, 255)  # Default white
    if product.get('product_line') == 'Vitamin C':
        bg_color = (255, 200, 100)  # Orange-ish for Vitamin C
    elif product.get('product_line') == 'Retinol':
        bg_color = (200, 230, 255)  # Light blue for Retinol
    
    # Create image
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font
    try:
        # Try to use Arial on Windows, or a default system font
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        # If font file not found, use default
        font_large = ImageFont.load_default()
        font_small = font_large
    
    # Draw product name
    product_name = product.get('name', 'Unknown Product')
    
    # Wrap text
    lines = textwrap.wrap(product_name, width=20)
    
    # Draw each line of text
    y_position = 150
    for line in lines:
        # Different versions of PIL/Pillow have different textsize signatures
        try:
            line_width, line_height = draw.textsize(line, font=font_large)
        except:
            try:
                line_width, line_height = draw.textbbox((0, 0), line, font=font_large)[2:]
            except:
                # Fallback to approximation
                line_width, line_height = len(line) * 20, 40
        
        draw.text(((width - line_width) / 2, y_position), line, font=font_large, fill=(0, 0, 0))
        y_position += line_height + 10
    
    # Draw product price
    price = product.get('price', 0)
    price_text = f"₦{price:,.2f}" if price else ""
    
    # Different versions of PIL/Pillow have different text anchor options
    try:
        # For newer versions with anchor
        if price_text:
            draw.text((width // 2, height - 150), price_text, font=font_large, fill=(0, 0, 0), anchor="mm")
        
        # Draw product line and skin concern
        product_line = product.get('product_line', '')
        skin_concern = product.get('skin_concern', '')
        
        if product_line:
            draw.text((width // 2, height - 100), product_line, font=font_small, fill=(0, 0, 0), anchor="mm")
        
        if skin_concern:
            draw.text((width // 2, height - 50), skin_concern, font=font_small, fill=(0, 0, 0), anchor="mm")
        
        # Draw "Neutriherbs" at the top
        draw.text((width // 2, 50), "Neutriherbs", font=font_large, fill=(0, 0, 0), anchor="mm")
    except:
        # For older versions without anchor
        if price_text:
            # Approximate centering
            price_width, price_height = 0, 0
            try:
                price_width, price_height = draw.textsize(price_text, font=font_large)
            except:
                price_width, price_height = len(price_text) * 20, 40
            
            draw.text((width // 2 - price_width // 2, height - 150), price_text, font=font_large, fill=(0, 0, 0))
        
        # Draw product line and skin concern
        product_line = product.get('product_line', '')
        skin_concern = product.get('skin_concern', '')
        
        if product_line:
            product_line_width, _ = 0, 0
            try:
                product_line_width, _ = draw.textsize(product_line, font=font_small)
            except:
                product_line_width, _ = len(product_line) * 15, 30
            
            draw.text((width // 2 - product_line_width // 2, height - 100), product_line, font=font_small, fill=(0, 0, 0))
        
        if skin_concern:
            skin_concern_width, _ = 0, 0
            try:
                skin_concern_width, _ = draw.textsize(skin_concern, font=font_small)
            except:
                skin_concern_width, _ = len(skin_concern) * 15, 30
            
            draw.text((width // 2 - skin_concern_width // 2, height - 50), skin_concern, font=font_small, fill=(0, 0, 0))
        
        # Draw "Neutriherbs" at the top
        neutriherbs_width, _ = 0, 0
        try:
            neutriherbs_width, _ = draw.textsize("Neutriherbs", font=font_large)
        except:
            neutriherbs_width, _ = len("Neutriherbs") * 20, 40
        
        draw.text((width // 2 - neutriherbs_width // 2, 50), "Neutriherbs", font=font_large, fill=(0, 0, 0))
    
    # Save image
    os.makedirs(output_dir, exist_ok=True)
    sanitized_name = product.get('name', 'unknown').replace(' ', '_').replace('/', '_').replace('\\', '_')
    sanitized_name = ''.join(c for c in sanitized_name if c.isalnum() or c in '_-.')
    
    filename = f"{sanitized_name}_{index}.jpg"
    output_path = os.path.join(output_dir, filename)
    
    img.save(output_path)
    print(f"Created placeholder image: {output_path}")
    
    return output_path

def create_placeholder_images(products):
    """Create placeholder images for all products"""
    updated_products = []
    
    for product in products:
        # Create placeholder images (3 per product)
        images = []
        for i in range(3):
            image_path = create_placeholder_image(product, i)
            images.append(image_path)
        
        # Update product with image paths
        product['images'] = images
        updated_products.append(product)
    
    # Save updated products
    with open('products.json', 'w') as f:
        json.dump(updated_products, f, indent=4)
    
    print(f"Created placeholder images for {len(products)} products and updated products.json")

def try_download_sample_images():
    """Try to download sample Neutriherbs product images from online sources"""
    sample_images = [
        "https://ng.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/75/8233501/1.jpg",
        "https://ng.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/75/8233501/2.jpg",
        "https://ng.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/51/5233501/1.jpg",
        "https://ng.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/46/097387/1.jpg",
        "https://ng.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/46/097387/2.jpg"
    ]
    
    os.makedirs('products', exist_ok=True)
    
    downloaded = []
    for i, url in enumerate(sample_images):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                filename = f"neutriherbs_sample_{i}.jpg"
                filepath = os.path.join('products', filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                downloaded.append(filepath)
                print(f"Downloaded sample image: {filepath}")
        except Exception as e:
            print(f"Error downloading sample image {url}: {e}")
    
    return downloaded

if __name__ == "__main__":
    print("Checking for downloaded product images...")
    if not check_downloads():
        print("Trying to download sample images from alternative sources...")
        sample_images = try_download_sample_images()
        
        if sample_images:
            print(f"Downloaded {len(sample_images)} sample images from alternative sources.")
        else:
            print("Could not download sample images. Using generated placeholders instead.")
    
    print("Check complete.") 