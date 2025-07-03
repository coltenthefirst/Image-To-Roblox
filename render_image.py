import os, time, sys
from PIL import Image

try:
    factor = float(sys.argv[1])
    rate = int(sys.argv[2])
except:
    sys.exit(1)

INPUT = "/tmp/input"
OUTPUT = "/tmp/output"
os.makedirs(OUTPUT, exist_ok=True)

for name in os.listdir(INPUT):
    path = os.path.join(INPUT, name)
    if not os.path.isfile(path): continue

    try:
        img = Image.open(path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        if factor != 1:
            img = img.resize((int(img.size[0]/factor), int(img.size[1]/factor)))
        px = img.load()
        w, h = img.size
        base = os.path.splitext(name)[0]

        for _ in range(5):
            try:
                with open(f"{OUTPUT}/{base}.lua", "w") as f:
                    bits = []
                    for y in range(h):
                        for x in range(w):
                            r, g, b = px[x, y]
                            bits.append(f"{r:03d}{g:03d}{b:03d}")
                    f.write(f"require(script.Parent.Parent):Draw({rate}, Vector3.new(0,0,0), {{{w},{h}}}, '{''.join(bits)}')")
                break
            except:
                time.sleep(1)
    except:
        pass
