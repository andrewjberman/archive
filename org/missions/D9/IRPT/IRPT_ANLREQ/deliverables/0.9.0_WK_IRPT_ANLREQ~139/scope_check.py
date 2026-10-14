#!/usr/bin/env python3
"""AR331-y-AC3 (TO-AR-y-331): the scope check over the commits of this order.

Reads `base` from the record JSON (the parent of the first commit of this order), prints it, then lists
`git diff --name-only <base> HEAD`. Prints SCOPE-OK only when every path lies under the investor-reporting tree or under
org/missions/D9/IRPT/IRPT_ANLREQ/; otherwise SCOPE-BAD <why>, exit 1. The reason for the check: the cell adds a served route
that a later signed release carries, so nothing outside the granted trees may move with it. ASCII only.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]  # deliverables/<serial> -> IRPT_ANLREQ -> IRPT -> D9 -> missions -> org -> root
RECORD = Path(__file__).resolve().parent / "r41" / "COMMENTARY_PDF_ROUTE_RECORD.json"
ALLOWED = ("infra/aws/lambda/investor-reporting/", "org/missions/D9/IRPT/IRPT_ANLREQ/")


def main():
    try:
        base = json.loads(RECORD.read_text(encoding="utf-8"))["base"]
    except (OSError, ValueError, KeyError) as exc:
        print("SCOPE-BAD the record JSON carries no base: %s" % exc.__class__.__name__)
        return 1
    print("BASE " + base)
    proc = subprocess.run(["git", "diff", "--name-only", base, "HEAD"], cwd=str(ROOT), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=120)
    if proc.returncode != 0:
        print("SCOPE-BAD git diff rc=%d" % proc.returncode)
        return 1
    paths = [line.strip() for line in proc.stdout.decode("utf-8", "replace").splitlines() if line.strip()]
    print("PATHS (%d):" % len(paths))
    for path in paths:
        print("  " + path)
    if not paths:
        print("SCOPE-BAD no path changed between the base and HEAD")
        return 1
    outside = [p for p in paths if not p.startswith(ALLOWED)]
    if outside:
        print("SCOPE-BAD %d path(s) outside the granted trees: %s" % (len(outside), "; ".join(outside)))
        return 1
    print("SCOPE-OK %d paths, all under the granted trees" % len(paths))
    return 0


if __name__ == "__main__":
    sys.exit(main())
