"""
NeutriherbsKenya Image Update Guide

This script does not perform any automated actions but serves as a guide for updating
the placeholder images with actual product images from the Google Drive.

Steps to update your images:

1. Download all folders from Google Drive: 
   https://drive.google.com/drive/folders/1MD9_OYdgy8Uwg410XWL2SG6_dIqAfskB

2. For each category below, find a suitable image and rename it to match the filename.
   Then copy it to the correct directory to replace the placeholder.

IMPORTANT: Make sure to maintain the exact same filenames as listed below.
"""

# Product Line Images (static/images/products/)
product_lines = {
    "vitamin-c.jpg": "From 'Vit C SERIES' or 'TURMERIC & VITAMIN C' folders - main lineup image",
    "retinol.jpg": "From 'PRO' folder - look for retinol products",
    "hyaluronic-acid.jpg": "From '4D HYALURONIC ACID GEL MOISTURIZER' folder - hero image",
    "skin-whitening.jpg": "From 'LIGHTEN SKIN' folder - main lineup image",
    "snail.jpg": "From 'NEW-Snail Series' folder - hero image",
    "turmeric.jpg": "From 'TURMERIC & VITAMIN C' folder - focus on turmeric products"
}

# Product Type Images (static/images/products/)
product_types = {
    "cleanser.jpg": "Image showing facial cleansers - find in various folders",
    "toner.jpg": "Image showing toners - search across product line folders",
    "serum.jpg": "From 'SERUM' folder - representative serum image",
    "face-cream.jpg": "From 'New Day & Night Cream' folder - cream product image",
    "facial-mask.jpg": "From 'Facial Sheet Mask' folder - sheet mask image",
    "soap.jpg": "Look for bar soap products across folders",
    "body-wash.jpg": "From 'SHOWER GEL' folder - shower gel/body wash image",
    "body-lotion.jpg": "From 'Body lotion' folder - body lotion product image"
}

# Skin Concern Images (static/images/concerns/)
skin_concerns = {
    "acne-skin.jpg": "From 'SALICYLIC ACID' folder - acne treatment image",
    "aging-skin.jpg": "Look for anti-aging products (retinol/collagen products)",
    "blackhead-removal.jpg": "Look for pore cleansing products",
    "brightening-skin.jpg": "From 'Vit C SERIES' or 'LIGHTEN SKIN' folders - brightening image",
    "dehydrated-skin.jpg": "From 'HYALURONIC ACID' folder - hydrating product image",
    "dry-skin.jpg": "Look for rich moisturizers for dry skin",
    "oily-skin.jpg": "Look for oil control products (mattifying products)",
    "soothing-skin.jpg": "Look for calming products (aloe vera, etc.)"
}

print("PRODUCT LINE IMAGES")
print("-----------------")
print("Directory: static/images/products/")
print()
for filename, description in product_lines.items():
    print(f"{filename:20} - {description}")

print("\n\nPRODUCT TYPE IMAGES")
print("-----------------")
print("Directory: static/images/products/")
print()
for filename, description in product_types.items():
    print(f"{filename:20} - {description}")

print("\n\nSKIN CONCERN IMAGES")
print("-----------------")
print("Directory: static/images/concerns/")
print()
for filename, description in skin_concerns.items():
    print(f"{filename:20} - {description}")

print("""
Manual update instructions:
1. Identify the appropriate image for each category from the Google Drive folders
2. Rename the image to match the exact filename listed above
3. Copy to the corresponding directory to replace the placeholder
4. Make sure the image is in JPG format
5. Recommended dimensions: 800x600 pixels
""") 