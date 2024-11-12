import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

factor = 30
rate = 400
input_directory = "/tmp/input"  
output_directory = "/tmp/output"

os.makedirs(output_directory, exist_ok=True)

def process_image(filename):
    image_path = os.path.join(input_directory, filename)
    if os.path.isfile(image_path):
        try:
            image = Image.open(image_path)
            image = image.resize((int(image.size[0] / factor), int(image.size[1] / factor)), Image.NEAREST)
            pixels = list(image.getdata())
            output_filename = os.path.splitext(filename)[0]

            with open(os.path.join(output_directory, f"{output_filename}.lua"), 'w') as f:
                bits = [''.join("{:03d}{:03d}{:03d}".format(p[0], p[1], p[2]) if isinstance(p, tuple) else "{:03d}{:03d}{:03d}".format(p, p, p)) for p in pixels]
                f.write(f"require(script.Parent.Parent):Draw({rate}, Vector3.new(0,0,0), {{{image.size[0]},{image.size[1]}}}, '{''.join(bits)}')")

            print(f"Processed: {filename}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

with ThreadPoolExecutor() as executor:
    executor.map(process_image, os.listdir(input_directory))

print("Done!")
