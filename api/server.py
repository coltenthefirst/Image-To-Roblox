import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

INPUT_FOLDER = "/tmp/input"
OUTPUT_FOLDER = "/tmp/output"
SCRIPT_DIR = "api"
IMAGE_NAME = "image.png"
VIDEO_NAME = "video.mp4"
MAX_RETRIES = 3

SCRIPT_MAPPING = {
    'high': 'high.py',
    'low': 'low.py',
    'mid': 'mid.py',
    'ehigh': 'extra-high.py',
    'elow': 'extra-low.py',
    'vtest': 'frame-extractor.py'
}

def save_file_from_url(file_url, file_path):
    for attempt in range(MAX_RETRIES):
        try:
            print(f"Attempting to download file from {file_url} (Attempt {attempt + 1})")
            response = requests.get(file_url)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"File saved to {file_path}")
                return True
            else:
                print(f"Failed to download file: {response.status_code} {response.text}")
                if response.status_code == 503 and attempt < MAX_RETRIES - 1:
                    continue
                return False
        except Exception as e:
            print(f"Error downloading file: {e}")
            return False

def run_script(button_clicked):
    selected_script = SCRIPT_MAPPING.get(button_clicked)
    if selected_script:
        script_path = os.path.join(SCRIPT_DIR, selected_script)
        try:
            if button_clicked == "vtest":
                input_video_path = os.path.join(INPUT_FOLDER, VIDEO_NAME)
                output_folder = os.path.join(OUTPUT_FOLDER, "video")
                os.makedirs(output_folder, exist_ok=True)
                command = f"python3 {script_path} --input {input_video_path} --output {output_folder}"
            else:
                command = f"python3 {script_path}"
            print(f"Executing command: {command}")
            os.system(command)
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
    print(f"Raw data received: {data}")

    if not data or not data.get('image_url') or not data.get('button_clicked'):
        print("Error: Missing image_url or button_clicked")
        return jsonify({"status": "error", "message": "Missing image_url or button_clicked"}), 400

    file_url = data['image_url']
    button_clicked = data['button_clicked']
    
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    
    if button_clicked == "vtest":
        file_path = os.path.join(INPUT_FOLDER, VIDEO_NAME)
    else:
        file_path = os.path.join(INPUT_FOLDER, IMAGE_NAME)

    if not save_file_from_url(file_url, file_path):
        return jsonify({"status": "error", "message": "Failed to download file"}), 400

    if not run_script(button_clicked):
        return jsonify({"status": "error", "message": f"Error executing script for button {button_clicked}"}), 500

    if button_clicked == "vtest":
        output_file = os.path.join(OUTPUT_FOLDER, "video", VIDEO_NAME.replace('.mp4', '.lua'))
    else:
        output_file = os.path.join(OUTPUT_FOLDER, IMAGE_NAME.replace('.png', '.lua'))
    
    lua_script = get_lua_script(output_file)
    if lua_script:
        return jsonify({"status": "success", "lua_script": lua_script})
    else:
        return jsonify({"status": "error", "message": "Error reading Lua script"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
