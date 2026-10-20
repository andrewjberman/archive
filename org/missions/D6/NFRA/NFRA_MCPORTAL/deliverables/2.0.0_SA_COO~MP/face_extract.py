#!/usr/bin/env python3
"""face_extract.py -- write an order's WORKER FACE to its own file (OGW round 2, CTO point 4 / row Z-W42-S2).

A plain Read of a task order returns the RECORD FACE below the marker in the same result. The worker is handed the extract
file below instead and is told not to open the order. Usage: face_extract.py <order.md> [<out_dir>]
Writes <out_dir>/<TO id>.face.md (default org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/worker-faces/):
the order's lines from the first line down to, and excluding, the RECORD FACE marker. Refuses (rc 2) when the marker is absent
or when a line above it starts with a record-face-only token (**ISSUER NOTES, <status>). Prints the output path and its line count.
"""
import os
import sys

MARKER = "RECORD FACE"
BAD = ("**ISSUER NOTES", "<status>")  # matched at the START of a line only: the face may mention a tag in prose
DEFAULT_OUT = "org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/worker-faces"


def main(argv):
    if len(argv) < 2:
        print("usage: face_extract.py <order.md> [<out_dir>]")
        return 2
    src = argv[1]
    out_dir = argv[2] if len(argv) > 2 else DEFAULT_OUT
    with open(src, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    cut = next((i for i, ln in enumerate(lines) if MARKER in ln and ln.lstrip().startswith("<!--")), None)
    if cut is None:
        print("REFUSED: no '<!-- ... RECORD FACE ... -->' marker line in %s" % src)
        return 2
    face = lines[:cut]
    for ln in face:
        if any(ln.lstrip().startswith(tok) for tok in BAD):
            print("REFUSED: record-face token %r above the marker in %s" % ([t for t in BAD if ln.lstrip().startswith(t)][0], src))
            return 2
    name = os.path.basename(src)
    to_id = name.split(".md")[0].split(".")[0] + "." + name.split(".")[1] if name.count(".") >= 2 else name
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, to_id + ".face.md")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(face) + "\n")
    print("%s (%d lines of %d)" % (out.replace("\\", "/"), len(face), len(lines)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
