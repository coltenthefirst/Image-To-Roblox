import os
from PIL import Image
from moviepy.editor import VideoFileClip

factor = 30
rate = 400
input_video_path = '/tmp/input/video.mp4'
output_directory = '/tmp/output'

os.makedirs(output_directory, exist_ok=True)

clip = VideoFileClip(input_video_path)

frame_interval = 5 / clip.fps

frame_count = 0
current_time = 0

while current_time < clip.duration:
    frame = clip.get_frame(current_time)

    image = Image.fromarray(frame)
    image = image.resize((int(image.size[0] / factor), int(image.size[1] / factor)))
    pixels = image.load()
    
    output_filename = f"frame_{frame_count}"
    with open(os.path.join(output_directory, f"{output_filename}.lua"), 'w') as f:
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

        f.write("require(script.Parent.Parent):Draw(" + str(rate) + 
                ", Vector3.new(0,0,0), {" + str(image.size[0]) + "," + str(image.size[1]) + 
                "}, '" + ''.join(bits) + "')")
    
    print(f"Processed and saved: {output_filename}.lua")

    current_time += frame_interval
    frame_count += 1

print("Done!")
