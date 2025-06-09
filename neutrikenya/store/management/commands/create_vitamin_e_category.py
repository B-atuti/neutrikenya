from django.core.management.base import BaseCommand
from store.models import Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Create Vitamin E category'

    def handle(self, *args, **options):
        # Create the category
        category_name = 'Vitamin E'
        category_slug = slugify(category_name)
        
        # Ensure unique slug
        counter = 1
        while Category.objects.filter(slug=category_slug).exists():
            category_slug = f"{slugify(category_name)}-{counter}"
            counter += 1
        
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={
                'slug': category_slug,
                'description': 'Products enriched with Vitamin E, a powerful antioxidant that helps protect the skin from free radical damage, moisturize, and promote skin healing. Our Vitamin E range includes serums, creams, and body care products designed to nourish and protect your skin.'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Successfully created category: {category.name}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Category already exists: {category.name}")) 