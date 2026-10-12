"""Annotated panorama from the balcony, built from Alexandre's PeakFinder capture.

Keeps the real landscape band of photos_src/a-peakfinder.png (below the app's
labels, above its GPS chip), removes the app's buttons and the sun marker, and
redraws the 19 summit labels in a band above. Leader x positions were measured
on the capture (dark vertical lines). No GPS coordinates are kept.
Run: python3 src/panorama.py  ->  img/panorama-2400.jpg, img/panorama-1200.jpg
"""
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "photos_src" / "a-peakfinder.png"

# (name, altitude, leader x on the capture); Combin is just beyond the left edge
PEAKS = [
    ("Les Louèrettes", 3068, 60),
    ("Bec de la Montau", 2922, 199),
    ("Mont Gelé", 3023, 511),
    ("Pointe de Champ Ferret", 2742, 618),
    ("Dent de Nendaz", 2463, 784),
    ("Mont Blanc", 4807, 895),
    ("Pierre Avoi", 2473, 994),
    ("Arête de la Lys", 2796, 1087),
    ("Aiguille de la Floria", 2888, 1244),
    ("Mont de l’Arpille", 2085, 1343),
    ("Pointe de Vouilloz", 2672, 1428),
    ("Sommet de l’Ardève", 1507, 1539),
    ("Grand Chavalard", 2901, 1635),
    ("Six Tremble", 2701, 1745),
    ("Tête de Vertsan", 2563, 1843),
    ("Haut de Cry", 2968, 1959),
    ("Grand Muveran", 3051, 2069),
    ("Prabé", 2041, 2258),
]
HIGHLIGHT = {"Mont Blanc"}

X0, X1, Y0, Y1 = 0, 2400, 552, 962   # landscape band kept from the capture
BAND = 440                             # label band height above the photo
INK = (36, 31, 27)
TERRA = (164, 80, 47)
PAPER = (243, 239, 232)


def clean_band(a):
    """Remove the app's controls and the sun marker. Plain sky is horizontally
    smooth, so masked pixels are filled row by row between their neighbours,
    working on the full-width capture so the right edge has context."""
    a = a.copy()
    h, w = a.shape[:2]
    mask = np.zeros((h, w), bool)
    def box(x0, y0, x1, y1):
        mask[y0:y1, x0:x1] = True
    box(1832, 548, 1988, 690)    # 17:36 badge and arrow
    hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)
    yellow = cv2.inRange(hsv, (18, 120, 150), (40, 255, 255)) > 0
    yellow = cv2.dilate(yellow.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
    yellow[:Y0 - 20] = False
    mask |= yellow
    # leader stub ends (ridge) measured on the untouched capture
    g = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY).astype(int)
    ends = {}
    for _, _, x in PEAKS:
        y = 560
        while y < Y1 - 1 and g[y, x - 1:x + 2].min() < 110:
            y += 1
        ends[x] = y
    # textured areas (arrows, shutter): patch with the neighbouring strip of the
    # same rows (sky, ridge and trees continue horizontally), feathered edges
    def patch(y0, y1, x0, x1, sx):
        nonlocal a
        src = a[y0:y1, sx:sx + (x1 - x0)].astype(np.float32)
        dst = a[y0:y1, x0:x1].astype(np.float32)
        m = np.zeros((y1 - y0, x1 - x0), np.float32)
        m[12:-12, 12:-12] = 1
        m = cv2.GaussianBlur(m, (0, 0), 6)[..., None]
        a[y0:y1, x0:x1] = np.clip(dst * (1 - m) + src * m, 0, 255).astype(np.uint8)
    patch(480, 720, 110, 300, 300)
    patch(495, 700, 2250, 2440, 2060)
    mask[:, 2400:] = False
    af = a.astype(np.float32)
    for y in range(Y0, Y1):
        m = mask[y]
        if not m.any():
            continue
        xs = np.arange(w)
        good = ~m
        for c in range(3):
            af[y, m, c] = np.interp(xs[m], xs[good], af[y, good, c])
    rng = np.random.default_rng(3)
    af[mask] += rng.normal(0, 1.5, (mask.sum(), 3))
    out = np.clip(af, 0, 255).astype(np.uint8)[Y0:Y1, X0:X1]
    # redraw every leader down to the ridge so cleaned areas stay consistent
    for _, _, x in PEAKS:
        end = {60: 668, 199: 684}.get(x, ends[x] if ends[x] > 600 else 690)
        cv2.line(out, (x - X0, 0), (x - X0, end - Y0), (40, 40, 40), 2, cv2.LINE_AA)
    return out


def pill(text, alt, color, font, font_b):
    pad_x, pad_y = 24, 11
    w1 = font.getlength(text + "  ")
    w2 = font_b.getlength(str(alt))
    w, h = int(w1 + w2 + 2 * pad_x), 58
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=color + (235,))
    d.text((pad_x, h / 2), text, font=font, fill=(255, 255, 255), anchor="lm")
    d.text((pad_x + w1, h / 2), str(alt), font=font_b, fill=(255, 255, 255, 200), anchor="lm")
    return im


def main():
    a = np.array(Image.open(SRC).convert("RGB"))
    photo = Image.fromarray(clean_band(a))
    W = X1 - X0
    canvas = Image.new("RGB", (W, BAND + photo.height), PAPER)
    canvas.paste(photo, (0, BAND))
    font = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Medium.otf", 28)
    font_b = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Regular.otf", 24)
    d = ImageDraw.Draw(canvas)
    for name, alt, x in PEAKS:
        color = TERRA if name in HIGHLIGHT else INK
        # leader from the label foot down into the photo
        d.line((x, BAND - 34, x, BAND + 4), fill=(60, 60, 60), width=2)
        p = pill(name, alt, color, font, font_b).rotate(48, expand=True, resample=Image.BICUBIC)
        # anchor: bottom-left corner of the rotated pill sits on the leader top
        canvas.paste(p, (int(x - 22), int(BAND - 34 - p.height + 22)), p)
    # Grand Combin stands just beyond the left edge of the frame
    t = "← Grand Combin de Grafeneire  4314"
    d.text((22, 34), t, font=font, fill=TERRA)
    out = ROOT / "img"
    canvas.save(out / "panorama-2400.jpg", quality=84, optimize=True, progressive=True)
    c = canvas.resize((1200, int(canvas.height * 1200 / canvas.width)), Image.LANCZOS)
    c = c.filter(ImageFilter.UnsharpMask(radius=1, percent=40, threshold=3))
    c.save(out / "panorama-1200.jpg", quality=84, optimize=True, progressive=True)
    print(canvas.size)


if __name__ == "__main__":
    main()
