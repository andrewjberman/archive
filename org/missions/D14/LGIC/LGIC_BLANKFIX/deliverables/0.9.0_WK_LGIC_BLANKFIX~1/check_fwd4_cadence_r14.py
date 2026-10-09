"""check_fwd4_cadence_r14 -- FWD-4 R1 (LGIC_BLANKFIX BF-ac-1): every schedule line's cadence word against its own expression.

Over every root the root map covers, every EVENT_RULE / SCHEDULE line the root check prints is read. The expression is read from
the resource block the line points at (opal_naming_cadence.cadences(root)); the word the line's NEW name carries is read with
opal_naming_cadence.carried_word(). Each line is exactly one of:
  agree        the expression decides a word and the new name carries it
  mismatch     the expression decides a word and the new name carries another, or none        -> FAILS the run
  carried_over the expression decides NO word (uneven fires, an Nth weekday, no expression) and the new name still carries a
               cadence word: the old word was kept, not read                                   -> FAILS the run
  partial      the expression decides no word and the line carries no cadence word (or no new name): the reason is printed
The NEGATIVE ARM runs first, inside: planted lines whose word disagrees with their expression, and one that carries a word
over an uneven day, are classified by the same function and must land in mismatch and carried_over (they are never added to
the run's counts). Reads files only: no AWS, no network.

Last line: FWD4-CADENCE-R14 ok=True schedules=N agree=N partial=N mismatch=0 carried_over=0
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
            raise SystemExit("FWD4-CADENCE-R14 ok=False reason=repository root not found above %s" % __file__)
        d = up


ROOT = _repo_root()
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "lib"))
import opal_naming_cadence as cad  # noqa: E402
import opal_naming_rootcheck as rc  # noqa: E402
import opal_naming_scope as sc  # noqa: E402

MAP = "infra/logic/registry/root_map.json"
TYPES = ("EVENT_RULE", "SCHEDULE")


def classify(typ, new, expression):
    """(class, reason) of one line from its NEW name (None when the line carries none) and its expression (None when not stated).
    The expression is decided by opal_naming_cadence.word_for, never by the name."""
    if expression is None:
        word, basis = None, "no schedule expression is stated or readable"
    else:
        word, basis = cad.word_for(expression)
    carried = None if new is None else cad.carried_word(new, typ)
    if carried is not None and carried.startswith("on-"):
        carried = None  # an event token (P3, on-{event}) names the event the rule waits for, not a cadence word
    if new is None:
        return "partial", "the line carries no new name; " + basis
    if word is not None:
        if carried == word:
            return "agree", basis
        return "mismatch", "expression says %s (%s); the name carries %s" % (word, basis, carried)
    if carried is not None:
        return "carried_over", "expression decides no word (%s); the name still carries %s" % (basis, carried)
    return "partial", basis


def negative_arm():
    """Planted lines: every one must land where a wrong word belongs. Returns (ok, lines)."""
    plant = [
        ("a twice-a-day, 12 h apart expression under daily", "EVENT_RULE", "x-pull-daily", "cron(45 9,21 * * ? *)", "mismatch"),
        ("a once-a-day expression under 12h", "EVENT_RULE", "x-pull-12h", "cron(45 9 * * ? *)", "mismatch"),
        ("an hourly expression under daily", "SCHEDULE", "x-pull-daily", "rate(1 hour)", "mismatch"),
        ("an uneven three-a-day expression keeping 45min", "EVENT_RULE", "x-score-45min", "cron(55 0,13,20 * * ? *)", "carried_over"),
        ("an uneven two-a-day expression keeping daily", "EVENT_RULE", "x-pull-daily", "cron(30 14,21 * * ? *)", "carried_over"),
        ("an expression that is not stated, name keeping a word", "SCHEDULE", "x-pull-daily", None, "carried_over"),
        # the differences the other way: these must NOT be flagged
        ("the 12 h expression under 12h", "EVENT_RULE", "x-pull-12h", "cron(45 9,21 * * ? *)", "agree"),
        ("the once-a-day expression under daily", "EVENT_RULE", "x-pull-daily", "cron(45 9 * * ? *)", "agree"),
        ("an uneven expression with a partial name", "EVENT_RULE", "x-pull-{cadence}", "cron(30 14,21 * * ? *)", "partial"),
    ]
    ok, lines = True, []
    for label, typ, new, expr, want in plant:
        got, why = classify(typ, new, expr)
        good = got == want
        ok = ok and good
        lines.append("NEGATIVE-ARM %s %s: planted %s -> %s (wanted %s)" % ("held" if good else "BROKEN", "", label, got, want))
    return ok, lines


def main():
    arm_ok, arm_lines = negative_arm()
    for ln in arm_lines:
        print(ln)
    with open(MAP, "r", encoding="utf-8") as fh:
        keys = sorted(json.load(fh).get("roots") or {})
    count = {"agree": 0, "partial": 0, "mismatch": 0, "carried_over": 0}
    n = 0
    problems, out_lines = [], []
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
                count["mismatch"] += 1
                out_lines.append("MISMATCH %s %s [%s] no schedule block read at that line" % (typ, cur, where))
                continue
            if kind == "FIX":
                new = detail
            elif kind == "RIGHT":
                new = cur
            else:
                new = None  # NOT-ASKED, HOLE, CARDED...: the line prints no new name
            what, why = classify(typ, new, row["expression"])
            if new is None:
                why = "line kind %s: %s" % (kind, why)
            count[what] += 1
            if what != "agree":
                out_lines.append("%s %s %s -> %s [%s] expr=%s: %s" % (what.upper(), typ, cur, new, where, row["expression"], why))
    for p in problems:
        print("PROBLEM " + p)
    for o in out_lines:
        print(o)
    ok = (arm_ok and not problems and count["mismatch"] == 0 and count["carried_over"] == 0 and n > 0
          and n == sum(count.values()))
    print("FWD4-CADENCE-R14 ok=%s schedules=%d agree=%d partial=%d mismatch=%d carried_over=%d"
          % (ok, n, count["agree"], count["partial"], count["mismatch"], count["carried_over"]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
