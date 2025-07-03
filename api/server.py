# this code was made with AI. Rewrite soon.

import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, UnidentifiedImageError
import subprocess
import time
from urllib.parse import urlparse
import logging
import socket
from urllib.parse import urlparse
import ipaddress

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.ERROR)

INPUT_FOLDER = "/tmp/input"
OUTPUT_FOLDER = "/tmp/output"
SCRIPT_DIR = "."
IMAGE_NAME = "image.png"
GIF_NAME = "downloaded.gif"
MAX_RETRIES = 5

RESIZE_MAPPINGS = {
    "test": (15, 15),
    "elow": (15, 15),
    "ehigh": (240, 240),
    "low": (30, 30),
    "high": (120, 120),
    "mid": (60, 60),
    "testTwo": (350, 350),
    "testThree": (500, 500)
}

SCRIPT_MAPPING = {
    'high': 'high.py',
    'low': 'low.py',
    'mid': 'mid.py',
    'ehigh': 'extra-high.py',
    'elow': 'extra-low.py',
    'test': 'test.py',
    'testOne': 'testO.py',
    'testThree': 'testT.py'
}

CHECK_ALLOWED_DOMAINS = False # I set this to false for testing domains. You can set this to false for your project if you want.

ALLOWED_DOMAINS = [ # This is the list of the allowed direct link domains thing. pluh.
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
    "i.endpot.com",
    "dc.missuo.ru",
    "s3.gifyu.com",
    "i2.paste.pics",
    "s6.imgcdn.dev",
    "docs.google.com"
]

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_allowed_domain(url):
    if not CHECK_ALLOWED_DOMAINS:
        return True
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

def is_safe_ip(url):
    try:
        hostname = urlparse(url).hostname
        ip_address = socket.gethostbyname(hostname)
        if ip_address.startswith("10.") or ip_address.startswith("172.") or ip_address.startswith("192.168."):
            return False
        return True
    except Exception:
        return False

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
    if not is_safe_ip(gif_url):
        return None, "URL resolves to an unsafe IP address"
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
    uploaded_urls = [upload_image_to_imgbb(api_key, image_file) for image_file in frames] # test
    return [url for url in uploaded_urls if url], ""

def execute_gif_sender(uploaded_urls):
    result = subprocess.run(['python3', 'gif-sender.py'] + uploaded_urls, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout
    return None

@app.route('/gui_send_image', methods=['POST'])
def process_image():
    try:
        data = request.json
        if 'image_url' not in data or 'button_name' not in data:
            return jsonify({'status': 'error', 'message': 'Missing image_url or button_name'}), 400

        image_url = data['image_url']
        button_name = data['button_name']

        if button_name not in RESIZE_MAPPINGS:
            return jsonify({'status': 'error', 'message': f'Invalid button_name: {button_name}'}), 400

        max_size = RESIZE_MAPPINGS[button_name]

        allowed_domains = ["example.com", "anotherdomain.com"]
        parsed_url = urlparse(image_url)
        if parsed_url.netloc not in allowed_domains or not is_public_ip(parsed_url.netloc):
            return jsonify({'status': 'error', 'message': 'Domain not allowed or IP is not public'}), 400

        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            return jsonify({'status': 'error', 'message': 'Failed to download the image'}), 400

        image_path = os.path.join(INPUT_FOLDER, "downloaded_image.png")
        with open(image_path, 'wb') as f:
            f.write(image_response.content)

        try:
            image = Image.open(image_path)
        except UnidentifiedImageError:
            return jsonify({'status': 'error', 'message': 'The file is not a valid image'}), 400

        if image.mode in ("P", "RGBA", "L"):
            image = image.convert("RGB")
        elif image.mode not in ("RGB", "RGBA", "L"):
            image = image.convert("RGB")

        image.thumbnail(max_size, Image.Resampling.BICUBIC)

        lines_to_send = []
        pixels = image.load()
        width, height = image.size

        for y in range(height):
            row = ""
            for x in range(width):
                try:
                    rgb = pixels[x, y]
                    if isinstance(rgb, int):
                        rgb = (rgb, rgb, rgb)
                    elif isinstance(rgb, tuple) and len(rgb) != 3:
                        rgb = tuple(rgb[:3]) if len(rgb) >= 3 else (0, 0, 0)
                    elif not isinstance(rgb, tuple):
                        rgb = (0, 0, 0)

                    clamped_rgb = tuple(min(255, max(0, value)) for value in rgb)
                    row += f"<stroke color=\"rgb{clamped_rgb}\"><font color=\"rgb{clamped_rgb}\">■</font></stroke>"
                except Exception:
                    row += "<stroke color=\"rgb(0,0,0)\"><font color=\"rgb(0,0,0)\">■</font></stroke>"
            lines_to_send.append(row)

        return jsonify({
            'status': 'success',
            'message': 'Image processed and saved to /tmp/input',
            'image_path': image_path,
            'output_file': 'Result.lua',
            'lines': lines_to_send
        })

    except Exception as e:
        logging.error("Error processing image: %s", str(e))
        return jsonify({'status': 'error', 'message': 'An internal error has occurred.'}), 500

def is_public_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_global
    except Exception:
        return False

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
