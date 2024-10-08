import os
from PIL import Image

factor = 30  # Rate of change to resolution 1: Original resolution. ie: 640x640 - 6.4 - 100x100
rate = 400    # Rate that parts are created at

for filename in os.listdir("input"):
    image_path = os.path.join("input", filename)
    if os.path.isfile(image_path):
        image = Image.open(image_path)

        # Resize image
        image = image.resize((int(image.size[0] / factor), int(image.size[1] / factor)))
        pixels = image.load()

        # Prepare output filename without extension
        output_filename = os.path.splitext(filename)[0]

        # Write Lua file
        with open(f"{os.path.join('output', output_filename)}.lua", 'w') as f:

            bits = []

            # Iterate through pixels correctly
            for y in range(image.size[1]):  # Height
                for x in range(image.size[0]):  # Width
                    p = pixels[x, y]
                    p = ("{:03d}".format(p[0]), "{:03d}".format(p[1]), "{:03d}".format(p[2]))

                    bits.append(''.join(map(str, p)))

            # Write the Lua script content
            f.write("require(script.Parent.Parent):Draw(" + str(rate) + 
                    ", Vector3.new(0,0,0), {" + str(image.size[0]) + "," + str(image.size[1]) + 
                    "}, '" + ''.join(bits) + "')")

        print(f"Processed: {filename}")

print("Done!")