# hello fr

import os
import socket
import logging
import subprocess
import ipaddress
import requests
import shlex
import hashlib
import hmac
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, UnidentifiedImageError
from urllib.parse import urlparse
import mimetypes

app = Flask(__name__)
CORS(app)

# Security configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Simple rate limiting storage (in production use Redis)
request_counts = {}
RATE_LIMIT_REQUESTS = 100  # requests per window
RATE_LIMIT_WINDOW = 300   # 5 minutes

INPUT = "/tmp/input"
OUTPUT = "/tmp/output"
GIF_NAME = "downloaded.gif"

os.makedirs(INPUT, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)

logging.basicConfig(level=logging.ERROR)

# Security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# Error handlers for security
@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"status": "error", "message": "request too large"}), 413

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"status": "error", "message": "invalid request format"}), 400


SIZES = {
    "nocompression": (500, 500), # ts new btw 🤑 (coming next model)
    "ehigh": (240, 240),
    "high": (120, 120),
    "mid": (60, 60),
    "low": (30, 30),
    "elow": (15, 15)
}

COMPRESSION = {
    "ehigh": (1.6, 25),
    "high": (3.2, 50),
    "mid": (6.4, 100),
    "low": (12.8, 200),
    "elow": (30, 400)
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

ALLOWED_IMAGE_TYPES = {
    'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'image/bmp'
}

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}





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

def validate_content_type(response):
    """Validate content-type of downloaded content"""
    content_type = response.headers.get('content-type', '').lower()
    return any(allowed_type in content_type for allowed_type in ALLOWED_IMAGE_TYPES)

def validate_file_extension(url):
    """Validate file extension from URL"""
    parsed = urlparse(url)
    path = parsed.path.lower()
    return any(path.endswith(ext) for ext in ALLOWED_EXTENSIONS)

def sanitize_filename(filename):
    """Sanitize filename to prevent path traversal"""
    import re
    # Remove directory traversal patterns and dangerous characters
    filename = re.sub(r'[^\w\-_\.]', '', filename)
    filename = re.sub(r'\.\.+', '.', filename)
    return filename[:255]  # Limit length

def check_rate_limit():
    """Simple IP-based rate limiting"""
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    if not client_ip:
        client_ip = 'unknown'
        
    current_time = int(time.time())
    window_start = current_time - (current_time % RATE_LIMIT_WINDOW)
    
    key = f"{client_ip}:{window_start}"
    
    # Clean old entries
    keys_to_delete = [k for k in request_counts.keys() 
                     if int(k.split(':')[1]) < window_start - RATE_LIMIT_WINDOW]
    for k in keys_to_delete:
        del request_counts[k]
    
    # Check current count
    current_count = request_counts.get(key, 0)
    if current_count >= RATE_LIMIT_REQUESTS:
        return False
        
    request_counts[key] = current_count + 1
    return True




def download_img(imageURL, outPath, tries=5):
    if not is_url_good(imageURL):
        return False, "bad url" # yeah bad fucking boy >:(
    if not is_domain_allowed(imageURL):
        return False, "blocked domain" # wat da fuk is dat domain bro?? 😭✌️
    if not is_ip_safe(imageURL):
        return False, "unsafe IP"
    if not validate_file_extension(imageURL):
        return False, "invalid file extension"
    
    for _ in range(tries):
        try:
            r = requests.get(imageURL, timeout=10, stream=True)
            if r.status_code == 200:
                if not validate_content_type(r):
                    return False, "invalid content type"
                
                # Check file size
                content_length = r.headers.get('content-length')
                if content_length and int(content_length) > 16 * 1024 * 1024:  # 16MB
                    return False, "file too large"
                
                with open(outPath, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
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
    # Sanitize URLs to prevent injection
    sanitized_urls = []
    for url in listOfUrls:
        if isinstance(url, str) and is_url_good(url):
            sanitized_urls.append(shlex.quote(url))
        else:
            return None  # Invalid URL detected
    
    if not sanitized_urls:
        return None
        
    cmd = ["python3", "gif-sender.py"] + sanitized_urls
    result = subprocess.run(cmd, capture_output=True, text=True, cwd="/home/engine/project")
    if result.returncode == 0:
        return result.stdout
    return None

def run_script(key):
    # Validate key against allowed values to prevent injection
    if key not in SIZES and key != "nocompression":
        return False
        
    if key == "nocompression":
        try:
            subprocess.run(["python3", "no-compression.py"], check=True, cwd="/home/engine/project")
            return True
        except:
            return False

    cfg = COMPRESSION.get(key)
    if not cfg: 
        return False
    
    try:
        # Validate numeric parameters
        factor = float(cfg[0])
        rate = int(cfg[1])
        if factor <= 0 or rate <= 0:
            return False
            
        subprocess.run([
            "python3", "render-image.py", 
            str(factor), str(rate)
        ], check=True, cwd="/home/engine/project")
        return True
    except (ValueError, TypeError):
        return False
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
        return None, "unsafe IP" # 🤨
    if not validate_file_extension(gifURL):
        return None, "invalid file extension"
        
    os.makedirs(dumpPath, exist_ok=True)
    out = os.path.join(dumpPath, sanitize_filename(GIF_NAME))
    
    try:
        r = requests.get(gifURL, timeout=10, stream=True)
        if r.status_code == 200:
            if not validate_content_type(r):
                return None, "invalid content type"
                
            # Check file size
            content_length = r.headers.get('content-length')
            if content_length and int(content_length) > 16 * 1024 * 1024:  # 16MB
                return None, "file too large"
                
            with open(out, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return out, ""
    except Exception:
        pass
    return None, "gif fetch failed"




@app.route("/send_gif", methods=["POST"])
def send_gif():
    # Rate limiting check
    if not check_rate_limit():
        return jsonify({"status": "error", "message": "rate limit exceeded"}), 429
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "invalid JSON"}), 400
            
        gifURL = data.get("gif_url")
        fuckingApiKey = data.get("api_key")

        if not gifURL or not fuckingApiKey:
            return jsonify({"status": "error", "message": "missing data"}), 400
            
        # Validate input types
        if not isinstance(gifURL, str) or not isinstance(fuckingApiKey, str):
            return jsonify({"status": "error", "message": "invalid data types"}), 400
            
        # Validate URL length
        if len(gifURL) > 2048 or len(fuckingApiKey) > 512:
            return jsonify({"status": "error", "message": "input too long"}), 400
    except Exception:
        return jsonify({"status": "error", "message": "invalid request format"}), 400

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
    # Rate limiting check
    if not check_rate_limit():
        return jsonify({"status": "error", "message": "rate limit exceeded"}), 429
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "invalid JSON"}), 400
            
        imageURL = data.get("image_url")
        scriptKey = data.get("button_clicked")

        if not imageURL or not scriptKey:
            return jsonify({"status": "error", "message": "need image_url and button_clicked"}), 400
            
        # Validate input types
        if not isinstance(imageURL, str) or not isinstance(scriptKey, str):
            return jsonify({"status": "error", "message": "invalid data types"}), 400
            
        # Validate input lengths
        if len(imageURL) > 2048 or len(scriptKey) > 64:
            return jsonify({"status": "error", "message": "input too long"}), 400
    except Exception:
        return jsonify({"status": "error", "message": "invalid request format"}), 400

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
    # Rate limiting check
    if not check_rate_limit():
        return jsonify({"status": "error", "message": "rate limit exceeded"}), 429
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "invalid JSON"}), 400
            
        imageURL = data.get("image_url")
        button = data.get("button_name")

        if not imageURL or not button:
            return jsonify({"status": "error", "message": "missing required fields"}), 400
            
        # Validate input types
        if not isinstance(imageURL, str) or not isinstance(button, str):
            return jsonify({"status": "error", "message": "invalid data types"}), 400
            
        # Validate input lengths
        if len(imageURL) > 2048 or len(button) > 64:
            return jsonify({"status": "error", "message": "input too long"}), 400

        if button not in SIZES:
            return jsonify({"status": "error", "message": "invalid button name"}), 400

        # Apply same security validations as other endpoints
        if not is_url_good(imageURL):
            return jsonify({"status": "error", "message": "invalid URL"}), 400
        
        if not is_domain_allowed(imageURL):
            return jsonify({"status": "error", "message": "domain not allowed"}), 403
            
        if not is_ip_safe(imageURL):
            return jsonify({"status": "error", "message": "unsafe IP address"}), 403
            
        if not validate_file_extension(imageURL):
            return jsonify({"status": "error", "message": "invalid file extension"}), 400

        rawPath = os.path.join(INPUT, sanitize_filename("raw.png"))
        
        # Use secure download with proper validation
        success, error_msg = download_img(imageURL, rawPath)
        if not success:
            return jsonify({"status": "error", "message": error_msg}), 400

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
