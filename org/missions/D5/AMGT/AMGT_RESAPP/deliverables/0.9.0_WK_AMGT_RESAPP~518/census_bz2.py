"""Census for the AMGT-bz-2 receipt: the Management section of the PDF and of the rich export, at base 8e81e269f7 and at HEAD,
for the eight round-119 served fixtures. Scratch only; reads the fixtures and the two renderer modules, writes nothing to the repo."""
import copy
import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(os.getcwd())
sys.path.insert(0, str(ROOT))
import pymupdf  # noqa: E402
from lib.research.print import render_pack as head_rp  # noqa: E402

BASE_PATH = ROOT / "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~518/base_8e81e269f7/render_pack.py"
spec = importlib.util.spec_from_file_location("base_render_pack_8e81", str(BASE_PATH))
base_rp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base_rp)
# the base snapshot sits outside lib/research/print, so its FONT_DIR (computed from its own __file__) is pointed at the HEAD fonts
base_rp.FONT_DIR = head_rp.FONT_DIR

FIX = ROOT / "lib/research/print/tests/fixtures"
NAMES = ["RIO_LN", "ICT_PM", "GOOGL_US", "ICICIBC_IN", "HD_US", "BA_US", "KMB_US", "TSM_US"]
RUN = "2026-10-18"


def bundle_of(name):
    return json.loads((FIX / ("bz_served_thesis_%s.json" % name)).read_text(encoding="utf-8"))


def block_of(bundle):
    key = bundle["security_key"]
    return {"security": key.replace("_", " "), "security_key": key, "figures": copy.deepcopy(bundle["header_figures"])}


def pdf_mgmt(pdf_path):
    doc = pymupdf.open(str(pdf_path))
    try:
        text = "\n".join(page.get_text() for page in doc)
    finally:
        doc.close()
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    start = lines.index("Management") + 1
    return lines[start:lines.index("Positioning", start)]


def md_mgmt(md_path):
    lines = Path(md_path).read_text(encoding="utf-8").split("\n")
    start = lines.index("## Management/Board") + 1
    end = next(i for i in range(start, len(lines)) if lines[i].startswith("## "))
    return [ln for ln in lines[start:end] if ln.strip()]


def run(mod, name, label):
    bundle = bundle_of(name)
    block = block_of(bundle)
    tmp = Path(tempfile.mkdtemp(prefix="bz2_%s_%s_" % (label, name)))
    pdf_path, _txt = mod.build_pack(block["security"], block, out_dir=tmp / "pdf", run_date=RUN, thesis_bundle=bundle)
    md_path = mod.build_rich_text(block["security"], block, thesis_bundle=bundle, out_dir=tmp / "md")
    return pdf_mgmt(pdf_path), md_mgmt(md_path)


if __name__ == "__main__":
    out = {}
    for name in NAMES:
        bp, bm = run(base_rp, name, "base")
        hp, hm = run(head_rp, name, "head")
        out[name] = {"base_pdf": bp, "base_rich": bm, "head_pdf": hp, "head_rich": hm}
    dest = ROOT / ".scratch" / "census_bz2.json"
    dest.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    for name in NAMES:
        o = out[name]
        def ceo(lines):
            return [ln for ln in lines if "CEO public" in ln or "could not be read" in ln or "no public profile" in ln or "UNREADABLE" in ln]

        print("== %s" % name)
        print("  base PDF lines=%d  base RICH lines=%d  head PDF lines=%d  head RICH lines=%d" % (
            len(o["base_pdf"]), len(o["base_rich"]), len(o["head_pdf"]), len(o["head_rich"])))
        print("  base PDF == head PDF: %s" % (o["base_pdf"] == o["head_pdf"]))
        print("  base PDF CEO/passage-key lines: %r" % ceo(o["base_pdf"]))
        print("  base RICH CEO lines: %r" % ceo(o["base_rich"]))
        print("  head RICH CEO lines: %r" % ceo(o["head_rich"]))
        print("  head RICH CEO/absence lines (count of 'could not be read'): %d" % sum("could not be read" in ln for ln in o["head_rich"]))
