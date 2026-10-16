"""IRPT_ANLREQ AR-g-125 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g125_checks.py build   the default yfinance port reads a symbol Yahoo has no data for as a clean empty answer (NOT_KEPT, NO_ROWS): a yfinance ticker-missing
                                     class (by exact name in the MRO) OR a curl_cffi HTTPError (the REAL 0.13.0 classes, loaded from curl_cffi_0_13_0/ beside this file) whose
                                     response status is 404 and whose response URL is the quoteSummary endpoint of a *.finance.yahoo.com host naming THIS symbol as the last path
                                     segment (URL-decoded); hide_exceptions is restored; the worker's fixtures equal the issuer's and the test file uses them
    python ar_g125_checks.py guard   everything else stays CHECK_FAILED: 401, 403, 429 and a rate-limit class (PUSHBACK, the step stops), a 404 on another symbol's URL, on
                                     another endpoint, on another host, with no URL or no response object, a lookalike HTTPError from another module, 500 and 503, a curl_cffi
                                     Timeout (TIMEOUT), ConnectionError and DNSError, a data error and a plain error (EXCEPTION); and SPY rows read KEPT
    python ar_g125_checks.py regress each existing test file run on its own, then the scope check
    python ar_g125_checks.py scope   the branch changed only the checker, its test file, its fixtures, the order and the worker's folder (against the merge-base with box/dell2)

Prints one RESULT line: AR-G125-OK / AR-G125-FAIL (or -REGRESS- / -SCOPE-); rc 0 only on OK. ASCII only.
"""
import importlib.util
import subprocess
import sys
import tempfile
import types
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
YF_EXC_FILE = HERE / "yfinance_exceptions_1_2_0.py"
CURL_DIR = HERE / "curl_cffi_0_13_0"
IR = "infra/aws/lambda/investor-reporting/intake/"
CHECKER = IR + "yfinance_check.py"
TEST = IR + "tests/test_yfinance_check.py"
FIX_YF = IR + "tests/fixtures/yfinance_exceptions_1_2_0.py"
FIX_CURL = IR + "tests/fixtures/curl_cffi_0_13_0"
ORDER = "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-125.checker-symbol-404-is-not-kept.md"
OWN = (CHECKER, TEST, FIX_YF, ORDER)
OWN_PREFIX = (FIX_CURL + "/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~260/",
              "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/", "org/tier2_senior/0.7.0_AE_CloudOps~AQ2/task_orders/")
REGRESS_FILES = (TEST, IR + "tests/test_kept_holding.py",
                 "infra/aws/lambda/investor-reporting/ycharts/session/tests/test_resident_session_checker.py")
GOOD_URL = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/%s?modules=financialData%%2CquoteType&corsDomain=finance.yahoo.com&formatted=false&symbol=%s&crumb=abc"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_curl():
    """The REAL curl_cffi 0.13.0 exception classes: the fixture's .pyfix members are copied to a temp folder as .py (see the fixture README) and imported from there."""
    tmp = Path(tempfile.mkdtemp(prefix="g125_curl_"))
    for src in CURL_DIR.rglob("*.pyfix"):
        dst = tmp / src.relative_to(CURL_DIR).with_suffix(".py")
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())
    sys.path.insert(0, str(tmp))
    try:
        import curl_cffi.requests.exceptions as mod
    finally:
        sys.path.remove(str(tmp))
    return mod


class Response:
    """The part of curl_cffi.requests.Response that raise_for_status uses (models.py, 0.13.0): HTTPError(f"HTTP Error {status}: {reason}", 0, self)."""

    def __init__(self, curl, status, url, reason=""):
        self.curl, self.status_code, self.url, self.reason = curl, status, url, reason

    @property
    def ok(self):
        return 200 <= self.status_code < 400

    def raise_for_status(self):
        if not self.ok:
            raise self.curl.HTTPError("HTTP Error %s: %s" % (self.status_code, self.reason), 0, self)


def http_error(curl, status, url):
    try:
        Response(curl, status, url).raise_for_status()
    except curl.HTTPError as err:
        return err
    raise AssertionError("no error raised")


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


def tree(root):
    root = Path(root)
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file() and "__pycache__" not in p.parts}


def arms_build(checker_mod, yf_exc, curl):
    fails = []
    cases = [("YFTzMissingError", "ZQXWVK", lambda: yf_exc.YFTzMissingError("ZQXWVK")),
             ("YFPricesMissingError", "ZQXWVK", lambda: yf_exc.YFPricesMissingError("ZQXWVK", "(1mo)")),
             ("curl_cffi HTTPError 404 on quoteSummary/ZQXWVK", "ZQXWVK", lambda: http_error(curl, 404, GOOD_URL % ("ZQXWVK", "ZQXWVK"))),
             ("curl_cffi HTTPError 404 on quoteSummary/%5EZQXW (the symbol URL-encoded)", "^ZQXW", lambda: http_error(curl, 404, GOOD_URL % ("%5EZQXW", "%5EZQXW"))),
             ("curl_cffi HTTPError 404, host query1.finance.yahoo.com, lowercase path symbol", "ZQXWVK",
              lambda: http_error(curl, 404, "https://query1.finance.yahoo.com/v10/finance/quoteSummary/zqxwvk?modules=x"))]
    for label, symbol, make in cases:
        try:
            out, module = run_check(checker_mod, lambda s, make=make: ("raise", make()), [symbol])
        except Exception as err:
            fails.append("%s raised out of check(): %r" % (label, err))
            continue
        row = out.get(symbol, {})
        if not (row.get("state") == "NOT_KEPT" and row.get("reason") == "NO_ROWS" and row.get("rows") == 0):
            fails.append("%s read %r (want NOT_KEPT NO_ROWS 0 rows)" % (label, row))
        if module.config.debug.hide_exceptions is not True:
            fails.append("%s left hide_exceptions at %r (want restored True)" % (label, module.config.debug.hide_exceptions))
    fix_yf, fix_curl = Path(FIX_YF), Path(FIX_CURL)
    if not fix_yf.is_file() or fix_yf.read_bytes() != YF_EXC_FILE.read_bytes():
        fails.append("the yfinance exceptions fixture is absent or differs from the issuer's")
    if not fix_curl.is_dir() or tree(fix_curl) != tree(CURL_DIR):
        fails.append("the curl_cffi fixture folder %s is absent or differs from the issuer's curl_cffi_0_13_0" % FIX_CURL)
    text = Path(TEST).read_text(encoding="utf-8") if Path(TEST).is_file() else ""
    if "curl_cffi_0_13_0" not in text or "yfinance_exceptions_1_2_0" not in text:
        fails.append("the test file does not load both real-class fixtures")
    return fails


def arms_guard(checker_mod, yf_exc, curl):
    fails = []

    class Lookalike(Exception):
        pass

    Lookalike.__name__ = "HTTPError"
    Lookalike.__module__ = "other.lib"
    deco = Lookalike("HTTP Error 404: ")
    deco.response = Response(curl, 404, GOOD_URL % ("ZQXWVK", "ZQXWVK"))
    no_url = http_error(curl, 404, GOOD_URL % ("ZQXWVK", "ZQXWVK"))
    no_url.response.url = None
    no_response = curl.HTTPError("HTTP Error 404: ", 0, None)
    cases = [("rate limit class", yf_exc.YFRateLimitError(), "PUSHBACK"),
             ("HTTP 429 on the symbol URL", http_error(curl, 429, GOOD_URL % ("ZQXWVK", "ZQXWVK")), "PUSHBACK"),
             ("HTTP 401 on the symbol URL", http_error(curl, 401, GOOD_URL % ("ZQXWVK", "ZQXWVK")), "PUSHBACK"),
             ("HTTP 403 on the symbol URL", http_error(curl, 403, GOOD_URL % ("ZQXWVK", "ZQXWVK")), "PUSHBACK"),
             ("HTTP 404 on ANOTHER symbol's quoteSummary URL", http_error(curl, 404, GOOD_URL % ("OTHER", "OTHER")), "EXCEPTION"),
             ("HTTP 404 on the chart endpoint of the same symbol", http_error(curl, 404, "https://query2.finance.yahoo.com/v8/finance/chart/ZQXWVK?range=1mo"), "EXCEPTION"),
             ("HTTP 404 from a host that is not finance.yahoo.com", http_error(curl, 404, "https://evil.example.com/v10/finance/quoteSummary/ZQXWVK"), "EXCEPTION"),
             ("HTTP 404 whose response has no URL", no_url, "EXCEPTION"),
             ("HTTP 404 with no response object", no_response, "EXCEPTION"),
             ("a lookalike HTTPError from another module, 404 on the right URL", deco, "EXCEPTION"),
             ("HTTP 500 on the symbol URL", http_error(curl, 500, GOOD_URL % ("ZQXWVK", "ZQXWVK")), "EXCEPTION"),
             ("HTTP 503 on the symbol URL", http_error(curl, 503, GOOD_URL % ("ZQXWVK", "ZQXWVK")), "EXCEPTION"),
             ("curl_cffi Timeout", curl.Timeout("timed out"), "TIMEOUT"),
             ("curl_cffi ConnectionError", curl.ConnectionError("reset"), "EXCEPTION"),
             ("curl_cffi DNSError", curl.DNSError("no such host"), "EXCEPTION"),
             ("a yfinance data error", yf_exc.YFDataException("*** YAHOO! FINANCE IS CURRENTLY DOWN! ***"), "EXCEPTION"),
             ("a plain error", RuntimeError("boom"), "EXCEPTION")]
    for label, err, reason in cases:
        out, _ = run_check(checker_mod, lambda s, err=err: ("raise", err), ["ZQXWVK", "ABCDEF"])
        row = out.get("ZQXWVK", {})
        if not (row.get("state") == "CHECK_FAILED" and row.get("reason") == reason):
            fails.append("%s read %r (want CHECK_FAILED %s)" % (label, row, reason))
        if reason == "PUSHBACK" and out.get("ABCDEF", {}).get("reason") != "STEP_STOPPED":
            fails.append("%s did not stop the step: %r" % (label, out.get("ABCDEF")))
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
        print("AR-G125-%s-%s %s" % (mode.upper(), "FAIL" if fails else "OK", "; ".join(fails)))
        return 1 if fails else 0
    if mode not in ("build", "guard"):
        print("AR-G125-FAIL usage: build | guard | scope | regress")
        return 2
    checker_mod = load("yfinance_check_under_test", CHECKER)
    yf_exc = load("yfinance_exceptions_real", YF_EXC_FILE)
    curl = load_curl()
    fails = arms_build(checker_mod, yf_exc, curl) if mode == "build" else arms_guard(checker_mod, yf_exc, curl)
    print("AR-G125-%s %s: %s" % ("FAIL" if fails else "OK", mode, "; ".join(fails) if fails else "all arms"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
