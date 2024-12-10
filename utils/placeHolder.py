"""
Creates The PlaceHolder sprite.
"""

from PIL import Image, ImageDraw

# Define image size and number of sections
image_size = 512
num_sections = 8
section_size = image_size // num_sections

# Create a new image with RGB mode
image = Image.new("RGB", (image_size, image_size), "white")
draw = ImageDraw.Draw(image)

# Define the colors
black = (0, 0, 0)
purple = (128, 0, 128)

# Loop to fill sections with alternating colors
for i in range(num_sections):
    color = black if i % 2 == 0 else purple
    draw.rectangle(
        [i * section_size, 0, (i + 1) * section_size, image_size], fill=color
    )

# Save the image
image.save("ressources/sprites/placeHolder.png")
