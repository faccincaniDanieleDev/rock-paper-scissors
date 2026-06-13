"""imageUtils.py — Utility functions for generating game button images."""
from PIL import Image, ImageDraw

def generate_button_image(assets_path: str, ring_color: str, badge_text: str, bg_color: str = "#141721") ->Image.Image:
    """Generates a circular button image with a neon ring and badge.

    Removes the grey background from the asset, applies a circular
    crop mask and composes the final button layout with a neon ring.

    Args:
        asset_path: Path to the source image asset.
        ring_color: Hex color string for the neon ring and badge.
        badge_text: Text to display inside the bottom badge.
        bg_color:   Background color of the canvas.

    Returns:
        A PIL Image object ready to be used as a button icon.
    """
    
    canvas_size = (180,200)
    base = Image.new("RGBA", canvas_size,bg_color)
    draw = ImageDraw.Draw(base)
    
    # Outer neon ring
    draw.ellipse([10,10,170,170], outline=ring_color, width=5)
    
    # Remove grey background from asset
    obj_img = Image.open(assets_path).convert("RGBA")
    cleaned_pixels = [
        (0,0,0,0) if (115 <= p[0] <= 142 and 115 <= p[1] <= 142 and 115 <= p[2] <= 142) else p
        for p in obj_img.getdata()
    ]
    
    obj_img.putdata(cleaned_pixels)
    obj_img = obj_img.resize((110,110), Image.Resampling.LANCZOS)
    
    # Circular crop mask to remove white edge artifacts
    crop_mask = Image.new("L", (110,110), 0)
    ImageDraw.Draw(crop_mask).ellipse((10,10,100,100), fill=255)
    
    cleaned_obj = Image.new("RGBA", (110,110), (0,0,0,0))
    cleaned_obj.paste(obj_img, (0,0), mask=crop_mask)
    
    # Paste asset onto base
    base.paste(cleaned_obj, (35,35), mask=cleaned_obj)
    
    # Bottom numeric badge
    ImageDraw.Draw(base).ellipse([75,155,105,185], fill=ring_color)
    
    try:
        ImageDraw.Draw(base).text((85,162), badge_text, fill="#ffffff")
        
    except Exception:
        pass
    
    return base