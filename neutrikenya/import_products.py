import os
import django
import shutil
from pathlib import Path
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neutrikenya.settings')
django.setup()

from django.core.files import File
from django.utils.text import slugify
from store.models import Product, Category, ProductImage

def import_products():
    """Import downloaded products into the Django database"""
    print("Starting product import...")
    
    # Check if the products.json file exists (generated from download_images.py)
    if not os.path.exists('products.json'):
        print("Products JSON file not found. Please run download_images.py first.")
        return
    
    # Load the products data
    with open('products.json', 'r') as f:
        products_data = json.load(f)
    
    # Create a default category for imported products
    neutriherbs_category, created = Category.objects.get_or_create(
        name="Neutriherbs Products",
        slug="neutriherbs-products",
        defaults={
            "description": "Products imported from Neutriherbs Nigeria website"
        }
    )
    
    if created:
        print(f"Created new category: {neutriherbs_category.name}")
    else:
        print(f"Using existing category: {neutriherbs_category.name}")
    
    products_created = 0
    products_updated = 0
    images_imported = 0
    
    # Import each product
    for product_data in products_data:
        name = product_data.get('name')
        if not name:
            print("Skipping product with no name")
            continue
        
        # Create a slug from the name
        slug = slugify(name)
        
        # Check if product already exists
        product, created = Product.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'description': product_data.get('description', ''),
                'price': product_data.get('price', 0),
                'category': neutriherbs_category,
                'is_available': True,
                'stock': 10,  # Default stock
                'product_line': product_data.get('product_line', ''),
                'skin_concern': product_data.get('skin_concern', '')
            }
        )
        
        if created:
            products_created += 1
            print(f"Created new product: {product.name}")
        else:
            products_updated += 1
            print(f"Updating existing product: {product.name}")
        
        # Import images for this product
        image_paths = product_data.get('images', [])
        for image_path in image_paths:
            if os.path.exists(image_path):
                try:
                    # Get filename
                    filename = os.path.basename(image_path)
                    
                    # Check if this image already exists
                    if not ProductImage.objects.filter(product=product, image=f"products/{filename}").exists():
                        # Copy image to media/products/
                        media_products_dir = os.path.join('media', 'products')
                        os.makedirs(media_products_dir, exist_ok=True)
                        
                        # Destination path
                        dest_path = os.path.join(media_products_dir, filename)
                        
                        # Copy the file
                        shutil.copy2(image_path, dest_path)
                        
                        # Create the ProductImage instance
                        product_image = ProductImage(
                            product=product,
                            is_main=False  # Set first image as main below
                        )
                        
                        # Open the file and save it to the model
                        with open(dest_path, 'rb') as f:
                            product_image.image.save(filename, File(f), save=True)
                        
                        images_imported += 1
                        print(f"Imported image: {filename} for product {product.name}")
                except Exception as e:
                    print(f"Error importing image {image_path}: {e}")
        
        # Set the first image as the main image if one exists
        product_images = ProductImage.objects.filter(product=product)
        if product_images.exists() and not product_images.filter(is_main=True).exists():
            first_image = product_images.first()
            first_image.is_main = True
            first_image.save()
            print(f"Set main image for {product.name}")
    
    print(f"Import complete. Created {products_created} products, updated {products_updated} products, imported {images_imported} images.")

if __name__ == "__main__":
    import_products() 