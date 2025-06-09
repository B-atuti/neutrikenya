import os
import requests
import json
import time
import shutil
from pathlib import Path
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils.text import slugify
from store.models import Product, Category, ProductImage

class Command(BaseCommand):
    help = 'Import hair care products from Neutriherbs.com'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting hair care product import from Neutriherbs.com'))
        
        # Create directories if they don't exist
        products_dir = 'products'
        if not os.path.exists(products_dir):
            os.makedirs(products_dir)
        
        # Download and process products
        products_data = self.fetch_neutriherbs_haircare_products()
        
        # Save to JSON for reference
        with open('haircare_products.json', 'w') as f:
            json.dump(products_data, f, indent=4)
        
        # Import the products into the database
        self.import_products(products_data)

    def download_image(self, url, folder, filename=None):
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
                self.stdout.write(f"Downloaded: {filepath}")
                return filepath
            else:
                self.stdout.write(self.style.ERROR(f"Failed to download {url}: HTTP {response.status_code}"))
                return None
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error downloading {url}: {e}"))
            return None

    def extract_product_data(self, product_url):
        """Extract product details from a product page"""
        try:
            response = requests.get(product_url)
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"Failed to access product page {product_url}: HTTP {response.status_code}"))
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
                    self.stdout.write(self.style.WARNING(f"Could not parse price from '{price_text}'"))
            
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
            self.stdout.write(self.style.ERROR(f"Error extracting product data from {product_url}: {e}"))
            return None

    def fetch_neutriherbs_haircare_products(self):
        """Fetch hair care products from neutriherbs.com"""
        products_data = []
        
        # Base URL for the Neutriherbs Global website
        BASE_URL = "https://neutriherbs.com"
        HAIR_CARE_URL = "/collections/hair-care"
        
        try:
            # Fetch hair care collection page
            self.stdout.write(f"Fetching hair care products from {BASE_URL}{HAIR_CARE_URL}")
            response = requests.get(f"{BASE_URL}{HAIR_CARE_URL}")
            
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"Failed to fetch hair care page: HTTP {response.status_code}"))
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
            
            self.stdout.write(f"Found {len(product_links)} product links")
            
            # Extract data from each product page
            for product_url in product_links:
                self.stdout.write(f"Processing {product_url}")
                product_data = self.extract_product_data(product_url)
                
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
                            filepath = self.download_image(image_url, 'products', filename)
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
            self.stdout.write(self.style.ERROR(f"Error fetching hair care products: {e}"))
        
        return products_data

    def import_products(self, products_data):
        """Import hair care products into the Django database"""
        self.stdout.write("Starting import to database...")
        
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
            self.stdout.write(self.style.SUCCESS(f"Created new category: {hair_care_category.name}"))
        else:
            self.stdout.write(f"Using existing category: {hair_care_category.name}")
        
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
                self.stdout.write(self.style.SUCCESS(f"Created sub-category: {sub_category.name}"))
        
        products_created = 0
        products_updated = 0
        images_imported = 0
        
        # Import each product
        for product_data in products_data:
            name = product_data.get('name')
            if not name:
                self.stdout.write(self.style.WARNING("Skipping product with no name"))
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
                self.stdout.write(self.style.SUCCESS(f"Created new product: {product.name} in category {sub_category.name}"))
            else:
                products_updated += 1
                self.stdout.write(f"Updating existing product: {product.name} in category {sub_category.name}")
            
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
                            self.stdout.write(f"Imported image: {filename} for product {product.name}")
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error importing image {image_path}: {e}"))
            
            # Set the first image as the main image if one exists
            product_images = ProductImage.objects.filter(product=product)
            if product_images.exists() and not product_images.filter(is_main=True).exists():
                first_image = product_images.first()
                first_image.is_main = True
                first_image.save()
                self.stdout.write(f"Set main image for {product.name}")
        
        self.stdout.write(self.style.SUCCESS(
            f"Import complete. Created {products_created} products, updated {products_updated} products, imported {images_imported} images."
        )) 