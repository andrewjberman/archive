"""AMGT_RESAPP round 44, AMGT-rs-3 AC1 -- the four-input trace is COMPLETE and every citation RESOLVES.
Reads deliverables/0.9.0_WK_AMGT_RESAPP~162/FOUR_INPUTS_TRACE.json: exactly the four inputs of the round-42/43 analyses (spans,
unit_sign, social_chatter, universe), each carrying producer (path:line), commit, owner_project, write_surface, served_evidence and
proposed_cell; each producer path must exist at its cited commit and the line must fall inside it.
usage (repo root): python <this>"""
import json
import subprocess
import sys
from pathlib import Path

P = Path("org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~162/FOUR_INPUTS_TRACE.json")
WANT = {"spans", "unit_sign", "social_chatter", "universe"}
FIELDS = ("producer", "commit", "owner_project", "write_surface", "served_evidence", "proposed_cell")
if not P.exists():
    print("FAIL: no trace at %s" % P)
    sys.exit(1)
rows = json.loads(P.read_text(encoding="utf-8")).get("inputs") or []
seen, bad = set(), []
for r in rows:
    iid = r.get("input")
    seen.add(iid)
    for f in FIELDS:
        if not str(r.get(f) or "").strip():
            bad.append("%s: %s empty" % (iid, f))
    prod = str(r.get("producer") or "")
    if ":" in prod:
        path, _, line = prod.rpartition(":")
        blob = subprocess.run(["git", "show", "%s:%s" % (r.get("commit"), path)], capture_output=True)
        first = line.split("-")[0]
        if blob.returncode != 0:
            bad.append("%s: %s does not exist at %s" % (iid, path, r.get("commit")))
        elif not first.isdigit() or int(first) > blob.stdout.count(b"\n") + 1:
            bad.append("%s: line %s beyond %s at %s" % (iid, line, path, r.get("commit")))
    else:
        bad.append("%s: producer carries no path:line" % iid)
print("inputs traced: %d of %d; missing %s; extra %s; citation defects %d" % (
    len(seen & WANT), len(WANT), sorted(WANT - seen), sorted(seen - WANT), len(bad)))
for b in bad[:12]:
    print("  " + b)
sys.exit(0 if seen == WANT and not bad else 1)
