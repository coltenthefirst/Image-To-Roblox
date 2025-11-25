from PIL import Image
import os
import time

rate = 0
os.makedirs("/tmp/output", exist_ok=True)

for name in os.listdir("/tmp/input"):
    path = os.path.join("/tmp/input", name)
    if not os.path.isfile(path): continue

    try:
        img = Image.open(path)
        if img.mode != "RGB":
            img = img.convert("RGB")

        w, h = img.size
        px = img.load()
        base = os.path.splitext(name)[0]

        for _ in range(5):
            try:
                with open(f"/tmp/output/{base}.lua", "w") as f:
                    bits = []
                    for y in range(h):
                        for x in range(w):
                            r, g, b = px[x, y]
                            bits.append(f"{r:03d}{g:03d}{b:03d}")
                    f.write(f"require(script.Parent.Parent):Draw({rate}, Vector3.new(0,0,0), {{{w},{h}}}, '{''.join(bits)}')")
                break
            except Exception:
                time.sleep(1)
    except:
        pass
