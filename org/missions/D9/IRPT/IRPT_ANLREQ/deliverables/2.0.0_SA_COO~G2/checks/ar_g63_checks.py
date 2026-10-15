"""IRPT_ANLREQ AR-g-63 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g63_checks.py g63       the portfolio-series module answers its twelve cases, and the new test file passes
    python ar_g63_checks.py hygiene   the module is ASCII, imports only the allowed standard library names, opens no connection

Prints one RESULT line: AR-G63-OK / AR-G63-FAIL or AR-G63-HYGIENE-OK / AR-G63-HYGIENE-FAIL; rc 0 only on OK. ASCII only.
"""
import ast
import datetime
import importlib.util
import re
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/ycharts/research/"
MODULE = R + "portfolio_series.py"
TESTS = R + "tests/test_portfolio_series.py"
ALLOWED_IMPORTS = {"__future__", "math", "datetime", "re", "bisect", "collections", "typing", "calendar"}


def bad_count(line):
    return sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))


def pytest_line(target):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", target],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    lines = [ln for ln in (out.stdout + out.stderr).splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    return out.returncode, line, int(m.group(1)) if m else 0


def ms(day):
    d = datetime.date.fromisoformat(day)
    return int((d - datetime.date(1970, 1, 1)).days * 86400000)


def close(a, b):
    return abs(a - b) <= 1e-9 * max(1.0, abs(b))


def cases(ps):
    d1, d2, d3, d4 = "2026-10-12", "2026-10-13", "2026-10-14", "2026-10-15"
    out = {}

    # 1: to_epoch_ms is UTC midnight in milliseconds; 1970-01-01 is 0
    out["epoch ms"] = ps.to_epoch_ms("1970-01-01") == 0 and ps.to_epoch_ms(d1) == ms(d1)
    # 2: a bad date is a typed refusal, not a default
    refused = []
    for bad in ("2026-13-45", "10/12/2026", None, 20261012, ""):
        try:
            ps.to_epoch_ms(bad)
            refused.append("NO-REFUSAL")
        except ValueError as exc:
            refused.append(str(exc))
        except Exception as exc:
            refused.append("WRONG-TYPE:" + type(exc).__name__)
    out["bad date refused"] = refused == ["SERIES_DATE"] * 5
    # 3: to_pairs makes ascending [ms, float] pairs, drops bad rows, the later value of a repeated date wins
    rows = [[d3, 12], [d1, 10.0], ["bad", 1.0], [d2, 11.0], [d2, 11.5], [d4, float("nan")], [d4, 0], [d4, "x"]]
    out["to_pairs"] = ps.to_pairs(rows) == [[ms(d1), 10.0], [ms(d2), 11.5], [ms(d3), 12.0]]
    # 4: two tickers with a common start: level is 100 at t0 and follows the buy-and-hold sum
    a = [[ms(d1), 10.0], [ms(d2), 11.0], [ms(d3), 12.0]]
    b = [[ms(d1), 20.0], [ms(d2), 20.0], [ms(d3), 22.0]]
    r = ps.buy_and_hold({"A": a, "B": b}, {"A": 100.0, "B": 100.0})
    want = [[ms(d1), 100.0], [ms(d2), 105.0], [ms(d3), 115.0]]
    out["common start"] = (r["status"] == "OK" and len(r["pairs"]) == 3
                           and all(p[0] == w[0] and close(p[1], w[1]) for p, w in zip(r["pairs"], want))
                           and r["used"] == ["A", "B"] and r["excluded"] == [] and close(r["coverage"], 1.0) and r["t0"] == ms(d1))
    # 5: a later start moves t0 to the latest first date; the earlier ticker is based at its value as of t0
    b2 = [[ms(d2), 20.0], [ms(d3), 22.0]]
    r = ps.buy_and_hold({"A": a, "B": b2}, {"A": 100.0, "B": 100.0})
    v3 = (100.0 * 12.0 / 11.0 + 100.0 * 22.0 / 20.0) / 200.0 * 100.0
    out["later start"] = (r["status"] == "OK" and r["t0"] == ms(d2) and len(r["pairs"]) == 2
                          and close(r["pairs"][0][1], 100.0) and close(r["pairs"][1][1], v3))
    # 6: observation times are the union; a ticker is carried at its last observation at or before each time
    c = [[ms(d1), 5.0], [ms(d3), 6.0]]
    r = ps.buy_and_hold({"A": a, "C": c}, {"A": 100.0, "C": 100.0})
    v2 = (100.0 * 11.0 / 10.0 + 100.0 * 5.0 / 5.0) / 200.0 * 100.0
    out["union of times, as-of carry"] = (len(r["pairs"]) == 3 and close(r["pairs"][1][1], v2))
    # 7: amounts weight the sum
    r = ps.buy_and_hold({"A": a, "B": b}, {"A": 300.0, "B": 100.0})
    v2 = (300.0 * 11.0 / 10.0 + 100.0 * 20.0 / 20.0) / 400.0 * 100.0
    out["amount weighting"] = close(r["pairs"][1][1], v2)
    # 8: a ticker with no series, or a non-positive base, is excluded with a typed reason; coverage is the amount share used
    z = [[ms(d1), 0.0], [ms(d2), 1.0]]
    r = ps.buy_and_hold({"A": a, "Z": z}, {"A": 100.0, "Z": 50.0, "N": 50.0})
    ex = {e["ticker"]: e["reason"] for e in r["excluded"]}
    out["exclusions typed"] = (r["used"] == ["A"] and ex == {"Z": "BAD_BASE", "N": "NO_SERIES"} and close(r["coverage"], 0.5))
    # 9: a bad amount is ignored and named
    r = ps.buy_and_hold({"A": a, "B": b}, {"A": 100.0, "B": -5.0})
    out["bad amount"] = r["used"] == ["A"] and {e["ticker"]: e["reason"] for e in r["excluded"]}.get("B") == "BAD_AMOUNT"
    # 10: nothing usable -> NO_SERIES with no pairs; one pair only -> TOO_SHORT with no pairs
    r0 = ps.buy_and_hold({}, {"A": 100.0})
    r1 = ps.buy_and_hold({"A": [[ms(d1), 10.0]]}, {"A": 100.0})
    out["status NO_SERIES and TOO_SHORT"] = (r0["status"] == "NO_SERIES" and r0["pairs"] == [] and r1["status"] == "TOO_SHORT"
                                             and r1["pairs"] == [])
    # 11: the inputs are not changed
    a_copy, b_copy = [list(p) for p in a], [list(p) for p in b]
    ps.buy_and_hold({"A": a, "B": b}, {"A": 100.0, "B": 100.0})
    out["inputs untouched"] = a == a_copy and b == b_copy
    # 12: named_series wraps pairs with a key, and is None for fewer than two pairs or a blank key
    ok = ps.named_series(a, "benchmark:^SP500TR")
    out["named series"] = (ok == {"series": a, "key": "benchmark:^SP500TR"} and ps.named_series(a[:1], "k") is None
                           and ps.named_series(a, "") is None)
    return out


def main(mode):
    if mode == "g63":
        try:
            spec = importlib.util.spec_from_file_location("portfolio_series", MODULE)
            ps = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(ps)
            ps.buy_and_hold
        except Exception as exc:
            print("AR-G63-FAIL import %s: %s" % (type(exc).__name__, str(exc)[:160]))
            return 1
        try:
            got = cases(ps)
        except Exception as exc:
            print("AR-G63-FAIL a case raised %s: %s" % (type(exc).__name__, str(exc)[:200]))
            return 1
        wrong = [k for k, ok in got.items() if not ok]
        rc, line, passed = pytest_line(TESTS)
        print("cases %d, wrong %s" % (len(got), wrong or "none"))
        print("worker tests: %s" % line)
        if wrong or rc != 0 or bad_count(line) or passed < 8:
            print("AR-G63-FAIL wrong=%s tests rc=%d passed=%d (need >= 8)" % (wrong or "none", rc, passed))
            return 1
        print("AR-G63-OK cases=%d tests=%d" % (len(got), passed))
        return 0
    if mode == "hygiene":
        try:
            with open(MODULE, "rb") as fh:
                raw = fh.read()
        except OSError as exc:
            print("AR-G63-HYGIENE-FAIL no module: %s" % type(exc).__name__)
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
            print("AR-G63-HYGIENE-FAIL " + "; ".join(problems))
            return 1
        print("AR-G63-HYGIENE-OK imports=%s" % ",".join(sorted(imported)))
        return 0
    print("usage: ar_g63_checks.py g63|hygiene")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
