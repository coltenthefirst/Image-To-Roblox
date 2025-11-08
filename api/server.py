# hello fr

import os
import re
import socket
import logging
import subprocess
import ipaddress
import requests
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, UnidentifiedImageError
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)

# config - this was requested by one if my friends to make things a bit easlier
class Config:
    INPUT = tempfile.mkdtemp(prefix="input_")
    OUTPUT = tempfile.mkdtemp(prefix="output_")
    GIF_NAME = "downloaded.gif"

    SIZES = {
        "nocompression": (500, 500),  # ts new btw 🤑
        "ehigh": (240, 240),
        "high": (120, 120),
        "mid": (60, 60),
        "low": (30, 30),
        "elow": (15, 15),
    }

    COMPRESSION = {
        "ehigh": (1.6, 25),
        "high": (3.2, 50),
        "mid": (6.4, 100),
        "low": (12.8, 200),
        "elow": (30, 400),
    }

    TRUSTED_DOMAINS = [ # I'll add more domains later on
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
        "docs.google.com",
    ]

    ALLOWED_SCRIPTS = {
        "nocompression": ["python3", "no-compression.py"],
        "ehigh": ["python3", "render-image.py", "1.6", "25"],
        "high": ["python3", "render-image.py", "3.2", "50"],
        "mid": ["python3", "render-image.py", "6.4", "100"],
        "low": ["python3", "render-image.py", "12.8", "200"],
        "elow": ["python3", "render-image.py", "30", "400"],
    }

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")



def is_url_good(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        path = parsed.path.lower() # imgur bug fix
        return bool(re.search(r"\.(png|jpg|jpeg|gif|webp|bmp|tiff)$", path))
    except Exception:
        return False


def is_domain_allowed(url):
    domain = urlparse(url).netloc
    return any(domain.endswith(ok) for ok in Config.TRUSTED_DOMAINS)

def is_ip_safe(url):
    try:
        host = urlparse(url).hostname
        ip = socket.gethostbyname(host)
        return ipaddress.ip_address(ip).is_global
    except Exception:
        return False

def safe_download(url, dest_path, timeout=10):
    if not is_url_good(url):
        return False
    if not is_domain_allowed(url):
        return False
    if not is_ip_safe(url):
        return False
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            with open(dest_path, "wb") as f:
                f.write(r.content)
            return True, ""
    except requests.RequestException as e:
        return False

def extract_gif_frames(gif_path, out_dir, fps="max"):
    os.makedirs(out_dir, exist_ok=True)
    with Image.open(gif_path) as gif:
        total = gif.n_frames

        # yuh fixed fps system
        if fps != "max":
            try:
                fps = int(fps)
            except ValueError:
                fps = "max"
        skip = 1 if fps == "max" else max(1, total // int(fps))

        frames = []
        for i in range(0, total, skip):
            gif.seek(i)
            frame_path = os.path.join(out_dir, f"frame_{i}.png")
            gif.save(frame_path, format="PNG")
            frames.append(frame_path)
        return frames

def upload_img(api_key, path):
    r = requests.post(
        "https://api.imgbb.com/1/upload",
        data={"key": api_key},
        files={"image": open(path, "rb")}
    )
    if r.status_code == 200:
        return r.json().get("data", {}).get("url")
    return None

def gif_to_links(api_key, gif_path, output_dir, fps="max"):
    frames = extract_gif_frames(gif_path, output_dir, fps)
    links = []
    for f in frames:
        url = upload_img(api_key, f)
        if url:
            links.append(url)
    return links

def run_script(key):
    cmd = ALLOWED_SCRIPTS.get(key)
    if not cmd:
        return False
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        return False

def get_lua(filepath):
    try:
        with open(filepath, "r") as f:
            return f.read()
    except Exception:
        return None



# TODO: possibly merge this function in the render-image.py script
def convert_image_to_strokes(image_url, button):
    raw_path = os.path.join(Config.INPUT, "raw.png")
    ok, msg = safe_download(image_url, raw_path)
    if not ok:
        return None, msg

    try:
        img = Image.open(raw_path)
    except UnidentifiedImageError:
        return None,

    img = img.convert("RGB")
    img.thumbnail(Config.SIZES[button], Image.Resampling.BICUBIC)

    pixels = img.load()
    w, h = img.size
    result = []

    for y in range(h):
        row = ""
        for x in range(w):
            try:
                px = pixels[x, y]
                px = tuple(max(0, min(255, v)) for v in px)
                row += f'<stroke color="rgb{px}"><font color="rgb{px}">■</font></stroke>'
            except Exception:
                row += '<stroke color="rgb(0,0,0)"><font color="rgb(0,0,0)">■</font></stroke>'
        result.append(row)

    return {
        "image_path": raw_path,
        "output_file": "Result.lua",
        "lines": result
    }, ""



@app.route("/send_gif", methods=["POST"])
def send_gif():
    data = request.get_json()
    gif_url = data.get("gif_url")
    api_key = data.get("api_key")

    if not gif_url or not api_key:
        return jsonify({"status": "error", "message": "missing data"}), 400

    gif_path = os.path.join(Config.INPUT, Config.GIF_NAME)
    ok, msg = safe_download(gif_url, gif_path)
    if not ok:
        return jsonify({"status": "error", "message": msg}), 400

    links = gif_to_links(api_key, gif_path, Config.OUTPUT)
    if not links:
        return jsonify({"status": "error", "message": "upload failed"}), 400

    result = subprocess.run(["python3", "gif-sender.py"] + links, capture_output=True, text=True)
    if result.returncode == 0:
        return jsonify({"status": "success", "uploaded_urls": links, "gif_sender_output": result.stdout})

    return jsonify({"status": "error", "message": "sender broke"}), 500

@app.route("/send_image", methods=["POST"])
def send_image():
    data = request.get_json()
    image_url = data.get("image_url")
    script_key = data.get("button_clicked")

    if not image_url or not script_key:
        return jsonify({"status": "error", "message": "need image_url and button_clicked"}), 400

    image_path = os.path.join(Config.INPUT, "image.png")
    ok, msg = safe_download(image_url, image_path)
    if not ok:
        return jsonify({"status": "error", "message": msg}), 400

    if not run_script(script_key):
        return jsonify({"status": "error", "message": "script failed"}), 500

    lua_path = os.path.join(Config.OUTPUT, "image.lua")
    script_text = get_lua(lua_path)
    if script_text:
        return jsonify({"status": "success", "lua_script": script_text})

    return jsonify({"status": "error", "message": "lua not found"}), 500

@app.route("/gui_send_image", methods=["POST"])
def gui_send_image():
    data = request.get_json()
    image_url = data.get("image_url")
    button = data.get("button_name")

    if not image_url or button not in Config.SIZES:
        return jsonify({"status": "error", "message": "bad request"}), 400

    result, msg = convert_image_to_strokes(image_url, button)
    if not result:
        return jsonify({"status": "error", "message": msg}), 400

    return jsonify({"status": "success", "message": "image good", **result})



if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") in ["1", "true", "yes"]
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=debug)
