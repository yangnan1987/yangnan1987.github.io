# -*- coding: utf-8 -*-
"""
Extract focal photo crops from PDF page composites (device/product shots only).
Strips ornate page borders — never publishes full flyer frames or text bands.
"""
import io
import sys
from pathlib import Path

try:
    import fitz
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymupdf", "-q"])
    import fitz

try:
    import numpy as np
    from PIL import Image
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "numpy", "-q"])
    import numpy as np
    from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "clinic-menu"
MAX_WIDTH = 640

FRAME_INSET = 0.14

# (left, top, right, bottom) relative to frame-stripped composite
FOCAL_REGIONS = {
    "device_only": (0.05, 0.22, 0.21, 0.41),
    "face_panel": (0.06, 0.32, 0.46, 0.50),
    "illustration": (0.18, 0.24, 0.82, 0.46),
    "iv_photo": (0.56, 0.10, 0.98, 0.40),
    "injection_photo": (0.06, 0.14, 0.94, 0.32),
    "portrait_photo": (0.52, 0.12, 0.98, 0.32),
    "nmn_photo": (0.05, 0.10, 0.48, 0.28),
}

TREATMENT_PAGES = {
    "picoway": (1, "device_only"),
    "ipl": (5, "device_only"),
    "gentlemax": (8, "device_only"),
    "dermapen": (10, "device_only"),
    "dds": (14, "device_only"),
    "hifu": (16, "device_only"),
    "massagepeel": (25, "device_only"),
    "electro": (28, "device_only"),
    "filler": (19, "injection_photo"),
    "botox": (22, "portrait_photo"),
    "drip": (31, "iv_photo"),
    "vc": (31, "iv_photo"),
    "nmn": (33, "nmn_photo"),
    "stemsup-drip": (31, "iv_photo"),
    "ortho": (35, "illustration"),
    "allergy": (37, "illustration"),
    "regen": (39, "device_only"),
}

HERO_PAGES = {
    "laser": (1, "device_only"),
    "skin": (10, "device_only"),
    "injection": (19, "injection_photo"),
    "drip": (31, "iv_photo"),
    "advanced": (33, "nmn_photo"),
}


def find_pdf():
    desk = Path(r"C:\Users\w\Desktop")
    pdfs = list(desk.glob("*.pdf"))
    if not pdfs:
        raise FileNotFoundError("No PDF on Desktop")
    return max(pdfs, key=lambda p: p.stat().st_size)


def page_composite(doc: fitz.Document, page_num: int) -> Image.Image:
    page = doc[page_num - 1]
    imgs = page.get_images(full=True)
    if not imgs:
        raise ValueError(f"No images on page {page_num}")
    xref = imgs[0][0]
    base = doc.extract_image(xref)
    return Image.open(io.BytesIO(base["image"])).convert("RGB")


def strip_outer_frame(im: Image.Image) -> Image.Image:
    w, h = im.size
    m = int(min(w, h) * FRAME_INSET)
    return im.crop((m, m, w - m, h - m))


def trim_near_white_borders(im: Image.Image, threshold: int = 32) -> Image.Image:
    arr = np.array(im.convert("RGB"))
    h, w, _ = arr.shape
    corners = np.array(
        [arr[0, 0], arr[0, w - 1], arr[h - 1, 0], arr[h - 1, w - 1]], dtype=np.float32
    )
    bg = corners.mean(axis=0)
    dist = np.sqrt(((arr.astype(np.float32) - bg) ** 2).sum(axis=2))
    mask = dist > threshold
    if not mask.any():
        return im
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    pad = 6
    y0 = max(0, int(rows[0]) - pad)
    y1 = min(h, int(rows[-1]) + pad + 1)
    x0 = max(0, int(cols[0]) - pad)
    x1 = min(w, int(cols[-1]) + pad + 1)
    return im.crop((x0, y0, x1, y1))


def strip_bottom_label_band(im: Image.Image, max_strip: float = 0.14) -> Image.Image:
    w, h = im.size
    arr = np.array(im.convert("RGB"))
    strip_h = max(12, int(h * max_strip))
    bottom = arr[h - strip_h : h]
    if bottom.std() > 40:
        return im.crop((0, 0, w, h - strip_h))
    return im


def refine_subject(crop: Image.Image, mode: str) -> Image.Image:
    """Drop title bands / logo type still inside regional crop."""
    w, h = crop.size
    if mode == "device_only":
        return crop.crop((0, 0, int(w * 0.82), h))
    if mode == "iv_photo":
        return crop.crop((0, int(h * 0.28), w, h))
    if mode == "injection_photo":
        return crop.crop((int(w * 0.04), int(h * 0.06), int(w * 0.96), int(h * 0.94)))
    if mode == "portrait_photo":
        return crop.crop((0, 0, int(w * 0.88), int(h * 0.92)))
    if mode == "nmn_photo":
        return crop.crop((0, int(h * 0.05), int(w * 0.92), int(h * 0.95)))
    if mode == "illustration":
        return crop.crop((int(w * 0.06), int(h * 0.06), int(w * 0.94), int(h * 0.88)))
    return crop


def focal_crop(im: Image.Image, mode: str) -> Image.Image:
    region = FOCAL_REGIONS.get(mode, FOCAL_REGIONS["device_only"])
    w, h = im.size
    l, t, r, b = region
    crop = im.crop((int(w * l), int(h * t), int(w * r), int(h * b)))
    crop = trim_near_white_borders(crop)
    crop = refine_subject(crop, mode)
    crop = trim_near_white_borders(crop)
    if mode == "face_panel":
        crop = strip_bottom_label_band(crop)
    return crop


def save_webp(im: Image.Image, dest: Path):
    if im.width > MAX_WIDTH:
        nh = int(im.height * MAX_WIDTH / im.width)
        im = im.resize((MAX_WIDTH, nh), Image.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=86, method=6)


def process_page(doc, page_num: int, mode: str) -> Image.Image:
    raw = page_composite(doc, page_num)
    trimmed = strip_outer_frame(raw)
    return focal_crop(trimmed, mode)


def main():
    pdf_path = find_pdf()
    doc = fitz.open(str(pdf_path))
    OUT.mkdir(parents=True, exist_ok=True)

    for tid, (pn, mode) in TREATMENT_PAGES.items():
        try:
            im = process_page(doc, pn, mode)
            save_webp(im, OUT / f"{tid}.webp")
            print("treatment", tid, im.size)
        except Exception as e:
            print("skip", tid, e)

    for slug, (pn, mode) in HERO_PAGES.items():
        try:
            im = process_page(doc, pn, mode)
            save_webp(im, OUT / f"hero-{slug}.webp")
            print("hero", slug, im.size)
        except Exception as e:
            print("skip hero", slug, e)

    doc.close()
    print("done ->", OUT)


if __name__ == "__main__":
    main()
