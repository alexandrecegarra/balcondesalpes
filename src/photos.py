"""Prepare web images from Alexandre's originals.

Originals are NOT kept in the repo (too heavy): put them in photos_src/
(same file names) and run:  python3 src/photos.py
Outputs img/<slug>-1600.jpg and img/<slug>-800.jpg.

No CosyHome photo may appear on the site: only Alexandre's own photos
(photos_src/a-*, IMG_*, pdf-*). "keep" (share of height kept from the top) and
"bars" remain available for cropping.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "photos_src"
OUT = ROOT / "img"

# slug: (source file, options)
PHOTOS = {
    # all photos are Alexandre's own (no CosyHome image on the site)
    "hero":           ("a-balcon-crate.jpg", {}),
    "vallee":         ("IMG_7668.jpeg", {}),
    "soir-fenetre":   ("IMG_8764.jpeg", {}),
    "soir-balcon":    ("IMG_8767.jpeg", {}),
    "soir-table":     ("IMG_8815.jpeg", {}),
    "lampe-b":        ("IMG_8818.jpeg", {}),
    "vallee-nuit":    ("IMG_8939.jpeg", {}),
    "immeuble-hiver": ("pdf-immeuble-hiver.jpg", {}),
    "toio":           ("pdf-toio.jpg", {}),
    "cheminee":       ("pdf-cheminee.jpg", {}),
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
    "sejour-spider":  ("a-sejour-spider.png", {"bars": True}),
    "cheminee-soleil":("a-cheminee-soleil.jpg", {}),
    "lucca-string":   ("a-lucca-string.jpg", {}),
    "bouilloire":     ("a-bouilloire.jpg", {}),
    "chambre-soleil": ("a-chambre-soleil.jpg", {}),
    "chambre-nuit":   ("a-chambre-nuit.jpg", {}),
    "coin-cesca":     ("a-coin-cesca.jpg", {}),
    "lits-portrait":  ("a-lits-portrait.jpg", {}),
    "lits-mouton":    ("a-lits-mouton.jpg", {}),
    "lits-lattes":    ("a-lits-lattes.jpg", {}),
    "sdb-large":      ("a-sdb-large.jpg", {}),
    "vasque-nuit":    ("a-vasque-nuit.jpg", {}),
    "vallee-voile":   ("a-vallee-voile.jpg", {}),
    "sommets-soir":   ("a-sommets-soir.jpg", {}),
    "lune":           ("a-lune.jpg", {}),
    "hiver-soleil":   ("a-hiver-soleil.jpg", {}),
}

# full-bleed photos shown edge to edge between chapters: also exported at 2400 px
PLATES = {"hero", "cheminee-soleil", "vallee-voile", "lucca-string", "lune", "hiver-soleil"}

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
        sizes = ((2400, 78), (1600, 80), (800, 76)) if slug in PLATES else ((1600, 80), (800, 76))
        for size, q in sizes:
            c = im.copy()
            c.thumbnail((size, size), Image.LANCZOS)
            c.save(OUT / f"{slug}-{size}.jpg", quality=q, optimize=True, progressive=True)
        print(slug, im.size)


if __name__ == "__main__":
    main()
