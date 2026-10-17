#!/usr/bin/env python
"""OG-ap-36 Phase A step 2: attribute EACH hunk of app/tools.py (live ref -> trunk_sha) to OG-en-21, to the POSITION MOVE of harvest_get_published_analysis (OG-ap-33), or to
the live ref's own (none expected); an unattributable hunk is a STOP. Also checks the seam to destructive_ops.py (not taken): its live->trunk difference is one reordered line.
usage: python ap36_attr.py <live_ref> <trunk_sha> <out.json>   (repository root; read-only)"""
from __future__ import annotations

import collections
import json
import re
import subprocess
import sys

LIVE, TRUNK, OUT = sys.argv[1:4]
G = "infra/aws/ec2/opal-gateway/"
F = G + "app/tools.py"
NAMED = re.compile(r"OG-en-21\b")


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True).stdout.decode("utf-8", "replace")


def changed(patch):
    return {ln.rstrip("\r") for ln in patch.split("\n") if (ln.startswith("+") or ln.startswith("-")) and not ln.startswith(("+++", "---"))}


hunks, cur = [], None
for ln in git("diff", "-U0", LIVE, TRUNK, "--", F).split("\n"):
    if ln.startswith("@@"):
        cur = {"head": ln.split("@@")[1].strip(), "plus": [], "minus": []}
        hunks.append(cur)
    elif cur is not None and ln.startswith("+") and not ln.startswith("+++"):
        cur["plus"].append(ln[1:].rstrip("\r"))
    elif cur is not None and ln.startswith("-") and not ln.startswith("---"):
        cur["minus"].append(ln[1:].rstrip("\r"))
named = [(h, s) for h, _, s in (x.partition("\t") for x in git("log", "--no-merges", "--format=%H\t%s", "%s..%s" % (LIVE, TRUNK), "--", F).splitlines()) if NAMED.search(s)]
covered = set()
for h, _s in named:
    covered |= changed(git("show", "-U0", "--format=", h, "--", F))
allplus = collections.Counter(p for h in hunks for p in h["plus"])
allminus = collections.Counter(m for h in hunks for m in h["minus"])
rows = []
for h in hunks:
    lines = {"+" + p for p in h["plus"]} | {"-" + m for m in h["minus"]}
    if lines <= covered:
        who = "OG-en-21"
    elif all(allminus[p] and allplus[p] for p in h["plus"] if p.strip()) and all(allplus[m] and allminus[m] for m in h["minus"] if m.strip()):
        who = "position move (the same lines leave one hunk and arrive in another)"
    else:
        who = "UNATTRIBUTABLE"
    rows.append({"hunk": h["head"], "plus": len(h["plus"]), "minus": len(h["minus"]), "attributed_to": who})
    print("  hunk %-18s +%-3d -%-3d -> %s" % (h["head"], len(h["plus"]), len(h["minus"]), who))
# the whole-file multiset check: no live line is lost, no trunk line is unexplained
live_lines = collections.Counter(git("show", "%s:%s" % (LIVE, F)).split("\n"))
trunk_lines = collections.Counter(git("show", "%s:%s" % (TRUNK, F)).split("\n"))
lost_from_live = sum((live_lines - trunk_lines).values())
only_trunk = sum((trunk_lines - live_lines).values())
t = git("show", "%s:%s" % (TRUNK, F))
once = {"import harvest_published": len(re.findall(r"^from \. import harvest_published as _hvpub", t, re.M)),
        "def harvest_get_published_analysis": len(re.findall(r"^(?:async )?def harvest_get_published_analysis\(", t, re.M))}
d_live, d_trunk = collections.Counter(git("show", "%s:%sapp/destructive_ops.py" % (LIVE, G)).split("\n")), collections.Counter(git("show", "%s:%sapp/destructive_ops.py" % (TRUNK, G)).split("\n"))
dest_same_multiset = d_live == d_trunk
print("tools.py: %d hunks, %d attributed, %d unattributable; live lines absent from trunk's (multiset) %d; trunk lines not in live's %d; names once: %s" % (
    len(rows), sum(1 for r in rows if r["attributed_to"] != "UNATTRIBUTABLE"), sum(1 for r in rows if r["attributed_to"] == "UNATTRIBUTABLE"), lost_from_live, only_trunk, once))
print("destructive_ops.py (seam, not taken): live and trunk hold the same lines as a multiset: %s" % dest_same_multiset)
json.dump({"live": LIVE, "trunk": TRUNK, "named_commits": [[h[:10], s[:70]] for h, s in named], "hunks": rows, "live_lines_absent_from_trunk": lost_from_live, "trunk_lines_not_in_live": only_trunk,
           "names_once": once, "destructive_ops_same_lines_as_multiset": dest_same_multiset}, open(OUT, "w"), indent=1)
