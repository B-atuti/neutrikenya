import os
import shutil
from pathlib import Path

# Map existing images to their destination paths
image_mappings = [
    # Format: (source path, destination directory, new filename)
    
    # Product line images
    ("static/images/1 (3).jpg", "static/images/products", "vitamin-c.jpg"),
    ("static/images/1 (4).jpg", "static/images/products", "retinol.jpg"),
    ("static/images/1 (17).jpg", "static/images/products", "hyaluronic-acid.jpg"),
    ("static/images/1 (1) (3).jpg", "static/images/products", "skin-whitening.jpg"),
    
    # Additional mappings can be added for other skincare images
]

def copy_images():
    """Copy and rename images to the appropriate destinations"""
    successful = 0
    failed = 0
    
    # Ensure directories exist
    os.makedirs("static/images/products", exist_ok=True)
    os.makedirs("static/images/concerns", exist_ok=True)
    
    for source_path, dest_dir, new_filename in image_mappings:
        source = Path(source_path)
        # Handle absolute paths if provided
        if not source.exists() and not source.is_absolute():
            # Try with absolute path from the workspace root
            abs_source = Path("C:/Users/Lawi/OneDrive/Documents/neutrikenya") / source_path
            if abs_source.exists():
                source = abs_source
        
        dest = Path(dest_dir) / new_filename
        
        try:
            if source.exists():
                shutil.copy2(source, dest)
                print(f"✓ Copied {source} to {dest}")
                successful += 1
            else:
                print(f"✗ Source file not found: {source}")
                failed += 1
        except Exception as e:
            print(f"✗ Error copying {source}: {e}")
            failed += 1
    
    print(f"\nCopying complete: {successful} successful, {failed} failed")
    
    # Print remaining images that need to be replaced
    all_product_line_images = ["vitamin-c.jpg", "retinol.jpg", "hyaluronic-acid.jpg", 
                              "skin-whitening.jpg", "snail.jpg", "turmeric.jpg"]
    
    all_product_type_images = ["cleanser.jpg", "toner.jpg", "serum.jpg", "face-cream.jpg",
                              "facial-mask.jpg", "soap.jpg", "body-wash.jpg", "body-lotion.jpg"]
    
    all_skin_concern_images = ["acne-skin.jpg", "aging-skin.jpg", "blackhead-removal.jpg",
                              "brightening-skin.jpg", "dehydrated-skin.jpg", "dry-skin.jpg",
                              "oily-skin.jpg", "soothing-skin.jpg"]
    
    # Get filenames of destination images we've already mapped
    mapped_filenames = [mapping[2] for mapping in image_mappings]
    
    # Find missing product line images
    missing_product_lines = [img for img in all_product_line_images 
                             if img not in mapped_filenames]
    
    # Find missing product type images
    missing_product_types = [img for img in all_product_type_images 
                            if img not in mapped_filenames]
    
    # Find missing skin concerns
    missing_skin_concerns = [img for img in all_skin_concern_images 
                             if img not in mapped_filenames]
    
    print("\nRemaining images needed:")
    
    if missing_product_lines:
        print("\nProduct Line Images (static/images/products/):")
        for img in missing_product_lines:
            print(f"- {img}")
    
    if missing_product_types:
        print("\nProduct Type Images (static/images/products/):")
        for img in missing_product_types:
            print(f"- {img}")
    
    if missing_skin_concerns:
        print("\nSkin Concern Images (static/images/concerns/):")
        for img in missing_skin_concerns:
            print(f"- {img}")

if __name__ == "__main__":
    print("NeutriherbsKenya Image Copy Utility")
    print("===================================")
    print("This script will copy existing images to the skincare page locations\n")
    copy_images() 