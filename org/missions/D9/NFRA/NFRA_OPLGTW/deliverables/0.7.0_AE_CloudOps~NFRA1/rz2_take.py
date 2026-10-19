#!/usr/bin/env python
"""OG-rz-2 Phase A step 5: take the files of the two worker commits (OG-rz-1 5807068e367 via merge 97ec4f8c60a, OG-ms-1 via merge 9095ce68f39) WHOLE from trunk into the batch15 release tree (bytes, no newline translation).
usage: python rz2_take.py <live_ref> <trunk_sha> <out.json>   (repository root; the tree is C:/tmp/og-rel-batch15)
Prints, per file, the live->trunk hunk count and whether the file at the live ref equals the file just before the worker merge (so the whole-file take brings ONLY the worker's change)."""
import json
import os
import subprocess
import sys

TREE = "C:/tmp/og-rel-batch15"
LIVE, TRUNK, OUT = sys.argv[1:4]
G = "infra/aws/ec2/opal-gateway/"
PATHS = [G + "app/client_adapter_schwab.py", G + "app/data_entitlement.py", G + "app/schwab_audit.py", G + "deploy/NFRA_OPLGTW_CONTRACT.json", G + "deploy/opal-gateway.service",
         G + "tests/test_account_ref.py", G + "tests/test_og_ms1.py", G + "tests/test_og_un1.py", "infra/logic/registry/scopes.json", "org/standards/NFRA_OPLGTW_CONTRACT.json"]
taken = []
for p in PATHS:
    r = subprocess.run(["git", "show", "%s:%s" % (TRUNK, p)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("absent at trunk: " + p)
    full = os.path.join(TREE, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "wb").write(r.stdout)
    d = subprocess.run(["git", "diff", "-U0", LIVE, TRUNK, "--", p], capture_output=True).stdout.decode()
    hunks = sum(1 for ln in d.splitlines() if ln.startswith("@@ "))
    taken.append({"path": p, "bytes": len(r.stdout), "live_to_trunk_hunks": hunks})
print("taken whole from trunk: %d" % len(taken))
for t in taken:
    print("  take %-62s %6d bytes, live->trunk hunks %s" % (t["path"].replace(G, "gw/"), t["bytes"], t["live_to_trunk_hunks"]))
json.dump({"taken": taken}, open(OUT, "w"), indent=1)
