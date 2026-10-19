#!/usr/bin/env python
"""OG-ap-46 Phase A step 2: take the two files of the tenth release into the release tree (bytes, no newline translation).
usage: python ap46_take.py <live_ref> <trunk_sha> <out.json>   (repository root; the tree is C:/tmp/og-rel-batch12)
WHOLE from trunk_sha: app/family_depth.py, app/refs/silver_families.json, tests/test_og_cd1.py (OG-cd-1, on trunk and in no release) and app/probe_listener.py (the OG-en-34 comment). The optional MP pair (app/admin_people_access.py + tests/test_admin_people_access.py) only with --mp.
Prints the live->trunk hunk count per file; the hunks are attributed to the cells by ap38_attr.py. NOT taken: anything else."""
import json
import os
import subprocess
import sys

TREE = "C:/tmp/og-rel-batch12"
LIVE, TRUNK, OUT = [a for a in sys.argv[1:] if not a.startswith("--")][:3]
G = "infra/aws/ec2/opal-gateway/"
PATHS = [G + "app/family_depth.py", G + "app/refs/silver_families.json", G + "tests/test_og_cd1.py", G + "app/probe_listener.py"]
if "--mp" in sys.argv:
    PATHS += [G + "app/admin_people_access.py", G + "tests/test_admin_people_access.py"]
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
