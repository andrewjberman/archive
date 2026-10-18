#!/usr/bin/env python
"""OG-ap-39 Phase A step 2: take the five files of the Z-S375 repair release into the release tree (bytes, no newline translation).
usage: python ap39_take.py <live_ref> <trunk_sha> <out.json>   (repository root; the tree is C:/tmp/og-rel-batch8)
WHOLE from trunk_sha: app/tools.py (OG-en-28, docstring lines only) and tests/test_og_db3.py (OG-en-27).
Prints the live->trunk hunk count per file; the hunks are attributed to the cells by ap38_attr.py. NOT taken: anything else."""
import json
import os
import subprocess
import sys

TREE = "C:/tmp/og-rel-batch8"
LIVE, TRUNK, OUT = sys.argv[1:4]
G = "infra/aws/ec2/opal-gateway/"
PATHS = [G + "app/tools.py", G + "tests/test_og_db3.py"]
taken = []
for p in PATHS:
    r = subprocess.run(["git", "show", "%s:%s" % (TRUNK, p)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("absent at trunk: " + p)
    full = os.path.join(TREE, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "wb").write(r.stdout)
    hunks = subprocess.run(["git", "diff", "-U0", LIVE, TRUNK, "--", p], capture_output=True).stdout.decode().count("\n@@ ") + subprocess.run(
        ["git", "diff", "-U0", LIVE, TRUNK, "--", p], capture_output=True).stdout.decode().startswith("@@ ")
    taken.append({"path": p, "bytes": len(r.stdout), "live_to_trunk_hunks": int(hunks)})
print("taken whole from trunk: %d" % len(taken))
for t in taken:
    print("  take %-52s %6d bytes, live->trunk hunks %s" % (t["path"].split("opal-gateway/")[1], t["bytes"], t["live_to_trunk_hunks"]))
json.dump({"taken": taken}, open(OUT, "w"), indent=1)
