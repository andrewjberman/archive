"""IRPT_ANLREQ AR-g-81..84 checks (issuer 2.0.0_SA_COO~G2): the four price adapters. Run from the worktree root.

    python ar_g8x_checks.py g81|g82|g83|g84       the adapter answers its direct cases with fakes, and its own new test file passes (6 or more)
    python ar_g8x_checks.py hygiene81|...|hygiene84   ASCII; top-level imports only the allowed standard library names and tr_level;
                                                  nested imports only pandas, pyarrow, yfinance, io, json, time; no open/print/exec/eval

Prints one RESULT line: AR-G8x-OK / AR-G8x-FAIL or AR-G8x-HYGIENE-OK / AR-G8x-HYGIENE-FAIL; rc 0 only on OK. ASCII only.
"""
import ast
import datetime
import importlib.util
import re
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/ycharts/research/"
MODS = {"81": ("price_adapter_bbg", "test_price_adapter_bbg"), "82": ("price_adapter_demque", "test_price_adapter_demque"),
        "83": ("price_adapter_yfinance", "test_price_adapter_yfinance"), "84": ("price_adapter_ycharts", "test_price_adapter_ycharts")}
TOP_OK = {"__future__", "math", "re", "datetime", "time", "bisect", "collections", "typing", "sys", "os", "tr_level"}
NESTED_OK = {"pandas", "pyarrow", "yfinance", "io", "json", "time"}
D1, D2, D3, D4 = "2026-10-12", "2026-10-13", "2026-10-14", "2026-10-15"


def bad_count(line):
    return sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))


def pytest_line(target):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", target],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    lines = [ln for ln in (out.stdout + out.stderr).splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    return out.returncode, line, int(m.group(1)) if m else 0


def close(a, b):
    return abs(a - b) <= 1e-9 * max(1.0, abs(b))


def levels_match(got, want):
    return (isinstance(got, list) and len(got) == len(want)
            and all(tuple(g)[0] == w[0] and close(tuple(g)[1], w[1]) for g, w in zip(got, want)))


def ms(day):
    return int((datetime.date.fromisoformat(day) - datetime.date(1970, 1, 1)).days * 86400000)


class Boom:
    """A client that must not be touched."""

    def __getattr__(self, name):
        raise AssertionError("the injected client was used: " + name)


def cases81(m):
    pct = "DAY_TO_DAY_TOT_RETURN_GROSS_DVDS"

    def row(day, sec, p, last=100.0):
        return {"date": day, "security": sec, "PX_LAST": last, pct: p}
    part1 = (D1, [row(D1, "SPY US Equity", 0.5), row(D2, "SPY US Equity", 1.0), row(D1, "QQQ US Equity", 9.0)])
    part2 = (D2, [row(D3, "SPY US Equity", -2.0), row(D2, "QQQ US Equity", 1.0)])
    reader = m.make_reader(Boom(), partitions=[part1, part2])
    out = {}
    out["levels chain the percent / 100"] = levels_match(reader("SPY", D1, D4), [(D1, 100.0), (D2, 101.0), (D3, 98.98)])
    out["case and blanks in the symbol"] = levels_match(reader(" spy ", D1, D4), [(D1, 100.0), (D2, 101.0), (D3, 98.98)])
    out["the window cuts before chaining"] = levels_match(reader("SPY", D2, D3), [(D2, 100.0), (D3, 98.0)])
    out["another security is not mixed in"] = levels_match(reader("QQQ", D1, D4), [(D1, 100.0), (D2, 101.0)])
    out["an unknown symbol is []"] = reader("ZZZ", D1, D4) == []
    later = m.make_reader(Boom(), partitions=[(D1, [row(D1, "SPY US Equity", 0.0), row(D2, "SPY US Equity", 10.0)]),
                                              (D2, [row(D2, "SPY US Equity", 1.0)])])
    out["a later partition wins for the same security and date"] = levels_match(later("SPY", D1, D4), [(D1, 100.0), (D2, 101.0)])
    nulls = m.make_reader(Boom(), partitions=[(D1, [row(D1, "SPY US Equity", None), row(D2, "SPY US Equity", float("nan")),
                                                    row(D3, "SPY US Equity", 2.0), row(D4, "SPY US Equity", 1.0)])])
    out["null and NaN percents never seed the base"] = levels_match(nulls("SPY", D1, D4), [(D3, 100.0), (D4, 101.0)])
    try:
        m.make_reader(None)("SPY", D1, D4)
        refused = "NO-REFUSAL"
    except ValueError as exc:
        refused = str(exc)
    out["no source is a typed refusal"] = refused == "BBG_SOURCE"
    return out


def cases82(m):
    def idx(cusip, sym, vfrom, vto):
        return {"cusip": cusip, "yahoo_symbol": sym, "valid_from": vfrom, "valid_to": vto}

    def px(day, r):
        return {"date": day, "total_return": r}
    index_rows = [idx("222222222", "SPY", "2020-01-02", None), idx("111111111", "SPY", "2000-01-01", "2020-01-01"),
                  idx("333333333", "QQQ", "2000-01-01", None)]
    prices = {"111111111": [px(D1, 0.5), px(D2, 0.5)], "222222222": [px(D1, None), px(D2, 0.01), px(D3, 0.01), px(D4, -0.02)],
              "333333333": [px(D1, 0.0), px(D2, float("nan")), px(D3, 0.10)]}
    out = {}
    reader = m.make_reader(Boom(), index_rows=index_rows, price_rows=prices)
    out["the open index row's store is read, total_return is a fraction"] = levels_match(
        reader("SPY", D1, D4), [(D2, 100.0), (D3, 101.0), (D4, 98.98)])
    out["case and blanks in the symbol"] = levels_match(reader(" spy", D1, D4), [(D2, 100.0), (D3, 101.0), (D4, 98.98)])
    out["the window cuts before chaining"] = levels_match(reader("SPY", D3, D4), [(D3, 100.0), (D4, 98.0)])
    out["a NaN return never seeds and is dropped"] = levels_match(reader("QQQ", D1, D4), [(D1, 100.0), (D3, 110.0)])
    calls = []

    class Prices(dict):
        def __getitem__(self, k):
            calls.append(k)
            return dict.__getitem__(self, k)
    spy = m.make_reader(Boom(), index_rows=index_rows, price_rows=Prices(prices))
    spy("NOPE", D1, D4)
    out["an unknown symbol is [] with no price read"] = spy("NOPE", D1, D4) == [] and calls == []
    try:
        m.make_reader(None)("SPY", D1, D4)
        refused = "NO-REFUSAL"
    except ValueError as exc:
        refused = str(exc)
    out["no source is a typed refusal"] = refused == "DEMQUE_SOURCE"
    out["rows are (date, float) tuples"] = all(isinstance(r[0], str) and isinstance(r[1], float) for r in reader("SPY", D1, D4))
    return out


def cases83(m):
    def row(day, close_, div=0.0, split=0.0):
        return {"date": day, "Close": close_, "Dividends": div, "Stock Splits": split}
    out = {}
    plain = m.make_reader(fetch=lambda s: [row(D1, 100.0), row(D2, 101.0), row(D3, 102.01)])
    out["the first row seeds the base, later rows chain the daily return"] = levels_match(plain("SPY", D1, D4), [(D1, 100.0), (D2, 101.0), (D3, 102.01)])
    divs = m.make_reader(fetch=lambda s: [row(D1, 100.0), row(D2, 101.0, div=1.0), row(D3, 102.0)])
    out["a dividend adds to the day's return"] = levels_match(divs("SPY", D1, D4), [(D1, 100.0), (D2, 102.0), (D3, 102.0 * 102.0 / 102.0 * (102.0 / 101.0))])
    split = m.make_reader(fetch=lambda s: [row(D1, 50.0), row(D2, 51.0, split=2.0), row(D3, 51.51)])
    out["served split-adjusted Close: a 2-for-1 split on D2 is undone (D1 served 50 is 100 as traded)"] = levels_match(
        split("SPY", D1, D4), [(D1, 100.0), (D2, 102.0), (D3, 102.0 * (51.51 / 51.0))])
    mixed = m.make_reader(fetch=lambda s: [row(D1, 50.0), row(D2, 50.0, div=0.5), row(D3, 51.0, split=2.0), row(D4, 51.51)])
    out["a served dividend dated before a later split is undone to as traded"] = levels_match(
        mixed("SPY", D1, D4), [(D1, 100.0), (D2, 101.0), (D3, 101.0 * 1.02), (D4, 101.0 * 1.02 * (51.51 / 51.0))])
    gap = m.make_reader(fetch=lambda s: [row(D1, 50.0), row(D2, None, split=2.0), row(D3, 51.51)])
    out["a split on a dropped bad-Close row still counts for the return across the gap"] = levels_match(
        gap("SPY", D1, D4), [(D1, 100.0), (D3, 103.02)])
    zero = m.make_reader(fetch=lambda s: [row(D1, 100.0, split=0.0), row(D2, 110.0, split=float("nan")), row(D3, 99.0, split=None)])
    out["a zero, NaN or missing split ratio counts as 1"] = levels_match(zero("SPY", D1, D4), [(D1, 100.0), (D2, 110.0), (D3, 99.0)])
    bad = m.make_reader(fetch=lambda s: [row(D1, 100.0), row(D2, None), row(D3, -5.0), row(D4, 110.0)])
    out["a bad Close row is dropped and the next return spans the gap"] = levels_match(bad("SPY", D1, D4), [(D1, 100.0), (D4, 110.0)])
    out["the window cuts before chaining"] = levels_match(plain("SPY", D2, D3), [(D2, 100.0), (D3, 101.0)])
    seen = []
    watch = m.make_reader(fetch=lambda s: seen.append(s) or [row(D1, 1.0)])
    watch(" spy ", D1, D4)
    out["the symbol is stripped and upper-cased"] = seen == ["SPY"]

    def boom(symbol):
        raise RuntimeError("secret-xyz-token")
    try:
        m.make_reader(fetch=boom)("SPY", D1, D4)
        raised = "NO-RAISE"
    except RuntimeError:
        raised = "raised"
    out["a fetch error propagates (the chain types it)"] = raised == "raised"

    class Frame:
        def reset_index(self):
            return self

        def to_dict(self, kind):
            assert kind == "records"
            return [{"Date": datetime.datetime(2026, 10, 12), "Close": 100.0, "Dividends": 0.0, "Stock Splits": 0.0},
                    {"Date": datetime.datetime(2026, 10, 13), "Close": 101.0, "Dividends": 0.0, "Stock Splits": 0.0}]

    class FakeTicker:
        def __init__(self, symbol):
            self.symbol = symbol

        def history(self, **kw):
            assert kw.get("auto_adjust") is False and kw.get("actions") is True
            return Frame()

    class YF:
        Ticker = FakeTicker
    out["a yfinance-like module is used with auto_adjust False and actions True"] = levels_match(
        m.make_reader(yf=YF)("SPY", D1, D4), [(D1, 100.0), (D2, 101.0)])
    return out


def cases84(m):
    def answer(points):
        return {"chart_data": [[{"raw_data": points}]]}
    calls, naps = [], []

    def transport(path, params):
        calls.append((path, dict(params)))
        return answer([[ms(D1), 50.0], [ms(D2), 55.0], [ms(D3), 49.5], [ms(D4), 0.0]])
    out = {}
    reader = m.make_reader(transport, sleep=naps.append)
    got = reader(" spy", D1, D4)
    out["levels become a base-100 total-return series, first row seeds"] = levels_match(got, [(D1, 100.0), (D2, 110.0), (D3, 99.0)])
    out["one call per symbol, the fund_data path, max zoom, the id form"] = (
        len(calls) == 1 and calls[0][0] == "/charts/fund_data.json" and calls[0][1].get("zoom") == "max"
        and calls[0][1].get("securities") == "id:SPY,include:true,")
    out["no sleep before the first call"] = naps == []
    reader("QQQ", D1, D4)
    out["the 2 s spacing sleeps before the second call"] = naps == [2.0] and len(calls) == 2
    out["the window cuts before chaining"] = levels_match(reader("SPY", D2, D3), [(D2, 100.0), (D3, 90.0)])
    blank_calls = len(calls)
    out["a blank symbol is [] with no call"] = reader("  ", D1, D4) == [] and len(calls) == blank_calls
    odd = m.make_reader(lambda p, q: {"nothing": 1}, sleep=lambda s: None)
    out["a malformed answer is []"] = odd("SPY", D1, D4) == []

    def boom(path, params):
        raise RuntimeError("secret-xyz-token")
    try:
        m.make_reader(boom, sleep=lambda s: None)("SPY", D1, D4)
        raised = "NO-RAISE"
    except RuntimeError:
        raised = "raised"
    out["a transport error propagates (the chain types it)"] = raised == "raised"
    return out


CASES = {"81": cases81, "82": cases82, "83": cases83, "84": cases84}


def hygiene(num):
    name = MODS[num][0]
    try:
        with open(R + name + ".py", "rb") as fh:
            raw = fh.read()
    except OSError as exc:
        print("AR-G%s-HYGIENE-FAIL no module: %s" % (num, type(exc).__name__))
        return 1
    problems = []
    if any(b > 127 for b in raw):
        problems.append("non-ASCII byte")
    tree = ast.parse(raw.decode("utf-8", errors="replace"))
    top = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            top |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            top.add((node.module or "").split(".")[0])
    nested = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Import):
                    nested |= {a.name.split(".")[0] for a in sub.names}
                elif isinstance(sub, ast.ImportFrom):
                    nested.add((sub.module or "").split(".")[0])
    if top - TOP_OK:
        problems.append("top-level imports outside the allowed set: %s" % ",".join(sorted(top - TOP_OK)))
    if nested - NESTED_OK - TOP_OK:
        problems.append("nested imports outside the allowed set: %s" % ",".join(sorted(nested - NESTED_OK - TOP_OK)))
    calls = {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    for forbidden in ("open", "print", "exec", "eval", "__import__"):
        if forbidden in calls:
            problems.append("calls %s" % forbidden)
    if problems:
        print("AR-G%s-HYGIENE-FAIL %s" % (num, "; ".join(problems)))
        return 1
    print("AR-G%s-HYGIENE-OK top=%s nested=%s" % (num, ",".join(sorted(top)), ",".join(sorted(nested)) or "none"))
    return 0


def main(mode):
    m = re.fullmatch(r"(g|hygiene)(8[1-4])", mode or "")
    if not m:
        print("usage: ar_g8x_checks.py g81|g82|g83|g84|hygiene81|hygiene82|hygiene83|hygiene84")
        return 2
    kind, num = m.group(1), m.group(2)
    if kind == "hygiene":
        return hygiene(num)
    name, test = MODS[num]
    sys.path[:0] = [R]
    try:
        spec = importlib.util.spec_from_file_location(name, R + name + ".py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.make_reader
    except Exception as exc:
        print("AR-G%s-FAIL import %s: %s" % (num, type(exc).__name__, str(exc)[:160]))
        return 1
    try:
        got = CASES[num](mod)
    except Exception as exc:
        print("AR-G%s-FAIL a case raised %s: %s" % (num, type(exc).__name__, str(exc)[:200]))
        return 1
    wrong = [k for k, ok in got.items() if not ok]
    rc, line, passed = pytest_line(R + "tests/" + test + ".py")
    print("cases %d, wrong %s" % (len(got), wrong or "none"))
    print("worker tests: %s" % line)
    if wrong or rc != 0 or bad_count(line) or passed < 6:
        print("AR-G%s-FAIL wrong=%s tests rc=%d passed=%d (need >= 6)" % (num, wrong or "none", rc, passed))
        return 1
    print("AR-G%s-OK cases=%d tests=%d" % (num, len(got), passed))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
