import os
import sys
import django
import shutil
from pathlib import Path

# Add the project to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neutrikenya.neutrikenya.settings')
django.setup()

from django.core.files import File
from django.utils.text import slugify
from neutrikenya.store.models import Product, Category, ProductImage

def add_vitamin_c_products():
    """Add Vitamin C products to the database"""
    print("Adding Vitamin C products...")
    
    # Get or create the Skincare category
    skincare_category, created = Category.objects.get_or_create(
        name="Skincare",
        slug="skincare",
        defaults={
            "description": "Skincare products for all skin types"
        }
    )
    
    if created:
        print(f"Created new category: {skincare_category.name}")
    else:
        print(f"Using existing category: {skincare_category.name}")
    
    # Product 1: Vitamin C 20% Plus Serum
    product1, created = Product.objects.get_or_create(
        slug="neutriherbs-vitamin-c-20-plus-serum",
        defaults={
            'name': "Neutriherbs Vitamin C 20% Plus Serum",
            'description': "A powerful antioxidant serum that brightens skin, fades hyperpigmentation, and protects against environmental damage. Suitable for all skin types except sensitive skin.",
            'price': 1800.00,
            'original_price': 2200.00,
            'category': skincare_category,
            'is_available': True,
            'stock': 15,
            'product_line': "Vitamin C",
            'skin_concern': "Brightening, Anti-aging",
            'featured': True
        }
    )
    
    if created:
        print(f"Created new product: {product1.name}")
    else:
        print(f"Using existing product: {product1.name}")
    
    # Product 2: Vitamin C Brightening Serum
    product2, created = Product.objects.get_or_create(
        slug="neutriherbs-vitamin-c-brightening-serum",
        defaults={
            'name': "Neutriherbs Vitamin C Brightening Serum",
            'description': "Enriched with Vitamin C to brighten your complexion, reduce dark spots, and improve skin elasticity. Contains orange extract for natural glow.",
            'price': 1500.00,
            'original_price': 1800.00,
            'category': skincare_category,
            'is_available': True,
            'stock': 20,
            'product_line': "Vitamin C",
            'skin_concern': "Brightening, Hyperpigmentation",
            'featured': True
        }
    )
    
    if created:
        print(f"Created new product: {product2.name}")
    else:
        print(f"Using existing product: {product2.name}")
    
    # Product 3: Vitamin C Brightening & Glow Daily Facial Cleanser
    product3, created = Product.objects.get_or_create(
        slug="neutriherbs-vitamin-c-brightening-facial-cleanser",
        defaults={
            'name': "Neutriherbs Vitamin C Brightening & Glow Daily Facial Cleanser",
            'description': "Effectively cleanses the skin and removes dirt, oil and makeup. Enriched with Vitamin E, Camellia Sinensis, Orange and Glycyrrhiza Glabra for gentle brightening and skin health. Suitable for all skin types.",
            'price': 1200.00,
            'original_price': 1500.00,
            'category': skincare_category,
            'is_available': True,
            'stock': 25,
            'product_line': "Vitamin C",
            'skin_concern': "Brightening, Cleansing",
            'featured': False
        }
    )
    
    if created:
        print(f"Created new product: {product3.name}")
    else:
        print(f"Using existing product: {product3.name}")
    
    # Process and save the images
    products = [
        (product1, "vitamin_c_20_serum.jpg"),
        (product2, "vitamin_c_brightening_serum.jpg"),
        (product3, "vitamin_c_cleanser.jpg")
    ]
    
    # Save temporary images from temp_images folder to media
    for product, image_name in products:
        try:
            # Source path from temp_images
            src_path = os.path.join("temp_images", image_name)
            
            # Check if source image exists
            if not os.path.exists(src_path):
                print(f"Image not found: {src_path}")
                continue
                
            # Create media directory if it doesn't exist
            media_products_dir = os.path.join('neutrikenya', 'media', 'products')
            os.makedirs(media_products_dir, exist_ok=True)
            
            # Destination path
            dest_path = os.path.join(media_products_dir, image_name)
            
            # Copy the file to media directory
            shutil.copy2(src_path, dest_path)
            
            # Check if image already exists for this product
            if ProductImage.objects.filter(product=product, image=f"products/{image_name}").exists():
                print(f"Image already exists for product: {product.name}")
                continue
            
            # Create the ProductImage instance
            product_image = ProductImage(
                product=product,
                is_main=True
            )
            
            # Save the image to the model
            with open(dest_path, 'rb') as f:
                product_image.image.save(image_name, File(f), save=True)
            
            print(f"Added image for product: {product.name}")
        except Exception as e:
            print(f"Error adding image for {product.name}: {e}")

    print("Vitamin C products added successfully!")

if __name__ == "__main__":
    add_vitamin_c_products() 