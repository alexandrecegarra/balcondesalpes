"""Prepare web images from Alexandre's originals.

Originals are NOT kept in the repo (too heavy): put them in photos_src/
(same file names) and run:  python3 src/photos.py
Outputs img/<slug>-1600.jpg and img/<slug>-800.jpg.

No CosyHome watermark may appear on the site: their photos are either replaced
by Alexandre's own (photos_src/a-*) or cropped above the mark ("keep" = share of
the height kept from the top).
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "photos_src"
OUT = ROOT / "img"

# slug: (source file, options)
PHOTOS = {
    # CosyHome photos, cropped above the watermark
    "hero":           ("IMG_1977.png",  {"bars": True, "keep": 0.77}),
    "chambre":        ("IMG_1963.png",  {"bars": True, "keep": 0.84}),
    "sdb":            ("IMG_1971.jpeg", {"keep": 0.86}),
    "sdb-vasque":     ("IMG_1972.jpeg", {"keep": 0.87}),
    "sdb-douche":     ("IMG_1973.jpeg", {"keep": 0.86}),
    "balcon-facade":  ("IMG_1982.jpeg", {"keep": 0.86}),
    "string":         ("pdf-string.jpg", {"keep": 0.94}),
    # Alexandre's own photos
    "vallee":         ("IMG_7668.jpeg", {}),
    "soir-fenetre":   ("IMG_8764.jpeg", {}),
    "soir-balcon":    ("IMG_8767.jpeg", {}),
    "soir-table":     ("IMG_8815.jpeg", {}),
    "lampe-b":        ("IMG_8818.jpeg", {}),
    "vallee-nuit":    ("IMG_8939.jpeg", {}),
    "immeuble-hiver": ("pdf-immeuble-hiver.jpg", {}),
    "cheminee":       ("pdf-cheminee.jpg", {}),
    "toio":           ("pdf-toio.jpg", {}),
    "ete":            ("pdf-ete.jpg", {}),
    "automne":        ("pdf-automne.jpg", {}),
    "plan":           ("pdf-plan.jpg", {}),
    "facade-34":      ("a-facade-34.jpg", {}),
    "facade-ete":     ("a-facade-ete.jpg", {}),
    "hiver-balcon":   ("a-hiver-balcon.jpg", {}),
    "fenetre-hiver":  ("a-fenetre-hiver.jpg", {}),
    "crans-montana":  ("a-crans-montana.jpg", {}),
    "sejour-soleil":  ("a-sejour-soleil.jpg", {}),
    "table-vue":      ("a-table-vue.jpg", {}),
    "enfilade":       ("a-enfilade.jpg", {}),
    "bar-jour":       ("a-bar-jour.jpg", {}),
    "bar-nuit":       ("a-bar-nuit.jpg", {}),
    "parentesi":      ("a-parentesi.jpg", {}),
    "lits-1":         ("a-lits-1.jpg", {}),
    "lits-2":         ("a-lits-2.jpg", {}),
    "sejour-spider":  ("a-sejour-spider.png", {"bars": True}),
}

# privacy: blur number plates and a passer-by (pixel boxes on the source image)
BLUR = {
    "immeuble-hiver": [(540, 990, 650, 1045), (1820, 960, 1910, 1005), (1960, 930, 2090, 1040)],
}


def trim_bars(im):
    """Remove black bands (CosyHome exports top/bottom, iPhone screenshots left/right)."""
    w, h = im.size
    g = im.convert("L")

    def dark_row(y):
        return max(g.crop((0, y, w, y + 1)).resize((50, 1)).getdata()) < 25

    def dark_col(x):
        return max(g.crop((x, 0, x + 1, h)).resize((1, 50)).getdata()) < 25

    t, b, l, r = 0, h - 1, 0, w - 1
    while t < h // 6 and dark_row(t):
        t += 1
    while b > h - h // 6 and dark_row(b):
        b -= 1
    while l < w // 6 and dark_col(l):
        l += 1
    while r > w - w // 6 and dark_col(r):
        r -= 1
    m = 4  # small safety margin
    return im.crop((l + (m if l else 0), t + (m if t else 0), r + 1 - (m if r < w - 1 else 0), b + 1 - (m if b < h - 1 else 0)))


def main():
    OUT.mkdir(exist_ok=True)
    for slug, (name, opt) in PHOTOS.items():
        im = ImageOps.exif_transpose(Image.open(SRC / name)).convert("RGB")
        for box in BLUR.get(slug, []):
            im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(14)), box[:2])
        if opt.get("bars"):
            im = trim_bars(im)
        if "keep" in opt:
            im = im.crop((0, 0, im.width, int(im.height * opt["keep"])))
        for size, q in ((1600, 80), (800, 76)):
            c = im.copy()
            c.thumbnail((size, size), Image.LANCZOS)
            c.save(OUT / f"{slug}-{size}.jpg", quality=q, optimize=True, progressive=True)
        print(slug, im.size)


if __name__ == "__main__":
    main()
