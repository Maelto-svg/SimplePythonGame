import sys
from PIL import Image

def resize_image(input_image, output_image, width, height):
    # Open the image file
    with Image.open(input_image) as img:
        # Resize the image
        resized_img = img.resize((width, height))
        # Save the resized image
        resized_img.save(output_image)
        print(f"Image resized and saved as {output_image}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python resize_image.py <input_image> [<output_image>] [<width>] [<height>]")
    else:
        input_image = sys.argv[1]
        
        output_image = f"resized_{input_image}"
        
        if len(sys.argv) > 2:
            output_image = sys.argv[2]
        
        width = int(sys.argv[3]) if len(sys.argv) > 3 else 64
        height = int(sys.argv[4]) if len(sys.argv) > 4 else 64
        
        resize_image(input_image, output_image, width, height)
