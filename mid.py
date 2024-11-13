import os
import time
from PIL import Image

factor = 6.4
rate = 100

os.makedirs("/tmp/output", exist_ok=True)

for filename in os.listdir("/tmp/input"):
    image_path = os.path.join("/tmp/input", filename)
    if os.path.isfile(image_path):
        image = Image.open(image_path)
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        image = image.resize((int(image.size[0] / factor), int(image.size[1] / factor)))
        pixels = image.load()
        output_filename = os.path.splitext(filename)[0]
        
        max_retries = 5
        retry_delay = 1
        success = False

        for attempt in range(max_retries):
            try:
                with open(f"{os.path.join('/tmp/output', output_filename)}.lua", 'w') as f:
                    bits = []
                    for y in range(image.size[1]):
                        for x in range(image.size[0]):
                            p = pixels[x, y]
                            p = ("{:03d}".format(p[0]), "{:03d}".format(p[1]), "{:03d}".format(p[2]))
                            bits.append(''.join(map(str, p)))

                    f.write("require(script.Parent.Parent):Draw(" + str(rate) + 
                            ", Vector3.new(0,0,0), {" + str(image.size[0]) + "," + str(image.size[1]) + 
                            "}, '" + ''.join(bits) + "')")
                print(f"Processed: {filename}")
                success = True
                break
            except FileNotFoundError as e:
                print(f"Error opening file for {filename}: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"Failed to process {filename} after {max_retries} attempts.")

if success:
    print("All files processed successfully!")
else:
    print("Some files could not be processed after multiple attempts.")
