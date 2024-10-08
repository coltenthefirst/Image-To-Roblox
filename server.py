from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Constants
INPUT_FOLDER = "input"  # Use relative paths for folders
OUTPUT_FOLDER = "output"  # Use relative paths for folders
SCRIPT_DIR = "."  # Assuming the scripts are in the same directory as the app
IMAGE_NAME = "1727325916.jumpyjackal_canvas_2044_7_1_bd__1_.png"
MAX_RETRIES = 3
SCRIPT_MAPPING = {
    'high': 'high.py',
    'low': 'low.py',
    'mid': 'mid.py',
    'ehigh': 'extra-high.py',
    'elow': 'extra-low.py',
}

def save_image_from_url(image_url, image_path):
    """Download an image from a URL and save it to the specified path."""
    for attempt in range(MAX_RETRIES):
        try:
            print(f"Attempting to download image from {image_url} (Attempt {attempt + 1})")
            response = requests.get(image_url)
            if response.status_code == 200:
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
    """Run the appropriate Python script based on button clicked."""
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
    """Read and return the content of the Lua script."""
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

    image_url = data['image_url']
    button_clicked = data['button_clicked']
    
    # Create the input folder if it doesn't exist
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    image_path = os.path.join(INPUT_FOLDER, IMAGE_NAME)

    # Step 1: Download the image
    if not save_image_from_url(image_url, image_path):
        return jsonify({"status": "error", "message": "Failed to download image"}), 400

    # Step 2: Run the corresponding script
    if not run_script(button_clicked):
        return jsonify({"status": "error", "message": f"Error executing script for button {button_clicked}"}), 500

    # Step 3: Fetch the generated Lua script
    output_file = os.path.join(OUTPUT_FOLDER, IMAGE_NAME.replace('.png', '.lua'))
    
    # Create the output folder if it doesn't exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    lua_script = get_lua_script(output_file)
    if lua_script:
        return jsonify({"status": "success", "lua_script": lua_script})
    else:
        return jsonify({"status": "error", "message": "Error reading Lua script"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use the PORT environment variable
    app.run(debug=True, host='0.0.0.0', port=port)
