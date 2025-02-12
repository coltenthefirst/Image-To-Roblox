from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, UnidentifiedImageError
import requests

app = Flask(__name__)
CORS(app)

RESIZE_MAPPINGS = {
    "test": (350, 350),
    "elow": (15, 15),
    "ehigh": (240, 240),
    "low": (30, 30),
    "high": (120, 120),
    "mid": (60, 60),
}

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

        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            return jsonify({'status': 'error', 'message': 'Failed to download the image'}), 400

        image_path = 'downloaded_image.png'
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
                except Exception as e:
                    row += "<stroke color=\"rgb(0,0,0)\"><font color=\"rgb(0,0,0)\">■</font></stroke>"
            lines_to_send.append(row)

        return jsonify({
            'status': 'success',
            'message': 'Image processed and file created',
            'output_file': 'Result.lua',
            'lines': lines_to_send
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5015)
