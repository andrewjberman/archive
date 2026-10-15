"""IRPT_ANLREQ AR-g-99 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g99_checks.py g99       yahoo_history_days answers 24 direct cases on fakes (the span rule, batching in chunks and the request
                                     count, omitted and empty tickers, a failed request, the chunk guard, the default download over a
                                     fake yfinance, laziness, hygiene, use through swap_replacement), and the six named new tests pass
    python ar_g99_checks.py regress   three existing test files (run one at a time) still pass, 51 tests in all, and the branch changed
                                     only the cell's own files (measured against the merge-base with box/dell2)

Prints one RESULT line: AR-G99-OK / AR-G99-FAIL or AR-G99-REGRESS-OK / AR-G99-REGRESS-FAIL; rc 0 only on OK. ASCII only.
"""
import datetime
import re
import subprocess
import sys
from pathlib import Path

R = "infra/aws/lambda/investor-reporting/"
RES = R + "ycharts/research/"
MODULE = RES + "yahoo_history_days.py"
NEW_TESTS = {
    RES + "tests/test_yahoo_history_days.py": [
        "test_days_of_counts_the_span_and_needs_two_dates",
        "test_prefetch_batches_the_tickers_in_chunks_and_counts_the_requests",
        "test_a_ticker_the_answer_omits_or_leaves_empty_answers_none",
        "test_a_failed_request_raises_for_the_ticker_and_prefetch_tolerates_it",
        "test_the_default_download_reads_each_tickers_close_from_a_frame",
        "test_a_chunk_must_be_a_positive_int",
    ],
}
REGRESS = [RES + "tests/test_price_adapter_yfinance.py", RES + "tests/test_swap_replacement.py", RES + "tests/test_price_source.py"]
MIN_TOTAL = 51
OWN_FILES = (MODULE, RES + "tests/test_yahoo_history_days.py")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")


def bad_count(line):
    return sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))


def pytest_run(targets):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", *targets],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    text = out.stdout + out.stderr
    lines = [ln for ln in text.splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    return out.returncode, line, int(m.group(1)) if m else 0


class Download:
    def __init__(self, table, fail_on=()):
        self.table, self.fail_on, self.asked = table, set(fail_on), []

    def __call__(self, tickers):
        self.asked.append(list(tickers))
        if self.fail_on & set(tickers):
            raise RuntimeError("down")
        return {t: self.table[t] for t in tickers if t in self.table}


class Series:
    def __init__(self, rows):
        self.rows = rows

    def dropna(self):
        return Series([(d, v) for d, v in self.rows if v is not None])

    @property
    def index(self):
        return [datetime.datetime.strptime(d, "%Y-%m-%d") for d, _ in self.rows]


class Frame:
    def __init__(self, table):
        self.table = table

    def __getitem__(self, ticker):
        if ticker not in self.table:
            raise KeyError(ticker)
        return {"Close": Series(self.table[ticker])}


class FakeYf:
    def __init__(self, frame):
        self.frame, self.kwargs, self.calls = frame, [], 0

    def download(self, tickers, **kwargs):
        self.calls += 1
        self.kwargs.append((list(tickers), kwargs))
        return self.frame


def cases():
    sys.path.insert(0, str(Path(RES).resolve()))
    import yahoo_history_days as yh
    import swap_replacement as sr
    out = []

    def case(name, ok, why=""):
        out.append((name, bool(ok), why))

    case("D1-span", yh.days_of(["2020-01-01", "2020-01-31"]) == 30 and yh.days_of(["2019-01-01", "2020-01-01"]) == 365)
    case("D2-unordered-and-repeated", yh.days_of(["2020-03-01", "2020-01-01", "2020-01-01"]) == 60)
    case("D3-fewer-than-two", yh.days_of(["2020-01-01"]) is None and yh.days_of([]) is None and yh.days_of(None) is None and yh.days_of(["2020-01-01", "2020-01-01"]) is None)
    case("D4-bad-dates-ignored", yh.days_of(["x", "2020-01-01", "2020-01-04", "y"]) == 3 and yh.days_of(["x", "y"]) is None)
    case("D5-timestamp-strings", yh.days_of(["2020-01-01 00:00:00", "2020-01-11T00:00:00"]) == 10)
    table = {"T%02d" % i: ["2020-01-01", "2020-01-%02d" % (i + 2)] for i in range(7)}
    port = Download(table)
    days = yh.make_history_days(download=port, chunk=3)
    names = sorted(table)
    days.prefetch(names + names[:2])
    case("C1-chunks", port.asked == [names[0:3], names[3:6], names[6:7]] and days.calls == 3, str(port.asked))
    case("C2-answers-from-the-fetch", days("T00") == 1 and days("T06") == 7 and days.calls == 3)
    days.prefetch(names)
    case("C3-no-refetch", days.calls == 3 and len(port.asked) == 3)
    single = yh.make_history_days(download=Download(table), chunk=50)
    case("C4-an-unfetched-ticker-is-asked-alone-once", single("T01") == 2 and single.calls == 1 and single("T01") == 2 and single.calls == 1)
    om = yh.make_history_days(download=Download({"A": ["2020-01-01", "2021-01-01"], "E": [], "ONE": ["2020-05-05"]}), chunk=10)
    om.prefetch(["A", "E", "ONE", "GONE"])
    case("O1-omitted-empty-one-date", (om("A"), om("E"), om("ONE"), om("GONE")) == (366, None, None, None))
    fport = Download({"A": ["2020-01-01", "2020-02-01"], "B": ["2020-01-01", "2020-03-01"], "C": ["2020-01-01", "2020-04-01"]}, fail_on={"B"})
    fd = yh.make_history_days(download=fport, chunk=1)
    fd.prefetch(["A", "B", "C"])
    case("F1-prefetch-tolerates-a-failed-chunk", fd("A") == 31 and fd("C") == 91 and fd.calls == 3, str(fd.calls))
    try:
        fd("B")
        raised = False
    except RuntimeError:
        raised = True
    case("F2-a-failed-request-raises-for-the-ticker", raised and fd.calls == 4, str(fd.calls))
    case("F3-a-failure-is-not-recorded-as-unpriced", "B" not in fd._days)
    for bad in (0, -1, True, 2.5, "3", None):
        try:
            yh.make_history_days(download=Download({}), chunk=bad)
            ok = False
        except ValueError:
            ok = True
        case("G1-chunk-guard-%r" % (bad,), ok)
    case("G2-default-chunk-is-fifty", yh.DEFAULT_CHUNK == 50)
    fake = FakeYf(Frame({"A": [("2019-12-01", None), ("2020-01-01", 1.0), ("2020-02-01", None), ("2020-03-01", 2.0), ("2020-04-01", None)], "B": [("2020-01-01", None)]}))
    dd = yh.make_history_days(yf=fake, chunk=5)
    dd.prefetch(["A", "B", "C"])
    names_asked, kwargs = fake.kwargs[0]
    case("Y1-default-download-arguments", names_asked == ["A", "B", "C"] and kwargs == {"period": "max", "interval": "1mo", "auto_adjust": False,
                                                                                       "progress": False, "group_by": "ticker", "threads": True}, str(kwargs))
    case("Y2-default-download-reads-close", (dd("A"), dd("B"), dd("C")) == (60, None, None) and fake.calls == 1, str((dd("A"), dd("B"), dd("C"))))
    pool = [{"ticker": t, "asset_class": "equity", "sub_asset_class": "USLargeCap"} for t in ("AAA", "BBB", "CCC")]
    cdl = Download({"AAA": ["2020-01-01", "2020-02-01"], "BBB": ["2015-01-01", "2020-01-01"], "CCC": ["2015-01-01", "2020-01-01"]})
    use = sr.choose_replacement("ZZZ", {"asset_class": "equity", "sub_asset_class": "USLargeCap"}, pool, [], yh.make_history_days(download=cdl))
    case("U1-works-as-the-history-port-of-choose-replacement", use["status"] == "REPLACED" and use["replacement"] == "BBB", str(use.get("replacement")))
    text = Path(MODULE).read_text(encoding="utf-8")
    top_level_yf = [ln for ln in text.splitlines() if re.match(r"(import yfinance|from yfinance)", ln)]
    case("L1-yfinance-imported-only-inside", not top_level_yf, str(top_level_yf))
    banned = [w for w in ("os.environ", "getenv", "print(", "boto3", "import requests", "urllib", "socket", "subprocess", "time.time", "date.today", "datetime.now", "utcnow", "time.sleep", "import random") if w in text]
    case("H1-hygiene", not banned and all(ord(c) < 128 for c in text), str(banned))
    return out


def g99():
    try:
        out = cases()
    except Exception as exc:
        print("AR-G99-FAIL the cases could not run: %s: %s" % (type(exc).__name__, str(exc)[:200]))
        return 1
    failed = [(n, why) for n, ok, why in out if not ok]
    for name, why in failed:
        print("CASE-FAIL", name, why)
    bad = list(failed)
    for path, names in NEW_TESTS.items():
        text = Path(path).read_text(encoding="utf-8") if Path(path).is_file() else ""
        missing = [n for n in names if not re.search(r"^def %s\(" % re.escape(n), text, re.M)]
        if missing:
            bad.append(("missing named tests in " + path, missing))
            continue
        rc, line, passed = pytest_run([path])
        if rc != 0 or bad_count(line) or passed < len(names):
            bad.append(("named tests", line))
    if bad:
        print("AR-G99-FAIL %d of %d cases failed or a named test is missing: %s" % (len(failed), len(out), str(bad)[:300]))
        return 1
    print("AR-G99-OK %d cases, %d named tests pass" % (len(out), sum(len(v) for v in NEW_TESTS.values())))
    return 0


def regress():
    total, bad = 0, []
    for path in REGRESS:
        rc, line, passed = pytest_run([path])
        total += passed
        if rc != 0 or bad_count(line):
            bad.append((Path(path).name, line))
    diff = subprocess.run(["git", "diff", "--name-only", "box/dell2...HEAD"], capture_output=True, text=True).stdout.split()
    folder = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~"
    order = "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-99."
    stray = [p for p in diff if p not in OWN_FILES and not p.startswith(ISSUER) and not p.startswith(folder) and not p.startswith(order)]
    if bad or total < MIN_TOTAL or stray:
        print("AR-G99-REGRESS-FAIL total=%d (want at least %d) bad=%s stray=%s" % (total, MIN_TOTAL, str(bad)[:200], str(stray[:5])))
        return 1
    print("AR-G99-REGRESS-OK %d tests in %d files, %d changed paths all the cell's own" % (total, len(REGRESS), len(diff)))
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "g99":
        sys.exit(g99())
    if mode == "regress":
        sys.exit(regress())
    print("usage: ar_g99_checks.py g99 | regress")
    sys.exit(2)
