"""Home-screen icon: square crop of Alexandre's balcony photo (eave beams, snowy peaks, railing).
Needs photos_src/a-balcon-crate.jpg. Run: python3 src/icon.py"""
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

im = ImageOps.exif_transpose(Image.open(ROOT / "photos_src/a-balcon-crate.jpg")).convert("RGB")
W, H = im.size
side = int(W * 0.62)
x, y = int(W * 0.30), int(H * 0.17)
c = im.crop((x, y, x + side, y + side)).resize((1024, 1024), Image.LANCZOS)
c = ImageEnhance.Contrast(c).enhance(1.08)
c = ImageEnhance.Color(c).enhance(1.10)
for name, s in (("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)):
    c.resize((s, s), Image.LANCZOS).save(ROOT / name, optimize=True)
