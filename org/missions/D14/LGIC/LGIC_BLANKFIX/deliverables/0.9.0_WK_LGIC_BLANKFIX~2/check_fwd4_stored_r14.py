#!/usr/bin/env python3
"""BAC3-AC1 (LGIC_BLANKFIX round 14, BF-ac-3; rulings R4 and R5): over every mapped root's printed lines, read every
stored-file line (type S3Key) and prove:
  - a FIX or RIGHT line prints THREE labelled fields, `source=<x> owner=<who moves the store> scope=<whose file it is>`,
    and owner is never the scope word in its place (two columns, never one in place of the other);
  - a field no row decides prints `UNDECIDED (<reason>)`, never a bare UNDECIDED;
  - a per-firm ruling is shown as a PATTERN with its per-firm fill named (scope={scope}) and a named owner.
Nothing is renamed and nothing is moved: read only.

Negative arm, inside the check: a planted line in the round-13 two-field form (no scope) is caught as missing a field, and a
planted bare UNDECIDED is caught as having no reason. The run fails if the arm does not catch the plants.

Last line, printed once:
  FWD4-STORED-R14 ok=True files=N owner_and_scope=N per_firm_patterns=N undecided=N owner_unnamed=N
  files             stored-file lines read: FIX and RIGHT lines, plus the per-firm PATTERN lines
  owner_and_scope   FIX/RIGHT lines whose source, owner and scope are all decided
  per_firm_patterns per-firm rulings shown as PATTERN (fill named)
  undecided         FIX/RIGHT lines with an open {source} or {scope} place (UNDECIDED, reason printed)
  owner_unnamed     FIX lines whose place is decided but no key ruling row names who moves the store (UNDECIDED, reason printed)
  ok                files = owner_and_scope + per_firm_patterns + undecided + owner_unnamed, every line well formed
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
    print("FWD4-STORED-R14 ok=False files=0 owner_and_scope=0 per_firm_patterns=0 undecided=0 owner_unnamed=0 "
          "(repository root not found)")
    sys.exit(1)
sys.path.insert(0, os.path.join(ROOT, "lib"))
import opal_naming_rootcheck as rc  # noqa: E402
import opal_naming_rootmap as rm  # noqa: E402

MAP = os.path.join(ROOT, "infra", "logic", "registry", "root_map.json")
REASONED = re.compile(r"^UNDECIDED \(.+\)$")


def classify(ln):
    """(class, problem) of one stored-file line. class is one of owner_and_scope, per_firm, undecided, owner_unnamed, or None."""
    parts = rc._split_line(ln)
    if parts is None:
        return None, "the line does not parse: %s" % (ln,)
    kind, typ, _cur, detail, _where = parts
    if typ != "S3Key" or kind not in ("FIX", "RIGHT", "PATTERN"):
        return None, None
    _d, src, own, scope = rc.split_stored_fields(detail)
    if kind == "PATTERN":
        if src is None and own is None and scope is None:
            return None, None  # a pattern in the current name, not a per-firm ruling: no fields owed
        if None in (src, own, scope):
            return None, "a per-firm pattern line lacks one of source, owner, scope: %s" % (ln,)
        if "is filled per firm" not in detail or scope != "{scope}" or own.startswith("UNDECIDED"):
            return None, "a per-firm pattern line must name its fill, show scope={scope} and name an owner: %s" % (ln,)
        return "per_firm", None
    if None in (src, own, scope):
        return None, "a %s stored-file line lacks one of source, owner, scope: %s" % (kind, ln)
    for label, val in (("source", src), ("owner", own), ("scope", scope)):
        if val.startswith("UNDECIDED") and not REASONED.match(val):
            return None, "%s is UNDECIDED with no reason: %s" % (label, ln)
        if not val.strip():
            return None, "%s is empty: %s" % (label, ln)
    if own == scope:
        return None, "owner and scope are the same value, one in place of the other: %s" % (ln,)
    if src.startswith("UNDECIDED") or scope.startswith("UNDECIDED"):
        return "undecided", None
    if own.startswith("UNDECIDED"):
        return "owner_unnamed", None
    return "owner_and_scope", None


def main():
    problems = []
    # negative arm
    old = "FIX S3Key a/b.json -> blackdiamond/49financial/gold/b.json source=blackdiamond owner=49financial  [planted.tf:1]"
    bare = ("FIX S3Key a/b.json -> blackdiamond/49financial/gold/b.json source=blackdiamond owner=UNDECIDED "
            "scope=49financial  [planted.tf:1]")
    good = ("FIX S3Key a/b.json -> blackdiamond/49financial/gold/b.json source=blackdiamond owner=ADVI_FIRMBKTS moves it "
            "scope=49financial  [planted.tf:1]")
    c1, p1 = classify(old)
    c2, p2 = classify(bare)
    c3, p3 = classify(good)
    if not (c1 is None and p1):
        problems.append("negative arm: a two-field (round-13) line was not caught")
    if not (c2 is None and p2):
        problems.append("negative arm: a bare UNDECIDED owner was not caught")
    if not (c3 == "owner_and_scope" and p3 is None):
        problems.append("negative arm: a well-formed three-field line was wrongly refused: %s %s" % (c3, p3))

    doc = rm.load_map(MAP)
    counts = {"owner_and_scope": 0, "per_firm": 0, "undecided": 0, "owner_unnamed": 0}
    files = roots_read = 0
    shown = {}
    for key in sorted(doc.get("roots") or {}):
        if rm.nothing_to_name(doc["roots"][key]):
            continue
        lines = []
        try:
            rc.check_root(key, MAP, out=lines.append, report_only=True)
        except Exception as exc:  # a root that stops is a failure, never dropped
            problems.append("root %s stopped: %s: %s" % (key, type(exc).__name__, exc))
            continue
        roots_read += 1
        for ln in lines[:-1]:
            cls, prob = classify(ln)
            if prob:
                problems.append("root %s: %s" % (key, prob))
            if cls:
                files += 1
                counts[cls] += 1
                shown.setdefault(cls, "(root %s) %s" % (key, ln))
    for cls in ("owner_and_scope", "per_firm", "undecided", "owner_unnamed"):
        print("EXAMPLE %s: %s" % (cls, shown.get(cls, "none")))
    for p in problems:
        print("FAIL: " + p)
    total = sum(counts.values())
    ok = (not problems and roots_read > 0 and files > 0 and total == files and counts["owner_and_scope"] > 0
          and counts["per_firm"] > 0 and counts["undecided"] > 0)
    print("FWD4-STORED-R14 ok=%s files=%d owner_and_scope=%d per_firm_patterns=%d undecided=%d owner_unnamed=%d"
          % (ok, files, counts["owner_and_scope"], counts["per_firm"], counts["undecided"], counts["owner_unnamed"]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
