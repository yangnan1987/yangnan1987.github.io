# -*- coding: utf-8 -*-
"""Debug: list images per PDF page with bbox and size."""
import sys
from pathlib import Path

import fitz

desk = Path(r"C:\Users\w\Desktop")
pdf = max(desk.glob("*.pdf"), key=lambda p: p.stat().st_size)
doc = fitz.open(str(pdf))
for pn in [0, 1, 9, 18]:
    page = doc[pn]
    print(f"\n=== page {pn+1} ===")
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if b.get("type") != 1:
            continue
        x0, y0, x1, y1 = b["bbox"]
        w, h = x1 - x0, y1 - y0
        print(f"  bbox {w:.0f}x{h:.0f} at ({x0:.0f},{y0:.0f})")
    for i, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base = doc.extract_image(xref)
        print(f"  xref {xref}: {base['width']}x{base['height']} ext={base['ext']}")
doc.close()
