# Generates the organisation logo. Variant A is the one in use:
#   python3 make-logo.py A org-logo.png   (needs Pillow)
import math, sys
from PIL import Image, ImageDraw, ImageFilter
K = 8; N = 512 * K
BLUE_A, BLUE_B = (0x13, 0xB9, 0xFD), (0x02, 0x56, 0x9B)      # Flutter-style blues
MAG_A, MAG_B = (0xFF, 0x3D, 0x9A), (0xA5, 0x00, 0x5E)        # webOS-style magenta
def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
def S(*v): return tuple(int(x * K) for x in v)

def background(c0, c1):
    sm = Image.new('RGB', (128, 128))
    for y in range(128):
        for x in range(128):
            sm.putpixel((x, y), lerp(c0, c1, (x + y) / 254))
    g = sm.resize((N, N), Image.BILINEAR).convert('RGBA')
    m = Image.new('L', (N, N), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, N - 1, N - 1), radius=112 * K, fill=255)
    img = Image.new('RGBA', (N, N), (0, 0, 0, 0)); img.paste(g, (0, 0), m)
    return img

def helix(img, x0, x1, cy, amp, turns, width, rung_w, vertical=False, glow=True):
    """Two strands; strand 1 blue, strand 2 magenta; depth-sorted at crossings."""
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    steps = 600
    pts = []
    for i in range(steps + 1):
        t = i / steps
        a = 2 * math.pi * turns * t + math.pi / 2
        u = x0 + (x1 - x0) * t
        y1 = cy + amp * math.sin(a); y2 = cy - amp * math.sin(a)
        z1 = math.cos(a)
        pts.append((t, u, y1, y2, z1))
    def P(u, y): return S(y, u) if vertical else S(u, y)
    def seg(strand, front):
        for (t, u, y1, y2, z), (_, u2, y1b, y2b, _) in zip(pts, pts[1:]):
            zs = z if strand == 1 else -z
            if (zs >= 0) != front: continue
            col = lerp(BLUE_A, BLUE_B, t) if strand == 1 else lerp(MAG_A, MAG_B, t)
            shade = 1.0 if front else 0.62
            col = tuple(int(c * shade) for c in col) + (255,)
            ya, yb = (y1, y1b) if strand == 1 else (y2, y2b)
            d.line([P(u, ya), P(u2, yb)], fill=col, width=int(width * K * (1 if front else .8)))
            r = width * K * (1 if front else .8) / 2
            cx, cyy = P(u, ya); d.ellipse((cx - r, cyy - r, cx + r, cyy + r), fill=col)
    seg(1, False); seg(2, False)
    # rungs (base pairs)
    nr = int(turns * 10)
    for j in range(1, nr):
        t = j / nr
        a = 2 * math.pi * turns * t + math.pi / 2
        u = x0 + (x1 - x0) * t
        y1 = cy + amp * math.sin(a); y2 = cy - amp * math.sin(a)
        if abs(y1 - y2) < width * 1.2: continue
        top, bot = (y1, y2) if y1 < y2 else (y2, y1)
        topc = BLUE_A if (y1 < y2) else MAG_A
        botc = MAG_A if (y1 < y2) else BLUE_A
        mid = (top + bot) / 2
        d.line([P(u, top), P(u, mid)], fill=topc + (215,), width=int(rung_w * K))
        d.line([P(u, mid), P(u, bot)], fill=botc + (215,), width=int(rung_w * K))
    seg(1, True); seg(2, True)
    if glow:
        g = layer.filter(ImageFilter.GaussianBlur(10 * K)); img.alpha_composite(g); img.alpha_composite(g)
    img.alpha_composite(layer)

def tv(img, x0, y0, x1, y1, stroke, fill_screen=None):
    d = ImageDraw.Draw(img)
    if fill_screen: d.rounded_rectangle(S(x0, y0, x1, y1), radius=26 * K, fill=fill_screen)
    d.rounded_rectangle(S(x0, y0, x1, y1), radius=26 * K, outline=(255, 255, 255, 235), width=stroke * K)
    cx = (x0 + x1) / 2
    d.rounded_rectangle(S(cx - 70, y1 + 26, cx + 70, y1 + 44), radius=9 * K, fill=(255, 255, 255, 235))
    d.rectangle(S(cx - 14, y1, cx + 14, y1 + 30), fill=(255, 255, 255, 235))

def save(img, name):
    out = img.resize((1024, 1024), Image.LANCZOS); out.save(name, optimize=True); return out

v = sys.argv[1]; out = sys.argv[2]
if v == 'A':   # helix inside a TV
    img = background((0x0d, 0x1b, 0x3a), (0x2a, 0x10, 0x3f))
    tv(img, 70, 110, 442, 360, 14, fill_screen=(0x08, 0x0f, 0x22, 255))
    helix(img, 108, 404, 235, 70, 1.6, 15, 6)
elif v == 'B':  # bold diagonal helix only
    img = background((0x0b, 0x1a, 0x36), (0x25, 0x0e, 0x3a))
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    helix(lay, 70, 442, 256, 92, 1.75, 22, 8)
    lay = lay.rotate(45, resample=Image.BICUBIC, center=(N / 2, N / 2))
    m = Image.new('L', (N, N), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, N - 1, N - 1), radius=112 * K, fill=255)
    clip = Image.new('RGBA', img.size, (0, 0, 0, 0)); clip.paste(lay, (0, 0), m)
    img.alpha_composite(clip)
elif v == 'C':  # vertical helix rising out of a TV screen
    img = background((0x02, 0x3e, 0x80), (0x6b, 0x0f, 0x5a))
    tv(img, 96, 250, 416, 400, 14, fill_screen=(0x08, 0x0f, 0x22, 230))
    helix(img, 58, 330, 256, 64, 1.5, 17, 6, vertical=True)
save(img, out)
