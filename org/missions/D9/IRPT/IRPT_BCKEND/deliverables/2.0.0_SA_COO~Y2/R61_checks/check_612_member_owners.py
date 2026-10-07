#!/usr/bin/env python3
"""E-Y2 / cell IB-yr-612: every unclaimed changed member of irpt-ycharts-generate has an owner.

Reads the owner table (default: the worker's deliverable, or --file <path>) and checks:
  - it lists EXACTLY the 15 members below, once each (the riders of the r57 census not claimed by an order);
  - each entry's "owner_lane" is a lane in .owned-paths.yaml, or the entry's "disposition" is "REMOVE";
  - each entry's "evidence_commit" exists and touched that member's repo path;
  - a member in 2.0.0_SA_COO~G2's one-writer set (CTO~DELL2 msg 91) is owned by 2.0.0_SA_COO~G2.
Prints PASS or FAIL lines. ASCII only.
"""
import json
import subprocess
import sys

import yaml

SRC = "infra/aws/lambda/investor-reporting/ycharts/generate/"
MEMBERS = sorted(["fixtures/har/" + n for n in (
    "FIXTURE_MANIFEST.json", "collection.json", "create_201.json", "create_422_fee.json", "dashboard.json",
    "decision_branches.json", "generate_201.json", "generate_404_minimal.json", "report.pdf", "status_drifted.json",
    "status_ok.json", "templates.json", "upload_ok.json", "validate_200.json")] + ["templates.json"])
G2_SET = {"resident_worker.py", "upload_suggestions.py", "security_resolution.py"}
DEFAULT = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~150/MEMBER_OWNERS.json"


def main(argv):
    path = argv[argv.index("--file") + 1] if "--file" in argv else DEFAULT
    fails = []
    try:
        rows = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("FAIL: owner table unreadable at %s (%s)" % (path, type(exc).__name__))
        return 1
    lanes = set(yaml.safe_load(open(".owned-paths.yaml", encoding="utf-8"))["lanes"])
    listed = sorted(r.get("member", "") for r in rows)
    if listed != MEMBERS:
        fails.append("member set differs: missing %s, extra %s" % (
            sorted(set(MEMBERS) - set(listed)), sorted(set(listed) - set(MEMBERS))))
    for r in rows:
        m = r.get("member", "")
        if r.get("disposition") != "REMOVE" and r.get("owner_lane") not in lanes:
            fails.append("%s: owner_lane %r is not a lane in .owned-paths.yaml" % (m, r.get("owner_lane")))
        if m in G2_SET and "2.0.0_SA_COO~G2" not in r.get("owner_serials", []):
            fails.append("%s: in the one-writer set of 2.0.0_SA_COO~G2 but not owned by it" % m)
        c = r.get("evidence_commit", "")
        touched = subprocess.run(["git", "show", "--name-only", "--format=", c or "NONE", "--", SRC + m],
                                 capture_output=True, text=True)
        if touched.returncode != 0 or (SRC + m) not in touched.stdout.split("\n"):
            fails.append("%s: evidence_commit %r did not touch %s" % (m, c, SRC + m))
    for f in fails:
        print("FAIL: " + f)
    if fails:
        print("FAIL: %d problem(s) across %d row(s)" % (len(fails), len(rows)))
        return 1
    print("PASS: %d of %d members owned (%d REMOVE); lanes checked against .owned-paths.yaml" % (
        len(rows), len(MEMBERS), sum(r.get("disposition") == "REMOVE" for r in rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
