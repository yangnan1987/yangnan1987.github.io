# -*- coding: utf-8 -*-
"""
INTERNAL ONLY — do not commit output.

Extracts desktop PDF pages to _local/ for staff reference when updating
beauty-menu-data.yaml. Never deploy these images to the public site.
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
    from PIL import Image
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
    from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT_PAGES = ROOT / "_local" / "pdf-reference" / "pages"
OUT_FIGURES = ROOT / "_local" / "pdf-reference" / "figures"
MAX_WIDTH = 1400
WEBP_QUALITY = 82


def find_pdf():
    desk = Path(r"C:\Users\w\Desktop")
    pdfs = list(desk.glob("*.pdf"))
    if not pdfs:
        raise FileNotFoundError("No PDF on Desktop")
    return max(pdfs, key=lambda p: p.stat().st_size)


def save_webp(pix, dest: Path):
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    if img.width > MAX_WIDTH:
        h = int(img.height * MAX_WIDTH / img.width)
        img = img.resize((MAX_WIDTH, h), Image.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "WEBP", quality=WEBP_QUALITY, method=6)


def main():
    pdf_path = find_pdf()
    OUT_PAGES.mkdir(parents=True, exist_ok=True)
    OUT_FIGURES.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf_path))
    scale = MAX_WIDTH / doc[0].rect.width if doc.page_count else 2.0
    mat = fitz.Matrix(scale, scale)
    fig_idx = 0
    for i in range(doc.page_count):
        page = doc[i]
        pix = page.get_pixmap(matrix=mat, alpha=False)
        save_webp(pix, OUT_PAGES / f"p{i+1:02d}.webp")
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            try:
                base = doc.extract_image(xref)
                if base["width"] < 120 or base["height"] < 120:
                    continue
                fig_idx += 1
                raw = base["image"]
                im = Image.open(io.BytesIO(raw))
                if im.mode in ("RGBA", "P"):
                    im = im.convert("RGBA")
                else:
                    im = im.convert("RGB")
                w = min(800, im.width)
                h = int(im.height * w / im.width)
                im = im.resize((w, h), Image.LANCZOS)
                out = OUT_FIGURES / f"p{i+1:02d}_fig{fig_idx}.webp"
                im.save(out, "WEBP", quality=82)
            except Exception:
                pass
    n = len(list(OUT_PAGES.glob("*.webp")))
    doc.close()
    print(f"Wrote {n} pages to {OUT_PAGES} (local reference only)")


if __name__ == "__main__":
    main()
