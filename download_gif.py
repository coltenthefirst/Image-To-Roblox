import os
import requests
import sys
import subprocess

def download_gif(gif_url, temp_folder):
    os.makedirs(temp_folder, exist_ok=True)
    gif_filename = os.path.join(temp_folder, "downloaded.gif")
    
    response = requests.get(gif_url)
    if response.status_code == 200:
        with open(gif_filename, "wb") as f:
            f.write(response.content)
        return gif_filename
    else:
        return None

if __name__ == "__main__":
    gif_url = sys.argv[1]
    temp_folder = sys.argv[2]
    
    gif_filename = download_gif(gif_url, temp_folder)
    if gif_filename:
        print(f"Downloaded GIF to {gif_filename}")
        subprocess.run(["python3", "extract_frames.py", gif_filename, "/tmp/extracted_frames", "max"])
    else:
        print("Failed to download GIF")
        sys.exit(1)
