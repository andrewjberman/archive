#!/usr/bin/env python
"""OG-ap-36 Phase A step 2: take the round-39 batch into the release tree (bytes, no newline translation).
usage: python ap36_take.py <trunk_sha> <out.json>   (repository root; the tree is C:/tmp/og-rel-batch6)
WHOLE from trunk_sha: the 4 app files (ap36_attr.json: 44 of 44 hunks attributed to the named orders, 0 unattributable) and the 13 test files named in the orders' <paths>.
NOT taken: anything else. No deploy script, no manifest."""
import json
import os
import subprocess
import sys

TREE = "C:/tmp/og-rel-batch6"
TRUNK, OUT = sys.argv[1:3]
LIVE = "9d5b7125571520b977401634a01935924f4c9787"
G = "infra/aws/ec2/opal-gateway/"
APP = ["tools", "client_core", "client_adapter_bd49f"]
TESTS = ["test_og_en21", "test_og_en22", "test_og_en23", "test_og_db3"]
paths = [G + "app/%s.py" % m for m in APP] + [G + "deploy-to-ec2.sh"] + [G + "tests/%s.py" % t for t in TESTS]
taken, skipped = [], []
for p in paths:
    r = subprocess.run(["git", "show", "%s:%s" % (TRUNK, p)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("absent at trunk: " + p)
    live = subprocess.run(["git", "show", "%s:%s" % (LIVE, p)], capture_output=True)
    if p.endswith(tuple("%s.py" % t for t in TESTS)) and live.returncode == 0 and live.stdout == r.stdout:
        skipped.append(p)
        continue
    full = os.path.join(TREE, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "wb").write(r.stdout)
    taken.append(p)
print("taken whole from trunk: %d; test files equal to the live ref, not taken: %d" % (len(taken), len(skipped)))
for t in taken:
    print("  take", t.split("opal-gateway/")[1])
json.dump({"taken": taken, "tests_equal_to_live_not_taken": skipped}, open(OUT, "w"), indent=1)
