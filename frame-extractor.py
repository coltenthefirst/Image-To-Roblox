import os
from moviepy.editor import VideoFileClip
from PIL import Image

factor = 30
input_video_path = '/tmp/input/video.mp4'
output_directory = '/tmp/output/video'

os.makedirs(output_directory, exist_ok=True)

clip = VideoFileClip(input_video_path)
frame_interval = 5 / clip.fps

frame_count = 0
current_time = 0

while current_time < clip.duration:
    frame = clip.get_frame(current_time)

    image = Image.fromarray(frame)
    image = image.resize((int(image.size[0] / factor), int(image.size[1] / factor)))
    
    output_filename = f"frame_{frame_count}.png"
    image.save(os.path.join(output_directory, output_filename))

    print(f"Extracted and saved: {output_filename}")

    current_time += frame_interval
    frame_count += 1

print("Frame extraction done!")

os.system("python3 videotest.py")
