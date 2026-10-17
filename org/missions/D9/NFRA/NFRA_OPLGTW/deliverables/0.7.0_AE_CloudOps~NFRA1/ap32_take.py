#!/usr/bin/env python
"""OG-ap-32 Phase A step 2: take the round-39 batch into the release tree (bytes, no newline translation).
usage: python ap31_take.py <trunk_sha> <out.json>   (repository root; the tree is C:/tmp/og-rel-batch4)
WHOLE from trunk_sha: the 4 app files (ap31_attr.json: 44 of 44 hunks attributed to the named orders, 0 unattributable) and the 13 test files named in the orders' <paths>.
NOT taken: anything else. No deploy script, no manifest."""
import json
import os
import subprocess
import sys

TREE = "C:/tmp/og-rel-batch4"
TRUNK, OUT = sys.argv[1:3]
G = "infra/aws/ec2/opal-gateway/"
APP = ["client_adapter_bd49f"]
TESTS = ["test_og_en17", "test_og_en15", "test_og_cl2"]
paths = [G + "app/%s.py" % m for m in APP] + [G + "app/refs/DATA_CATALOG.yaml"] + [G + "tests/%s.py" % t for t in TESTS]
taken = []
for p in paths:
    r = subprocess.run(["git", "show", "%s:%s" % (TRUNK, p)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("absent at trunk: " + p)
    full = os.path.join(TREE, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "wb").write(r.stdout)
    taken.append(p)
print("taken whole from trunk: %d (%d app, %d tests)" % (len(taken), len(APP), len(TESTS)))
json.dump({"taken": taken}, open(OUT, "w"), indent=1)
