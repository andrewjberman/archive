"""IRPT_ANLREQ AR-g-161 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g161_checks.py build   the resident's pricing as_of is lib/trading_calendar.py's frontier, called: reports/resident_installed.py `_t_minus_1(epoch)` returns
                                     prev_trading_day(expected_last_trading_day(<the UTC date of epoch>)) as an ISO string and carries no local weekday rule (no `weekday() >= 5`). Pinned cases (2027): Saturday 01-16 and Sunday
                                     01-17 and the Martin Luther King holiday Monday 01-18 give Thursday 01-14; the day after the holiday, Tuesday 01-19, gives Friday 01-15; an ordinary Wednesday 01-20 gives Tuesday 01-19.
                                     The existing test that pinned the weekday rule (test_t_minus_1_skips_weekends) is replaced by those cases.
    python ar_g161_checks.py guard   nothing else moves: `_t_minus_1` keeps its name and one argument and returns a YYYY-MM-DD string, and `_pricing_extras` still calls it with the clock
    python ar_g161_checks.py regress each existing test file that loads resident_installed on its own, then the scope check
    python ar_g161_checks.py scope   the branch changed only resident_installed.py, test_opal_pricing_binding.py, the order and the worker's folder (against the merge-base with box/dell2)

Prints one RESULT line: AR-G161-OK / AR-G161-FAIL (or -REGRESS- / -SCOPE-); rc 0 only on OK. ASCII only.
"""
import ast
import datetime
import re
import subprocess
import sys

IR = "infra/aws/lambda/investor-reporting/"
INSTALLED = IR + "reports/resident_installed.py"
TEST = IR + "reports/tests/test_opal_pricing_binding.py"
OWN = (INSTALLED, TEST, "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-161.pricing-as-of-calendar-frontier.md")
OWN_PREFIX = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~282/", "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/", "org/tier2_senior/0.7.0_AE_CloudOps~IB2/")
REGRESS_FILES = (TEST, IR + "reports/tests/test_ycharts_price_tier.py", IR + "reports/tests/test_resident_installed.py")
CASES = (("2027-01-16", "2027-01-14"), ("2027-01-17", "2027-01-14"), ("2027-01-18", "2027-01-14"), ("2027-01-19", "2027-01-15"), ("2027-01-20", "2027-01-19"))


def function_source(text, name):
    tree = ast.parse(text)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(text, node), node
    return None, None


def epoch(day):
    return int(datetime.datetime.fromisoformat(day + "T08:00:00+00:00").timestamp())


def load_function():
    text = open(INSTALLED, encoding="utf-8").read()
    src, node = function_source(text, "_t_minus_1")
    if src is None:
        return None, None, text
    sys.path.insert(0, "lib")
    ns = {"datetime": datetime}
    exec(compile(src, INSTALLED, "exec"), ns)  # the function alone: it imports the calendar inside itself
    return ns["_t_minus_1"], src, text


def arms_build():
    fails = []
    fn, src, text = load_function()
    if fn is None:
        return ["_t_minus_1 not found in %s" % INSTALLED]
    if re.search(r"weekday\(\)\s*>=\s*5", src):
        fails.append("_t_minus_1 still carries a local weekday rule")
    if "trading_calendar" not in src:
        fails.append("_t_minus_1 does not call lib/trading_calendar.py")
    for day, want in CASES:
        try:
            got = fn(epoch(day))
        except Exception as exc:  # a check prints what is raised
            fails.append("_t_minus_1(%s) raised %s: %s" % (day, type(exc).__name__, exc))
            continue
        if got != want:
            fails.append("_t_minus_1(%s) is %r, want %r" % (day, got, want))
    test_text = open(TEST, encoding="utf-8").read()
    if "test_t_minus_1_skips_weekends" in test_text and '== "2027-01-15"' in test_text.split("def test_t_minus_1_skips_weekends")[1].split("def ")[0]:
        fails.append("the weekday-rule test still pins 2027-01-15 for a Sunday or the holiday")
    for day, want in CASES:
        if day not in test_text or want not in test_text:
            fails.append("the test file does not pin %s -> %s" % (day, want))
    return fails


def arms_guard():
    fails = []
    text = open(INSTALLED, encoding="utf-8").read()
    src, node = function_source(text, "_t_minus_1")
    if node is None or [a.arg for a in node.args.args] != ["epoch"]:
        fails.append("_t_minus_1 lost its one argument `epoch`")
    fn, _src, _text = load_function()
    if fn is not None:
        try:
            out = fn(epoch("2027-01-20"))
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", out):
                fails.append("_t_minus_1 no longer returns YYYY-MM-DD: %r" % (out,))
        except Exception:
            pass  # the build arm reports a raise
    if '"as_of": _t_minus_1(clock())' not in text:
        fails.append("_pricing_extras no longer sets as_of from _t_minus_1(clock())")
    return fails


def scope():
    rc = subprocess.run(["git", "merge-base", "HEAD", "box/dell2"], capture_output=True)
    base = rc.stdout.decode().strip()
    if rc.returncode != 0 or not base:
        return ["no merge-base with box/dell2"]
    diff = subprocess.run(["git", "diff", "--name-only", base, "HEAD"], capture_output=True)
    if diff.returncode != 0:
        return ["git diff rc=%d" % diff.returncode]
    names = [n for n in diff.stdout.decode().splitlines() if n.strip()]
    stray = [n for n in names if n not in OWN and not n.startswith(OWN_PREFIX + ISSUER)]
    return ["outside the cell's write set: %s" % ", ".join(stray)] if stray else []


def regress():
    fails = []
    for path in REGRESS_FILES:
        out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", path], capture_output=True, text=True)
        if out.returncode != 0:
            fails.append("%s: rc=%d %s" % (path.rsplit("/", 1)[-1], out.returncode, (out.stdout or out.stderr).strip().splitlines()[-1:] or ""))
    return fails + scope()


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode in ("scope", "regress"):
        fails = scope() if mode == "scope" else regress()
        print("AR-G161-%s-%s %s" % (mode.upper(), "FAIL" if fails else "OK", "; ".join(fails)))
        return 1 if fails else 0
    if mode not in ("build", "guard"):
        print("AR-G161-FAIL usage: build | guard | scope | regress")
        return 2
    fails = arms_build() if mode == "build" else arms_guard()
    print("AR-G161-%s %s: %s" % ("FAIL" if fails else "OK", mode, "; ".join(fails) if fails else "all arms"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
