#!/usr/bin/env python3
"""BF-v-4 check: every root the round-6 ruling file marks `verdict: DECLARES-NAMES` reads names > 0 or uncounted > 0.

Reads the ruling file (the `### <root>` heading above each `verdict: DECLARES-NAMES` line), runs the `all` command once and
reads each such root's UNMAPPED line. Last line: DECLARES-CHECK ok=True roots=N still_zero=N.
ok=True when every such root reads names > 0 or uncounted > 0 and roots equals the ruling file's count of the verdict.
Python 3.9; ASCII only.
"""
import os
import re
import subprocess
import sys

RULING = ("org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~1/MAP_ENTRIES_FOR_RULING_round6.md")
MAP = "infra/logic/registry/root_map.json"


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    p = subprocess.run(["git", "-C", here, "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("git rev-parse failed: %s" % p.stderr.strip())
    return p.stdout.strip()


def declares_roots(text):
    """(roots in file order, count of `verdict: DECLARES-NAMES` lines)."""
    roots, head, count = [], None, 0
    for ln in text.replace("\r\n", "\n").split("\n"):
        if ln.startswith("### "):
            head = ln[4:].strip()
        elif ln.strip() == "verdict: DECLARES-NAMES":
            count += 1
            roots.append(head)
    return roots, count


def main():
    top = repo_root()
    with open(os.path.join(top, *RULING.split("/")), encoding="utf-8") as fh:
        roots, count = declares_roots(fh.read())
    p = subprocess.run([sys.executable, os.path.join("lib", "opal_naming_rootcheck.py"), "all", "--map", MAP],
                       capture_output=True, text=True, cwd=top)
    lines = p.stdout.split("\n")
    seen, still_zero, bad = {}, 0, []
    for ln in lines:
        m = re.match(r"^UNMAPPED (\S+) names=(\d+) uncounted=(\d+)$", ln)
        if m:
            seen[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    for r in roots:
        if r not in seen:
            bad.append(r)
            print("MISSING %s: no UNMAPPED line" % (r,))
            continue
        n, u = seen[r]
        z = n == 0 and u == 0
        still_zero += 1 if z else 0
        print("%s %s names=%d uncounted=%d" % ("ZERO" if z else "READS", r, n, u))
    ok = (p.returncode == 0 and count > 0 and len(roots) == count and not bad and still_zero == 0
          and all(r is not None for r in roots))
    print("DECLARES-CHECK ok=%s roots=%d still_zero=%d" % (ok, len(roots), still_zero))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
