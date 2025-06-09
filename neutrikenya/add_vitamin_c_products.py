import os
import sys
import django
import shutil
from pathlib import Path

# Add the project to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
django_project_path = os.path.join(project_root, 'neutrikenya')
sys.path.append(django_project_path)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neutrikenya.settings')
django.setup()

from django.core.files import File
from django.utils.text import slugify
from store.models import Product, Category, ProductImage

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
    
    # Define all Vitamin C products
    products_data = [
        {
            'slug': "neutriherbs-vitamin-c-20-plus-serum",
            'name': "Neutriherbs Vitamin C 20% Plus Brightening Serum",
            'description': "A powerful antioxidant serum that brightens skin, fades hyperpigmentation, and protects against environmental damage. Contains 20% Vitamin C for maximum efficacy.",
            'price': 1800.00,
            'original_price': 2200.00,
            'image_name': "Vitamin_c_plus-2_b9e3f212-0d1a-4479-a5be-85c716df7ac4.webp"
        },
        {
            'slug': "neutriherbs-vitamin-c-serum",
            'name': "Neutriherbs Vitamin C Brightening Serum",
            'description': "Enriched with Vitamin C to brighten your complexion, reduce dark spots, and improve skin elasticity. Contains orange extract for natural glow.",
            'price': 1500.00,
            'original_price': 1800.00,
            'image_name': "2023-VitaminCSerum-6.webp"
        },
        {
            'slug': "neutriherbs-vitamin-c-cream",
            'name': "Neutriherbs Vitamin C Brightening Cream",
            'description': "Rich moisturizing cream infused with Vitamin C for brightening and antioxidant protection. Perfect for daily use.",
            'price': 1600.00,
            'original_price': 1900.00,
            'image_name': "Vitaminccream-10.webp"
        },
        {
            'slug': "neutriherbs-vitamin-c-cleanser",
            'name': "Neutriherbs Vitamin C Brightening Cleanser",
            'description': "Gentle yet effective cleanser enriched with Vitamin C to brighten while cleansing. Removes impurities without stripping the skin.",
            'price': 1200.00,
            'original_price': 1500.00,
            'image_name': "Vitaminccleanser-25.webp"
        },
        {
            'slug': "neutriherbs-vitamin-c-toner",
            'name': "Neutriherbs Vitamin C Brightening Toner",
            'description': "Alcohol-free toner with Vitamin C to balance, brighten and prep skin for the rest of your routine.",
            'price': 1300.00,
            'original_price': 1600.00,
            'image_name': "2024-Vitamin_C_Skin_Toner-13.webp"
        },
        {
            'slug': "neutriherbs-vitamin-c-sunscreen-spf50",
            'name': "Neutriherbs Vitamin C Sunscreen SPF50",
            'description': "High protection sunscreen with Vitamin C for brightening and UV protection. Water-resistant formula.",
            'price': 1700.00,
            'original_price': 2000.00,
            'image_name': "SunscreenLotion-SPF50-54.webp"
        },
        {
            'slug': "neutriherbs-vitamin-c-sunscreen-spf30",
            'name': "Neutriherbs Vitamin C Sunscreen SPF30",
            'description': "Daily sunscreen with Vitamin C for light protection and brightening benefits. Perfect for everyday use.",
            'price': 1500.00,
            'original_price': 1800.00,
            'image_name': "SunscreenLotion-SPF30-24.webp"
        }
    ]
    
    # Create products and add images
    for product_data in products_data:
        # Create or update product
        product, created = Product.objects.get_or_create(
            slug=product_data['slug'],
            defaults={
                'name': product_data['name'],
                'description': product_data['description'],
                'price': product_data['price'],
                'original_price': product_data['original_price'],
                'category': skincare_category,
                'is_available': True,
                'stock': 15,
                'product_line': "Vitamin C",
                'skin_concern': "Brightening, Anti-aging",
                'featured': True
            }
        )
        
        if created:
            print(f"Created new product: {product.name}")
        else:
            print(f"Using existing product: {product.name}")
        
        try:
            # Source path from brightening with vc folder
            src_path = os.path.join(project_root, "brightening with vc", product_data['image_name'])
            
            # Check if source image exists
            if not os.path.exists(src_path):
                print(f"Image not found: {src_path}")
                continue
                
            # Create media directory if it doesn't exist
            media_products_dir = os.path.join(django_project_path, 'media', 'products')
            os.makedirs(media_products_dir, exist_ok=True)
            
            # Destination path
            dest_path = os.path.join(media_products_dir, product_data['image_name'])
            
            # Copy the file to media directory
            shutil.copy2(src_path, dest_path)
            
            # Check if image already exists for this product
            if ProductImage.objects.filter(product=product, image=f"products/{product_data['image_name']}").exists():
                print(f"Image already exists for product: {product.name}")
                continue
            
            # Create the ProductImage instance
            product_image = ProductImage(
                product=product,
                is_main=True
            )
            
            # Save the image to the model
            with open(dest_path, 'rb') as f:
                product_image.image.save(product_data['image_name'], File(f), save=True)
            
            print(f"Added image for product: {product.name}")
        except Exception as e:
            print(f"Error adding image for {product.name}: {e}")

    print("Vitamin C products added successfully!")

if __name__ == "__main__":
    add_vitamin_c_products() 