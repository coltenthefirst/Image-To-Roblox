import os
from PIL import Image
import sys
import subprocess

def extract_frames(gif_path, output_folder, fps="10"):
    os.makedirs(output_folder, exist_ok=True)
    with Image.open(gif_path) as gif:
        total_frames = gif.n_frames
        frames = []
        
        if fps == "max":
            frame_interval = 1
        elif fps == 1:
            frame_interval = gif.info['duration'] / 1000
        else:
            frame_interval = gif.n_frames / fps
        
        for i in range(0, total_frames, int(frame_interval)):
            gif.seek(i)
            frame_path = os.path.join(output_folder, f"frame_{i}.png")
            gif.save(frame_path, format="PNG")
            frames.append(frame_path)
    
    return frames

if __name__ == "__main__":
    gif_path = sys.argv[1]
    output_folder = sys.argv[2]
    fps = sys.argv[3]
    
    frames = extract_frames(gif_path, output_folder, fps)
    if frames:
        print(f"Extracted {len(frames)} frames.")
        subprocess.run(["python3", "upload_frames.py", "/tmp/extracted_frames", "your_imgbb_api_key"])
    else:
        print("Failed to extract frames.")
        sys.exit(1)
