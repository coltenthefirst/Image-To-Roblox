import os
import argparse
from moviepy.editor import VideoFileClip
from PIL import Image

parser = argparse.ArgumentParser(description="Extract frames from video and save as PNG")
parser.add_argument("--input", required=True, help="Path to input video file")
parser.add_argument("--output", required=True, help="Directory to save extracted frames")
args = parser.parse_args()

input_video_path = args.input
output_directory = args.output

os.makedirs(output_directory, exist_ok=True)

factor = 30
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
    current_time += frame_interval
    frame_count += 1

print("Frame extraction done!")
