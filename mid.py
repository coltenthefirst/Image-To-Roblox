import os
import time
from PIL import Image

factor = 6.4
rate = 100
input_directory = "/tmp/input"
output_directory = "/tmp/output"

os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir(input_directory):
    image_path = os.path.join(input_directory, filename)
    if os.path.isfile(image_path):
        try:
            image = Image.open(image_path)
            image = image.resize((int(image.size[0] / factor), int(image.size[1] / factor)))
            pixels = image.load()
            output_filename = os.path.splitext(filename)[0]
            lua_file_path = os.path.join(output_directory, f"{output_filename}.lua")

            with open(lua_file_path, 'w') as f:
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

            time.sleep(10)
            if os.path.exists(lua_file_path):
                os.remove(lua_file_path)
                print(f"Deleted: {lua_file_path}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Done!")
