"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the checks of FWD-10 (Core), the comparison section of the Opal-built report.
Run from the worktree root.

    python ar_compare_checks.py <cell> build|guard|regress     cell is 171, 173, 174 or 175
    python ar_compare_checks.py calibrate                      the checker's own formulas against the shipped layout (must read OK at base)
    python ar_compare_checks.py baseline                       writes compare_base_status.json (the status of every element at the base)

cell 171: K1 model_source.py + model_code_map.json.   cell 173: K2 comparables.py.   cell 174: K3 the layout's five COMPARE_* methods.
cell 175: K4 the producer stage and the resident ports, end to end through the SHIPPED producer on the REAL multi map.
(Cell 172, the Terraform grant, is graded by its own order: terraform validate and the plan text, not by this file.)
Prints one RESULT line: AR-CMP-<cell>-OK / -FAIL (or -REGRESS-); rc 0 only on OK. ASCII only. Every number is computed here from the
checker's own deterministic fixtures, never read back from the code under test.
"""
import datetime
import gzip
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ar_price_checks as pc  # noqa: E402  (the round-57 fixtures: AAA/BBB/CCC, SPY, BIL, as_of, tier readers)

IR = "infra/aws/lambda/investor-reporting/"
RES = IR + "ycharts/research"
TESTS = RES + "/tests"
GEN = IR + "ycharts/generate"
MAPS = "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps/"
CHK = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/"
BASE_JSON = CHK + "compare_base_status.json"
AS_OF = pc.AS_OF  # 2026-10-14
NAMES = ("window", "chart", "returns", "risk", "allocation")
IDS = ["opal.compare." + n for n in NAMES]
METHODS = ["COMPARE_WINDOW", "COMPARE_CHART", "COMPARE_RETURNS", "COMPARE_RISK", "COMPARE_ALLOCATION"]
KINDS = ["text", "chart", "table", "table", "table"]
PERIODS = ["1m", "3m", "ytd", "1y", "3y", "5y", "10y"]
CODES = ("UST", "ST", "INT", "LT", "ULT")
SERIES_KEY = "json/benchmarks/model_portfolio_timeseries.json"
POSITIONING_KEY = "json/positioning/positioning_data.json"
MODEL_START = "2024-04-14"  # the first date of every model fixture series (a model's inception in the real file is 2024-04-30)
# model fixture: monthly returns r_k = f(k) - 1 for k >= 1 (the first row's own return is deliberately odd and must be IGNORED)
MODEL_F = {"UST": lambda k: 1.002, "ST": lambda k: 1.004 if k % 6 else 0.995, "INT": lambda k: 1.006 if k % 5 else 0.99,
           "LT": lambda k: 1.009 if k % 4 else 0.98, "ULT": lambda k: 1.011 if k % 3 else 0.975}
MODEL_N = 31  # 2024-04-14 .. 2026-10-14
ALLOC = {"UST": (0.0, 100.0, 0.0, 0.0, 0.0, 0.0, 0.0), "ST": (2.0, 80.0, 18.0, 0.0, 0.0, 0.0, 0.0),
         "INT": (1.0, 60.0, 39.0, 0.0, 0.0, 0.0, 0.0), "LT": (1.5, 40.0, 58.0, 0.0, 0.0, 0.0, 0.5),
         "ULT": (1.0, 20.0, 76.0, 0.0, 0.0, 1.0, 2.0)}  # cash, fixed_income, equity, hedge, structured, commodities, alternatives (percent)
ALLOC_KEYS = ("cash", "fixed_income", "equity", "hedge", "structured", "commodities", "alternatives")
ALLOC_LABELS = ("Cash", "Fixed Income", "Equity", "Hedge", "Structured", "Commodities", "Alternatives")
IWM_F = lambda k: 1.011 if k % 4 else 0.975  # noqa: E731
pc.FACT["IWM"] = IWM_F
pc.TIER["IWM"] = "yfinance"
CATALOGUE = {"opal_ultra_short_term": ("UST", "Opal Ultra Short-Term"), "opal_short_term": ("ST", "Opal Short-Term"),
             "opal_intermediate_term": ("INT", "Opal Intermediate-Term"), "opal_long_term": ("LT", "Opal Long-Term"),
             "opal_ultra_long_term": ("ULT", "Opal Ultra Long-Term")}


# ---------------------------------------------------------------- dates, fixtures
def ms(day):
    d = datetime.datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
    return int(d.timestamp() * 1000)


def shift(day, months):
    """The 14th of the month `months` earlier (the fixtures sit on the 14th)."""
    y, m = int(day[:4]), int(day[5:7])
    total = y * 12 + (m - 1) - months
    return "%04d-%02d-14" % (total // 12, total % 12 + 1)


def month_dates(start, n):
    return [shift(start, -k) for k in range(n)]


def model_levels(code):
    """[(date, level)] per the K1 rule: 100.0 on the first date, then x (1 + model_return)."""
    out, v = [], 100.0
    for k, d in enumerate(month_dates(MODEL_START, MODEL_N)):
        if k:
            v *= MODEL_F[code](k)
        out.append((d, v))
    return out


def series_json():
    rows = []
    for code in CODES:
        prev = 100.0
        for k, (d, v) in enumerate(model_levels(code)):
            r = -0.0123 if k == 0 else v / prev - 1.0  # row 0: an odd return that must not move the base
            prev = v
            rows.append({"date": d, "model_code": code, "model_return": r, "benchmark_return": 0.001,
                         "index_benchmark_return": 0.001, "etf_benchmark_return": 0.001, "rfr": 0.0001})
    return json.dumps({"generated_at": "2026-10-20T11:06:25Z", "data_as_of": "2026-10-14", "inception_date": MODEL_START,
                       "rfr_tenors": {c: "x" for c in CODES}, "series_note": "fixture", "timeseries": rows}).encode("utf-8")


def positioning_json(gz=True):
    doc = {"generated_at": "2026-10-20T11:06:27Z", "data_as_of": "2026-10-19", "data_date": "20261019", "note": "fixture",
           "benchmarks": {}, "current_holdings": {},
           "portfolios": {c: {"code": c, "name": "fixture", "allocation": dict(zip(ALLOC_KEYS, ALLOC[c]))} for c in CODES}}
    raw = json.dumps(doc).encode("utf-8")
    return gzip.compress(raw) if gz else raw


def get_bytes(plain_positioning=False):
    def get(key):
        if key == SERIES_KEY:
            return series_json()
        if key == POSITIONING_KEY:
            return positioning_json(not plain_positioning)
        raise KeyError(key)
    return get


# ---------------------------------------------------------------- the checker's own arithmetic (independent of the layout)
def as_of_level(series, day):
    got = [v for d, v in series if d <= day]
    return got[-1] if got else None


def rebase(series, start):
    base = as_of_level(series, start)
    return [(d, v / base * 100.0) for d, v in series if d >= start]


def total_return(path, key):
    end = path[-1][0]
    if key == "ytd":
        target = "%d-12-31" % (int(end[:4]) - 1)
    else:
        n = int(key[:-1]) * (12 if key.endswith("y") else 1)
        target = shift(end, n)
    if path[0][0] > target:
        return None
    return (path[-1][1] / as_of_level(path, target) - 1.0) * 100.0


def months(levels_by_date, end, n):
    lv = [as_of_level(levels_by_date, shift(end, n - k)) for k in range(n + 1)]
    return [lv[i] / lv[i - 1] - 1.0 for i in range(1, n + 1)]


def svar(xs):
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def risk(path, bench, rfree, years):
    """std_dev, sharpe, sortino, max_drawdown, alpha, beta over `years` whole years ending at the path's last date."""
    n = 12 * years
    end = path[-1][0]
    rp, rb, rf = months(path, end, n), months(bench, end, n), months(rfree, end, n)
    out = {"std_dev": math.sqrt(svar(rp)) * math.sqrt(12.0) * 100.0}
    ex = [a - f for a, f in zip(rp, rf)]
    mean = sum(ex) / n
    out["sharpe"] = mean * math.sqrt(12.0) / math.sqrt(svar(ex))
    down = math.sqrt(sum(min(x, 0.0) ** 2 for x in ex) / n)
    out["sortino"] = mean * math.sqrt(12.0) / down
    mp, mb, mf = sum(rp) / n, sum(rb) / n, sum(rf) / n
    beta = sum((a - mp) * (b - mb) for a, b in zip(rp, rb)) / (n - 1) / svar(rb)
    out["beta"] = beta
    out["alpha"] = ((mp - mf) - beta * (mb - mf)) * 12.0 * 100.0
    target = shift(end, n)
    start_v = as_of_level(path, target)
    walk = [start_v] + [v for d, v in path if d > target]
    peak, worst = walk[0], 0.0
    for v in walk:
        peak = max(peak, v)
        worst = min(worst, v / peak - 1.0)
    out["max_drawdown"] = worst * 100.0
    return out


def fin(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def close(a, b, rel=1e-7):
    return fin(a) and fin(b) and abs(a - b) <= rel * max(1.0, abs(a), abs(b))


def pts_ms(series):
    return [[ms(d), v] for d, v in series]


# ---------------------------------------------------------------- calibrate: the formulas above against the shipped statistic engine
def calibrate():
    fails = []
    sys.path.insert(0, RES)
    sys.path.insert(0, "lib")
    import layout_overview as lo
    port = pc.portfolio_points()
    bench = [r for r in pc.levels("SPY") if "2016-10-14" <= r[0] <= AS_OF]
    rfree = [r for r in pc.levels("BIL") if "2016-10-14" <= r[0] <= AS_OF]
    P, B, R = pts_ms(port), pts_ms(bench), pts_ms(rfree)
    mine = risk(port, bench, rfree, 3)
    for name, stat in (("std_dev", "std_dev_3y"), ("sharpe", "sharpe_3y"), ("sortino", "sortino_3y"), ("alpha", "alpha_3y"),
                       ("beta", "beta_3y"), ("max_drawdown", "max_drawdown_3y")):
        want = lo.statistic_of(P, stat, B, R)
        if not close(mine[name], want):
            fails.append("calibration: %s over 3y is %r here and %r in the layout" % (name, mine[name], want))
    for key in ("1m", "3m", "ytd", "1y", "3y", "5y", "10y"):
        want = lo.statistic_of(P, "total_return_" + key)
        have = total_return(port, key)
        if not close(have, want):
            fails.append("calibration: total return %s is %r here and %r in the layout" % (key, have, want))
    return fails


# ---------------------------------------------------------------- the K2 fixtures and expectations
def k2_inputs():
    portfolio_full = pc.portfolio_points()  # 2016-10-14 .. 2026-10-14, 121 points
    etf = [r for r in pc.levels("IWM") if "2016-10-14" <= r[0] <= AS_OF]
    comps = [{"key": "opal_long_term", "name": "Opal Long-Term", "kind": "model", "series": pts_ms(model_levels("LT")), "reason": None},
             {"key": "opal_ultra_long_term", "name": "Opal Ultra Long-Term", "kind": "model", "series": pts_ms(model_levels("ULT")), "reason": None},
             {"key": "IWM", "name": "iShares Russell 2000 ETF", "kind": "ticker", "series": pts_ms(etf), "reason": None}]
    bench = [r for r in pc.levels("SPY") if "2016-10-14" <= r[0] <= AS_OF]
    rfree = [r for r in pc.levels("BIL") if "2016-10-14" <= r[0] <= AS_OF]
    full = {"portfolio": portfolio_full, "Opal Long-Term": model_levels("LT"), "Opal Ultra Long-Term": model_levels("ULT"),
            "iShares Russell 2000 ETF": etf}
    return portfolio_full, comps, bench, rfree, full


def expected_rows(full, bench, rfree, start="2024-04-14", years=2):
    rows = {}
    for name, series in full.items():
        path = rebase(series, start)
        rows[name] = {"path": path, "returns": {k: total_return(path, k) for k in PERIODS}, "risk": risk(path, bench, rfree, years)}
    return rows


def check_record(rec, comps, full, bench, rfree, tag, fails):
    want = expected_rows(full, bench, rfree)
    w = rec.get("window") or {}
    if (w.get("start"), w.get("end")) != ("2024-04-14", "2026-10-14"):
        fails.append("%s window is %r..%r, want 2024-04-14..2026-10-14 (the latest first date and the earliest last date)" % (
            tag, w.get("start"), w.get("end")))
    if not close(w.get("years"), 2.5):
        fails.append("%s window years is %r, want 2.5" % (tag, w.get("years")))
    if not (isinstance(w.get("rule"), str) and len(w["rule"]) > 20):
        fails.append("%s window rule is not a sentence" % tag)
    rows = rec.get("rows") or []
    names = [r.get("name") for r in rows]
    if names != ["Opal Long-Term", "Opal Ultra Long-Term", "iShares Russell 2000 ETF"] and names[1:] != [c["name"] for c in comps]:
        fails.append("%s row names are %r" % (tag, names))
    for r in rows:
        key = r.get("name") if r.get("kind") else "portfolio"
        if r.get("kind") is None or r.get("key") == "portfolio":
            key = "portfolio"
        exp = want.get(key)
        if exp is None or r.get("status") != "VALUE":
            if exp is not None:
                fails.append("%s row %s status is %r" % (tag, key, r.get("status")))
            continue
        path = r.get("path") or []
        if len(path) != len(exp["path"]) or not close(path[0][1], 100.0) or not close(path[-1][1], exp["path"][-1][1]):
            fails.append("%s row %s path: %d points, first %r, last %r; want %d points, 100.0, %r" % (
                tag, key, len(path), path[0][1] if path else None, path[-1][1] if path else None, len(exp["path"]), exp["path"][-1][1]))
        for k in PERIODS:
            have, w_ = (r.get("returns") or {}).get(k), exp["returns"][k]
            if (w_ is None) != (have is None) or (w_ is not None and not close(have, w_)):
                fails.append("%s row %s return %s is %r, want %r" % (tag, key, k, have, w_))
        rk = r.get("risk") or {}
        if rk.get("years") != 2:
            fails.append("%s row %s risk years is %r, want 2 (floor of the 2.5-year window)" % (tag, key, rk.get("years")))
        for k, w_ in exp["risk"].items():
            if not close(rk.get(k), w_):
                fails.append("%s row %s risk %s is %r, want %r" % (tag, key, k, rk.get(k), w_))
    return rows


def alloc_inputs():
    portfolio = {"name": "Your portfolio", "weights": {"Equity": 70.0, "Fixed Income": 30.0}}
    comps = [{"name": "Opal Long-Term", "kind": "model", "weights": {lab: v for lab, v in zip(ALLOC_LABELS, ALLOC["LT"])},
              "asset_class": None, "as_of": "2026-10-19", "reason": None},
             {"name": "iShares Russell 2000 ETF", "kind": "ticker", "weights": None, "asset_class": "Equity", "as_of": None, "reason": None},
             {"name": "NoSource Fund", "kind": "ticker", "weights": None, "asset_class": None, "as_of": None,
              "reason": "no classification is held for it"}]
    return portfolio, comps


# ---------------------------------------------------------------- the build arms
def arms_build_171():
    fails = []
    sys.path.insert(0, RES)
    try:
        import model_source as ms_
    except ImportError as exc:
        return ["model_source cannot be imported: %s" % exc]
    for name, val in (("BUCKET", "opal-data-portal-v2"), ("SERIES_KEY", SERIES_KEY), ("POSITIONING_KEY", POSITIONING_KEY),
                      ("CODES", CODES)):
        if getattr(ms_, name, None) != val:
            fails.append("model_source.%s is %r, want %r" % (name, getattr(ms_, name, None), val))
    for key, (code, _) in CATALOGUE.items():
        if ms_.code_for_key(key) != code:
            fails.append("code_for_key(%r) is %r, want %r" % (key, ms_.code_for_key(key), code))
    for bad in ("Opal Long-Term", "IWM", "", None):
        if ms_.code_for_key(bad) is not None:
            fails.append("code_for_key(%r) is %r, want None (no display-name matching)" % (bad, ms_.code_for_key(bad)))
    got = ms_.read_series(get_bytes())
    if got.get("inception") != MODEL_START or got.get("as_of") != "2026-10-14":
        fails.append("read_series as_of / inception are %r / %r" % (got.get("as_of"), got.get("inception")))
    series = got.get("series") or {}
    if sorted(series) != sorted(CODES):
        fails.append("read_series codes are %r" % sorted(series))
    for code in CODES:
        want = pts_ms(model_levels(code))
        have = series.get(code) or []
        if len(have) != len(want) or any(a[0] != b[0] or not close(a[1], b[1], 1e-9) for a, b in zip(have, want)):
            fails.append("read_series %s differs from level 100 on the first date x (1 + return) after it (first row's own return ignored); "
                         "have %r.. want %r.." % (code, have[:2], want[:2]))
    for plain in (False, True):  # the positioning object is gzip in the bucket; plain JSON must read too
        alloc = ms_.read_allocation(get_bytes(plain_positioning=plain))
        if alloc.get("as_of") != "2026-10-19":
            fails.append("read_allocation as_of is %r (plain=%s), want 2026-10-19" % (alloc.get("as_of"), plain))
        for code in CODES:
            want = dict(zip(ALLOC_LABELS, ALLOC[code]))
            have = (alloc.get("allocation") or {}).get(code)
            if have != want:
                fails.append("read_allocation %s (plain=%s) is %r, want %r" % (code, plain, have, want))
    for label, bad in (("missing key", lambda k: (_ for _ in ()).throw(KeyError(k))), ("not json", lambda k: b"not json at all"),
                       ("wrong shape", lambda k: b'{"timeseries": 7}')):
        for fn in (ms_.read_series, ms_.read_allocation):
            try:
                fn(bad)
                fails.append("%s: %s did not refuse" % (label, fn.__name__))
            except ms_.ModelSourceRefused:
                pass
            except Exception as exc:  # noqa: BLE001
                fails.append("%s: %s raised %s, not ModelSourceRefused" % (label, fn.__name__, type(exc).__name__))
    path = os.path.join(RES, "model_code_map.json")
    try:
        doc = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return fails + ["model_code_map.json cannot be read: %s" % exc]
    want = {code: {"catalogue_key": key, "label": label} for key, (code, label) in CATALOGUE.items()}
    if doc.get("schema") != "irpt-model-code-map-v1" or doc.get("codes") != want:
        fails.append("model_code_map.json is %r, want schema irpt-model-code-map-v1 and codes %r" % (doc, want))
    cat = json.load(open(GEN + "/templates.json", encoding="utf-8"))["comparison_catalog"]["entries"]
    live = {e["key"]: e["label"] for e in cat}
    if live != {k: v[1] for k, v in CATALOGUE.items()}:
        fails.append("the catalogue (templates.json) no longer holds the five Opal model keys and labels this checker was cut on: %r" % live)
    return fails


def arms_build_173():
    fails = []
    sys.path.insert(0, RES)
    sys.path.insert(0, "lib")
    try:
        import comparables as cmp_
    except ImportError as exc:
        return ["comparables cannot be imported: %s" % exc]
    port_full, comps, bench, rfree, full = k2_inputs()
    rec = cmp_.build_compare({"name": "Your portfolio", "series": pts_ms(port_full)}, comps, pts_ms(bench), pts_ms(rfree))
    rows = check_record(rec, comps, full, bench, rfree, "3 comparables", fails)
    if not rows or rows[0].get("name") != "Your portfolio" or rows[0].get("key") != "portfolio":
        fails.append("row 0 is not the portfolio (name Your portfolio, key portfolio): %r" % (rows[:1],))
    # a comparable with no series: stated, left out of the window, the others unchanged
    gap = comps + [{"key": "ZZZZ", "name": "ZZZZ", "kind": "ticker", "series": None, "reason": "no price was found for it"}]
    rec2 = cmp_.build_compare({"name": "Your portfolio", "series": pts_ms(port_full)}, gap, pts_ms(bench), pts_ms(rfree))
    last = (rec2.get("rows") or [{}])[-1]
    if (last.get("name"), last.get("status")) != ("ZZZZ", "NOT_AVAILABLE") or last.get("reason") != "no price was found for it":
        fails.append("the series-less comparable reads %r, want NOT_AVAILABLE with its reason" % (last,))
    if last.get("path") != [] or any(v is not None for v in (last.get("returns") or {}).values()):
        fails.append("the series-less comparable carries figures: %r" % (last,))
    if rec2.get("window") != rec.get("window"):
        fails.append("a series-less comparable moved the common window: %r vs %r" % (rec2.get("window"), rec.get("window")))
    check_record({**rec2, "rows": rec2["rows"][:-1]}, comps, full, bench, rfree, "with a gap row", fails)
    # no benchmark / risk-free: alpha, beta, Sharpe, Sortino are None, std dev and drawdown stay
    rec3 = cmp_.build_compare({"name": "Your portfolio", "series": pts_ms(port_full)}, comps, None, None)
    rk = (rec3.get("rows") or [{}])[0].get("risk") or {}
    if any(rk.get(k) is not None for k in ("alpha", "beta", "sharpe", "sortino")) or not fin(rk.get("std_dev")):
        fails.append("without benchmark and risk-free the risk block is %r" % (rk,))
    # a window shorter than one year: the risk block carries years None and no figure
    short = [{"key": "S", "name": "Short", "kind": "model", "series": pts_ms(model_levels("LT")[-8:]), "reason": None}]
    rec4 = cmp_.build_compare({"name": "Your portfolio", "series": pts_ms(port_full)}, short, pts_ms(bench), pts_ms(rfree))
    for r in rec4.get("rows") or []:
        k = r.get("risk") or {}
        if k.get("years") is not None or any(k.get(n) is not None for n in ("std_dev", "sharpe", "sortino", "max_drawdown", "alpha", "beta")):
            fails.append("a window under one year still carries risk figures for %s: %r" % (r.get("name"), k))
    # allocation
    portfolio, acomps = alloc_inputs()
    table = cmp_.build_allocation(portfolio, acomps)
    if table.get("classes") != ["Cash", "Fixed Income", "Equity", "Alternatives"]:
        fails.append("allocation classes are %r, want the canonical order restricted to classes some row holds a non-zero weight in: "
                     "Cash, Fixed Income, Equity, Alternatives" % (table.get("classes"),))
    arows = table.get("rows") or []
    if [r.get("name") for r in arows] != ["Your portfolio", "Opal Long-Term", "iShares Russell 2000 ETF", "NoSource Fund"]:
        fails.append("allocation row names are %r" % ([r.get("name") for r in arows],))
    else:
        want0 = {"Cash": 0.0, "Fixed Income": 30.0, "Equity": 70.0, "Alternatives": 0.0}
        want1 = {"Cash": 1.5, "Fixed Income": 40.0, "Equity": 58.0, "Alternatives": 0.5}
        want2 = {"Cash": 0.0, "Fixed Income": 0.0, "Equity": 100.0, "Alternatives": 0.0}
        for r, w_ in ((arows[0], want0), (arows[1], want1), (arows[2], want2)):
            if r.get("weights") != w_:
                fails.append("allocation weights of %s are %r, want %r" % (r.get("name"), r.get("weights"), w_))
        if arows[1].get("as_of") != "2026-10-19" or "2026-10-19" not in str(arows[1].get("basis")):
            fails.append("the model row is not dated 2026-10-19 (as_of %r, basis %r)" % (arows[1].get("as_of"), arows[1].get("basis")))
        if arows[3].get("weights") is not None or "no classification is held for it" not in str(arows[3].get("reason")):
            fails.append("the unclassified row reads %r, want weights None and its reason" % (arows[3],))
    return fails


def compute_with(record, allocation, pricing=True):
    sys.path.insert(0, RES)
    sys.path.insert(0, "lib")
    import layout_overview as lo
    elements = [{"id": i, "page": 1, "kind": k, "label": i, "source": {"computed": m, "call": None, "columns": [], "field": None,
                                                                    "sleeve": None, "statistic": None}}
                for i, k, m in zip(IDS, KINDS, METHODS)]
    map_doc = {"schema": "irpt-ycdgen-map-v1", "report_type": "MULTICOMP", "calls": [], "elements": elements}
    run_doc = {"holdings": {"basis": "USD", "rows": [{"ticker": "AAA", "amount": 500.0}, {"ticker": "BBB", "amount": 300.0},
                                                      {"ticker": "CCC", "amount": 200.0}]}, "calls": []}
    return lo.compute_all(run_doc, {}, map_doc, None, None, None, {}, None, pricing, compare={"record": record, "allocation": allocation})


def arms_build_174():
    fails = []
    sys.path.insert(0, RES)
    sys.path.insert(0, "lib")
    try:
        import layout_overview as lo
        import comparables as cmp_
    except ImportError as exc:
        return ["cannot import: %s (the K2 module must be merged before this cell is graded; its own build arm gates that)" % exc]
    for m in METHODS:
        if getattr(lo, m, None) != m:
            fails.append("layout_overview.%s is %r, want %r" % (m, getattr(lo, m, None), m))
    port_full, comps, bench, rfree, full = k2_inputs()
    gap = comps + [{"key": "ZZZZ", "name": "ZZZZ", "kind": "ticker", "series": None, "reason": "no price was found for it"}]
    rec = cmp_.build_compare({"name": "Your portfolio", "series": pts_ms(port_full)}, gap, pts_ms(bench), pts_ms(rfree))
    portfolio, acomps = alloc_inputs()
    table = cmp_.build_allocation(portfolio, acomps)
    out = compute_with(rec, table)
    miss = [i for i in IDS if i not in out]
    if miss:
        return fails + ["compute_all returned no entry for %s" % ", ".join(miss)]
    for i in IDS:
        if out[i]["state"] != "value":
            fails.append("%s is %s (%s), want value" % (i, out[i]["state"], (out[i]["trace"] or {}).get("reason")))
    if fails:
        return fails
    win = out[IDS[0]]["value"]
    if not (isinstance(win, str) and "2024-04-14" in win and "2026-10-14" in win and "2.5" in win):
        fails.append("%s is %r, want a sentence naming 2024-04-14, 2026-10-14 and 2.5 years" % (IDS[0], win))
    chart = out[IDS[1]]["value"]
    names = [c.get("name") for c in chart] if isinstance(chart, list) else None
    if names != ["Your portfolio", "Opal Long-Term", "Opal Ultra Long-Term", "iShares Russell 2000 ETF"]:
        fails.append("%s lines are %r, want the portfolio then the three priced comparables (the gap row has no line)" % (IDS[1], names))
    else:
        for line in chart:
            if not line.get("points") or not close(line["points"][0][1], 100.0):
                fails.append("%s line %s does not start at 100.0" % (IDS[1], line.get("name")))
    want = expected_rows(full, bench, rfree)
    ret = out[IDS[2]]["value"]
    cols = ["Name", "1M", "3M", "YTD", "1Y", "3Y", "5Y", "10Y"]
    if not (isinstance(ret, dict) and isinstance(ret.get("rows"), list) and ret["rows"] and list(ret["rows"][0]) == cols):
        fails.append("%s is not {rows, gaps} with the columns %r: %r" % (IDS[2], cols, str(ret)[:200]))
    else:
        for row in ret["rows"]:
            key = "portfolio" if row["Name"] == "Your portfolio" else row["Name"]
            exp = want.get(key)
            if exp is None:
                fails.append("%s has an unexpected row %r" % (IDS[2], row["Name"]))
                continue
            for k, c in zip(PERIODS, cols[1:]):
                w_ = exp["returns"][k]
                have = row[c]
                if (w_ is None and have != "n/a") or (w_ is not None and not close(have, w_)):
                    fails.append("%s %s %s is %r, want %r" % (IDS[2], row["Name"], c, have, "n/a" if w_ is None else w_))
        if ret.get("gaps") != ["not available for ZZZZ: no price was found for it"]:
            fails.append("%s gaps are %r, want ['not available for ZZZZ: no price was found for it']" % (IDS[2], ret.get("gaps")))
    rk = out[IDS[3]]["value"]
    rcols = ["Name", "Std dev (%)", "Sharpe", "Sortino", "Max drawdown (%)", "Alpha (%)", "Beta"]
    if not (isinstance(rk, dict) and isinstance(rk.get("rows"), list) and rk["rows"] and list(rk["rows"][0]) == rcols):
        fails.append("%s is not {rows, gaps, note} with the columns %r: %r" % (IDS[3], rcols, str(rk)[:200]))
    else:
        for row in rk["rows"]:
            key = "portfolio" if row["Name"] == "Your portfolio" else row["Name"]
            exp = want[key]["risk"]
            for c, k in zip(rcols[1:], ("std_dev", "sharpe", "sortino", "max_drawdown", "alpha", "beta")):
                if not close(row[c], exp[k]):
                    fails.append("%s %s %s is %r, want %r" % (IDS[3], row["Name"], c, row[c], exp[k]))
        note = str(rk.get("note"))
        if "2 years" not in note or "SPY" not in note or "BIL" not in note:
            fails.append("%s note is %r, want it to state the 2 years and the references SPY and BIL" % (IDS[3], note))
    al = out[IDS[4]]["value"]
    if not (isinstance(al, dict) and isinstance(al.get("rows"), list) and len(al["rows"]) == 3):
        fails.append("%s is not {rows, gaps} with three rows (the portfolio, the model, the ETF; the unclassified one is a gap): %r" % (
            IDS[4], str(al)[:200]))
    else:
        eq = [r for r in al["rows"] if r.get("Name") == "iShares Russell 2000 ETF"]
        if not eq or eq[0].get("Equity") != 100.0:
            fails.append("%s ETF row is %r, want Equity 100.0" % (IDS[4], eq))
        if "not available for NoSource Fund: no classification is held for it" not in (al.get("gaps") or []):
            fails.append("%s gaps are %r, want the NoSource Fund line" % (IDS[4], al.get("gaps")))
    off = compute_with(rec, table, pricing=False)
    for i in IDS:
        t = off[i]["trace"]
        if off[i]["state"] != "not_available" or t.get("reason") != "NOT_IN_THIS_VERSION":
            fails.append("pricing off: %s is %s / %s, want not_available / NOT_IN_THIS_VERSION" % (i, off[i]["state"], t.get("reason")))
    return fails


# ---------------------------------------------------------------- cell 175: end to end through the shipped producer
def classifier_with_iwm(tp):
    clf = tp.FakeClassifier()
    clf.rows["IWM"] = {"ticker": "IWM", "asset_class": "equity", "sub_asset_class": "Fixture Small Blend", "name": "iShares Russell 2000 ETF"}
    return clf


def run_producer(map_name, comparables, pricing=True, models=True):
    sys.path.insert(0, TESTS)
    sys.path.insert(0, "lib")
    import test_opal_producer as tp
    mp = json.load(open(MAPS + map_name, encoding="utf-8"))
    over = {"classifier": classifier_with_iwm(tp)}
    if pricing:
        over.update(pricing=True, as_of=AS_OF, price_readers=pc.readers())
    if comparables is not None:
        over["comparables"] = comparables
    if models:
        over["model_bytes"] = get_bytes()
    stores = tp.make_stores(map=mp, **over)
    import opal_producer as op
    rec = op.produce(tp.REQ, tp.FIRM, stores)
    sec = {}
    for s in stores["reports"].persisted[0]["report"]["sections"]:
        v = s.get("value")
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except ValueError:
                pass
        sec[s["section_id"]] = {**s, "value": v}
    return rec, sec, "".join(stores["html"])


ENTRIES = [{"key": "opal_long_term", "label": "Opal Long-Term", "ticker": None},
           {"key": "opal_ultra_long_term", "label": "Opal Ultra Long-Term", "ticker": None},
           {"key": "IWM", "label": "iShares Russell 2000 ETF", "ticker": "IWM"}]


def arms_build_175():
    fails = []
    rec, sec, html = run_producer("multi_map.json", ENTRIES)
    byid = {e["id"]: e for e in rec["elements"]}
    for i in IDS:
        if i not in byid or byid[i]["status"] != "VALUE":
            fails.append("%s is %r in the run record, want VALUE" % (i, byid.get(i, {}).get("status", "absent")))
    if fails:
        return fails
    port = pc.portfolio_points()
    bench = [r for r in pc.levels("SPY") if "2016-10-14" <= r[0] <= AS_OF]
    rfree = [r for r in pc.levels("BIL") if "2016-10-14" <= r[0] <= AS_OF]
    etf = [r for r in pc.levels("IWM") if "2016-10-14" <= r[0] <= AS_OF]
    full = {"portfolio": port, "Opal Long-Term": model_levels("LT"), "Opal Ultra Long-Term": model_levels("ULT"),
            "iShares Russell 2000 ETF": etf}
    want = expected_rows(full, bench, rfree)
    ret = sec[IDS[2]]["value"]
    risk_v = sec[IDS[3]]["value"]
    if not (isinstance(ret, dict) and isinstance(risk_v, dict)):
        return fails + ["returns / risk sections are not {rows, gaps} values: %r / %r" % (str(ret)[:120], str(risk_v)[:120])]
    if len(ret.get("rows") or []) != 4:
        fails.append("returns has %d rows, want 4 (the portfolio and three comparables)" % len(ret.get("rows") or []))
    for row in ret.get("rows") or []:
        exp = want["portfolio" if row["Name"] == "Your portfolio" or row is (ret["rows"] or [None])[0] else row["Name"]]
        for k, c in zip(PERIODS, ["1M", "3M", "YTD", "1Y", "3Y", "5Y", "10Y"]):
            if exp["returns"][k] is not None and not close(row.get(c), exp["returns"][k]):
                fails.append("returns %s %s is %r, want %r" % (row["Name"], c, row.get(c), exp["returns"][k]))
    for row in risk_v.get("rows") or []:
        exp = want["portfolio" if row is risk_v["rows"][0] else row["Name"]]["risk"]
        if not close(row.get("Std dev (%)"), exp["std_dev"]) or not close(row.get("Beta"), exp["beta"]):
            fails.append("risk %s std dev / beta are %r / %r, want %r / %r" % (row["Name"], row.get("Std dev (%)"), row.get("Beta"),
                                                                               exp["std_dev"], exp["beta"]))
    al = sec[IDS[4]]["value"]
    rows = {r.get("Name"): r for r in (al.get("rows") if isinstance(al, dict) else []) or []}
    port_row = [r for k, r in rows.items() if k not in ("Opal Long-Term", "Opal Ultra Long-Term", "iShares Russell 2000 ETF")]
    if not port_row or port_row[0].get("Equity") != 70.0 or port_row[0].get("Fixed Income") != 30.0:
        fails.append("the portfolio allocation row is %r, want Equity 70.0 and Fixed Income 30.0 (AAA 500 + CCC 200 equity, BBB 300 bond)" % port_row)
    lt = rows.get("Opal Long-Term") or {}
    for label, v in zip(ALLOC_LABELS, ALLOC["LT"]):
        if label in lt and lt[label] != v:
            fails.append("Opal Long-Term allocation %s is %r, want %r (positioning fixture)" % (label, lt[label], v))
    if (rows.get("iShares Russell 2000 ETF") or {}).get("Equity") != 100.0:
        fails.append("the ETF allocation row is %r, want Equity 100.0" % rows.get("iShares Russell 2000 ETF"))
    for text in ("Opal Long-Term", "Opal Ultra Long-Term", "iShares Russell 2000 ETF", "2024-04-14", "2026-10-14", "2026-10-19"):
        if text not in html:
            fails.append("the rendered page never prints %r" % text)
    for vendor in ("YCharts", "ycharts"):
        if vendor in html.replace("Licensed market data", ""):
            fails.append("the rendered page names the vendor (%s): R8" % vendor)
    # a comparable no price can be found for: stated in words, the others unchanged
    rec2, sec2, html2 = run_producer("multi_map.json", ENTRIES + [{"key": "ZZZZ", "label": "ZZZZ", "ticker": "ZZZZ"}])
    if "not available for ZZZZ" not in html2:
        fails.append("the page never prints 'not available for ZZZZ: <reason>' for the unpriced comparable")
    r2 = {e["id"]: e["status"] for e in rec2["elements"]}
    if any(r2.get(i) != "VALUE" for i in IDS):
        fails.append("an unpriced comparable took the section down: %r" % {i: r2.get(i) for i in IDS})
    # the Comparison map (one comparable) and the no-comparable and pricing-off cases
    rec3, sec3, _ = run_producer("comparison_map.json", ENTRIES[:1])
    if {e["id"]: e["status"] for e in rec3["elements"]}.get(IDS[2]) != "VALUE":
        fails.append("the Comparison map with one model comparable has no VALUE returns section")
    rec4, _, _ = run_producer("overview_map.json", None, models=False)
    if any(e["id"] in IDS for e in rec4["elements"]):
        fails.append("an Overview with no comparables lists compare elements")
    rec5, _, _ = run_producer("multi_map.json", ENTRIES, pricing=False)
    if any(e["id"] in IDS and e["status"] == "VALUE" for e in rec5["elements"]):
        fails.append("with pricing off a compare element reads VALUE")
    return fails


BUILD = {171: arms_build_171, 173: arms_build_173, 174: arms_build_174, 175: arms_build_175}
TEST_FILES = [TESTS + "/" + n for n in ("test_layout_overview.py", "test_opal_producer.py", "test_opal_producer_prices.py",
                                          "test_opal_producer_page_wording.py", "test_opal_producer_not_in_this_version.py",
                                          "test_price_pages_repoint.py", "test_price_pages_series.py", "test_price_pages_text.py",
                                          "test_price_pages_table.py", "test_producer_held_layout_guard.py")]
OWN = {171: (RES + "/model_source.py", RES + "/model_code_map.json", TESTS + "/test_model_source.py"),
       172: (IR.replace("lambda/investor-reporting/", "terraform/investor-reporting/") + "ycharts/iam.tf",),
       173: (RES + "/comparables.py", TESTS + "/test_comparables.py"),
       174: (RES + "/layout_overview.py", TESTS + "/test_compare_elements.py"),
       175: (RES + "/opal_producer.py", GEN + "/resident_worker.py", IR + "reports/resident_installed.py",
             TESTS + "/test_compare_producer.py", IR + "reports/tests/test_compare_ports.py")}
SLOT = {171: 330, 173: 330, 174: 330, 175: 330}
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/")
CH = "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md"


def status_map(rec):
    return {e["id"]: [e["status"], e.get("reason")] for e in rec["elements"]}


def baseline():
    doc = {}
    for label, mp, comps, pricing in (("overview_on", "overview_map.json", None, True), ("overview_off", "overview_map.json", None, False),
                                       ("multi_on", "multi_map.json", None, True), ("comparison_on", "comparison_map.json", None, True)):
        rec, _, _ = run_producer(mp, comps, pricing=pricing, models=False)
        doc[label] = status_map(rec)
    json.dump(doc, open(BASE_JSON, "w", encoding="utf-8", newline="\n"), indent=1, sort_keys=True)
    return doc


def arms_guard(cell):
    """Nothing outside the cell moves: every element of the Overview, the Multi and the Comparison reads as at the base (the new
    compare elements are absent when no comparable is given)."""
    fails = []
    base = json.load(open(BASE_JSON, encoding="utf-8"))
    for label, mp, pricing in (("overview_on", "overview_map.json", True), ("overview_off", "overview_map.json", False),
                               ("multi_on", "multi_map.json", True), ("comparison_on", "comparison_map.json", True)):
        rec, _, _ = run_producer(mp, None, pricing=pricing, models=False)
        got = status_map(rec)
        for i, want in base[label].items():
            if got.get(i) != want:
                fails.append("%s: %s reads %r, base %r" % (label, i, got.get(i), want))
        extra = sorted(set(got) - set(base[label]))
        if extra:
            fails.append("%s: new elements with no comparable given: %s" % (label, ", ".join(extra[:6])))
    return fails


def scope(cell):
    rc = subprocess.run(["git", "merge-base", "HEAD", "box/dell2"], capture_output=True)
    base = rc.stdout.decode().strip()
    if rc.returncode != 0 or not base:
        return ["no merge-base with box/dell2"]
    diff = subprocess.run(["git", "diff", "--name-only", base, "HEAD"], capture_output=True)
    if diff.returncode != 0:
        return ["git diff rc=%d" % diff.returncode]
    own = set(OWN[cell]) | {CH}
    for c in (171, 173, 174, 175):  # one worker queue: its earlier cells are already on its branch
        if c <= cell:
            own |= set(OWN[c])
    prefixes = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~%d/" % SLOT.get(cell, 330),) + ISSUER
    names = [n for n in diff.stdout.decode().splitlines() if n.strip()]
    stray = [n for n in names if n not in own and not n.startswith(prefixes) and "/task-orders/IRPT_ANLREQ.TO-AR-g-17" not in n]
    return ["outside the cell's write set: %s" % ", ".join(stray)] if stray else []


def regress(cell):
    fails = []
    own_tests = [p for c in (171, 173, 174, 175) if c <= cell for p in OWN[c] if "/tests/" in p and os.path.exists(p)]
    out = subprocess.run([sys.executable, "-m", "pytest", "--color=no", "-q", "-p", "no:cacheprovider"] + TEST_FILES + own_tests,
                         capture_output=True, text=True)
    last = ((out.stdout or out.stderr).strip().splitlines() or [""])[-1]
    if out.returncode != 0:
        fails.append("pytest rc=%d: %s" % (out.returncode, last))
    return fails + scope(cell)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "calibrate":
        fails = calibrate()
        print("AR-CMP-CALIBRATE-%s %s" % ("FAIL" if fails else "OK", "; ".join(fails) if fails else "the checker's formulas agree with the shipped layout"))
        return 1 if fails else 0
    if mode == "baseline":
        doc = baseline()
        print("AR-CMP-BASELINE-OK " + " ".join("%s=%d" % (k, len(v)) for k, v in sorted(doc.items())))
        return 0
    if mode not in ("171", "173", "174", "175") or (sys.argv[2:3] or [""])[0] not in ("build", "guard", "regress"):
        print("AR-CMP-FAIL usage: <171|173|174|175> build|guard|regress | calibrate | baseline")
        return 2
    cell, arm = int(mode), sys.argv[2]
    if arm == "regress":
        fails = regress(cell)
        print("AR-CMP-%d-REGRESS-%s %s" % (cell, "FAIL" if fails else "OK", "; ".join(fails)))
    else:
        fails = BUILD[cell]() if arm == "build" else arms_guard(cell)
        print("AR-CMP-%d-%s %s: %s" % (cell, "FAIL" if fails else "OK", arm, "; ".join(fails) if fails else "all arms"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
