from django.core.management.base import BaseCommand
from store.models import Product, ProductImage, Category

class Command(BaseCommand):
    help = 'Check toner product and its images'

    def handle(self, *args, **options):
        # Check if toner category exists
        toner_category = Category.objects.filter(name__icontains='toner').first()
        if toner_category:
            self.stdout.write(self.style.SUCCESS(f"Found toner category: {toner_category.name}"))
        else:
            self.stdout.write(self.style.ERROR("Toner category not found!"))
            return

        # Check if toner product exists
        toner_product = Product.objects.filter(name__icontains='Vitamin C Brightening Toner').first()
        if toner_product:
            self.stdout.write(self.style.SUCCESS(f"Found toner product: {toner_product.name}"))
            self.stdout.write(f"Category: {toner_product.category.name}")
            self.stdout.write(f"Price: {toner_product.price}")
            self.stdout.write(f"Product Line: {toner_product.product_line}")
            self.stdout.write(f"Skin Concern: {toner_product.skin_concern}")
        else:
            self.stdout.write(self.style.ERROR("Toner product not found!"))
            return

        # Check product images
        images = ProductImage.objects.filter(product=toner_product)
        if images.exists():
            self.stdout.write(self.style.SUCCESS(f"Found {images.count()} images for the toner product:"))
            for image in images:
                self.stdout.write(f"- {image.image.name} (Main: {image.is_main})")
        else:
            self.stdout.write(self.style.ERROR("No images found for the toner product!")) 