"""Prepare web images from Alexandre's originals.

Originals are NOT kept in the repo (too heavy): put them in photos_src/
(same file names) and run:  python3 src/photos.py
Outputs img/<slug>-1600.jpg and img/<slug>-800.jpg.
"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "photos_src"
OUT = ROOT / "img"

# slug: (source file, crop box in fractions (left, top, right, bottom) or None)
PHOTOS = {
    "immeuble":       ("IMG_0009.jpeg", None),
    "sejour":         ("IMG_1941.png",  "bars"),
    "sejour-vue":     ("IMG_1948.jpeg", None),
    "cuisine":        ("IMG_1960.png",  "bars"),
    "cesca":          ("IMG_1961.jpeg", None),
    "chambre":        ("IMG_1963.png",  "bars"),
    "chambre-enfants":("IMG_1967.png",  "bars"),
    "sdb":            ("IMG_1971.jpeg", None),
    "sdb-vasque":     ("IMG_1972.jpeg", None),
    "sdb-douche":     ("IMG_1973.jpeg", None),
    "balcon":         ("IMG_1977.png",  "bars"),
    "balcon-facade":  ("IMG_1982.jpeg", None),
    "escalier":       ("IMG_3869.jpeg", None),
    "vallee":         ("IMG_7668.jpeg", None),
    "soir-fenetre":   ("IMG_8764.jpeg", None),
    "soir-balcon":    ("IMG_8767.jpeg", None),
    "soir-table":     ("IMG_8815.jpeg", None),
    "lampe-b":        ("IMG_8818.jpeg", None),
    "vallee-nuit":    ("IMG_8939.jpeg", None),
}


def trim_bars(im):
    """CosyHome PNG exports carry ~31 px black bands top and bottom."""
    w, h = im.size
    g = im.convert("L")

    def dark(y):
        return max(g.crop((0, y, w, y + 1)).resize((50, 1)).getdata()) < 25

    t, b = 0, h - 1
    while t < h // 6 and dark(t):
        t += 1
    while b > h - h // 6 and dark(b):
        b -= 1
    m = 4  # small safety margin
    return im.crop((m, t + m, w - m, b - m))


def main():
    OUT.mkdir(exist_ok=True)
    for slug, (name, crop) in PHOTOS.items():
        im = ImageOps.exif_transpose(Image.open(SRC / name)).convert("RGB")
        if crop == "bars":
            im = trim_bars(im)
        for size, q in ((1600, 80), (800, 76)):
            c = im.copy()
            c.thumbnail((size, size), Image.LANCZOS)
            c.save(OUT / f"{slug}-{size}.jpg", quality=q, optimize=True, progressive=True)
        print(slug, im.size)


if __name__ == "__main__":
    main()
