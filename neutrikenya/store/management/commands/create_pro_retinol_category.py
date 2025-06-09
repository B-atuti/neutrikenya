from django.core.management.base import BaseCommand
from store.models import Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Create Pro Retinol category'

    def handle(self, *args, **options):
        category_name = 'Pro Retinol'
        category_slug = slugify(category_name)
        
        # Ensure unique slug
        counter = 1
        while Category.objects.filter(slug=category_slug).exists():
            category_slug = f"{slugify(category_name)}-{counter}"
            counter += 1
        
        # Create the category
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={
                'slug': category_slug,
                'description': 'Advanced retinol formulations designed to target signs of aging, improve skin texture, and promote cellular renewal. Our Pro Retinol line combines the power of retinol with complementary ingredients for maximum efficacy while maintaining skin comfort.'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Successfully created category: {category.name}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Category already exists: {category.name}")) 