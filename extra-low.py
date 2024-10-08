import os
from PIL import Image

factor = 30
rate = 400

input_directory = "input"

for filename in os.listdir(input_directory):
    image_path = os.path.join(input_directory, filename)
    
    if os.path.isfile(image_path):
        try:
            image = Image.open(image_path)
            image = image.resize((int(image.size[0] / factor), int(image.size[1] / factor)))
            pixels = image.load()
            output_filename = os.path.splitext(filename)[0]

            with open(f"/tmp/{output_filename}.lua", 'w') as f:
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

        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Done!")
