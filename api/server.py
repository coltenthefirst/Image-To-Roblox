import os
import requests
from flask import Flask, request, jsonify
from PIL import Image
import time
import subprocess

app = Flask(__name__)

INPUT_FOLDER = "/tmp/input"
OUTPUT_FOLDER = "/tmp/output"
SCRIPT_DIR = "."
IMAGE_NAME = "image.png"
GIF_NAME = "downloaded.gif"
MAX_RETRIES = 5

SCRIPT_MAPPING = {
    'high': 'high.py',
    'low': 'low.py',
    'mid': 'mid.py',
    'ehigh': 'extra-high.py',
    'elow': 'extra-low.py',
}

def save_image_from_url(image_url, image_path):
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                print("download image 1")
                return True
            else:
                if response.status_code == 503 and attempt < MAX_RETRIES - 1:
                    continue
                print("failed to download image error 503 thats sus")
                return False
        except Exception:
            print("error downloading image <error message> major l")
            return False

def run_script(button_clicked):
    selected_script = SCRIPT_MAPPING.get(button_clicked)
    if selected_script:
        script_path = os.path.join(SCRIPT_DIR, selected_script)
        try:
            os.system(f"python3 {script_path}")
            print("running script high.py vibes are high")
            return True
        except Exception:
            print("error running script for button high that's a no-go")
            return False
    return False

def get_lua_script(output_file):
    try:
        with open(output_file, 'r') as f:
            print("lua script read so lit")
            return f.read()
    except Exception:
        print("error reading lua script thats a no-go")
        return None

def download_gif(gif_url, temp_folder):
    os.makedirs(temp_folder, exist_ok=True)
    gif_filename = os.path.join(temp_folder, GIF_NAME)
    
    response = requests.get(gif_url)
    if response.status_code == 200:
        with open(gif_filename, "wb") as f:
            f.write(response.content)
        print("downloading gif its about to be skibidi")
        return gif_filename
    else:
        print("failed to download gif error 404 whole vibe")
        return None

def extract_frames(gif_path, output_folder, fps="max"):
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
            print(f"saved frame {i} flexing")
    
    return frames

def upload_image_to_imgbb(api_key, image_path):
    url = "https://api.imgbb.com/1/upload"
    payload = {"key": api_key}
    
    with open(image_path, "rb") as image_file:
        files = {"image": image_file}
        response = requests.post(url, data=payload, files=files)
    
    if response.status_code == 200:
        print("image uploaded big flex")
        result = response.json()
        return result['data']['url']
    else:
        print("failed to upload image error 500 that's a no-go")
        return None

def process_and_upload_gif(api_key, gif_url, output_folder, fps="max"):
    temp_folder = "/tmp/processed_gif"
    
    gif_path = download_gif(gif_url, temp_folder)
    if not gif_path:
        print("couldn't process gif major l")
        return []
    
    frames = extract_frames(gif_path, output_folder, fps)
    uploaded_urls = []
    
    for image_file in frames:
        url = upload_image_to_imgbb(api_key, image_file)
        if url:
            uploaded_urls.append(url)
        time.sleep(1 / fps if fps != "max" else 0.1)
    
    print("uploaded 30 frames that's a flex")
    return uploaded_urls

def execute_gif_sender(uploaded_urls):
    try:
        result = subprocess.run(
            ['python3', 'gif-sender.py'] + uploaded_urls,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("gif-sender ran success flexing")
            return result.stdout
        else:
            print("error with gif-sender major l")
            return None
    except Exception:
        print("failed to process and upload gif major sus")
        return None

@app.route('/send_image', methods=['POST'])
def send_image():
    data = request.get_json()
    if not data or not data.get('image_url') or not data.get('button_clicked'):
        print("missing image_url or button_clicked major sus")
        return jsonify({"status": "error", "message": "Missing image_url or button_clicked"}), 400

    image_url = data['image_url']
    button_clicked = data['button_clicked']
    
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    image_path = os.path.join(INPUT_FOLDER, IMAGE_NAME)

    if not save_image_from_url(image_url, image_path):
        print("failed to download image whole vibe")
        return jsonify({"status": "error", "message": "Failed to download image"}), 400

    if not run_script(button_clicked):
        print("error running script for button high that's a no-go")
        return jsonify({"status": "error", "message": f"Error executing script for button {button_clicked}"}), 500

    output_file = os.path.join(OUTPUT_FOLDER, IMAGE_NAME.replace('.png', '.lua'))
    
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    lua_script = get_lua_script(output_file)
    if lua_script:
        return jsonify({"status": "success", "lua_script": lua_script})
    else:
        print("error reading lua script thats sus")
        return jsonify({"status": "error", "message": "Error reading Lua script"}), 500

@app.route('/send_gif', methods=['POST'])
def send_gif():
    data = request.get_json()

    if not data or not data.get('gif_url') or not data.get('api_key'):
        print("missing gif_url or api_key whole vibe")
        return jsonify({"status": "error", "message": "Missing gif_url or api_key"}), 400

    gif_url = data['gif_url']
    api_key = data['api_key']

    uploaded_urls = process_and_upload_gif(api_key, gif_url, OUTPUT_FOLDER)

    if uploaded_urls:
        gif_sender_output = execute_gif_sender(uploaded_urls)
        
        if gif_sender_output:
            return jsonify({"status": "success", "uploaded_urls": uploaded_urls, "gif_sender_output": gif_sender_output})
        else:
            print("error executing gif-sender.py")
            return jsonify({"status": "error", "message": "Error executing gif-sender.py"}), 500
    else:
        print("failed to process and upload gif major sus")
        return jsonify({"status": "error", "message": "Failed to process and upload GIF frames"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "1"]
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
