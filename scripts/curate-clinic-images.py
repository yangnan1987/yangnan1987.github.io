# -*- coding: utf-8 -*-
"""
Copy curated device/illustration crops from local PDF extract into assets/clinic-menu/.
Uses embedded figures only (not full proposal pages). Run after extract-pdf-local-reference.py.
"""
import shutil
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
    from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "_local" / "pdf-reference" / "figures"
OUT = ROOT / "assets" / "clinic-menu"
MAX_WIDTH = 720

# treatment id -> source figure filename
TREATMENT_SOURCES = {
    "picoway": "p01_fig1.webp",
    "ipl": "p05_fig5.webp",
    "gentlemax": "p08_fig10.webp",
    "dermapen": "p10_fig13.webp",
    "dds": "p14_fig20.webp",
    "hifu": "p16_fig23.webp",
    "massagepeel": "p25_fig35.webp",
    "electro": "p28_fig38.webp",
    "filler": "p20_fig28.webp",
    "botox": "p22_fig32.webp",
    "drip": "p31_fig41.webp",
    "vc": "p32_fig42.webp",
    "nmn": "p33_fig43.webp",
    "stemsup-drip": "p34_fig44.webp",
    "ortho": "p35_fig45.webp",
    "allergy": "p37_fig48.webp",
    "regen": "p39_fig50.webp",
}

# page html file -> hero banner source
HERO_SOURCES = {
    "premium-medical-beauty-laser.html": "p02_fig2.webp",
    "premium-medical-beauty-skin.html": "p13_fig18.webp",
    "premium-medical-beauty-injection.html": "p19_fig27.webp",
    "premium-medical-beauty-drip.html": "p33_fig43.webp",
    "premium-medical-beauty-advanced.html": "p36_fig46.webp",
}


def save_optimized(src: Path, dest: Path):
    im = Image.open(src)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGBA")
    else:
        im = im.convert("RGB")
    if im.width > MAX_WIDTH:
        h = int(im.height * MAX_WIDTH / im.width)
        im = im.resize((MAX_WIDTH, h), Image.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=85, method=6)


def main():
    if not SRC.is_dir():
        raise SystemExit(f"Run extract-pdf-local-reference.py first. Missing {SRC}")
    OUT.mkdir(parents=True, exist_ok=True)
    for tid, fname in TREATMENT_SOURCES.items():
        src = SRC / fname
        if not src.exists():
            print("skip missing", fname)
            continue
        dest = OUT / f"{tid}.webp"
        save_optimized(src, dest)
        print("treatment", dest.name)
    for page, fname in HERO_SOURCES.items():
        slug = page.replace("premium-medical-beauty-", "").replace(".html", "")
        src = SRC / fname
        if not src.exists():
            continue
        dest = OUT / f"hero-{slug}.webp"
        save_optimized(src, dest)
        print("hero", dest.name)
    print("done ->", OUT)


if __name__ == "__main__":
    main()
