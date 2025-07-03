# hello fr

import os
import socket
import logging
import subprocess
import ipaddress
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, UnidentifiedImageError
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)

INPUT = "/tmp/input"
OUTPUT = "/tmp/output"
GIF_NAME = "downloaded.gif"

os.makedirs(INPUT, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)

logging.basicConfig(level=logging.ERROR)


SIZES = {
    "low": (30, 30),
    "mid": (60, 60),
    "high": (120, 120),
    "elow": (15, 15),
    "ehigh": (240, 240),
    "nocompression": (500, 500) # ts new btw 🤑 (coming next model)
}

SCRIPTS = {
    "low": "low.py",
    "mid": "mid.py",
    "high": "high.py",
    "elow": "extra-low.py",
    "ehigh": "extra-high.py",
    "nocompression": "no-compression.py" # new (coming next model)
}

TRUSTED_DOMAINS = [ # skidded from the last ai code 
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





def is_url_good(url): 
    try:
        p = urlparse(url)
        return p.scheme in ["http", "https"] and p.netloc
        # yes very good url
        # I just realized how better it is to add comments into your code fr
    except:
        return False

def is_domain_allowed(url, check=True):
    if not check:
        return True
    domain = urlparse(url).netloc
    return any(domain.endswith(ok) for ok in TRUSTED_DOMAINS)

def is_ip_safe(url):
    try:
        host = urlparse(url).hostname
        ip = socket.gethostbyname(host)
        return ipaddress.ip_address(ip).is_global
    except:
        return False




def download_img(imageURL, outPath, tries=5):
    if not is_url_good(imageURL):
        return False, "bad url" # yeah bad fucking boy >:(
    if not is_domain_allowed(imageURL):
        return False, "blocked domain" # wat da fuk is dat domain bro?? 😭✌️
    for _ in range(tries):
        try:
            r = requests.get(imageURL, timeout=10)
            if r.status_code == 200:
                with open(outPath, "wb") as f:
                    f.write(r.content)
                return True, ""
        except:
            pass
    return False, "couldn't fetch image"

def extract_gif_frames(gifPath, toDir, fps="max"):
    os.makedirs(toDir, exist_ok=True)
    with Image.open(gifPath) as g:
        total = g.n_frames
        skip = 1 if fps == "max" else max(1, total // int(fps))
        frames = []
        for i in range(0, total, skip):
            g.seek(i)
            p = os.path.join(toDir, f"frame_{i}.png")
            g.save(p, format="PNG")
            frames.append(p)
        return frames

def upload_img(fuckingApiKey, path): # reminder: change this var to like "fucking api key" or something in the future
    r = requests.post(
        "https://api.imgbb.com/1/upload",
        data={"key": fuckingApiKey},
        files={"image": open(path, "rb")}
    )
    if r.status_code == 200:
        return r.json().get("data", {}).get("url")
    return None

def gif_to_links(fuckingApiKey, gifPath, outputDir, fps="max"):
    frames = extract_gif_frames(gifPath, outputDir, fps)
    return [upload_img(fuckingApiKey, f) for f in frames if upload_img(fuckingApiKey, f)]




def gif_sender(listOfUrls):
    result = subprocess.run(["python3", "gif-sender.py"] + listOfUrls, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout
    return None

def run_script(scriptKey):
    file = SCRIPTS.get(scriptKey)
    if not file:
        return False
    try:
        subprocess.run(["python3", file], check=True)
        return True
    except:
        return False

def get_lua(filepath):
    try:
        with open(filepath, "r") as f:
            return f.read()
    except:
        return None

def download_gif(gifURL, dumpPath):
    if not is_url_good(gifURL):
        return None, "bad url"
    if not is_domain_allowed(gifURL):
        return None, "domain not whitelisted"
    if not is_ip_safe(gifURL):
        return None, "unsafe IP" } # 🤨
    os.makedirs(dumpPath, exist_ok=True)
    out = os.path.join(dumpPath, GIF_NAME)
    r = requests.get(gifURL, timeout=10)
    if r.status_code == 200:
        with open(out, "wb") as f:
            f.write(r.content)
        return out, ""
    return None, "gif fetch failed"




@app.route("/send_gif", methods=["POST"])
def send_gif():
    data = request.get_json()
    gifURL = data.get("gif_url")
    fuckingApiKey = data.get("api_key")

    if not gifURL or not fuckingApiKey:
        return jsonify({"status": "error", "message": "missing data"}), 400

    gifPath, msg = download_gif(gifURL, "/tmp/processed_gif")
    if not gifPath:
        return jsonify({"status": "error", "message": msg}), 400

    links = gif_to_links(fuckingApiKey, gifPath, OUTPUT)
    if not links:
        return jsonify({"status": "error", "message": "upload failed"}), 400

    sent = gif_sender(links)
    if sent:
        return jsonify({"status": "success", "uploaded_urls": links, "gif_sender_output": sent})

    return jsonify({"status": "error", "message": "sender broke"}), 500




@app.route("/send_image", methods=["POST"]) # my beloved...
def send_image():
    data = request.get_json()
    imageURL = data.get("image_url")
    scriptKey = data.get("button_clicked")

    if not imageURL or not scriptKey:
        return jsonify({"status": "error", "message": "need image_url and button_clicked"}), 400

    imagePath = os.path.join(INPUT, "image.png")
    ok, msg = download_img(imageURL, imagePath)
    if not ok:
        return jsonify({"status": "error", "message": msg}), 400

    if not run_script(scriptKey):
        return jsonify({"status": "error", "message": "script failed"}), 500

    luaPath = os.path.join(OUTPUT, "image.lua")
    scriptText = get_lua(luaPath)
    if scriptText:
        return jsonify({"status": "success", "lua_script": scriptText})

    return jsonify({"status": "error", "message": "lua not found"}), 500




@app.route("/gui_send_image", methods=["POST"]) # my hated!!!0

def gui_send_image():
    try:
        data = request.json
        imageURL = data.get("image_url")
        button = data.get("button_name")

        if not imageURL or button not in SIZES:
            return jsonify({"status": "error", "message": "bad request"}), 400

        rawPath = os.path.join(INPUT, "raw.png")
        r = requests.get(imageURL)
        if r.status_code != 200:
            return jsonify({"status": "error", "message": "img fetch failed"}), 400

        with open(rawPath, "wb") as f:
            f.write(r.content)

        try:
            img = Image.open(rawPath)
        except UnidentifiedImageError:
            return jsonify({"status": "error", "message": "not an image"}), 400

        if img.mode not in ("RGB", "RGBA", "L"):
            img = img.convert("RGB")
        elif img.mode != "RGB":
            img = img.convert("RGB")

        img.thumbnail(SIZES[button], Image.Resampling.BICUBIC)
        pixels = img.load()
        w, h = img.size
        result = []

        for y in range(h):
            row = ""
            for x in range(w):
                try:
                    px = pixels[x, y]
                    if isinstance(px, int):
                        px = (px, px, px)
                    elif isinstance(px, tuple) and len(px) != 3:
                        px = px[:3] if len(px) >= 3 else (0, 0, 0)
                    elif not isinstance(px, tuple):
                        px = (0, 0, 0)
                    px = tuple(max(0, min(255, v)) for v in px)
                    row += f'<stroke color="rgb{px}"><font color="rgb{px}">■</font></stroke>'
                except:
                    row += '<stroke color="rgb(0,0,0)"><font color="rgb(0,0,0)">■</font></stroke>'
            result.append(row)

        return jsonify({
            "status": "success",
            "message": "image good",
            "image_path": rawPath,
            "output_file": "Result.lua",
            "lines": result
        })

    except Exception as e:
        logging.error(str(e))
        return jsonify({"status": "error", "message": "shit broke"}), 500




if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") in ["1", "true", "yes"]
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=debug)

# I finally fucking finished the rewite 💔
