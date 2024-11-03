import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import Flask, request, jsonify

app = Flask(__name__)

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

INPUT_FOLDER = "/tmp/input"
OUTPUT_FOLDER = "/tmp/output"
IMAGE_NAME = "image.png"
VIDEO_NAME = "video.mp4"
MAX_RETRIES = 3

def save_file_from_url(file_url, file_path):
    for attempt in range(MAX_RETRIES):
        try:
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

def extract_frames_with_cloudinary(video_url):
    try:
        upload_response = cloudinary.uploader.upload_large(
            video_url,
            resource_type="video"
        )

        public_id = upload_response['public_id']
        duration = upload_response['duration']

        frame_urls = []
        interval = 2  # seconds

        for time in range(0, int(duration), interval):
            frame_url = cloudinary.utils.cloudinary_url(
                public_id + f".jpg",
                resource_type="video",
                start_offset=time,
                format="jpg"
            )[0]
            frame_urls.append(frame_url)

        return frame_urls

    except Exception as e:
        print(f"Error extracting frames with Cloudinary: {e}")
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

    if button_clicked == "vtest":
        frame_urls = extract_frames_with_cloudinary(file_url)
        if not frame_urls:
            return jsonify({"status": "error", "message": "Failed to extract frames with Cloudinary"}), 500
        return jsonify({"status": "success", "frame_urls": frame_urls})

    else:
        os.makedirs(INPUT_FOLDER, exist_ok=True)
        image_path = os.path.join(INPUT_FOLDER, IMAGE_NAME)
        
        if not save_file_from_url(file_url, image_path):
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

def run_script(button_clicked):
    SCRIPT_MAPPING = {
        'high': 'high.py',
        'low': 'low.py',
        'mid': 'mid.py',
        'ehigh': 'extra-high.py',
        'elow': 'extra-low.py'
    }
    selected_script = SCRIPT_MAPPING.get(button_clicked)
    if selected_script:
        script_path = os.path.join(".", selected_script)
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
