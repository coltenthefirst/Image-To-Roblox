import os
import time
from PIL import Image

factor = 30
rate = 400
output_directory = '/tmp/output/video'

images = [img for img in os.listdir(output_directory) if img.endswith('.png')]

for image_filename in images:
    image_path = os.path.join(output_directory, image_filename)
    output_filename = os.path.splitext(image_filename)[0]
    lua_output_path = os.path.join(output_directory, f"{output_filename}.lua")
    
    image = Image.open(image_path)
    pixels = image.load()
    
    with open(lua_output_path, 'w') as f:
        bits = []
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                p = pixels[x, y]
                if isinstance(p, int):
                    p = (p, p, p)
                else:
                    p = (p[0], p[1], p[2])
                p = ("{:03d}".format(p[0]), "{:03d}".format(p[1]), "{:03d}".format(p[2]))
                bits.append(''.join(map(str, p)))
        f.write("require(script.Parent.Parent):Draw(" + str(rate) + ", Vector3.new(0,0,0), {" + str(image.size[0]) + "," + str(image.size[1]) + "}, '" + ''.join(bits) + "')")
    
    time.sleep(2.5)
