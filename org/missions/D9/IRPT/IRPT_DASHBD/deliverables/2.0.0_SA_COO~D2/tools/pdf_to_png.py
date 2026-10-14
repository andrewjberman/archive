"""pdf_to_png.py -- rasterise every page of a PDF to a PNG so the page can be READ as an image (the Read tool refuses a PDF on this box).

Usage: python -I pdf_to_png.py <pdf> <out_dir> [dpi]     (dpi defaults to 70: a letter page is about 600 x 780 px, readable and small)
Writes <out_dir>/page_01.png ... and prints one line per page: "page N <bytes>" then "PAGES <n>". Reads the PDF, writes only into <out_dir>.
The library (pymupdf) is installed in the private folder C:/dev/_irpt_private_evidence_20261009/_pylib, outside the repo.
"""
import sys
sys.path.insert(0, "C:/dev/_irpt_private_evidence_20261009/_pylib")
import os
import fitz

pdf, out = sys.argv[1], sys.argv[2]
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 70
os.makedirs(out, exist_ok=True)
doc = fitz.open(pdf)
for i, page in enumerate(doc, 1):
    p = os.path.join(out, "page_%02d.png" % i)
    page.get_pixmap(dpi=dpi).save(p)
    print("page", i, os.path.getsize(p))
print("PAGES", len(doc))
