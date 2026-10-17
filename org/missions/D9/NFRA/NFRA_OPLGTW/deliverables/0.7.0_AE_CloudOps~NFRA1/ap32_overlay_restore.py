#!/usr/bin/env python
"""OG-ap-32 Phase B: restore the Phase A gate overlay (ap31_overlay.json) to the live ref's bytes, so the release tree is clean at the deploy.
usage: python ap31_overlay_restore.py <live_ref> <overlay.json>   (repository root; the tree is C:/tmp/og-rel-batch4)
Modified paths are rewritten from the live ref's blob (bytes, no newline translation); added paths are removed. No `checkout --` and no `clean` (the order forbids both)."""
import json
import os
import subprocess
import sys

TREE = "C:/tmp/og-rel-batch4"
LIVE, OVERLAY = sys.argv[1:3]
rows = json.load(open(OVERLAY, encoding="utf-8"))["laid"]
restored = removed = 0
for r in rows:
    full = os.path.join(TREE, r["path"])
    if r["status"] == "modified":
        b = subprocess.run(["git", "show", "%s:%s" % (LIVE, r["path"])], capture_output=True)
        if b.returncode != 0:
            raise SystemExit("live blob missing for a modified overlay path: " + r["path"])
        open(full, "wb").write(b.stdout)
        restored += 1
    else:
        if os.path.exists(full):
            os.remove(full)
            removed += 1
print("overlay restored: %d rewritten from the live ref, %d added files removed (of %d)" % (restored, removed, len(rows)))
