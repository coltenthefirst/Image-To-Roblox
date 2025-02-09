import os
import requests
import time
import sys
import subprocess

def upload_image_to_imgbb(api_key, image_path):
    url = "https://api.imgbb.com/1/upload"
    payload = {"key": api_key}
    
    with open(image_path, "rb") as image_file:
        files = {"image": image_file}
        response = requests.post(url, data=payload, files=files)
    
    if response.status_code == 200:
        result = response.json()
        return result['data']['url']
    else:
        return None

def upload_frames(frame_folder, api_key):
    uploaded_urls = []
    for filename in os.listdir(frame_folder):
        image_path = os.path.join(frame_folder, filename)
        if os.path.isfile(image_path):
            url = upload_image_to_imgbb(api_key, image_path)
            if url:
                uploaded_urls.append(url)
            time.sleep(0.1)
    return uploaded_urls

if __name__ == "__main__":
    frame_folder = sys.argv[1]
    api_key = sys.argv[2]
    
    uploaded_urls = upload_frames(frame_folder, api_key)
    if uploaded_urls:
        print(f"Uploaded {len(uploaded_urls)} frames.")
        subprocess.run(["python3", "execute_gif_sender.py"] + uploaded_urls)
    else:
        print("Failed to upload frames.")
        sys.exit(1)
