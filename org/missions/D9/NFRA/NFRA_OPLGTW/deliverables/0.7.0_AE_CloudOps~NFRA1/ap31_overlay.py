#!/usr/bin/env python
"""OG-ap-31 Phase A: lay the naming gate's INPUTS from trunk_sha into the release tree as an UNCOMMITTED working-tree overlay (the OG-ap-28 precedent: the live ref's
naming module and schema are an inconsistent pair -- lib/opal_naming.py reads cadence.interval_form, the live NAMING_SCHEMA.json lacks it -- so the commit-time gate cannot load).
usage: python ap31_overlay.py <live_ref> <trunk_sha> <out.json>   (repository root; the tree is C:/tmp/og-rel-batch3)
Only paths that differ live->trunk under the gate-input prefixes are written, with trunk bytes. Nothing here is committed; the release commit names its paths explicitly.
Phase B restores every overlay path to the live ref's bytes (git checkout of tracked paths, removal of the added ones) before the deploy tree's clean check."""
import json
import os
import subprocess
import sys

TREE = "C:/tmp/og-rel-batch3"
LIVE, TRUNK, OUT = sys.argv[1:4]
PREFIXES = (".tools/naming-", "infra/logic/", "lib/opal_naming", "org/standards/NAMING_SCHEMA.json", "org/missions/DIRECTIVES.yaml")


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True)


names = git("diff", "--name-status", "--no-renames", LIVE, TRUNK, "--", ".tools", "infra/logic", "lib", "org/standards", "org/missions/DIRECTIVES.yaml").stdout.decode().splitlines()
laid = []
for ln in names:
    st, _, p = ln.partition("\t")
    if not p.startswith(PREFIXES) or st not in ("A", "M"):
        continue
    b = git("show", "%s:%s" % (TRUNK, p)).stdout
    full = os.path.join(TREE, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "wb").write(b)
    laid.append({"path": p, "status": "added" if st == "A" else "modified"})
print("overlay: %d paths laid from trunk (%d added, %d modified)" % (len(laid), sum(1 for x in laid if x["status"] == "added"), sum(1 for x in laid if x["status"] == "modified")))
json.dump({"live": LIVE, "trunk": TRUNK, "laid": laid}, open(OUT, "w"), indent=1)
