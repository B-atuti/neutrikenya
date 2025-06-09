import os
import django
import shutil
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neutrikenya.settings')
django.setup()

from django.core.files import File
from django.utils.text import slugify
from store.models import Product, Category, ProductImage

def import_haircare_products():
    """Import hair care products into the Django database"""
    print("Starting hair care product import...")
    
    # Check if the haircare_products.json file exists
    if not os.path.exists('haircare_products.json'):
        print("Haircare products JSON file not found. Please run download_neutriherbs_global.py first.")
        return
    
    # Load the products data
    with open('haircare_products.json', 'r') as f:
        products_data = json.load(f)
    
    # Get or create Hair Care category
    hair_care_category, created = Category.objects.get_or_create(
        name="Hair Care",
        slug="hair-care",
        defaults={
            "description": "Natural hair care products from Neutriherbs to nourish and strengthen your hair."
        }
    )
    
    # Make sure Hair Care is a top-level category
    hair_care_category.parent = None
    hair_care_category.save()
    
    if created:
        print(f"Created new category: {hair_care_category.name}")
    else:
        print(f"Using existing category: {hair_care_category.name}")
    
    # Create sub-categories for different hair care product types
    sub_categories = {
        "Shampoo": "Natural shampoos for all hair types",
        "Conditioner": "Nourishing conditioners for healthy hair",
        "Hair Masks": "Deep treatment masks for damaged hair",
        "Hair Oils": "Natural oils to nourish and promote hair growth",
        "Hair Styling": "Styling products for beautiful hairstyles"
    }
    
    for name, description in sub_categories.items():
        sub_category, created = Category.objects.get_or_create(
            name=name,
            slug=slugify(name),
            defaults={
                "description": description,
                "parent": hair_care_category
            }
        )
        
        if created:
            sub_category.parent = hair_care_category
            sub_category.save()
            print(f"Created sub-category: {sub_category.name}")
    
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
        
        # Determine subcategory based on product name
        sub_category = hair_care_category  # Default to main category
        product_name_lower = name.lower()
        
        if 'shampoo' in product_name_lower or 'cleanser' in product_name_lower:
            sub_category = Category.objects.get(name="Shampoo", parent=hair_care_category)
        elif 'conditioner' in product_name_lower:
            sub_category = Category.objects.get(name="Conditioner", parent=hair_care_category)
        elif 'mask' in product_name_lower or 'treatment' in product_name_lower:
            sub_category = Category.objects.get(name="Hair Masks", parent=hair_care_category)
        elif 'oil' in product_name_lower or 'serum' in product_name_lower:
            sub_category = Category.objects.get(name="Hair Oils", parent=hair_care_category)
        elif 'spray' in product_name_lower or 'gel' in product_name_lower or 'mousse' in product_name_lower:
            sub_category = Category.objects.get(name="Hair Styling", parent=hair_care_category)
        
        # Check if product already exists
        product, created = Product.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'description': product_data.get('description', ''),
                'price': product_data.get('price', 0),
                'category': sub_category,
                'is_available': True,
                'stock': 10,  # Default stock
                'product_line': product_data.get('product_line', 'Hair Care'),
            }
        )
        
        # If product exists but has a different category, update it
        if not created and product.category != sub_category:
            product.category = sub_category
            product.save()
        
        if created:
            products_created += 1
            print(f"Created new product: {product.name} in category {sub_category.name}")
        else:
            products_updated += 1
            print(f"Updating existing product: {product.name} in category {sub_category.name}")
        
        # Convert USD price to KES (approx. conversion)
        if product.price > 0:
            # 1 USD ≈ 130 KES (approximate exchange rate)
            product.price = round(product.price * 130, -1)  # Round to nearest 10 KES
            product.save()
        
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
    import_haircare_products() 