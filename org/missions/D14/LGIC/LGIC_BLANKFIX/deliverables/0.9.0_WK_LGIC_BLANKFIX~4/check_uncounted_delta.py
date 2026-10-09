#!/usr/bin/env python3
"""BW2-AC2 -- uncounted falls, and what remains says why the repository cannot decide it (LGIC_BLANKFIX BF-w-2).

Reads the ALL-ROOTS last line of the round-7 saved run (the before), runs `lib/opal_naming_rootcheck.py all` once (the
after), counts every residual UNCOUNTED name by reason (the mapped roots print one line each; an unmapped root prints only
its count, so its names are read here with lib/opal_naming_scope.root_names), and prints, last:

  UNCOUNTED-DELTA ok=True before=N after=N hole_before=N hole_after=N mapped=N residual_reasons=N bare_reasons=0

ok=True when after < before, the live run prints ok=True, the residual lines add up to the live uncounted count, every
residual reason is in the closed set (opal_naming_scope.UNCOUNTED_REASONS) and none is a bare local / var / module /
json / interpolation. Python 3.9 syntax; stdlib only; ASCII only.
"""
from __future__ import annotations

import collections
import os
import re
import subprocess
import sys

BEFORE = "org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/2.0.0_SA_COO~G/ALL_ROOTS_round7.txt"
MAP = "infra/logic/registry/root_map.json"
BARE = ("local", "var", "module", "json", "interpolation")
_REASON_RE = re.compile(r" -- ([A-Za-z-]+)  \[")


def repo_root():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "lib", "opal_naming_rootcheck.py")):
        up = os.path.dirname(d)
        if up == d:
            raise SystemExit("UNCOUNTED-DELTA ok=False reason=no-repo-root")
        d = up
    return d


def last_all_roots(lines):
    got = [x for x in lines if x.startswith("ALL-ROOTS ")]
    if not got:
        return None
    return dict(w.split("=", 1) for w in got[-1].split()[1:] if "=" in w)


def main():
    root = repo_root()
    sys.path.insert(0, os.path.join(root, "lib"))
    with open(os.path.join(root, *BEFORE.split("/")), encoding="utf-8") as fh:
        before = last_all_roots(fh.read().split("\n"))
    cmd = [sys.executable, os.path.join(root, "lib", "opal_naming_rootcheck.py"), "all", "--map", os.path.join(root, *MAP.split("/"))]
    out = subprocess.run(cmd, capture_output=True, text=True, cwd=root, timeout=900)
    lines = out.stdout.split("\n")
    after = last_all_roots(lines)
    problems = []
    if before is None or after is None:
        problems.append("an ALL-ROOTS line is missing")
        print("UNCOUNTED-DELTA ok=False reason=missing-all-roots-line before=%s after=%s" % (before is not None, after is not None))
        return 1
    if after.get("ok") != "True":
        problems.append("the live run did not print ok=True")
    import opal_naming_scope as scope

    reasons = collections.Counter()
    for x in lines:
        if x.startswith("UNCOUNTED "):
            m = _REASON_RE.search(x)
            reasons[m.group(1) if m else "?"] += 1
    n_lines = sum(reasons.values())
    unmapped_n = 0
    for x in lines:
        m = re.match(r"UNMAPPED (\S+) names=\d+ uncounted=(\d+)", x)
        if m and int(m.group(2)) > 0:
            _items, unc, _st = scope.root_names(m.group(1))
            unmapped_n += int(m.group(2))
            if len(unc) != int(m.group(2)):
                problems.append("unmapped root %s: %d read here, %s printed" % (m.group(1), len(unc), m.group(2)))
            for u in unc:
                reasons[u["reason"]] += 1
    total = sum(reasons.values())
    if total != int(after["uncounted"]):
        problems.append("residual %d != live uncounted %s" % (total, after["uncounted"]))
    bare = sum(n for r, n in reasons.items() if r in BARE)
    outside = sorted(r for r in reasons if r not in scope.UNCOUNTED_REASONS)
    if outside:
        problems.append("a reason outside the closed set: %s" % (outside,))
    b_unc, a_unc = int(before["uncounted"]), int(after["uncounted"])
    if not a_unc < b_unc:
        problems.append("uncounted did not fall")
    print("BEFORE uncounted=%d hole=%s items=%s mapped=%s (%s)" % (b_unc, before["hole"], before["items"], before["mapped"], BEFORE))
    print("AFTER  uncounted=%d hole=%s items=%s mapped=%s (live run, %d printed lines + %d in unmapped roots)" % (
        a_unc, after["hole"], after["items"], after["mapped"], n_lines, unmapped_n))
    for r in sorted(reasons):
        print("RESIDUAL %-16s %d  %s" % (r, reasons[r], scope.REASON_WHY.get(r, "NOT IN THE CLOSED SET")))
    for p in problems:
        print("PROBLEM: " + p)
    print("UNCOUNTED-DELTA ok=%s before=%d after=%d hole_before=%s hole_after=%s mapped=%s residual_reasons=%d bare_reasons=%d" % (
        not problems, b_unc, a_unc, before["hole"], after["hole"], after["mapped"], len(reasons), bare))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
