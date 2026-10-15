"""IRPT_ANLREQ AR-g-88 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g88_checks.py g88       the layout's multi-column OWN_SERIES statistics answer their direct cases (hand-computed),
                                      and the eight named new tests exist and pass
    python ar_g88_checks.py regress   the layout's and producer's existing test files (run one at a time) still pass

Prints one RESULT line: AR-G88-OK / AR-G88-FAIL or AR-G88-REGRESS-OK / AR-G88-REGRESS-FAIL; rc 0 only on OK. ASCII only.
"""
import datetime
import json
import re
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/ycharts/research/"
T = R + "tests/"
MAP = "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps/overview_map.json"
NEW_TESTS = {
    T + "test_layout_own_series_columns.py": [
        "test_table_columns_give_labelled_values_and_na_for_a_column_the_series_is_too_short_for",
        "test_chart_columns_give_the_worked_out_values_in_column_order",
        "test_every_column_unworkable_is_the_first_columns_reason",
        "test_drawdown_columns_label_the_whole_series_column",
        "test_a_named_statistic_still_wins_over_columns",
        "test_no_columns_and_no_statistic_is_still_statistic_unknown",
        "test_pricing_off_is_still_not_in_this_version",
        "test_the_page_prints_the_labelled_rows_and_the_na_cells",
    ],
}
EXISTING = [T + "test_layout_overview.py", T + "test_layout_commentary.py", T + "test_opal_producer.py", T + "test_held_data.py",
            T + "test_map_pdf.py", T + "test_portfolio_series.py"]
RET_COLS = ["total_return_1m", "total_return_3m", "total_return_ytd", "total_return_1y", "total_return_3y", "total_return_5y",
            "total_return_10y", "total_return_15y"]
DD_COLS = ["max_drawdown_1y", "max_drawdown_3y", "max_drawdown_5y", "max_drawdown_10y", "max_drawdown_all"]
RUN = {"holdings": {"rows": [{"ticker": "AAA", "amount": "1"}], "basis": "USD"}, "calls": []}
CALLS = {"portfolio_level_series"}


def bad_count(line):
    return sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))


def pytest_run(targets, extra=()):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", *extra, *targets],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    text = out.stdout + out.stderr
    lines = [ln for ln in text.splitlines() if re.search(r"[0-9]+ (passed|failed|error|skipped)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    return out.returncode, line, int(m.group(1)) if m else 0, text


def ms(day):
    return int((datetime.date.fromisoformat(day) - datetime.date(1970, 1, 1)).days * 86400000)


def month_date(k):
    total = 2024 * 12 + 6 + k  # point 0 is 2024-07-14; point 27 is 2026-10-14
    return "%04d-%02d-14" % (total // 12, total % 12 + 1)


def series(factor):
    out, v = [], 100.0
    for k in range(28):
        if k:
            v *= factor(k)
        out.append([ms(month_date(k)), v])
    return out


def kept_of(points):
    return {"portfolio_level_series": {"name": "p", "step": 0, "response": {"status": 200, "body_json": {
        "chart_data": [[{"raw_data": points}]]}}}}


def element(kind, columns, statistic=None):
    return {"id": "t.e", "page": 2, "kind": kind, "label": "T", "source": {
        "computed": "OWN_SERIES", "call": "portfolio_level_series", "field": "$.chart_data[0][0].raw_data",
        "columns": columns, "sleeve": None, "statistic": statistic}}


def compute(lo, el, points, pricing=True):
    return lo.compute_element(el, kept_of(points), RUN, None, None, CALLS, None, None, pricing)


def close(a, b):
    return isinstance(a, (int, float)) and abs(a - b) <= 1e-9 * max(1.0, abs(b))


def load():
    sys.path.insert(0, R)
    import layout_overview as lo
    return lo


def cases(lo):
    out = {}
    g = 1.01
    pts = series(lambda k: g)
    want = {"Total return 1M": (g - 1) * 100, "Total return 3M": (g ** 3 - 1) * 100, "Total return YTD": (g ** 10 - 1) * 100,
            "Total return 1Y": (g ** 12 - 1) * 100}
    na = ["Total return 3Y", "Total return 5Y", "Total return 10Y", "Total return 15Y"]
    r = compute(lo, element("table", RET_COLS), pts)
    v = r["value"] if r["state"] == "value" else {}
    out["a table gives labelled values, hand-computed, and n/a where the series is too short"] = (
        r["state"] == "value" and list(v) == list(want) + na and all(close(v[k], want[k]) for k in want)
        and all(v[k] == "n/a" for k in na))
    out["the coverage is the share of columns worked out"] = close(r["trace"]["coverage"], 0.5) and r["trace"]["status"] == "VALUE"
    c = compute(lo, element("chart", RET_COLS), pts)
    out["a chart gives the worked-out values in column order"] = (
        c["state"] == "value" and isinstance(c["value"], list) and len(c["value"]) == 4
        and all(close(a, b) for a, b in zip(c["value"], want.values())) and close(c["trace"]["coverage"], 0.5))
    short = [[ms("2026-10-10"), 100.0], [ms("2026-10-14"), 101.0]]
    n = compute(lo, element("table", RET_COLS), short)
    out["no column workable gives the first column's own reason"] = (
        n["state"] == "not_available" and n["trace"]["reason"] == "SERIES_TOO_SHORT" and n["trace"]["status"] == "NOT_AVAILABLE")
    dd = series(lambda k: 0.90 if k == 20 else 1.01)
    d = compute(lo, element("table", DD_COLS), dd)
    dv = d["value"] if d["state"] == "value" else {}
    out["drawdown columns are labelled, the whole series is 'all'"] = (
        list(dv) == ["Max drawdown 1Y", "Max drawdown 3Y", "Max drawdown 5Y", "Max drawdown 10Y", "Max drawdown all"]
        and close(dv.get("Max drawdown 1Y"), -10.0) and close(dv.get("Max drawdown all"), -10.0)
        and [dv.get(k) for k in ("Max drawdown 3Y", "Max drawdown 5Y", "Max drawdown 10Y")] == ["n/a"] * 3)
    s = compute(lo, element("number", RET_COLS, statistic="total_return_1y"), pts)
    out["a named statistic wins over columns and stays a number"] = s["state"] == "value" and close(s["value"], want["Total return 1Y"])
    u = compute(lo, element("table", None), pts)
    e = compute(lo, element("table", []), pts)
    out["no columns and no statistic is still STATISTIC_UNKNOWN"] = (
        u["trace"]["reason"] == "STATISTIC_UNKNOWN:None" and e["trace"]["reason"] == "STATISTIC_UNKNOWN:None")
    off = compute(lo, element("table", RET_COLS), pts, pricing=False)
    out["pricing off is still NOT_IN_THIS_VERSION"] = off["state"] == "not_available" and off["trace"]["reason"] == lo.NOT_IN_THIS_VERSION
    html = lo._element_html(element("table", RET_COLS), {}, lo._palette({}), computed={"t.e": r}, map_calls=CALLS, pricing=True)
    out["the page prints the labelled rows and the n/a cells"] = (
        "Total return 1Y" in html and "12.6825" in html and html.count("n/a") == 4 and "total_return_1y" not in html)
    doc = json.load(open(MAP, encoding="utf-8"))
    real = {el["id"]: el for el in doc["elements"] if el["id"] in ("p2.e08", "p2.e13", "p6.e22")}
    got = {i: lo.compute_element(real[i], kept_of(dd), RUN, None, None, CALLS, None, None, True) for i in real}
    out["the three real map elements are values, not STATISTIC_UNKNOWN"] = (
        sorted(real) == ["p2.e08", "p2.e13", "p6.e22"] and all(x["state"] == "value" for x in got.values())
        and isinstance(got["p2.e13"]["value"], dict) and isinstance(got["p2.e08"]["value"], list)
        and isinstance(got["p6.e22"]["value"], dict))
    return out


def main(mode):
    if mode == "g88":
        try:
            lo = load()
        except Exception as exc:
            print("AR-G88-FAIL import %s: %s" % (type(exc).__name__, str(exc)[:160]))
            return 1
        try:
            got = cases(lo)
        except Exception as exc:
            print("AR-G88-FAIL a case raised %s: %s" % (type(exc).__name__, str(exc)[:240]))
            return 1
        wrong = [k for k, ok in got.items() if not ok]
        missing = []
        for path, names in NEW_TESTS.items():
            rc, line, passed, text = pytest_run([path], extra=("--collect-only",))
            have = set(re.findall(r"::(test_[A-Za-z0-9_]+)", text))
            missing += [n for n in names if n not in have]
        rc, line, passed, text = pytest_run(list(NEW_TESTS))
        need = sum(len(v) for v in NEW_TESTS.values())
        print("direct cases %d, wrong %s" % (len(got), wrong or "none"))
        print("named tests missing: %s" % (missing or "none"))
        print("new tests: %s" % line)
        if wrong or missing or rc != 0 or bad_count(line) or passed < need:
            print("AR-G88-FAIL wrong=%s missing=%s rc=%d passed=%d (need >= %d)" % (wrong or "none", missing or "none", rc, passed, need))
            return 1
        print("AR-G88-OK direct=%d named=%d passed=%d" % (len(got), need, passed))
        return 0
    if mode == "regress":
        total, bad = 0, []
        for path in EXISTING:
            rc, line, passed, text = pytest_run([path])
            print("%s: %s" % (path.split("/")[-1], line[:70]))
            total += passed
            if rc != 0 or bad_count(line) or passed == 0:
                bad.append(path.split("/")[-1])
        if bad or total < MIN_TOTAL:
            print("AR-G88-REGRESS-FAIL files=%s passed=%d (need >= %d)" % (bad or "none", total, MIN_TOTAL))
            return 1
        print("AR-G88-REGRESS-OK passed=%d" % total)
        return 0
    print("usage: ar_g88_checks.py g88|regress")
    return 2


MIN_TOTAL = 121

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
