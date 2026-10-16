"""IRPT_ANLREQ AR-g-121 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g121_checks.py build   the default yfinance port reads a TICKER-MISSING exception (the real yfinance 1.2.0 classes, loaded from
                                     yfinance_exceptions_1_2_0.py beside this file) as a clean empty answer: NOT_KEPT, reason NO_ROWS; the port restores
                                     hide_exceptions; the worker's test fixture is byte-equal to that file and the test file uses it
    python ar_g121_checks.py guard   every other exception stays CHECK_FAILED (rate limit PUSHBACK and the step stops; a data error, a plain
                                     error, a connection error and a lookalike class name are EXCEPTION), and SPY rows read KEPT
    python ar_g121_checks.py scope   the branch changed only the checker, its test file and its test fixture (against the merge-base with box/dell2)

Prints one RESULT line: AR-G121-OK / AR-G121-FAIL (or -SCOPE-); rc 0 only on OK. ASCII only.
"""
import importlib.util
import subprocess
import sys
import types
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
EXC_FILE = HERE / "yfinance_exceptions_1_2_0.py"
IR = "infra/aws/lambda/investor-reporting/intake/"
CHECKER = IR + "yfinance_check.py"
TEST = IR + "tests/test_yfinance_check.py"
FIXTURE = IR + "tests/fixtures/yfinance_exceptions_1_2_0.py"
OWN = (CHECKER, TEST, FIXTURE, "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-121.checker-ticker-missing-is-not-kept.md")
WORKER_PREFIXES = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~258/",
                   "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fake_yfinance(behaviour):
    module = types.ModuleType("yfinance")
    module.config = SimpleNamespace(debug=SimpleNamespace(hide_exceptions=True))
    shared = types.ModuleType("yfinance.shared")
    shared._ERRORS = {}
    module.shared = shared

    class _Frame:
        def __init__(self, rows):
            self.rows = rows

        def __len__(self):
            return len(self.rows)

        @property
        def columns(self):
            return ["Close"]

        @property
        def index(self):
            return ["%s 00:00:00-04:00" % day for day, _ in self.rows]

        def __getitem__(self, name):
            return [close for _, close in self.rows]

    class Ticker:
        def __init__(self, symbol):
            self.symbol = symbol

        def history(self, period, auto_adjust):
            kind, payload = behaviour(self.symbol)
            if kind == "rows":
                return _Frame(payload)
            if kind == "raise":
                if not module.config.debug.hide_exceptions:
                    raise payload
                return _Frame([])
            return _Frame([])

    module.Ticker = Ticker
    return module


def run_check(checker_mod, behaviour, symbols):
    module = fake_yfinance(behaviour)
    saved = sys.modules.get("yfinance")
    sys.modules["yfinance"] = module
    try:
        out = checker_mod.YfinanceChecker(sleep=lambda s: None).check(symbols)
    finally:
        if saved is None:
            sys.modules.pop("yfinance", None)
        else:
            sys.modules["yfinance"] = saved
    return out, module


def arms_build(checker_mod, exc):
    fails = []
    for label, make in (("YFTzMissingError", lambda: exc.YFTzMissingError("ZQXWVK")),
                        ("YFPricesMissingError", lambda: exc.YFPricesMissingError("ZQXWVK", "(1mo)"))):
        try:
            out, module = run_check(checker_mod, lambda s, make=make: ("raise", make()), ["ZQXWVK"])
        except Exception as err:  # the base port lets the exception out of check() only for CheckerUnavailable; anything else is a defect
            fails.append("%s raised out of check(): %r" % (label, err))
            continue
        row = out.get("ZQXWVK", {})
        if not (row.get("state") == "NOT_KEPT" and row.get("reason") == "NO_ROWS" and row.get("rows") == 0):
            fails.append("%s read %r (want NOT_KEPT NO_ROWS 0 rows)" % (label, row))
        if module.config.debug.hide_exceptions is not True:
            fails.append("%s left hide_exceptions at %r (want restored True)" % (label, module.config.debug.hide_exceptions))
    if not Path(FIXTURE).is_file():
        fails.append("the test fixture %s is absent" % FIXTURE)
    elif Path(FIXTURE).read_bytes() != EXC_FILE.read_bytes():
        fails.append("the test fixture differs from the real yfinance 1.2.0 exceptions module")
    if not Path(TEST).is_file() or "yfinance_exceptions_1_2_0" not in Path(TEST).read_text(encoding="utf-8"):
        fails.append("the test file does not load the real-class fixture")
    return fails


def arms_guard(checker_mod, exc):
    fails = []

    class YFTickerMissingErrorLike(ValueError):
        pass

    cases = [("rate limit", exc.YFRateLimitError(), "CHECK_FAILED", "PUSHBACK"),
             ("data exception", exc.YFDataException("*** YAHOO! FINANCE IS CURRENTLY DOWN! ***"), "CHECK_FAILED", "EXCEPTION"),
             ("plain error", RuntimeError("boom"), "CHECK_FAILED", "EXCEPTION"),
             ("connection error", ConnectionError("reset by peer"), "CHECK_FAILED", "EXCEPTION"),
             ("lookalike class name", YFTickerMissingErrorLike("not the yfinance class"), "CHECK_FAILED", "EXCEPTION")]
    for label, err, state, reason in cases:
        out, _ = run_check(checker_mod, lambda s, err=err: ("raise", err), ["ZQXWVK", "ABCDEF"])
        row = out.get("ZQXWVK", {})
        if not (row.get("state") == state and row.get("reason") == reason):
            fails.append("%s read %r (want %s %s)" % (label, row, state, reason))
        if label == "rate limit" and out.get("ABCDEF", {}).get("reason") != "STEP_STOPPED":
            fails.append("a rate limit did not stop the step: %r" % (out.get("ABCDEF"),))
    out, _ = run_check(checker_mod, lambda s: ("rows", [("2026-09-%02d" % d, 100.0 + d) for d in range(1, 23)]), ["SPY"])
    if out.get("SPY", {}).get("state") != "KEPT" or out["SPY"].get("reason") != "HISTORY_ROWS" or out["SPY"].get("rows") != 22:
        fails.append("SPY rows read %r (want KEPT HISTORY_ROWS 22)" % (out.get("SPY"),))
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
    stray = [n for n in names if n not in OWN and not n.startswith(ISSUER + WORKER_PREFIXES)]
    return ["outside the cell's write set: %s" % ", ".join(stray)] if stray else []


REGRESS_FILES = (TEST, IR + "tests/test_kept_holding.py",
                 "infra/aws/lambda/investor-reporting/ycharts/session/tests/test_resident_session_checker.py")


def regress():
    """Each existing test file on its own (one process each), then the scope check."""
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
        print("AR-G121-%s-%s %s" % (mode.upper(), "FAIL" if fails else "OK", "; ".join(fails)))
        return 1 if fails else 0
    if mode not in ("build", "guard"):
        print("AR-G121-FAIL usage: build | guard | scope | regress")
        return 2
    checker_mod = load("yfinance_check_under_test", CHECKER)
    exc = load("yfinance_exceptions_real", EXC_FILE)
    fails = arms_build(checker_mod, exc) if mode == "build" else arms_guard(checker_mod, exc)
    print("AR-G121-%s %s: %s" % ("FAIL" if fails else "OK", mode, "; ".join(fails) if fails else "all arms"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
