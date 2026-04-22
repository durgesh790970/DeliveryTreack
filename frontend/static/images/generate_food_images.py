#!/usr/bin/env python
"""Generate food category images for the menu"""

from PIL import Image, ImageDraw
import os

def create_food_images():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = script_dir
    
    # Food categories with colors
    categories = {
        'pizza': {'color': (255, 107, 53), 'label': 'Pizza'},
        'burger': {'color': (247, 147, 30), 'label': 'Burger'},
        'biryani': {'color': (139, 69, 19), 'label': 'Biryani'},
        'chicken': {'color': (212, 165, 116), 'label': 'Chicken'},
        'dosa': {'color': (218, 165, 32), 'label': 'Dosa'},
        'noodles': {'color': (255, 215, 0), 'label': 'Noodles'},
        'dessert': {'color': (255, 105, 180), 'label': 'Dessert'},
        'beverage': {'color': (65, 105, 225), 'label': 'Beverage'},
        'paneer': {'color': (255, 228, 181), 'label': 'Paneer'},
        'sushi': {'color': (255, 69, 0), 'label': 'Sushi'},
    }
    
    for name, data in categories.items():
        # Create image with gradient background
        img = Image.new('RGB', (400, 300), data['color'])
        draw = ImageDraw.Draw(img)
        
        # Add gradient effect (darker towards bottom)
        base_color = data['color']
        for y in range(300):
            ratio = y / 300.0
            r = max(0, int(base_color[0] * (1 - ratio * 0.4)))
            g = max(0, int(base_color[1] * (1 - ratio * 0.4)))
            b = max(0, int(base_color[2] * (1 - ratio * 0.4)))
            draw.line([(0, y), (400, y)], fill=(r, g, b))
        
        # Save image
        filepath = os.path.join(image_dir, f'{name}.jpg')
        img.save(filepath, 'JPEG', quality=85)
        print(f'✓ Created: {filepath}')
    
    print(f'\n✅ All {len(categories)} food images created successfully!')

if __name__ == '__main__':
    create_food_images()
