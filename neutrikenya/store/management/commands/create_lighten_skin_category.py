from django.core.management.base import BaseCommand
from store.models import Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Create Lighten Skin category'

    def handle(self, *args, **options):
        # Create the Lighten Skin category
        category_name = 'Lighten Skin'
        base_slug = slugify(category_name)
        slug = base_slug
        counter = 1
        
        # Ensure unique slug
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        try:
            category = Category.objects.create(
                name=category_name,
                slug=slug,
                description='Our range of natural skin lightening products that help even out skin tone and reduce hyperpigmentation for a brighter, more radiant complexion.'
            )
            self.stdout.write(self.style.SUCCESS(f"Successfully created category: {category.name}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating category: {str(e)}")) 