"""
Create Telegraf Icon
Generates a modern icon for the application
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a modern Telegraf icon"""
    # Create multiple sizes for Windows ICO
    sizes = [256, 128, 64, 48, 32, 16]
    images = []

    for size in sizes:
        # Create image with transparent background
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw gradient circle background
        for i in range(size):
            for j in range(size):
                # Distance from center
                dx = i - size/2
                dy = j - size/2
                distance = (dx*dx + dy*dy) ** 0.5

                if distance < size/2 - 2:
                    # Gradient from blue to purple
                    ratio = distance / (size/2)
                    r = int(100 + ratio * 50)
                    g = int(150 - ratio * 50)
                    b = int(255 - ratio * 100)
                    a = 255
                    img.putpixel((i, j), (r, g, b, a))

        # Draw white border
        draw.ellipse([2, 2, size-3, size-3], outline=(255, 255, 255, 200), width=max(2, size//32))

        # Draw rocket emoji or T letter
        if size >= 64:
            # Try to draw text
            try:
                font_size = size // 2
                font = ImageFont.truetype("seguiemj.ttf", font_size)
                text = "🚀"

                # Get text bounding box
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                # Center text
                x = (size - text_width) // 2 - bbox[0]
                y = (size - text_height) // 2 - bbox[1]

                draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
            except:
                # Fallback: draw T letter
                font_size = size // 2
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()

                text = "T"
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                x = (size - text_width) // 2 - bbox[0]
                y = (size - text_height) // 2 - bbox[1]

                draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
        else:
            # For small sizes, just draw a simple shape
            margin = size // 4
            draw.ellipse([margin, margin, size-margin, size-margin],
                        fill=(255, 255, 255, 255))

        images.append(img)

    # Save as ICO
    output_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'telegraf.ico')
    images[0].save(output_path, format='ICO', sizes=[(img.width, img.height) for img in images])

    print(f"[OK] Icon created: {output_path}")

    # Also save as PNG for preview
    png_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'telegraf.png')
    images[0].save(png_path, format='PNG')
    print(f"[OK] PNG preview created: {png_path}")

if __name__ == '__main__':
    create_icon()
