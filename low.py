import os
from PIL import Image

factor = 12.8
rate = 200
input_directory = "/tmp/input"
output_directory = "/tmp/output"
lua_file_path = os.path.join(output_directory, "output.lua")

os.makedirs(output_directory, exist_ok=True)

all_bits = []

with open(lua_file_path, 'w') as f:
    f.write("")

for filename in os.listdir(input_directory):
    image_path = os.path.join(input_directory, filename)
    if os.path.isfile(image_path):
        try:
            image = Image.open(image_path)
            image = image.resize((int(image.size[0] / factor), int(image.size[1] / factor)))
            pixels = image.load()

            for y in range(image.size[1]):
                for x in range(image.size[0]):
                    p = pixels[x, y]
                    p = ("{:03d}".format(p[0]), "{:03d}".format(p[1]), "{:03d}".format(p[2]))
                    all_bits.append(''.join(map(str, p)))

            print(f"Processed: {filename}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

with open(lua_file_path, 'w') as f:
    f.write("require(script.Parent.Parent):Draw(" + str(rate) + 
            ", Vector3.new(0,0,0), {" + str(image.size[0]) + "," + str(image.size[1]) + 
            "}, '" + ''.join(all_bits) + "')")

print(f"Wrote to Lua file: {lua_file_path}")
print("Done!")
