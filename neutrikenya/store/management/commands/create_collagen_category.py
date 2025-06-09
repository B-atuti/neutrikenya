from django.core.management.base import BaseCommand
from store.models import Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Create Collagen category'

    def handle(self, *args, **options):
        # Create the category
        category_name = 'Collagen'
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
                'description': 'Our Collagen collection features products enriched with collagen to help improve skin elasticity, reduce fine lines and wrinkles, and promote a more youthful appearance. These products are designed to support your skin\'s natural collagen production and maintain its firmness and structure.'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Successfully created category: {category.name}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Category already exists: {category.name}")) 