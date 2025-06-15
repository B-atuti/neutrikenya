from django.core.management.base import BaseCommand
from django.core.files import File
from store.models import Product, ProductImage, Category
import os
import shutil
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Import hyaluronic acid images from static folder to media folder and create product'

    def handle(self, *args, **options):
        # Get the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        
        # Source directory for hyaluronic acid images
        source_dir = os.path.join(project_root, 'static', 'images', 'Hyaluronic Acid')
        
        # Create media directory for products if it doesn't exist
        media_dir = os.path.join(project_root, 'media', 'products')
        os.makedirs(media_dir, exist_ok=True)
        
        # Get or create hyaluronic acid category
        try:
            hyaluronic_category = Category.objects.get(name='Hyaluronic Acid')
            self.stdout.write(self.style.SUCCESS(f"Found existing hyaluronic acid category: {hyaluronic_category.name}"))
        except Category.DoesNotExist:
            # Create new category with a unique slug
            base_slug = slugify('Hyaluronic Acid')
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            hyaluronic_category = Category.objects.create(
                name='Hyaluronic Acid',
                slug=slug,
                description='Our range of hyaluronic acid products for deep hydration and plumping'
            )
            self.stdout.write(self.style.SUCCESS(f"Created new hyaluronic acid category: {hyaluronic_category.name}"))
        
        # Create or get the product
        product_name = 'Hyaluronic Acid Hydrating Serum'
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
                'category': hyaluronic_category,
                'price': 3500.00,
                'description': 'A powerful hyaluronic acid serum that deeply hydrates, plumps, and smooths the skin while reducing fine lines.',
                'product_line': 'Hydration',
                'skin_concern': 'Dryness, Fine Lines',
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
            # Delete existing images for this product
            ProductImage.objects.filter(product=product).delete()
            
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
                
                # Create product image - use second image (index 1) as main
                with open(destination_path, 'rb') as f:
                    product_image = ProductImage(
                        product=product,
                        image=File(f, name=image_file),
                        is_main=(index == 0)  # Second image is main
                    )
                    product_image.save()
                
                self.stdout.write(self.style.SUCCESS(f"Imported image: {image_file}"))
            
            self.stdout.write(self.style.SUCCESS(f"Successfully imported {len(image_files)} images for {product.name}"))
        else:
            self.stdout.write(self.style.ERROR(f"Source directory not found: {source_dir}")) 