import os
import sys
import django
import shutil
from pathlib import Path

# Add the project to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neutrikenya.settings')
django.setup()

from django.core.files import File
from django.utils.text import slugify
from store.models import Product, Category, ProductImage

def add_beauty_tools():
    """Add Beauty Tools products to the database"""
    print("Adding Beauty Tools products...")
    
    # Get or create the Beauty Tools category
    beauty_tools_category, created = Category.objects.get_or_create(
        name="Beauty Tools",
        slug="beauty-tools",
        defaults={
            "description": "Facial massage tools for enhanced skincare results"
        }
    )
    
    if created:
        print(f"Created new category: {beauty_tools_category.name}")
    else:
        print(f"Using existing category: {beauty_tools_category.name}")
    
    # Product 1: Jade Roller
    product1, created = Product.objects.get_or_create(
        slug="neutriherbs-jade-roller",
        defaults={
            'name': "Facial Massage Jade Roller For Relaxing And De-stressing",
            'description': "100% Natural Jade Stone Roller & Gua Sha - Video Tutorial & Ebook Included. Face & Neck Massager for Skin Care, Facial Roller to Press Serums, Cream and Oil Into Skin. Beauty Roller to Improve the Appearance of Your Skin, Provide Relaxation, Massage Your Face & Enhance Your Skin Care Results.",
            'price': 2000.00,
            'original_price': 2500.00,
            'category': beauty_tools_category,
            'is_available': True,
            'stock': 15,
            'product_line': "Beauty Tool",
            'skin_concern': "Anti-aging, Relaxation",
            'featured': True
        }
    )
    
    if created:
        print(f"Created new product: {product1.name}")
    else:
        print(f"Using existing product: {product1.name}")
    
    # Product 2: Rose Quartz Roller
    product2, created = Product.objects.get_or_create(
        slug="neutriherbs-rose-quartz-roller",
        defaults={
            'name': "Rose Quartz Facial Jade Roller For Soothing And Calming",
            'description': "Natural Authentic Crystal-Jade Roller Gua Sha Alternative-Reduces Puffiness & Wrinkles. 100% Natural Crystal Stone, Anti Aging Facial Massager, Slimming Healing Gua Sha Massage Tool. Best Face Roller and Skincare Tool for Facial Massage, Quality Pink Stone Face Roller Great for Skin on Face and body.",
            'price': 1800.00,
            'original_price': 2200.00,
            'category': beauty_tools_category,
            'is_available': True,
            'stock': 20,
            'product_line': "Beauty Tool",
            'skin_concern': "Puffiness, Wrinkles",
            'featured': True
        }
    )
    
    if created:
        print(f"Created new product: {product2.name}")
    else:
        print(f"Using existing product: {product2.name}")
    
    # Product 3: Derma Roller
    product3, created = Product.objects.get_or_create(
        slug="neutriherbs-titanium-derma-roller",
        defaults={
            'name': "Neutriherbs® 0.3 Titanium Derma Roller For Starter and Sensitive Skin",
            'description': "Premium derma roller for face and sensitive skin. Perfect for beginners, this microneedle roller helps enhance product absorption and promote skin renewal. Use with your favorite serum for best results.",
            'price': 2000.00,
            'original_price': 2500.00,
            'category': beauty_tools_category,
            'is_available': True,
            'stock': 25,
            'product_line': "Beauty Tool",
            'skin_concern': "Acne Scars, Fine Lines",
            'featured': False
        }
    )
    
    if created:
        print(f"Created new product: {product3.name}")
    else:
        print(f"Using existing product: {product3.name}")
    
    # Product 4: Jade Facial Massager Beauty Set
    product4, created = Product.objects.get_or_create(
        slug="neutriherbs-jade-facial-massager-set",
        defaults={
            'name': "Neutriherbs Jade Facial Massager Beauty Set With Serum",
            'description': "Jade Roller and Gua Sha Scraping Set For Facial Massage & Anti-Aging Treatment. Facial Roller Massage Eye Treatment Roller for Natural Anti-aging, Skin Tightening, Rejuvenate Face and Neck. Face Roller and Facial Beauty Roller Skin Care Tools with complementary serum.",
            'price': 5400.00,
            'original_price': 6900.00,
            'category': beauty_tools_category,
            'is_available': True,
            'stock': 10,
            'product_line': "Beauty Tool",
            'skin_concern': "Anti-aging, Skin Tightening",
            'featured': True
        }
    )
    
    if created:
        print(f"Created new product: {product4.name}")
    else:
        print(f"Using existing product: {product4.name}")
    
    # Product 5: Rose Quartz Roller Beauty Set
    product5, created = Product.objects.get_or_create(
        slug="neutriherbs-rose-quartz-roller-set",
        defaults={
            'name': "Neutriherbs Rose Quartz Roller Beauty Set With Serum",
            'description': "Best Face Roller and Skincare Tool for Facial Massage, Quality Pink Stone Face Roller Great for Skin. Spa Grade Rose Quartz Facial Massage Roller, Best Jade Roller for Slimming Face, Eye Puffiness, and Wrinkles. Authentic Jade Roller, Natural Rose Quartz Roller and Gua Sha with complementary serum.",
            'price': 5400.00,
            'original_price': 6900.00,
            'category': beauty_tools_category,
            'is_available': True,
            'stock': 15,
            'product_line': "Beauty Tool",
            'skin_concern': "Puffiness, Wrinkles",
            'featured': True
        }
    )
    
    if created:
        print(f"Created new product: {product5.name}")
    else:
        print(f"Using existing product: {product5.name}")
    
    # Process and save the images
    products = [
        (product1, "jade_roller.jpg"),
        (product2, "rose_quartz_roller.jpg"),
        (product3, "derma_roller.jpg"),
        (product4, "jade_roller_set.jpg"),
        (product5, "rose_quartz_set.jpg")
    ]
    
    # Create temp images for now
    os.makedirs("temp_images", exist_ok=True)
    
    for _, image_name in products:
        temp_path = os.path.join("temp_images", image_name)
        if not os.path.exists(temp_path):
            with open(temp_path, 'wb') as f:
                f.write(b"Placeholder Image")
    
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
            media_products_dir = os.path.join('media', 'products')
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

    print("Beauty Tools products added successfully!")

if __name__ == "__main__":
    add_beauty_tools() 