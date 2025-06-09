from django.core.management.base import BaseCommand
from store.models import Product, ProductImage, Category

class Command(BaseCommand):
    help = 'Verify cleanser images in the database'

    def handle(self, *args, **options):
        # Get the cleanser product
        try:
            product = Product.objects.get(name='Vitamin C Face Cleanser')
            self.stdout.write(self.style.SUCCESS(f"Found product: {product.name}"))
            
            # Check images
            images = ProductImage.objects.filter(product=product)
            if images.exists():
                self.stdout.write(self.style.SUCCESS(f"Found {images.count()} images:"))
                for image in images:
                    self.stdout.write(f"- {image.image.name} (Main: {image.is_main})")
            else:
                self.stdout.write(self.style.ERROR("No images found for this product"))
                
        except Product.DoesNotExist:
            self.stdout.write(self.style.ERROR("Product 'Vitamin C Face Cleanser' not found")) 