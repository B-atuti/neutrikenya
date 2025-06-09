"""
NeutriherbsKenya Image Update Helper

This script provides guidance on which images from the Google Drive folder
should be used to replace each placeholder image on the website.
"""

import os
import sys
from textwrap import dedent

def print_section(title, content):
    """Print a section with a title and content."""
    print("\n" + "="*80)
    print(f"{title}".center(80))
    print("="*80 + "\n")
    print(dedent(content))
    
def create_directories():
    """Ensure the image directories exist."""
    os.makedirs("static/images/products", exist_ok=True)
    os.makedirs("static/images/concerns", exist_ok=True)
    print("✓ Image directories created/confirmed")

def main():
    """Main function to run the script."""
    print("\n" + "*"*80)
    print("NEUTRIHERBS KENYA IMAGE UPDATE GUIDE".center(80))
    print("*"*80 + "\n")

    print(dedent("""
    To update the placeholder images with real product images from Google Drive:
    
    1. Download all folders from this Google Drive link:
       https://drive.google.com/drive/folders/1MD9_OYdgy8Uwg410XWL2SG6_dIqAfskB
    
    2. For each category below, find a suitable image from the downloaded folders
       and rename it to match the required filename.
    
    3. Copy the renamed images to replace the placeholders in the correct directories.
    
    IMPORTANT: Maintain the exact filenames listed below to ensure the templates work.
    """))
    
    # Ensure directories exist
    create_directories()
    
    # Product Lines
    print_section("PRODUCT LINE IMAGES", """
    Location: static/images/products/
    
    vitamin-c.jpg       - From 'Vit C SERIES' folder - main lineup image
    retinol.jpg         - From 'PRO' folder - retinol product image
    hyaluronic-acid.jpg - From '4D HYALURONIC ACID' folder - hero image  
    skin-whitening.jpg  - From 'LIGHTEN SKIN' folder - main lineup image
    snail.jpg           - From 'NEW-Snail Series' folder - hero image
    turmeric.jpg        - From 'TURMERIC & VITAMIN C' folder - turmeric products
    """)
    
    # Product Types
    print_section("PRODUCT TYPE IMAGES", """
    Location: static/images/products/
    
    cleanser.jpg        - Image showing facial cleansers
    toner.jpg           - Image showing toners
    serum.jpg           - From 'SERUM' folder - serum product
    face-cream.jpg      - From 'New Day & Night Cream' folder - cream product
    facial-mask.jpg     - From 'Facial Sheet Mask' folder - sheet mask image
    soap.jpg            - Bar soap product image
    body-wash.jpg       - From 'SHOWER GEL' folder - body wash image
    body-lotion.jpg     - From 'Body lotion' folder - body lotion image
    """)
    
    # Skin Concerns
    print_section("SKIN CONCERN IMAGES", """
    Location: static/images/concerns/
    
    acne-skin.jpg           - From 'SALICYLIC ACID' folder - acne treatment
    aging-skin.jpg          - Anti-aging product (retinol/collagen)
    blackhead-removal.jpg   - Pore cleansing product image
    brightening-skin.jpg    - From 'Vit C' or 'LIGHTEN SKIN' - brightening product
    dehydrated-skin.jpg     - From 'HYALURONIC ACID' folder - hydrating product
    dry-skin.jpg            - Rich moisturizer product
    oily-skin.jpg           - Oil control product
    soothing-skin.jpg       - Calming product (aloe vera, etc.)
    """)
    
    # Tips
    print_section("TIPS FOR SELECTING IMAGES", """
    1. For product line pages: Choose images that show multiple products from the line
    
    2. For product type pages: Select images that clearly show the product type
    
    3. For skin concern pages: Use images that show the product targeting that concern
    
    4. Image recommendations:
       - JPG format
       - Landscape orientation (wider than tall)
       - Clear, professional product images
       - Resize to approximately 800x600 pixels if needed
    """)
    
    # Folder mapping
    print_section("FOLDER MAPPING GUIDE", """
    Vit C SERIES          → vitamin-c.jpg, brightening-skin.jpg
    TURMERIC & VITAMIN C  → turmeric.jpg 
    NEW-Snail Series      → snail.jpg
    HYALURONIC ACID       → hyaluronic-acid.jpg, dehydrated-skin.jpg
    LIGHTEN SKIN          → skin-whitening.jpg
    SALICYLIC ACID        → acne-skin.jpg, blackhead-removal.jpg
    Body lotion           → body-lotion.jpg
    SHOWER GEL            → body-wash.jpg
    Facial Sheet Mask     → facial-mask.jpg
    SERUM                 → serum.jpg
    New Day & Night Cream → face-cream.jpg
    PRO                   → retinol.jpg, aging-skin.jpg
    """)
    
if __name__ == "__main__":
    main() 