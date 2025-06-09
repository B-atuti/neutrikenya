import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_placeholder_image(directory, filename, text, size=(800, 600), bg_color="#f8f8f0", text_color="#333333"):
    """Create a placeholder image with text."""
    # Ensure directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Create image
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to load font, use default if not available
    try:
        # For Windows
        font_path = "C:\\Windows\\Fonts\\Arial.ttf"  
        font = ImageFont.truetype(font_path, 40)
        small_font = ImageFont.truetype(font_path, 30)
    except IOError:
        # If font file not found, use default
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw border
    border_width = 5
    draw.rectangle(
        [(border_width, border_width), 
         (size[0] - border_width, size[1] - border_width)],
        outline="#333333", width=border_width
    )
    
    # Draw company name at top
    company_name = "NeutriherbsKenya"
    draw.text((size[0]/2, 50), company_name, font=font, fill="#000000", anchor="mt")
    
    # Wrap and draw main text in center
    wrapped_text = textwrap.fill(text, width=20)
    draw.text((size[0]/2, size[1]/2), wrapped_text, font=font, fill=text_color, anchor="mm")
    
    # Add note at bottom
    note = "Placeholder Image"
    draw.text((size[0]/2, size[1]-50), note, font=small_font, fill="#666666", anchor="mb")
    
    # Save image
    full_path = os.path.join(directory, filename)
    img.save(full_path)
    print(f"Created: {full_path}")
    return full_path

# Create product line images
product_lines = [
    "vitamin-c", "retinol", "hyaluronic-acid", 
    "skin-whitening", "snail", "turmeric"
]

for line in product_lines:
    create_placeholder_image(
        "static/images/products", 
        f"{line}.jpg", 
        f"{line.replace('-', ' ').title()} Product Line"
    )

# Create product type images
product_types = [
    "cleanser", "toner", "serum", "face-cream", 
    "facial-mask", "soap", "body-wash", "body-lotion"
]

for p_type in product_types:
    create_placeholder_image(
        "static/images/products", 
        f"{p_type}.jpg", 
        f"{p_type.replace('-', ' ').title()} Products"
    )

# Create skin concern images
skin_concerns = [
    "acne-skin", "aging-skin", "blackhead-removal", 
    "brightening-skin", "dehydrated-skin", "dry-skin", 
    "oily-skin", "soothing-skin"
]

for concern in skin_concerns:
    create_placeholder_image(
        "static/images/concerns", 
        f"{concern}.jpg", 
        f"For {concern.replace('-', ' ').title()}"
    )

print("All placeholder images created successfully!") 