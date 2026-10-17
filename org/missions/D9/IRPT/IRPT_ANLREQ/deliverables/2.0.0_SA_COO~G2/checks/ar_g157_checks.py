"""IRPT_ANLREQ AR-g-157 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g157_checks.py build   the upload door's yfinance checker (intake/yfinance_check.py, YfinanceChecker) judges a symbol by its last FINITE close dated at or before the T-1 trading day:
                                     YfinanceChecker(..., now=<callable returning an aware UTC datetime>) (default: the wall clock); the T-1 day is lib/trading_calendar.py's
                                     prev_trading_day(expected_last_trading_day(now)); rows dated after it are ignored and rows whose close is not finite are dropped before the last row is chosen.
                                     A null newest row no longer turns a symbol Yahoo holds into NOT_KEPT; a Saturday run reads Thursday's close; the day after a holiday reads the trading day before it;
                                     a run on a weekday never reads that day's own row.
    python ar_g157_checks.py guard   nothing else moves: a good history reads KEPT with the last close and HISTORY_ROWS; an empty history NOT_KEPT NO_ROWS; a last close of zero NOT_KEPT
                                     LAST_CLOSE_NOT_POSITIVE; a history that is only non-finite closes NOT_KEPT LAST_CLOSE_NOT_FINITE; a raising history CHECK_FAILED; the cap and the stop on pushback
    python ar_g157_checks.py regress each existing test file of the checker, the door and the resolver on its own, then the scope check
    python ar_g157_checks.py scope   the branch changed only the checker, its test file, the order and the worker's folder (against the merge-base with box/dell2)

Prints one RESULT line: AR-G157-OK / AR-G157-FAIL (or -REGRESS- / -SCOPE-); rc 0 only on OK. ASCII only.
"""
import datetime
import subprocess
import sys

IR = "infra/aws/lambda/investor-reporting/"
CHECKER = IR + "intake/yfinance_check.py"
TESTS = IR + "intake/tests/test_yfinance_check.py"
OWN = (CHECKER, TESTS, "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-157.yfinance-checker-last-finite-close-at-t1.md")
OWN_PREFIX = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~280/", "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/", "org/tier2_senior/0.7.0_AE_CloudOps~IB2/")
REGRESS_FILES = (TESTS, IR + "intake/tests/test_security_resolution.py", IR + "intake/tests/test_decision_tree_findings.py",
                 IR + "ycharts/session/tests/test_resolution_broker.py")
NAN = float("nan")


def setup_paths():
    for entry in ("lib", IR + "intake", IR):
        sys.path.insert(0, entry)


def utc(text):
    return datetime.datetime.fromisoformat(text).replace(tzinfo=datetime.timezone.utc)


def checker(pairs, now=None, **kw):
    import yfinance_check as yc

    def history(symbol):
        if isinstance(pairs, Exception):
            raise pairs
        return pairs
    args = dict(history=history, sleep=lambda s: None, **kw)
    if now is not None:
        args["now"] = lambda: utc(now)
    return yc.YfinanceChecker(**args)


def one(pairs, now=None, **kw):
    return checker(pairs, now, **kw).check(["SPY"])["SPY"]


def arms_build():
    setup_paths()
    fails = []
    try:
        # a Saturday run, the newest row (Friday) null: Thursday's close is the answer (T-1 of a Saturday is Thursday)
        got = one([("2026-10-14", 100.0), ("2026-10-15", 101.0), ("2026-10-16", NAN)], "2026-10-17T00:50:00")
        if (got["state"], got["last_close"], got["reason"], got["rows"]) != ("KEPT", 101.0, "HISTORY_ROWS", 3):
            fails.append("a Saturday run with a null Friday row: %r" % (got,))
        # a Saturday run, Friday's close finite: still Thursday (the frontier, not the last row)
        got = one([("2026-10-14", 100.0), ("2026-10-15", 101.0), ("2026-10-16", 102.0)], "2026-10-17T00:50:00")
        if (got["state"], got["last_close"]) != ("KEPT", 101.0):
            fails.append("a Saturday run reads Thursday's close, not Friday's: %r" % (got,))
        # a weekday run never reads that day's own row (Wednesday 2026-10-14: T-1 is Tuesday)
        got = one([("2026-10-12", 97.0), ("2026-10-13", 98.0), ("2026-10-14", 99.0)], "2026-10-14T15:00:00")
        if (got["state"], got["last_close"]) != ("KEPT", 98.0):
            fails.append("a weekday run read the run's own day: %r" % (got,))
        # the day after Labor Day 2026 (Monday 2026-09-07 is a holiday): Tuesday 2026-09-08's T-1 is Friday 2026-09-04
        got = one([("2026-09-03", 49.0), ("2026-09-04", 50.0), ("2026-09-08", NAN)], "2026-09-08T15:00:00")
        if (got["state"], got["last_close"]) != ("KEPT", 50.0):
            fails.append("the day after a holiday: %r" % (got,))
        got = one([("2026-09-03", 49.0), ("2026-09-04", 50.0), ("2026-09-08", 51.0)], "2026-09-08T15:00:00")
        if (got["state"], got["last_close"]) != ("KEPT", 50.0):
            fails.append("the day after a holiday read the run's own day: %r" % (got,))
        # every row after the frontier: nothing at or before T-1
        got = one([("2026-10-16", 102.0)], "2026-10-15T15:00:00")
        if got["state"] != "NOT_KEPT" or got["reason"] != "NO_ROWS":
            fails.append("only rows after T-1: %r" % (got,))
        # the row ON the frontier day is null (Wednesday 2026-10-14: T-1 is Tuesday 2026-10-13): it is dropped, the last finite close before it wins
        got = one([("2026-10-09", 96.0), ("2026-10-12", 97.0), ("2026-10-13", NAN), ("2026-10-14", 99.0)], "2026-10-14T15:00:00")
        if (got["state"], got["last_close"]) != ("KEPT", 97.0):
            fails.append("a null row on the frontier day: %r" % (got,))
        # an interior null row is dropped, the last finite close wins
        got = one([("2026-10-12", 97.0), ("2026-10-13", NAN), ("2026-10-14", 99.0)], "2026-10-16T15:00:00")
        if (got["state"], got["last_close"]) != ("KEPT", 99.0):
            fails.append("an interior null row: %r" % (got,))
    except TypeError as exc:
        fails.append("YfinanceChecker does not take now=: %s" % exc)
    except Exception as exc:  # a check prints what is raised
        fails.append("build arm raised %s: %s" % (type(exc).__name__, exc))
    return fails


def arms_guard():
    setup_paths()
    fails = []
    old = [("2026-01-05", 10.0), ("2026-01-06", 11.0), ("2026-01-07", 12.5)]
    got = one(old)
    if (got["state"], got["last_close"], got["reason"], got["rows"]) != ("KEPT", 12.5, "HISTORY_ROWS", 3):
        fails.append("a good history moved: %r" % (got,))
    got = one([])
    if (got["state"], got["reason"], got["rows"]) != ("NOT_KEPT", "NO_ROWS", 0):
        fails.append("an empty history moved: %r" % (got,))
    got = one([("2026-01-05", 10.0), ("2026-01-06", 0.0)])
    if (got["state"], got["reason"]) != ("NOT_KEPT", "LAST_CLOSE_NOT_POSITIVE"):
        fails.append("a last close of zero moved: %r" % (got,))
    got = one([("2026-01-06", NAN)])
    if (got["state"], got["reason"]) != ("NOT_KEPT", "LAST_CLOSE_NOT_FINITE"):
        fails.append("an only-null history moved: %r" % (got,))
    got = one(RuntimeError("boom"))
    if got["state"] != "CHECK_FAILED":
        fails.append("a raising history is no longer CHECK_FAILED: %r" % (got,))
    many = ["S%02d" % i for i in range(12)]
    out = checker(old, cap=3).check(many)
    states = sorted(set(v["state"] for v in out.values()))
    if sum(1 for v in out.values() if v["state"] == "KEPT") != 3 or "NOT_CHECKED" not in states:
        fails.append("the cap moved: %r" % (states,))
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
        print("AR-G157-%s-%s %s" % (mode.upper(), "FAIL" if fails else "OK", "; ".join(fails)))
        return 1 if fails else 0
    if mode not in ("build", "guard"):
        print("AR-G157-FAIL usage: build | guard | scope | regress")
        return 2
    fails = arms_build() if mode == "build" else arms_guard()
    print("AR-G157-%s %s: %s" % ("FAIL" if fails else "OK", mode, "; ".join(fails) if fails else "all arms"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
