from django.core.management.base import BaseCommand
from django.core.files import File
from store.models import Product, ProductImage, Category
import os
import shutil
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Import 4D Hyaluronic Acid Gel Moisturizer images from static folder to media folder and create product'

    def handle(self, *args, **options):
        # Get the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        
        # Source directory for gel moisturizer images
        source_dir = os.path.join(project_root, 'static', 'images', '4D HYALURONIC ACID GEL MOISTURIZER')
        
        # Create media directory for products if it doesn't exist
        media_dir = os.path.join(project_root, 'media', 'products')
        os.makedirs(media_dir, exist_ok=True)
        
        # Get Hyaluronic Acid category
        try:
            hyaluronic_acid_category = Category.objects.get(name='Hyaluronic Acid')
            self.stdout.write(self.style.SUCCESS(f"Found Hyaluronic Acid category: {hyaluronic_acid_category.name}"))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR("Hyaluronic Acid category not found. Please run create_hyaluronic_acid_category command first."))
            return
        
        # Create or get the product
        product_name = '4D Hyaluronic Acid Gel Moisturizer'
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
                'category': hyaluronic_acid_category,
                'price': 2300.00,
                'description': '''A revolutionary 4D Hyaluronic Acid Gel Moisturizer that provides multi-dimensional hydration for plump, youthful skin. This lightweight gel formula combines four different molecular weights of Hyaluronic Acid to penetrate different layers of the skin, delivering intense hydration and helping to reduce the appearance of fine lines and wrinkles.

INGREDIENTS:
Aqua, Sodium Hyaluronate, Glycerin, Niacinamide, Panthenol, Aloe Barbadensis Leaf Juice, Allantoin, Sodium PCA, Betaine, Xanthan Gum, Phenoxyethanol, Ethylhexylglycerin, Fragrance (Parfum), Citric Acid, Sodium Citrate.

DIRECTIONS:
Apply a small amount to clean, dry skin after cleansing and toning. Gently massage in upward circular motions until fully absorbed. Use morning and evening for best results.

STORAGE:
Store in a cool, dry place away from direct sunlight. Keep the lid tightly closed when not in use.

KEY BENEFITS:
• Multi-dimensional hydration with 4D Hyaluronic Acid technology
• Lightweight, non-greasy gel formula
• Suitable for all skin types
• Helps reduce the appearance of fine lines and wrinkles
• Provides long-lasting moisture
• Improves skin elasticity and firmness
• Calms and soothes the skin
• Creates a smooth, plump complexion

RECOMMENDED FOR:
• Dry and dehydrated skin
• Mature skin
• Fine lines and wrinkles
• Loss of elasticity
• Dull complexion

WORKS WELL WITH:
• Vitamin C Serum - For enhanced brightening and antioxidant protection
• Snail Mucin Essence - For additional hydration and skin repair
• Retinol Night Cream - For comprehensive anti-aging benefits
• Turmeric Face Wash - For gentle cleansing and brightening
• Collagen Boosting Serum - For improved skin elasticity and firmness

NET WEIGHT: 50g''',
                'product_line': 'Hyaluronic Acid',
                'skin_concern': 'Dry Skin, Fine Lines, Dehydrated Skin',
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
                
                # Create product image - use first image as main
                with open(destination_path, 'rb') as f:
                    product_image = ProductImage(
                        product=product,
                        image=File(f, name=image_file),
                        is_main=(index == 0)  # First image is main
                    )
                    product_image.save()
                
                self.stdout.write(self.style.SUCCESS(f"Imported image: {image_file}"))
            
            self.stdout.write(self.style.SUCCESS(f"Successfully imported {len(image_files)} images for {product.name}"))
        else:
            self.stdout.write(self.style.ERROR(f"Source directory not found: {source_dir}")) 