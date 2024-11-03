import os
from moviepy.editor import VideoFileClip
from PIL import Image

# Input and output paths
input_video_path = '/Users/coltenparker/Downloads/2d gay Yiff by Zonkpunch Furry Porn Sex E621 FYE Egyptian god Sobek fucks Anubis Anal giant cock Scalie Crocodile Wolf - XXXiPORN Video.mp4'
output_folder = '/Users/coltenparker/Downloads/testingbinner'
factor = 6.4

# Create output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the video
clip = VideoFileClip(input_video_path)

# Calculate frame interval for 2 FPS
frame_interval = 5 / clip.fps  # Interval to capture each frame

# Frame extraction loop
frame_count = 0
current_time = 0

while current_time < clip.duration:
    # Get the frame at the current time
    frame = clip.get_frame(current_time)

    # Convert frame to PIL Image and resize
    image = Image.fromarray(frame)
    image = image.resize((int(image.size[0] / factor), int(image.size[1] / factor)))
    
    # Save as PNG with unique frame_count
    output_filename = f"frame_{frame_count}.png"
    image.save(os.path.join(output_folder, output_filename))

    print(f"Processed and saved: {output_filename}")

    # Increment time and frame count
    current_time += frame_interval
    frame_count += 1

print("Done!")