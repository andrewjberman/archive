#!/usr/bin/env python3
"""BAB3-AC1 (LGIC_BLANKFIX round 13, BF-ab-3, FWD-8): over every mapped root's printed lines, find every item whose
CURRENT value carries a code pattern (a %s / %d / %(name)s placeholder, a {name} or ${name} blank, an f-string field) and
assert each is printed as PATTERN -- never FIX, RIGHT, HOLE, NOT-ASKED, CARDED or REFUSED. Read only; nothing is renamed.

The finder here is this file's own (independent of the grader's _VAR_RE), so a pattern the decision missed is caught.
Negative arm, inside the check: a planted pattern item whose line is presented as FIX is caught and counted as
shown_as_name; a planted PATTERN line is not. The run fails if the arm does not catch the plant.

Last line, printed once:
  FWD8-PATTERNS ok=True roots=N items=N patterns=N shown_as_pattern=N shown_as_name=0
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def find_root(start):
    here = start
    while True:
        if os.path.isfile(os.path.join(here, "lib", "opal_naming_rootcheck.py")):
            return here
        up = os.path.dirname(here)
        if up == here:
            return None
        here = up


ROOT = find_root(HERE)
if ROOT is None:
    print("FWD8-PATTERNS ok=False roots=0 items=0 patterns=0 shown_as_pattern=0 shown_as_name=0 (repository root not found)")
    sys.exit(1)
sys.path.insert(0, os.path.join(ROOT, "lib"))
import opal_naming_rootcheck as rc  # noqa: E402
import opal_naming_rootmap as rm  # noqa: E402

MAP = os.path.join(ROOT, "infra", "logic", "registry", "root_map.json")
# a code pattern: printf-style %s %d %i %f %(name)s, ${name} or {name} blanks (an f-string field is a {name} too)
CODE_PATTERN = re.compile(r"%\(\w+\)[sdif]|%[sdif]|\$\{[^}]*\}|\{[^}]*\}")


def has_pattern(current):
    return CODE_PATTERN.search(current) is not None


def classify(lines):
    """(items, patterns, shown_as_pattern, violations) over the item lines of one root (the ROOTCHECK line is last)."""
    items = patterns = shown = 0
    bad = []
    for ln in lines:
        parts = rc._split_line(ln)
        if parts is None:
            continue
        items += 1
        kind, typ, cur, _detail, where = parts
        if not has_pattern(cur):
            continue
        patterns += 1
        if kind == "PATTERN":
            shown += 1
        else:
            bad.append("%s presented as %s: %s" % (cur, kind, ln))
    return items, patterns, shown, bad


def main():
    problems = []
    # negative arm
    plant_fix = "FIX S3Key data/%s/x.csv -> bd/data/x.csv  [planted.tf:1]"
    plant_pat = "PATTERN S3Key data/%s/x.csv -> a code pattern, not a name; variable '%s'  [planted.tf:1]"
    _i, p1, s1, b1 = classify([plant_fix])
    _i, p2, s2, b2 = classify([plant_pat])
    if not (p1 == 1 and s1 == 0 and len(b1) == 1):
        problems.append("negative arm: a pattern shown as a FIX line was not caught")
    if not (p2 == 1 and s2 == 1 and not b2):
        problems.append("negative arm: a pattern shown as PATTERN was wrongly counted as a name")

    doc = rm.load_map(MAP)
    roots = items = patterns = shown = 0
    per_root = {}
    violations = []
    for key in sorted(doc.get("roots") or {}):
        if rm.nothing_to_name(doc["roots"][key]):
            continue
        lines = []
        try:
            rc.check_root(key, MAP, out=lines.append, report_only=True)
        except Exception as exc:  # a root that stops is a failure, never dropped
            problems.append("root %s stopped: %s: %s" % (key, type(exc).__name__, exc))
            continue
        roots += 1
        n, p, s, bad = classify(lines[:-1])
        m = re.search(r" items=(\d+) ", lines[-1]) if lines else None
        if m is None or int(m.group(1)) != n:
            problems.append("root %s: item lines read (%d) differ from its ROOTCHECK items (%s)" % (key, n, m.group(1) if m else "none"))
        items += n
        patterns += p
        shown += s
        violations.extend("root %s: %s" % (key, b) for b in bad)
        if p:
            per_root[key] = p
    for key in sorted(per_root):
        print("PATTERNS root=%s patterns=%d" % (key, per_root[key]))
    for v in violations:
        print("VIOLATION: " + v)
    for p in problems:
        print("FAIL: " + p)
    as_name = patterns - shown
    ok = not problems and not violations and roots > 0 and patterns > 0 and as_name == 0
    print("FWD8-PATTERNS ok=%s roots=%d items=%d patterns=%d shown_as_pattern=%d shown_as_name=%d"
          % (ok, roots, items, patterns, shown, as_name))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
