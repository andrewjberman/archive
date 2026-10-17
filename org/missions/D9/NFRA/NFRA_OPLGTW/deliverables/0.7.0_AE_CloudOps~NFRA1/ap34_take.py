#!/usr/bin/env python
"""OG-ap-34 Phase A step 2: take the round-39 batch into the release tree (bytes, no newline translation).
usage: python ap34_take.py <trunk_sha> <out.json>   (repository root; the tree is C:/tmp/og-rel-batch5)
WHOLE from trunk_sha: the 4 app files (ap34_attr.json: 44 of 44 hunks attributed to the named orders, 0 unattributable) and the 13 test files named in the orders' <paths>.
NOT taken: anything else. No deploy script, no manifest."""
import json
import os
import subprocess
import sys

TREE = "C:/tmp/og-rel-batch5"
TRUNK, OUT = sys.argv[1:3]
LIVE = "d3ae88be463d88c6f4ea22fb297659bf44f43758"
G = "infra/aws/ec2/opal-gateway/"
APP = ["client_adapter_bd49f"]
TESTS = ["test_og_en13", "test_og_en15", "test_og_en17", "test_og_en18", "test_og_en19", "test_og_en20", "test_og_cl2"]
paths = [G + "app/%s.py" % m for m in APP] + [G + "app/refs/DATA_CATALOG.yaml"] + [G + "tests/%s.py" % t for t in TESTS]
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
