"""check_fwd4_cadence -- FWD-4 group C (LGIC_BLANKFIX BF-ab-1): the cadence word in a schedule's listed new name against the
word lib/opal_naming_cadence.py decides from that schedule's OWN schedule_expression.

Over every root the root map covers, every EVENT_RULE / SCHEDULE line the root check prints is read (FIX, RIGHT or any
other kind). The new name on a FIX or RIGHT line is read with opal_naming_cadence.carried_word(); the expression is read
from the resource block the line points at (opal_naming_cadence.cadences(root), matched on type, current name, file:line).
  agree      the word the name carries is the word the expression decides
  undecided  the expression cannot decide a word (or no expression is stated, or the line carries no new name): LISTED
  mismatch   the name carries a different word, or none, where the expression decides one
Prints one line per undecided or mismatch row, then last the FWD4-CADENCE line. Reads files only: no AWS, no network.
"""
import json
import os
import sys


def _repo_root():
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(d, "lib", "opal_naming.py")):
            return d
        up = os.path.dirname(d)
        if up == d:
            raise SystemExit("FWD4-CADENCE ok=False reason=repository root not found above %s" % __file__)
        d = up


ROOT = _repo_root()
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "lib"))
import opal_naming_cadence as cad  # noqa: E402
import opal_naming_rootcheck as rc  # noqa: E402
import opal_naming_scope as sc  # noqa: E402

MAP = "infra/logic/registry/root_map.json"
TYPES = ("EVENT_RULE", "SCHEDULE")


def main():
    with open(MAP, "r", encoding="utf-8") as fh:
        keys = sorted(json.load(fh).get("roots") or {})
    n = agree = undecided = mismatch = 0
    problems = []
    out_lines = []
    for key in keys:
        try:
            root = sc._map_key_root(key)
        except ValueError as exc:
            problems.append("map key %s: %s" % (key, exc))
            continue
        lines = []
        try:
            rc.check_root(root, MAP, out=lines.append, report_only=True)
            rows = cad.cadences(root)
        except Exception as exc:  # an unreadable root fails the run, never drops
            problems.append("root %s unread: %s: %s" % (root, type(exc).__name__, exc))
            continue
        by_where = {}
        for r in rows:
            by_where.setdefault((r["type"], r["current"], r["where"]), r)
        for line in lines:
            parts = rc._split_line(line)
            if parts is None:
                continue
            kind, typ, cur, detail, where = parts
            if typ not in TYPES:
                continue
            n += 1
            row = by_where.get((typ, cur, where))
            if row is None:
                mismatch += 1
                out_lines.append("MISMATCH %s %s %s [%s] no schedule block read at that line" % (typ, cur, kind, where))
                continue
            if kind not in ("FIX", "RIGHT"):
                undecided += 1
                out_lines.append("UNDECIDED %s %s [%s] line kind %s carries no new name" % (typ, cur, where, kind))
                continue
            new = detail if kind == "FIX" else cur
            carried = cad.carried_word(new, typ)
            if row["expression"] is None and not row["has_event_pattern"]:
                undecided += 1
                out_lines.append("UNDECIDED %s %s -> %s [%s] %s" % (typ, cur, new, where, row["basis"]))
            elif row["expression"] is None:
                undecided += 1
                out_lines.append("UNDECIDED %s %s -> %s [%s] no schedule expression; %s (name carries %s)"
                                 % (typ, cur, new, where, row["basis"], carried))
            elif row["word"] is None:
                undecided += 1
                out_lines.append("UNDECIDED %s %s -> %s [%s] expr=%s: %s (name carries %s)"
                                 % (typ, cur, new, where, row["expression"], row["basis"], carried))
            elif carried == row["word"]:
                agree += 1
            else:
                mismatch += 1
                out_lines.append("MISMATCH %s %s -> %s [%s] expr=%s expression_word=%s name_word=%s"
                                 % (typ, cur, new, where, row["expression"], row["word"], carried))
    for p in problems:
        print("PROBLEM " + p)
    for o in out_lines:
        print(o)
    ok = mismatch == 0 and not problems and n == agree + undecided + mismatch and n > 0
    print("FWD4-CADENCE ok=%s schedules=%d agree=%d undecided=%d mismatch=%d" % (ok, n, agree, undecided, mismatch))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
