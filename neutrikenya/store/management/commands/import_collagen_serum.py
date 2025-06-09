from django.core.management.base import BaseCommand
from django.core.files import File
from store.models import Product, ProductImage, Category
import os
import shutil
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Import Collagen Serum images from static folder to media folder and create product'

    def handle(self, *args, **options):
        # Get the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        
        # Source directory for serum images
        source_dir = os.path.join(project_root, 'static', 'images', 'COLLAGEN SERUM')
        
        # Create media directory for products if it doesn't exist
        media_dir = os.path.join(project_root, 'media', 'products')
        os.makedirs(media_dir, exist_ok=True)
        
        # Get Collagen category
        try:
            collagen_category = Category.objects.get(name='Collagen')
            self.stdout.write(self.style.SUCCESS(f"Found Collagen category: {collagen_category.name}"))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR("Collagen category not found. Please run create_collagen_category command first."))
            return
        
        # Create or get the product
        product_name = 'Collagen Serum'
        product_slug = slugify(product_name)
        
        # Ensure unique slug
        counter = 1
        while Product.objects.filter(slug=product_slug).exists():
            product_slug = f"{slugify(product_name)}-{counter}"
            counter += 1
        
        product, created = Product.objects.get_or_create(
            name=product_name,
            defaults={
                'slug': product_slug,
                'category': collagen_category,
                'price': 1700.00,
                'description': 'A powerful serum formulated with collagen to help improve skin elasticity and reduce the appearance of fine lines and wrinkles. This lightweight formula penetrates deeply into the skin to deliver active ingredients that support collagen production. Regular use helps to firm and plump the skin, resulting in a more youthful and radiant complexion.',
                'product_line': 'Collagen',
                'skin_concern': 'Aging, Loss of Elasticity, Fine Lines',
                'is_available': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created new product: {product.name}"))
        else:
            # Update the slug if it's missing
            if not product.slug:
                product.slug = product_slug
                product.save()
                self.stdout.write(self.style.SUCCESS(f"Updated slug for existing product: {product.name}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Found existing product: {product.name}"))
        
        # Import images
        if os.path.exists(source_dir):
            # Get all image files
            image_files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
            
            if not image_files:
                self.stdout.write(self.style.ERROR(f"No image files found in {source_dir}"))
                return
            
            # Sort files to ensure consistent order
            image_files.sort()
            
            # Import each image
            for index, image_file in enumerate(image_files):
                source_path = os.path.join(source_dir, image_file)
                destination_path = os.path.join(media_dir, image_file)
                
                # Copy file to media directory
                shutil.copy2(source_path, destination_path)
                
                # Create product image - use first image as main
                with open(destination_path, 'rb') as f:
                    product_image = ProductImage(
                        product=product,
                        image=File(f, name=image_file),
                        is_main=(index == 0)  # First image is main
                    )
                    product_image.save()
                
                self.stdout.write(self.style.SUCCESS(f"Imported image: {image_file}"))
            
            self.stdout.write(self.style.SUCCESS(f"Successfully imported {len(image_files)} images for {product.name}"))
        else:
            self.stdout.write(self.style.ERROR(f"Source directory not found: {source_dir}")) 