"""CTO~B copy-check: for each batch path, does its exact blob survive at a
non-batch path in the given tree? Usage: copy_check.py <paths_file> [<treeish>]"""
from __future__ import annotations
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

WS = Path(r"C:\Users\AndrewBerman\Desktop\ajb_workspace")
paths_file = Path(sys.argv[1])
tree = sys.argv[2] if len(sys.argv) > 2 else "HEAD"

batch = set(x for x in paths_file.read_text(encoding="utf-8").splitlines() if x)
out = subprocess.run(["git", "ls-tree", "-r", "-z", tree],
                     cwd=WS, capture_output=True, text=True, encoding="utf-8")
if out.returncode != 0:
    sys.exit(f"git ls-tree rc={out.returncode}: {out.stderr[:300]}")

blob_of: dict[str, str] = {}
survivors_by_blob: dict[str, list[str]] = defaultdict(list)
n_entries = 0
for rec in out.stdout.split("\0"):
    if not rec:
        continue
    n_entries += 1
    meta, path = rec.split("\t", 1)
    blob = meta.split()[2]
    if path in batch:
        blob_of[path] = blob
    else:
        survivors_by_blob[blob].append(path)

missing = batch - set(blob_of)
copies = sum(1 for p, b in blob_of.items() if b in survivors_by_blob)
unique = len(blob_of) - copies
print(f"[denominator] tree {tree}: {n_entries} entries; batch {len(batch)} "
      f"(resolved {len(blob_of)}, missing-from-tree {len(missing)})")
print(f"copy-check: {copies} of {len(blob_of)} have a surviving identical copy elsewhere; "
      f"{unique} have NO surviving copy (unique content)")
for p in sorted(missing)[:5]:
    print(f"  MISSING from tree: {p}")
