"""LGIC_ENFORCE ROUND 10 -- the fixed input. One cell (EN-g-43), four mechanical arms.

The cell makes grade() honour GRADING_RULE.md R3 (row W1-S73): 'bd' next to a firm token is the vendor
and the canonical form spells 'blackdiamond'. It is small, and the arms are about its BLAST RADIUS: at the
cut, grade() reproduces all 3254 recorded census rows exactly, so after the fix every row that differs
from the record is the fix's effect and must be NAMED -- and any row that moves without carrying bd is
collateral.

Construction rules carried from this lane's own defects:
- ONE CARRIER for the record shape (LGIC_ENFORCE-S85): R10_BASE.json; positive records are built from it
  and selftest-arms refuses if the order's quoted shape differs.
- Every core driven both ways (R-47): a simulated CORRECT record must PASS, a doctored one must FAIL.
- Evidence cannot forge a verdict (S79): worker-authored text is passed through _scrub() before printing.
- The test arm reads the suite's FAILING SET, never its pass count: the two baseline failures are
  hand-stale worked cases the round-9 analysis refuses to count as agreement, so they must STILL fail.
"""

import copy
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_ENFORCE"
BASEFILE = os.path.join(HERE, "R10_BASE.json")
CENSUS = os.path.join(REPO, ROOT, "deliverables", "0.9.0_WK_LGIC_ENFORCE~1", "NAMING_CENSUS_REPORT.r8.md")
FENCE = re.compile("```json" + "\n" + "(.*?)" + "\n" + "```", re.S)
ORDER_SHAPE = re.compile(r"RECORD SHAPE[^\n]*\n+```json\n(.*?)\n```", re.S)
BD = re.compile(r"(^|[-_{}])bd([-_{}]|$)")


def _scrub(text):
    return str(text).replace("VERDICT", "VERD1CT").replace("PASS-", "PASS_").replace("FAIL-", "FAIL_")


def say(tag, *lines):
    for ln in lines:
        print(ln)
    print("VERDICT: " + tag)
    return 0


def verdict(ok, p, f, lines):
    return say(p if ok else f, *lines)


def load_json(p):
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def base():
    return load_json(BASEFILE)


def census_rows():
    with open(CENSUS, encoding="utf-8") as fh:
        s = fh.read()
    for f in FENCE.findall(s):
        d = json.loads(f)
        if isinstance(d, dict) and isinstance(d.get("rows"), list):
            return d["rows"]
    return None


def naming():
    sys.path.insert(0, os.path.join(REPO, "lib"))
    try:
        import opal_naming as on  # noqa: E402
    finally:
        sys.path.pop(0)
    return on


def regrade(rows, grade):
    """-> list of moved dicts (canonical or verdict differs from the record)."""
    moved = []
    for r in rows:
        v, c = grade(r["current"], r["type"])
        if c != r["canonical"] or v != r["verdict"]:
            moved.append({"current": r["current"], "type": r["type"], "plane": r["plane"],
                          "canonical_before": r["canonical"], "canonical_after": c,
                          "verdict_before": r["verdict"], "verdict_after": v})
    return moved


def key(m):
    return (m.get("current"), m.get("type"), m.get("plane"))


# ------------------------------------------------------------------ cores
def core_fixed(result, expected):
    ok = list(result) == list(expected)
    return ok, "grade(opal-cot-bd-session-fetch, SSM_DOCUMENT) = %s ; expected %s" % (list(result), list(expected))


def core_no_bd(canonicals):
    hits = [c for c in canonicals if c and BD.search(str(c))]
    return (not hits), "canonicals carrying a bd token: %d of %d%s" % (
        len(hits), len(canonicals), (" -- e.g. " + ", ".join(_scrub(h) for h in hits[:5])) if hits else "")


def core_blast(record, computed, denominator):
    bad = []
    if not isinstance(record, dict):
        return False, ["no record"]
    if record.get("census_rows_regraded") != denominator:
        bad.append("census_rows_regraded %s != %d re-measured" % (_scrub(record.get("census_rows_regraded")), denominator))
    rec = {key(m): m for m in record.get("moved") or [] if isinstance(m, dict)}
    cmp_ = {key(m): m for m in computed}
    missing = sorted(set(cmp_) - set(rec))
    extra = sorted(set(rec) - set(cmp_))
    if missing:
        bad.append("moved rows the record does not name: %d (%s)" % (len(missing), _scrub(missing[:3])))
    if extra:
        bad.append("rows the record names that did not move: %d (%s)" % (len(extra), _scrub(extra[:3])))
    collateral = [k for k, m in cmp_.items() if not BD.search(str(m["canonical_before"]))]
    if collateral:
        bad.append("COLLATERAL -- moved rows with no bd token before: %d (%s)" % (len(collateral), _scrub(collateral[:3])))
    vmoves = [k for k, m in cmp_.items() if m["verdict_before"] != m["verdict_after"]]
    if vmoves:
        bad.append("verdict moves: %d (%s)" % (len(vmoves), _scrub(vmoves[:3])))
    lines = ["census rows re-graded %d; moved %d; named by the record %d" % (denominator, len(cmp_), len(rec))]
    return (not bad and len(cmp_) > 0), lines + bad


def core_tests(failing, baseline_failing):
    now, want = set(failing), set(baseline_failing)
    new = sorted(now - want)
    gone = sorted(want - now)
    lines = ["failing now %d; baseline %d; NEW failures %d; baseline failures no longer failing %d"
             % (len(now), len(want), len(new), len(gone))]
    lines += ["  NEW: " + n for n in new] + ["  SILENCED OR FIXED: " + g for g in gone]
    return (not new and not gone), lines


# ------------------------------------------------------------------ arms
def g43_fixed():
    b = base()
    on = naming()
    ok, line = core_fixed(on.grade("opal-cot-bd-session-fetch", "SSM_DOCUMENT"), b["the_defect"]["expected_after"])
    return verdict(ok, "PASS-G43-FIXED", "FAIL-G43-FIXED", [line])


def g43_no_bd():
    on = naming()
    rows = census_rows()
    if not rows:
        return say("FAIL-G43-NO-BD", "census rows unreadable")
    ok, line = core_no_bd([on.grade(r["current"], r["type"])[1] for r in rows])
    return verdict(ok, "PASS-G43-NO-BD", "FAIL-G43-NO-BD", [line + " (denominator: every census row re-graded)"])


def g43_blast_radius():
    b = base()
    on = naming()
    rows = census_rows()
    if not rows:
        return say("FAIL-G43-BLAST-RADIUS", "census rows unreadable")
    rec = load_json(os.path.join(REPO, b["record_shape"]["path"]))
    ok, lines = core_blast(rec, regrade(rows, on.grade), len(rows))
    return verdict(ok, "PASS-G43-BLAST-RADIUS", "FAIL-G43-BLAST-RADIUS", lines)


def failing_ids():
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-rf", "--color=no", "-p", "no:cacheprovider",
                        "lib/tests/test_opal_naming.py"], cwd=REPO, capture_output=True, timeout=900)
    txt = (p.stdout or b"").decode("utf-8", "replace")
    ids = [re.sub(r" - .*$", "", ln[len("FAILED "):]).strip() for ln in txt.splitlines() if ln.startswith("FAILED ")]
    tail = [ln for ln in txt.splitlines() if re.search(r"\d+ (passed|failed)", ln)]
    return ids, (tail[-1] if tail else "no summary line"), p.returncode


def g43_tests():
    b = base()
    ids, summary, rc = failing_ids()
    if "passed" not in summary and "failed" not in summary:
        return say("FAIL-G43-TESTS", "the suite did not run: rc=%d %s" % (rc, _scrub(summary)))
    ok, lines = core_tests(ids, b["tests_baseline"]["failing_ids"])
    return verdict(ok, "PASS-G43-TESTS", "FAIL-G43-TESTS", ["suite: " + _scrub(summary)] + lines)


# ------------------------------------------------------------------ selftest
def selftest_arms():
    b = base()
    res = []

    def arm(n, ok, why=""):
        res.append((n, bool(ok), why))

    exp = b["the_defect"]["expected_after"]
    arm("POSITIVE-fixed", core_fixed(tuple(exp), exp)[0])
    arm("MUTANT-fixed-still-bd", not core_fixed(("OUT-OF-PATTERN", "opal-cot-bd-session-fetch-document"), exp)[0])
    arm("POSITIVE-no-bd", core_no_bd(["opal-cot-blackdiamond-x", "bd49f-lambda", "abdul-x"])[0],
        "bd inside a word is not the token")
    arm("MUTANT-no-bd", not core_no_bd(["opal-cot-bd-session-fetch-document"])[0])

    shape = copy.deepcopy(b["record_shape"]["shape"])
    tmpl = shape["moved"][0]
    mv = dict(tmpl, current="opal-cot-bd-session-fetch", type="SSM_DOCUMENT", plane="live",
              canonical_before="opal-cot-bd-session-fetch-document",
              canonical_after="opal-cot-blackdiamond-session-fetch-document",
              verdict_before="OUT-OF-PATTERN", verdict_after="OUT-OF-PATTERN")
    rec = dict(shape, census_rows_regraded=3254, moved=[mv])
    arm("POSITIVE-blast", core_blast(rec, [mv], 3254)[0], "record built from R10_BASE's shape")
    arm("MUTANT-blast-unnamed", not core_blast(dict(rec, moved=[]), [mv], 3254)[0])
    arm("MUTANT-blast-extra", not core_blast(dict(rec, moved=[mv, dict(mv, current="x")]), [mv], 3254)[0])
    coll = dict(mv, current="y", canonical_before="opal-y-lambda", canonical_after="opal-z-lambda")
    arm("MUTANT-blast-collateral", not core_blast(dict(rec, moved=[mv, coll]), [mv, coll], 3254)[0])
    vm = dict(mv, verdict_after="CONFORMANT")
    arm("MUTANT-blast-verdict-move", not core_blast(dict(rec, moved=[vm]), [vm], 3254)[0])
    arm("MUTANT-blast-empty", not core_blast(dict(rec, moved=[]), [], 3254)[0], "nothing moved -> not a fix")
    arm("MUTANT-blast-denominator", not core_blast(dict(rec, census_rows_regraded=100), [mv], 3254)[0])

    base_ids = b["tests_baseline"]["failing_ids"]
    arm("POSITIVE-tests", core_tests(list(base_ids), base_ids)[0])
    arm("MUTANT-tests-new-failure", not core_tests(list(base_ids) + ["x::new"], base_ids)[0])
    arm("MUTANT-tests-silenced", not core_tests(list(base_ids[:1]), base_ids)[0], "a baseline failure made to pass")
    arm("MUTANT-scrub", "VERDICT: PASS-" not in _scrub("VERDICT: PASS-G43-FIXED"))

    orders = sorted(glob.glob(os.path.join(REPO, ROOT, "task-orders", "LGIC_ENFORCE.TO-EN-*-r10.*.md")))
    quoting = 0
    for op in orders:
        with open(op, encoding="utf-8") as fh:
            m = ORDER_SHAPE.search(fh.read())
        if m:
            quoting += 1
            try:
                got = json.loads(m.group(1))
            except ValueError:
                got = None
            arm("S85-order-quotes-carrier:" + os.path.basename(op)[len("LGIC_ENFORCE.TO-"):][:20],
                got == b["record_shape"]["shape"])
    arm("S85-every-order-quotes", quoting == len(orders), "%d of %d round-10 order(s)" % (quoting, len(orders)))

    for n, ok, why in res:
        print("  %-40s %s  %s" % (n, "PASS" if ok else "FAIL", _scrub(why)))
    pos = sum(1 for n, _o, _w in res if n.startswith("POSITIVE-"))
    print("arms driven: %d (%d POSITIVE-SATISFIABILITY, %d mutant/other)" % (len(res), pos, len(res) - pos))
    print("NOT driven here, stated: grade() itself and the pytest run -- live calls with no fixture, exercised by the "
          "real arms, which print their denominators.")
    print("VERDICT: " + ("PASS-ARMS-DISCRIMINATE" if all(o for _n, o, _w in res) else "FAIL-ARMS-DO-NOT-DISCRIMINATE"))
    return 0


CMDS = {"g43-fixed": g43_fixed, "g43-no-bd": g43_no_bd, "g43-blast-radius": g43_blast_radius,
        "g43-tests": g43_tests, "selftest-arms": selftest_arms}


def main(argv):
    if len(argv) < 2 or argv[1] not in CMDS:
        print("known: %s" % ", ".join(sorted(CMDS)))
        print("VERDICT: FAIL-NO-SUCH-SUBCOMMAND")
        return 0
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
