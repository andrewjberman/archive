"""Check whether any batch path is cited by live law/index surfaces.
Usage: law_citation_check.py <paths_file>"""
from __future__ import annotations
import sys
from pathlib import Path

WS = Path(r"C:\Users\AndrewBerman\Desktop\ajb_workspace")
MEM = Path(r"C:\Users\AndrewBerman\.claude\projects\C--Users-AndrewBerman-Desktop-ajb-workspace\memory")
surfaces = [WS / "CLAUDE.md", WS / "org" / "XXX.md"] + sorted(MEM.glob("*.md"))

paths = [x for x in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines() if x]
corpus: list[tuple[str, str]] = []
for s in surfaces:
    if s.exists():
        corpus.append((s.name, s.read_text(encoding="utf-8", errors="replace")))
print(f"[denominator] {len(paths)} batch paths x {len(corpus)} law/index surfaces")

hits = []
for p in paths:
    base = p.rsplit("/", 1)[-1]
    for name, text in corpus:
        if p in text or (len(base) > 12 and base in text):
            hits.append((p, name))
print(f"citations found: {len(hits)}")
for p, name in hits[:40]:
    print(f"  CITED {p}  <- {name}")
