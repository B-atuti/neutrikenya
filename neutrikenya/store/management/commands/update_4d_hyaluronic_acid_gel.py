from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = 'Update 4D Hyaluronic Acid Gel Moisturizer description'

    def handle(self, *args, **options):
        product_name = '4D Hyaluronic Acid Gel Moisturizer'
        
        try:
            product = Product.objects.get(name=product_name)
            product.description = '''A revolutionary 4D Hyaluronic Acid Gel Moisturizer that provides multi-dimensional hydration for plump, youthful skin. This lightweight gel formula combines four different molecular weights of Hyaluronic Acid to penetrate different layers of the skin, delivering intense hydration and helping to reduce the appearance of fine lines and wrinkles.

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

NET WEIGHT: 50g'''
            product.save()
            self.stdout.write(self.style.SUCCESS(f"Successfully updated product: {product.name}"))
        except Product.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Product not found: {product_name}")) 