"""IRPT_ANLREQ AR-g-51 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g51_checks.py g51       the price-source chain answers its twelve cases, and the new test file passes
    python ar_g51_checks.py hygiene   the module is ASCII, imports only the allowed standard library names, opens no connection

Prints one RESULT line: AR-G51-OK / AR-G51-FAIL or AR-G51-HYGIENE-OK / AR-G51-HYGIENE-FAIL; rc 0 only on OK. ASCII only.
"""
import ast
import importlib.util
import json
import re
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/ycharts/research/"
MODULE = R + "price_source.py"
TESTS = R + "tests/test_price_source.py"
ALLOWED_IMPORTS = {"__future__", "math", "datetime", "re", "collections", "typing"}
AS_OF = "2026-10-14"


def bad_count(line):
    """Failed tests plus errors named in a pytest summary line."""
    return sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))


def pytest_line(target):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", target],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    lines = [ln for ln in (out.stdout + out.stderr).splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    return out.returncode, line, int(m.group(1)) if m else 0


class Reader:
    """A fake tier: answers from a dict, counts its calls, or raises."""

    def __init__(self, data=None, boom=None):
        self.data, self.boom, self.calls = data or {}, boom, []

    def __call__(self, symbol, start, end):
        self.calls.append(symbol)
        if self.boom is not None:
            raise self.boom
        return self.data.get(symbol, [])


def cases(ps):
    def rows(*pairs):
        return [(d, p) for d, p in pairs]

    d1, d2, d3 = "2026-10-12", "2026-10-13", "2026-10-14"
    out = {}

    # 1: the estate wins when it holds the symbol; the later tiers are never called
    est, yf, yc = Reader({"SPY": rows((d1, 1.0), (d2, 2.0))}), Reader({"SPY": rows((d1, 9.0))}), Reader({"SPY": rows((d1, 8.0))})
    r = ps.resolve_prices(["SPY"], "2026-10-01", AS_OF, {"estate": est, "yfinance": yf, "ycharts": yc}, AS_OF)
    s = r["series"]["SPY"]
    out["estate wins, later tiers uncalled"] = (s["source"] == "estate" and s["status"] == "PRICED" and not yf.calls
                                                and not yc.calls and s["rows"] == [[d1, 1.0], [d2, 2.0]])

    # 2: an empty estate answer falls to yfinance; ycharts is not called
    est, yf, yc = Reader(), Reader({"QQQ": rows((d1, 5.0))}), Reader({"QQQ": rows((d1, 6.0))})
    r = ps.resolve_prices(["QQQ"], "2026-10-01", AS_OF, {"estate": est, "yfinance": yf, "ycharts": yc}, AS_OF)
    s = r["series"]["QQQ"]
    out["empty estate falls to yfinance"] = (s["source"] == "yfinance" and not yc.calls
                                             and [a["outcome"] for a in s["attempts"]] == ["NO_DATA", "DATA"])

    # 3: a raising tier is an ERROR:<class> attempt, its message never appears in the result, the next tier answers
    est, yf, yc = Reader(), Reader(boom=RuntimeError("secret-xyz-token")), Reader({"IWM": rows((d1, 3.0))})
    r = ps.resolve_prices(["IWM"], "2026-10-01", AS_OF, {"estate": est, "yfinance": yf, "ycharts": yc}, AS_OF)
    s = r["series"]["IWM"]
    out["error is typed, message not leaked, next tier answers"] = (
        s["source"] == "ycharts" and s["attempts"][1]["outcome"] == "ERROR:RuntimeError"
        and "secret-xyz-token" not in json.dumps(r))

    # 4: every tier empty -> MISSING, named in the missing list, three attempts, nothing raised
    r = ps.resolve_prices(["ZZZZ"], "2026-10-01", AS_OF, {"estate": Reader(), "yfinance": Reader(), "ycharts": Reader()}, AS_OF)
    s = r["series"]["ZZZZ"]
    out["all empty is MISSING"] = (s["status"] == "MISSING" and s["source"] is None and s["rows"] == []
                                   and r["missing"] == ["ZZZZ"] and len(s["attempts"]) == 3)

    # 5: rows after as_of are dropped; the as_of row is kept; a tier whose only rows are after as_of counts as NO_DATA
    est = Reader({"AAA": rows((d3, 1.0), ("2026-10-15", 2.0), ("2026-10-16", 3.0)), "BBB": rows(("2026-10-15", 1.0))})
    yf = Reader({"BBB": rows((d2, 4.0))})
    r = ps.resolve_prices(["AAA", "BBB"], "2026-10-01", AS_OF, {"estate": est, "yfinance": yf, "ycharts": Reader()}, AS_OF)
    out["cut at as_of"] = (r["series"]["AAA"]["last_date"] == d3 and len(r["series"]["AAA"]["rows"]) == 1
                           and r["series"]["BBB"]["source"] == "yfinance")

    # 6: ycharts is called once per symbol, and only for the symbols the first two tiers lack
    est, yf = Reader({"A1": rows((d1, 1.0))}), Reader({"B1": rows((d1, 1.0))})
    yc = Reader({"C1": rows((d1, 1.0)), "D1": rows((d1, 1.0))})
    ps.resolve_prices(["A1", "B1", "C1", "D1"], "2026-10-01", AS_OF, {"estate": est, "yfinance": yf, "ycharts": yc}, AS_OF)
    out["ycharts one symbol per call, only the lacking"] = sorted(yc.calls) == ["C1", "D1"] and yf.calls == ["B1", "C1", "D1"]

    # 7: an absent tier is a TIER_ABSENT attempt, not an exception
    r = ps.resolve_prices(["SPY"], "2026-10-01", AS_OF, {"estate": Reader()}, AS_OF)
    outcomes = [a["outcome"] for a in r["series"]["SPY"]["attempts"]]
    out["absent tier"] = outcomes == ["NO_DATA", "TIER_ABSENT", "TIER_ABSENT"] and r["series"]["SPY"]["status"] == "MISSING"

    # 8: symbols are stripped, upper-cased and de-duplicated in first-seen order; non-strings and blanks are rejected
    est = Reader({"SPY": rows((d1, 1.0)), "VTI": rows((d1, 2.0))})
    r = ps.resolve_prices([" spy", "SPY", "", None, 5, "vti"], "2026-10-01", AS_OF, {"estate": est}, AS_OF)
    out["symbols normalised"] = (list(r["series"]) == ["SPY", "VTI"] and len(r["rejected"]) == 3 and est.calls == ["SPY", "VTI"])

    # 9: non-positive, NaN, infinite, non-numeric prices and non-string dates are dropped
    est = Reader({"X": rows((d1, 0.0), (d2, float("nan")), (d3, 7.5), ("2026-10-10", -1.0), ("2026-10-09", float("inf")),
                            ("2026-10-08", "n/a"))})
    est.data["X"].append((20261011, 9.0))
    r = ps.resolve_prices(["X"], "2026-10-01", AS_OF, {"estate": est}, AS_OF)
    out["bad rows dropped"] = r["series"]["X"]["rows"] == [[d3, 7.5]]

    # 10: rows come back ascending by date even when a reader answers out of order; a repeated date keeps the later value
    est = Reader({"Y": rows((d3, 3.0), (d1, 1.0), (d2, 2.0), (d2, 2.5))})
    r = ps.resolve_prices(["Y"], "2026-10-01", AS_OF, {"estate": est}, AS_OF)
    s = r["series"]["Y"]
    out["ascending, repeat keeps later"] = (s["rows"] == [[d1, 1.0], [d2, 2.5], [d3, 3.0]]
                                            and s["first_date"] == d1 and s["last_date"] == d3)

    # 11: a bad readers argument or window is a typed ValueError, not a silent default
    def refused(**kw):
        args = {"symbols": ["SPY"], "start": "2026-10-01", "end": AS_OF, "readers": {"estate": Reader()}, "as_of": AS_OF}
        args.update(kw)
        try:
            ps.resolve_prices(**args)
        except ValueError as exc:
            return str(exc)
        except Exception as exc:
            return "WRONG-TYPE:" + type(exc).__name__
        return "NO-REFUSAL"
    out["typed refusals"] = (refused(readers=[Reader()]) == "PRICE_READERS" and refused(start="10/01/2026") == "PRICE_WINDOW"
                             and refused(as_of=None) == "PRICE_WINDOW" and refused(end=20261014) == "PRICE_WINDOW")

    # 12: the result summary names the sources used, sorted, and the window and as_of it was asked for
    est, yf = Reader({"A": rows((d1, 1.0))}), Reader({"B": rows((d1, 1.0))})
    r = ps.resolve_prices(["A", "B"], "2026-10-01", AS_OF, {"estate": est, "yfinance": yf}, AS_OF)
    out["summary"] = (r["sources_used"] == ["estate", "yfinance"] and r["as_of"] == AS_OF
                      and r["window"] == ["2026-10-01", AS_OF] and r["missing"] == [])
    return out


def main(mode):
    if mode == "g51":
        try:
            spec = importlib.util.spec_from_file_location("price_source", MODULE)
            ps = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(ps)
            ps.resolve_prices
            ps.CHAIN
        except Exception as exc:
            print("AR-G51-FAIL import %s: %s" % (type(exc).__name__, str(exc)[:160]))
            return 1
        try:
            got = cases(ps)
        except Exception as exc:
            print("AR-G51-FAIL a case raised %s: %s" % (type(exc).__name__, str(exc)[:200]))
            return 1
        wrong = [k for k, ok in got.items() if not ok]
        chain_ok = tuple(ps.CHAIN) == ("estate", "yfinance", "ycharts")
        rc, line, passed = pytest_line(TESTS)
        print("cases %d, wrong %s, CHAIN %s" % (len(got), wrong or "none", "ok" if chain_ok else "WRONG"))
        print("worker tests: %s" % line)
        if wrong or not chain_ok or rc != 0 or bad_count(line) or passed < 8:
            print("AR-G51-FAIL wrong=%s chain=%s tests rc=%d passed=%d (need >= 8)" % (wrong or "none", chain_ok, rc, passed))
            return 1
        print("AR-G51-OK cases=%d tests=%d" % (len(got), passed))
        return 0
    if mode == "hygiene":
        try:
            with open(MODULE, "rb") as fh:
                raw = fh.read()
        except OSError as exc:
            print("AR-G51-HYGIENE-FAIL no module: %s" % type(exc).__name__)
            return 1
        problems = []
        if any(b > 127 for b in raw):
            problems.append("non-ASCII byte")
        tree = ast.parse(raw.decode("utf-8", errors="replace"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                imported.add((node.module or "").split(".")[0])
        extra = sorted(imported - ALLOWED_IMPORTS)
        if extra:
            problems.append("imports outside the allowed set: %s" % ",".join(extra))
        calls = {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
        for forbidden in ("open", "print", "exec", "eval", "__import__"):
            if forbidden in calls:
                problems.append("calls %s" % forbidden)
        if problems:
            print("AR-G51-HYGIENE-FAIL " + "; ".join(problems))
            return 1
        print("AR-G51-HYGIENE-OK imports=%s" % ",".join(sorted(imported)))
        return 0
    print("usage: ar_g51_checks.py g51|hygiene")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
