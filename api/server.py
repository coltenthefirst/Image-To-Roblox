import os
import requests
from flask import Flask, request, jsonify
from PIL import Image
import subprocess
import time
from urllib.parse import urlparse

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

ALLOWED_DOMAINS = [
    "i.postimg.cc",
    "i.ibb.co",
    "i.imghippo.com",
    "www2.lunapic.com",
    "cdn-images.imagevenue.com",
    "pictr.com",
    "images4.imagebam.com",
    "imgbly.com",
    "picsur.org",
    "img86.pixhost.to",
    "files.catbox.moe",
    "litter.catbox.moe",
    "s3.amazonaws.com",
    "images2.imgbox.com",
    "i.endpot.com"
]

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_allowed_domain(url):
    domain = urlparse(url).netloc
    return any(domain.endswith(allowed) for allowed in ALLOWED_DOMAINS)

def save_image_from_url(image_url, image_path):
    if not is_valid_url(image_url):
        return False, "Invalid URL format"
    if not is_allowed_domain(image_url):
        return False, f"Invalid domain. Please use one of the following domains: {', '.join(ALLOWED_DOMAINS)}"
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(image_url, timeout=10, verify=True)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                return True, ""
        except requests.exceptions.RequestException:
            continue
    return False, "Failed to download image"

def run_script(button_clicked):
    selected_script = SCRIPT_MAPPING.get(button_clicked)
    if selected_script:
        script_path = os.path.join(SCRIPT_DIR, selected_script)
        subprocess.run(['python3', script_path], check=True)
        return True
    return False

def get_lua_script(output_file):
    try:
        with open(output_file, 'r') as f:
            return f.read()
    except Exception:
        return None

def download_gif(gif_url, temp_folder):
    if not is_valid_url(gif_url):
        return None, "Invalid URL format"
    if not is_allowed_domain(gif_url):
        return None, f"Invalid domain. Please use one of the following domains: {', '.join(ALLOWED_DOMAINS)}"
    os.makedirs(temp_folder, exist_ok=True)
    gif_filename = os.path.join(temp_folder, GIF_NAME)
    response = requests.get(gif_url, timeout=10, verify=True)
    if response.status_code == 200:
        with open(gif_filename, "wb") as f:
            f.write(response.content)
        return gif_filename, ""
    return None, "Failed to download GIF"

def extract_frames(gif_path, output_folder, fps="max"):
    os.makedirs(output_folder, exist_ok=True)
    with Image.open(gif_path) as gif:
        total_frames = gif.n_frames
        frame_interval = 1 if fps == "max" else total_frames // int(fps) if fps != "max" else 1
        frames = []
        for i in range(0, total_frames, frame_interval):
            gif.seek(i)
            frame_path = os.path.join(output_folder, f"frame_{i}.png")
            gif.save(frame_path, format="PNG")
            frames.append(frame_path)
    return frames

def upload_image_to_imgbb(api_key, image_path):
    url = "https://api.imgbb.com/1/upload"
    payload = {"key": api_key}
    with open(image_path, "rb") as image_file:
        files = {"image": image_file}
        response = requests.post(url, data=payload, files=files)
    if response.status_code == 200:
        return response.json().get('data', {}).get('url')
    return None

def process_and_upload_gif(api_key, gif_path, output_folder, fps="max"):
    frames = extract_frames(gif_path, output_folder, fps)
    uploaded_urls = [upload_image_to_imgbb(api_key, image_file) for image_file in frames]
    return [url for url in uploaded_urls if url], ""

def execute_gif_sender(uploaded_urls):
    result = subprocess.run(['python3', 'gif-sender.py'] + uploaded_urls, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout
    return None

@app.route('/send_image', methods=['POST'])
def send_image():
    data = request.get_json()
    if not data or not data.get('image_url') or not data.get('button_clicked'):
        return jsonify({"status": "error", "message": "Missing image_url or button_clicked"}), 400
    image_url = data['image_url']
    button_clicked = data['button_clicked']
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    image_path = os.path.join(INPUT_FOLDER, IMAGE_NAME)
    success, message = save_image_from_url(image_url, image_path)
    if not success:
        return jsonify({"status": "error", "message": message}), 400
    if not run_script(button_clicked):
        return jsonify({"status": "error", "message": "Error executing script for button " + button_clicked}), 500
    output_file = os.path.join(OUTPUT_FOLDER, IMAGE_NAME.replace('.png', '.lua'))
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    lua_script = get_lua_script(output_file)
    if lua_script:
        return jsonify({"status": "success", "lua_script": lua_script})
    return jsonify({"status": "error", "message": "Error reading Lua script"}), 500

@app.route('/send_gif', methods=['POST'])
def send_gif():
    data = request.get_json()
    if not data or not data.get('gif_url') or not data.get('api_key'):
        return jsonify({"status": "error", "message": "Missing gif_url or api_key"}), 400
    gif_url = data['gif_url']
    api_key = data['api_key']
    gif_path, message = download_gif(gif_url, "/tmp/processed_gif")
    if not gif_path:
        return jsonify({"status": "error", "message": message}), 400
    uploaded_urls, message = process_and_upload_gif(api_key, gif_path, OUTPUT_FOLDER)
    if not uploaded_urls:
        return jsonify({"status": "error", "message": message}), 400
    gif_sender_output = execute_gif_sender(uploaded_urls)
    if gif_sender_output:
        return jsonify({"status": "success", "uploaded_urls": uploaded_urls, "gif_sender_output": gif_sender_output})
    return jsonify({"status": "error", "message": "Error executing gif-sender.py"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "1"]
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
