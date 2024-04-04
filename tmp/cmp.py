from PIL import Image
import os

# Function to compress an image
def compress_image(input_path, output_path, quality=75):
    img = Image.open(input_path)
    img.save(output_path, optimize=True, quality=quality)

# Input and output directories
input_dir = "/home/u201853/tmp/cmp"
output_dir = "/home/u201853/tmp"

# Iterate over image files in the input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        compress_image(input_path, output_path, quality=50)
        print(f"Compressed image: {input_path} -> {output_path}")

print("Compression complete.")

