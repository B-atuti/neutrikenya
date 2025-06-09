from django.db import migrations
import json
import os
from django.core.files import File
from django.utils.text import slugify

def load_initial_data(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    Product = apps.get_model('store', 'Product')
    ProductImage = apps.get_model('store', 'ProductImage')

    # Create main categories
    skincare = Category.objects.create(
        name='Skincare',
        slug='skincare',
        description='All your skincare needs'
    )

    # Create subcategories based on product lines
    product_lines = [
        'Vitamin C',
        'Retinol',
        'Hyaluronic Acid',
        'Snail',
        'Turmeric',
        'Skin Whitening',
        'Argan Oil'
    ]

    categories = {}
    for line in product_lines:
        categories[line] = Category.objects.create(
            name=line,
            slug=slugify(line),
            description=f'{line} products',
            parent=skincare
        )

    # Load products from JSON file
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_file_path = os.path.join(base_dir, 'products.json')
    
    with open(json_file_path, 'r') as file:
        products_data = json.load(file)

    for product_data in products_data:
        # Get or create category based on product line
        category = categories.get(product_data['product_line'])
        if not category:
            continue

        # Create product
        product = Product.objects.create(
            name=product_data['name'],
            slug=slugify(product_data['name']),
            description=product_data['description'],
            price=product_data['price'],
            category=category,
            is_available=True,
            product_line=product_data['product_line'],
            skin_concern=product_data['skin_concern']
        )

def reverse_load(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    Category.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('store', '0004_order_delivery_instructions_order_payment_method_and_more'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, reverse_load),
    ] 