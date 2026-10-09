#!/usr/bin/env python3
"""BAB2-AC2 (LGIC_BLANKFIX round 13, BF-ab-2): over every mapped root's printed lines, read every stored-file line
(type S3Key, kind FIX or RIGHT) and prove it states `source=<system> owner=<firm or system>`; then read ONE file's move
from its list line alone (current key, new key, source, owner). Nothing is renamed and nothing is moved: read only.

Last line, printed once:  FWD4-STORED ok=True files=N with_source_owner=N undecided=N
  files            stored-file lines read (FIX and RIGHT) over every mapped root
  with_source_owner  lines whose source and owner are both decided words
  undecided        lines where at least one of the two says UNDECIDED (files = with_source_owner + undecided)
  ok               every line carries both fields, the move was read, and the move agrees with its own fields
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def find_root(start):
    """The repository root: the nearest folder above this file that holds lib/opal_naming_rootcheck.py, else None."""
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
    print("FWD4-STORED ok=False files=0 with_source_owner=0 undecided=0 (repository root not found)")
    sys.exit(1)
sys.path.insert(0, os.path.join(ROOT, "lib"))
import opal_naming_rootcheck as rc  # noqa: E402
import opal_naming_rootmap as rm  # noqa: E402

MAP = os.path.join(ROOT, "infra", "logic", "registry", "root_map.json")
# Round 14 (R4): a stored-file line carries `source=<x> owner=<who moves the store> scope=<whose file it is>`. This round-13
# check's "source and owner" of the ADDRESS is the line's source and SCOPE now; the owner field is the ruling row's mover.


def main():
    doc = rm.load_map(MAP)
    problems, stored, roots_read = [], [], 0
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
            parts = rc._split_line(ln)
            if parts is None:
                problems.append("a line of %s does not parse: %s" % (key, ln))
                continue
            if parts[1] == "S3Key" and parts[0] in ("FIX", "RIGHT"):
                stored.append((key, ln, parts))
    with_so = undecided = 0
    for key, ln, parts in stored:
        _d, src, _own, scope = rc.split_stored_fields(parts[3])
        if src is None or scope is None:
            problems.append("a stored-file line of %s carries no source and scope: %s" % (key, ln))
        elif src.startswith("UNDECIDED") or scope.startswith("UNDECIDED"):
            undecided += 1
        else:
            with_so += 1
    # one file's move, read from its list line alone: the first FIX line (in root order) whose source and owner are decided
    move = None
    for key, ln, parts in stored:
        kind, _typ, cur, detail, _where = parts
        detail, src, _mover, own = rc.split_stored_fields(detail)
        new = detail.split(" (", 1)[0].split(";", 1)[0]
        if (kind == "FIX" and src is not None and own is not None and not src.startswith("UNDECIDED")
                and not own.startswith("UNDECIDED") and new != cur
                and "{" not in new and " " not in new):
            move = (key, cur, new, src, own, ln)
            break
    if move is None:
        problems.append("no stored-file line with a decided source and owner and a different new location was found")
    else:
        key, cur, new, src, own, ln = move
        if not new.startswith("%s/%s/" % (src, own)):
            problems.append("the move's new key %s does not begin with its own source/owner %s/%s" % (new, src, own))
        print("LIST LINE (root %s): %s" % (key, ln))
        print("MOVE READ FROM THE LINE ALONE: current=%s new=%s source=%s owner=%s" % (cur, new, src, own))
        print("NO RENAME APPLIED: read only; a live move is a data act with its own pair")
    for p in problems:
        print("FAIL: " + p)
    ok = not problems and len(stored) > 0 and with_so > 0 and with_so + undecided == len(stored)
    print("FWD4-STORED ok=%s files=%d with_source_owner=%d undecided=%d" % (ok, len(stored), with_so, undecided))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
