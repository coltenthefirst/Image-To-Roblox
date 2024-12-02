import os
import asyncio
import aiohttp
from flask import Flask, request, jsonify
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import shutil
from multiprocessing import Pool

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

executor = ThreadPoolExecutor(max_workers=10)

async def fetch_image(session, url, path):
    for attempt in range(MAX_RETRIES):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, 'wb') as f:
                        f.write(await response.read())
                    return True
                elif response.status == 503 and attempt < MAX_RETRIES - 1:
                    continue
        except Exception:
            pass
    return False

async def download_gif(session, url, path):
    return await fetch_image(session, url, path)

def extract_and_save_frames(gif_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    with Image.open(gif_path) as gif:
        for frame_num in range(gif.n_frames):
            gif.seek(frame_num)
            frame_path = os.path.join(output_folder, f"frame_{frame_num}.png")
            gif.save(frame_path, format="PNG")
    return os.listdir(output_folder)

async def upload_frame_to_imgbb(session, api_key, frame_path):
    url = "https://api.imgbb.com/1/upload"
    payload = {"key": api_key}
    try:
        with open(frame_path, "rb") as image_file:
            data = aiohttp.FormData()
            data.add_field('key', api_key)
            data.add_field('image', image_file, filename=os.path.basename(frame_path))
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result['data']['url']
    except Exception:
        pass
    return None

async def process_and_upload_gif(api_key, gif_url, output_folder):
    temp_folder = "/tmp/processed_gif"
    os.makedirs(temp_folder, exist_ok=True)
    gif_path = os.path.join(temp_folder, GIF_NAME)

    async with aiohttp.ClientSession() as session:
        if not await download_gif(session, gif_url, gif_path):
            return []

        frames = extract_and_save_frames(gif_path, output_folder)
        upload_tasks = [
            upload_frame_to_imgbb(session, api_key, os.path.join(output_folder, frame))
            for frame in frames
        ]
        uploaded_urls = await asyncio.gather(*upload_tasks)
    shutil.rmtree(temp_folder, ignore_errors=True)
    return [url for url in uploaded_urls if url]

@app.route('/send_gif', methods=['POST'])
async def send_gif():
    data = request.get_json()
    if not data or not data.get('gif_url') or not data.get('api_key'):
        return jsonify({"status": "error", "message": "Missing gif_url or api_key"}), 400

    gif_url = data['gif_url']
    api_key = data['api_key']

    uploaded_urls = await process_and_upload_gif(api_key, gif_url, OUTPUT_FOLDER)

    if uploaded_urls:
        return jsonify({"status": "success", "uploaded_urls": uploaded_urls})
    else:
        return jsonify({"status": "error", "message": "Failed to process and upload GIF frames"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "1"]
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
