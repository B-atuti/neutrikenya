from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Category

class Command(BaseCommand):
    help = 'Fix missing category slugs'

    def handle(self, *args, **options):
        categories = Category.objects.all()
        fixed_count = 0
        
        for category in categories:
            if not category.slug:
                # Generate base slug
                base_slug = slugify(category.name)
                slug = base_slug
                counter = 1
                
                # Ensure unique slug
                while Category.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                # Update category
                category.slug = slug
                category.save()
                fixed_count += 1
                self.stdout.write(self.style.SUCCESS(f"Fixed slug for category: {category.name} -> {slug}"))
        
        self.stdout.write(self.style.SUCCESS(f"Successfully fixed {fixed_count} category slugs")) 