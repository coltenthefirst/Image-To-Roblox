import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

INPUT_FOLDER = "/tmp/input"
OUTPUT_FOLDER = "/tmp/output"
SCRIPT_DIR = "."
IMAGE_NAME = "image.png"
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
            print(f"Attempting to download image (Attempt {attempt + 1})")
            response = requests.get(image_url)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                print(f"Image saved to {image_path}")
                return True
            else:
                print(f"Failed to download image: {response.status_code} {response.text}")
                if response.status_code == 503 and attempt < MAX_RETRIES - 1:
                    print("Retrying...")
                    continue
                return False
        except Exception as e:
            print(f"Error downloading image: {e}")
            return False

def run_script(button_clicked):
    selected_script = SCRIPT_MAPPING.get(button_clicked)
    if selected_script:
        script_path = os.path.join(SCRIPT_DIR, selected_script)
        try:
            print(f"Executing script: {selected_script}")
            os.system(f"python3 {script_path}")
            return True
        except Exception as e:
            print(f"Error running script: {e}")
            return False
    return False

def get_lua_script(output_file):
    try:
        with open(output_file, 'r') as f:
            lua_script = f.read()
        print(f"Successfully read Lua script from {output_file}")
        return lua_script
    except Exception as e:
        print(f"Error reading output Lua file: {e}")
        return None

@app.route('/send_image', methods=['POST'])
def send_image():
    print("Received POST request to /send_image")
    data = request.get_json()
    print(f"Raw data received")

    if not data or not data.get('image_url') or not data.get('button_clicked'):
        print("Error: Missing image_url or button_clicked")
        return jsonify({"status": "error", "message": "Missing image_url or button_clicked"}), 400

    image_url = data['image_url']
    button_clicked = data['button_clicked']
    
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    image_path = os.path.join(INPUT_FOLDER, IMAGE_NAME)

    if not save_image_from_url(image_url, image_path):
        return jsonify({"status": "error", "message": "Failed to download image"}), 400

    if not run_script(button_clicked):
        return jsonify({"status": "error", "message": f"Error executing script for button {button_clicked}"}), 500

    output_file = os.path.join(OUTPUT_FOLDER, IMAGE_NAME.replace('.png', '.lua'))
    
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    lua_script = get_lua_script(output_file)
    if lua_script:
        return jsonify({"status": "success", "lua_script": lua_script})
    else:
        return jsonify({"status": "error", "message": "Error reading Lua script"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "1"]
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
