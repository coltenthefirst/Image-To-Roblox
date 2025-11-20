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


    # I did this because the server is hosted with vercel
    INPUT = "/tmp/input"
    OUTPUT = "/tmp/output"
    
    os.makedirs(INPUT, exist_ok=True)
    os.makedirs(OUTPUT, exist_ok=True)
    
    
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
        return parsed.scheme in ("http", "https") and re.search(r"\.(png|jpg|jpeg|gif|webp|bmp|tiff)$", parsed.path.lower())
    except:
        return False

def is_domain_allowed(url):
    return any(urlparse(url).netloc.endswith(ok) for ok in Config.TRUSTED_DOMAINS)

def is_ip_safe(url):
    try:
        return ipaddress.ip_address(socket.gethostbyname(urlparse(url).hostname)).is_global
    except:
        return False

def safe_download(url, dest, timeout=10):
    if not (is_url_good(url) and is_domain_allowed(url) and is_ip_safe(url)):
        return False, "Invalid or unsafe URL"
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            return False, f"HTTP {r.status_code}"
        open(dest, "wb").write(r.content)
        return True, ""
    except Exception as e:
        return False, f"Download failed: {e}"

def extract_gif_frames(gif_path, out_dir, fps="max"):
    os.makedirs(out_dir, exist_ok=True)
    gif = Image.open(gif_path)
    total = gif.n_frames

    # yuh fixed fps system
    skip = 1 if fps == "max" else max(1, total // int(fps or 1))
    frames = []

    for i in range(0, total, skip):
        gif.seek(i)
        frame = os.path.join(out_dir, f"frame_{i}.png")
        gif.save(frame)
        frames.append(frame)
    return frames

upload_img = lambda key, p: (
    (lambda r: r.json().get("data", {}).get("url") if r.status_code == 200 else None)
    (requests.post("https://api.imgbb.com/1/upload", data={"key": key}, files={"image": open(p, "rb")}))
)

def gif_to_links(key, path, out, fps="max"):
    return [u for f in extract_gif_frames(path, out, fps) if (u := upload_img(key, f))]

def run_script(key):
    cmd = Config.ALLOWED_SCRIPTS.get(key)
    try:
        return subprocess.run(cmd, check=True).returncode == 0
    except:
        return False

def get_lua(path):
    try:
        return open(path).read()
    except:
        return None


# TODO: possibly merge this function in the render-image.py script
def convert_image_to_strokes(url, button):
    raw = os.path.join(Config.INPUT, "raw.png")
    ok, msg = safe_download(url, raw)
    if not ok: return None, msg

    try:
        img = Image.open(raw).convert("RGB")
    except UnidentifiedImageError:
        return None, ""

    img.thumbnail(Config.SIZES[button], Image.Resampling.BICUBIC)
    pixels = img.load()
    w, h = img.size

    result = [
        "".join(
            f'<stroke color="rgb{px}"><font color="rgb{px}">■</font></stroke>'
            for px in (pixels[x, y] if isinstance(pixels[x, y], tuple) else (0, 0, 0),)
        )
        for y in range(h)
    ]

    return {"image_path": raw, "output_file": "Result.lua", "lines": result}, ""


@app.route("/send_gif", methods=["POST"])
def send_gif():
    data = request.get_json()
    gif_url, key = data.get("gif_url"), data.get("api_key")
    if not gif_url or not key:
        return jsonify({"status": "error", "message": "missing data"}), 400

    path = os.path.join(Config.INPUT, Config.GIF_NAME)
    ok, msg = safe_download(gif_url, path)
    if not ok:
        return jsonify({"status": "error", "message": msg}), 400

    links = gif_to_links(key, path, Config.OUTPUT)
    if not links:
        return jsonify({"status": "error", "message": "upload failed"}), 400

    out = subprocess.run(["python3", "gif-sender.py"] + links, capture_output=True, text=True)
    return (
        jsonify({"status": "success", "uploaded_urls": links, "gif_sender_output": out.stdout})
        if out.returncode == 0 else
        (jsonify({"status": "error", "message": "sender broke"}), 500)
    )


@app.route("/send_image", methods=["POST"])
def send_image():
    data = request.get_json()
    url, key = data.get("image_url"), data.get("button_clicked")
    if not url or not key:
        return jsonify({"status": "error", "message": "need image_url and button_clicked"}), 400

    path = os.path.join(Config.INPUT, "image.png")
    ok, msg = safe_download(url, path)
    if not ok:
        return jsonify({"status": "error", "message": msg}), 400

    if not run_script(key):
        return jsonify({"status": "error", "message": "script failed"}), 500

    lua = get_lua(os.path.join(Config.OUTPUT, "image.lua"))
    return (
        jsonify({"status": "success", "lua_script": lua})
        if lua else
        (jsonify({"status": "error", "message": "lua not found"}), 500)
    )

@app.route("/gui_send_image", methods=["POST"])
def gui_send_image():
    data = request.get_json()
    url, button = data.get("image_url"), data.get("button_name")

    if not url or button not in Config.SIZES:
        return jsonify({"status": "error", "message": "bad request"}), 400

    result, msg = convert_image_to_strokes(url, button)
    if not result:
        return jsonify({"status": "error", "message": msg}), 400

    return jsonify({"status": "success", "message": "image good", **result})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "0") in ["1", "true", "yes"]
    )
    app.run(host="0.0.0.0", port=port, debug=debug)
