import os
from moviepy.editor import VideoFileClip
from PIL import Image

input_video_path = '/Users/coltenparker/Downloads/2d gay Yiff by Zonkpunch Furry Porn Sex E621 FYE Egyptian god Sobek fucks Anubis Anal giant cock Scalie Crocodile Wolf - XXXiPORN Video.mp4'
output_folder = '/Users/coltenparker/Downloads/testingbinner'
factor = 6.4

os.makedirs(output_folder, exist_ok=True)

clip = VideoFileClip(input_video_path)

frame_interval = 5 / clip.fps

frame_count = 0
current_time = 0

while current_time < clip.duration:
    frame = clip.get_frame(current_time)

    image = Image.fromarray(frame)
    image = image.resize((int(image.size[0] / factor), int(image.size[1] / factor)))
    
    output_filename = f"frame_{frame_count}.png"
    image.save(os.path.join(output_folder, output_filename))

    print(f"Processed and saved: {output_filename}")

    current_time += frame_interval
    frame_count += 1

print("Done!")
