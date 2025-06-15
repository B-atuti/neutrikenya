import os
import shutil
from django.core.files import File
from django.core.management.base import BaseCommand
from store.models import Product, ProductImage, Category

class Command(BaseCommand):
    help = 'Import cleanser images from static folder to media folder and create product'

    def handle(self, *args, **options):
        # Get the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        
        # Source directory for cleanser images
        src_dir = os.path.join(project_root, 'static', 'images', 'Cleansers')
        
        # Create media directory if it doesn't exist
        media_products_dir = os.path.join(project_root, 'media', 'products')
        os.makedirs(media_products_dir, exist_ok=True)
        
        # Get or create the cleanser category
        cleanser_category, _ = Category.objects.get_or_create(
            name='Cleanser',
            defaults={'description': 'Facial cleansers for all skin types'}
        )
        
        # Create the cleanser product
        product, created = Product.objects.get_or_create(
            name='Vitamin C Face Cleanser',
            slug='vitamin-c-face-cleanser',
            defaults={
                'description': 'A gentle yet effective cleanser that removes makeup and impurities while brightening the skin with Vitamin C.',
                'price': 1400,
                'category': cleanser_category,
                'is_available': True,
                'stock': 10,
                'product_line': 'Vitamin C',
                'skin_concern': 'All Skin Types'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created new product: {product.name}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Using existing product: {product.name}"))
        
        # Get all image files from the source directory
        image_files = [f for f in os.listdir(src_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        # Sort images to ensure consistent order
        image_files.sort()
        
        # Import each image
        for i, image_file in enumerate(image_files):
            try:
                # Source path
                src_path = os.path.join(src_dir, image_file)
                
                # Destination path
                dest_path = os.path.join(media_products_dir, image_file)
                
                # Copy the file to media directory
                shutil.copy2(src_path, dest_path)
                
                # Check if image already exists for this product
                if ProductImage.objects.filter(product=product, image=f"products/{image_file}").exists():
                    self.stdout.write(f"Image already exists: {image_file}")
                    continue
                
                # Create the ProductImage instance
                product_image = ProductImage(
                    product=product,
                    is_main=(i == 0)  # Set first image as main
                )
                
                # Save the image to the model
                with open(dest_path, 'rb') as f:
                    product_image.image.save(image_file, File(f), save=True)
                
                self.stdout.write(self.style.SUCCESS(f"Imported image: {image_file}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error importing image {image_file}: {e}"))
        
        self.stdout.write(self.style.SUCCESS("Cleanser images imported successfully!")) 