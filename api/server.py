import os
import replicate
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

INPUT_FOLDER = "/tmp/input"
OUTPUT_FOLDER = "/tmp/output"
IMAGE_NAME = "image.png"
VIDEO_NAME = "video.mp4"
MAX_RETRIES = 3

REPLICATE_MODEL_ID = "fofr/video-to-frames:ad9374d1b385c86948506b3ad287af9fca23e796685221782d9baa2bc43f14a9"

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
                if response.status_code == 503 and attempt < MAX_RETRIES - 1:
                    continue
                return False
        except Exception as e:
            print(f"Error downloading file: {e}")
            return False

def extract_frames_with_replicate(video_url):
    try:
        output = replicate.run(
            REPLICATE_MODEL_ID,
            input={"video": video_url}
        )
        frame_urls = []
        for index, item in enumerate(output):
            frame_filename = f"output_{index}.png"
            frame_path = os.path.join(OUTPUT_FOLDER, frame_filename)
            frame_urls.append(item)

            response = requests.get(item)
            with open(frame_path, "wb") as file:
                file.write(response.content)
            print(f"Frame {index} saved as {frame_path}")
        return frame_urls
    except Exception as e:
        print(f"Error extracting frames with Replicate: {e}")
        return None

@app.route('/send_image', methods=['POST'])
def send_image():
    data = request.get_json()

    if not data or not data.get('image_url') or not data.get('button_clicked'):
        return jsonify({"status": "error", "message": "Missing image_url or button_clicked"}), 400

    file_url = data['image_url']
    button_clicked = data['button_clicked']
    
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    
    if button_clicked == "vtest":
        frame_urls = extract_frames_with_replicate(file_url)
        if not frame_urls:
            return jsonify({"status": "error", "message": "Failed to extract frames with Replicate"}), 500
        return jsonify({"status": "success", "frame_urls": frame_urls})

    else:
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
