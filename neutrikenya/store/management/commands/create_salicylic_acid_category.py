from django.core.management.base import BaseCommand
from store.models import Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Create Salicylic Acid category'

    def handle(self, *args, **options):
        category_name = 'Salicylic Acid'
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
                'description': 'Products formulated with Salicylic Acid to effectively treat acne, unclog pores, and exfoliate the skin. These specialized products help to control oil production, reduce breakouts, and promote clearer, healthier-looking skin.'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Successfully created category: {category.name}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Category already exists: {category.name}")) 