#!/usr/bin/env python3
"""MDPF_CANON cell CN-p-2 -- the Global AUA Trend over full history, portal side (PRD v2.19, v2.20, v2.21; CRO spec amendment 1).

Issuer's check (2.0.0_SA_COO~D1). Read-only for every worker: never edit this file.

  python r9_cn_p_2.py oracle    the pure functions against the CRO spec's AMENDED period-end oracle ($M), Variant 1 (7 arms, 1 control)
  python r9_cn_p_2.py variants  Variant 2, the demo-tenant case, the stitch OFF for a non-internal session, carried points, notes (12 arms)
  python r9_cn_p_2.py wiring    the page, the types and the scope: tolerant source arms, whitespace-collapsed (10 arms, 2 controls)
  python r9_cn_p_2.py selftest  unpatched base red, reference green, one planted mutant per arm; issuer only

The logic is exercised, not grepped: `bun` imports <src>/lib/trendGrouping.ts and calls the exported pure functions on fixtures that follow the
CONTRACT of the producer cell CN-p-1 (top-level arrays client_supervised_aua, etf_strategies_aua, alt_strategies_aua aligned to dates[], and
carried_dates[]). The page arms read normalised text (CRLF folded, runs of whitespace collapsed to one space), so a rewrapped expression passes.

Target: a portal `src` directory: `<git toplevel>/portal/src`, or the directory in env R9_SRC (selftest and the base dry-run use it).
Output: `ROUND 9 CN-P-2 <NAME>: k of n arms`, exit 0 only when k == n. ASCII only.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_COMMIT = "f8c7d310dfef6ef5eb68a25f2244ae3245c7a2bf"   # scratch/canon-i3-base: PROD 5ab67a65 plus CN-i-1, CN-l-2, CN-i-2
OWNED = ("src/lib/trendGrouping.ts", "src/pages/ModelPortfolios.tsx", "src/api/portal-proxy.ts")
OWNED_TEST_RE = re.compile(r"^src/lib/trendGrouping[A-Za-z0-9._-]*\.test\.ts$")
PROTECTED = ("src/components/CategoryViewTree.tsx", "src/lib/otherModelsAsOf.ts", "src/api/endpoints/aum.ts")
N_ORACLE, N_VARIANTS, N_WIRING = 7, 12, 10


def root():
    return subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()


def src_root():
    return os.environ.get("R9_SRC") or os.path.join(root(), "portal", "src")


def read(p):
    try:
        with open(p, "rb") as fh:
            return fh.read().decode("utf-8")
    except OSError:
        return ""


def norm(text):
    return re.sub(r"\s+", " ", text.replace("\r\n", "\n"))


# ---------------------------------------------------------------------------------------------- fixtures
UST, ST, INT_, LT, ULT = "Ultra-Short Term", "Short Term", "Intermediate Term", "Long Term", "Ultra-Long Term"
PRIMARY = (UST, ST, INT_, LT, ULT)
BEGINS = "2026-05-15"
POOL_FROM = "2026-07-20"          # the first date the fold's pooled line is held by two firms (so served)
# The CRO spec's AMENDED oracle, $M: period end -> UST, ST, INT, LT, ULT, Custom, Client Sup., ETF, ALT, Total
ORACLE = (
    ("2024-12-31", 0.0, 64.3, 182.4, 118.6, 146.6, 0.0, 356.8, 5.8, 0.0, 874.6),
    ("2025-03-31", 72.7, 68.4, 201.5, 192.8, 152.8, 0.0, 275.8, 13.1, 0.0, 977.0),
    ("2025-06-30", 59.9, 69.9, 225.6, 279.4, 182.8, 0.0, 234.3, 17.2, 0.0, 1069.1),
    ("2025-09-30", 51.6, 76.6, 246.2, 361.4, 189.0, 0.0, 239.4, 19.9, 0.0, 1184.0),
    ("2025-12-31", 55.6, 80.1, 257.1, 506.0, 191.0, 0.0, 268.8, 22.2, 0.0, 1380.8),
    ("2026-03-31", 58.7, 93.4, 262.3, 600.0, 189.1, 0.0, 250.7, 23.7, 0.0, 1477.9),
    ("2026-06-30", 48.4, 111.3, 365.1, 755.8, 204.1, 34.3, 228.6, 23.1, 0.0, 1770.6),
    ("2026-09-30", 68.4, 131.9, 451.6, 872.9, 205.6, 66.9, 266.6, 21.2, 24.8, 2109.9),
    ("2026-10-13", 70.0, 138.3, 456.7, 888.5, 211.3, 69.2, 292.3, 21.5, 29.2, 2177.1),
)
M = 1_000_000.0


def dollars(x):
    return None if x is None else round(x * M, 2)


def oracle_fixture():
    dates = [r[0] for r in ORACLE]
    served = {"dates": dates, "total": [], "modelAua": [], "primary": {k: [] for k in PRIMARY}, "otherModels": [],
              "clientSupervised": [], "etfStrategies": [], "altStrategies": [], "carriedDates": []}
    firm49 = {k: [] for k in PRIMARY}
    infl = []
    for r in ORACLE:
        d = r[0]
        five = r[1:6]
        custom, client, etf, alt, total = r[6], r[7], r[8], r[9], r[10]
        pre = d < BEGINS
        served["total"].append(dollars(total))
        served["modelAua"].append(dollars(sum(five) + custom))
        for k, v in zip(PRIMARY, five):
            served["primary"][k].append(None if pre else dollars(v))
            if pre:
                firm49[k].append({"period": d, "aum": None if v == 0.0 else dollars(v)})   # UST holds no value before 2025-01-16
        served["otherModels"].append(dollars(custom) if d >= POOL_FROM else None)
        served["clientSupervised"].append(dollars(client))
        served["etfStrategies"].append(dollars(etf))
        # ALT draws nothing before its first observation (2026-09-30): the producer serves null, not 0
        served["altStrategies"].append(dollars(alt) if d >= "2026-09-30" else None)
        if BEGINS <= d < POOL_FROM and custom:
            infl.append({"period": d, "aum": dollars(custom)})
    return served, {"firm49": firm49, "inflectionCustom": infl}


def boundary_fixture():
    """A short axis around the fold boundary, the pool's first served date and the 05-30 .. 05-31 carried pair."""
    dates = ["2025-01-04", "2025-01-16", "2026-05-14", "2026-05-15", "2026-05-29", "2026-05-30", "2026-05-31", "2026-06-01",
             "2026-06-02", "2026-07-19", "2026-07-20"]
    n = len(dates)
    z = [None] * n

    def col(**kw):
        a = list(z)
        for d, v in kw.items():
            a[dates.index(d.replace("_", "-"))] = v
        return a
    served = {
        "dates": dates,
        "total": [800.0, 810.0, 1000.0, 1100.0, 1150.0, None, None, 1160.0, 1165.0, 1200.0, 1210.0],
        "modelAua": [500.0, 510.0, 700.0, 800.0, 840.0, None, None, 850.0, 855.0, 880.0, 890.0],
        "primary": {
            UST: col(**{"2026_05_15": 100.0, "2026_05_29": 105.0, "2026_06_01": 106.0, "2026_06_02": 107.0, "2026_07_19": 110.0, "2026_07_20": 111.0}),
            ST: col(**{"2026_05_15": 100.0, "2026_05_29": 105.0, "2026_06_01": 106.0, "2026_06_02": 107.0, "2026_07_19": 110.0, "2026_07_20": 111.0}),
            INT_: col(**{"2026_05_15": 200.0, "2026_05_29": 210.0, "2026_06_01": 212.0, "2026_06_02": 214.0, "2026_07_19": 220.0, "2026_07_20": 222.0}),
            LT: col(**{"2026_05_15": 250.0, "2026_05_29": 260.0, "2026_06_01": 262.0, "2026_06_02": 264.0, "2026_07_19": 270.0, "2026_07_20": 272.0}),
            ULT: col(**{"2026_05_15": 100.0, "2026_05_29": 105.0, "2026_06_01": 106.0, "2026_06_02": 107.0, "2026_07_19": 110.0, "2026_07_20": 111.0}),
        },
        "otherModels": col(**{"2026_07_20": 55.0}),
        "clientSupervised": [300.0, 301.0, 302.0, 303.0, 304.0, None, None, 305.0, None, 307.0, 308.0],
        "etfStrategies": [5.0, 5.0, 6.0, 7.0, 8.0, None, None, 9.0, 9.5, 10.0, 11.0],
        "altStrategies": z[:],
        "carriedDates": ["2025-01-04", "2026-05-30", "2026-05-31"],
    }
    # 49F's own series before the boundary (UST has no value before 2025-01-16: it is NEVER back-filled)
    firm49 = {
        UST: [{"period": "2026-05-14", "aum": 100.0}],
        ST: [{"period": "2026-05-14", "aum": 100.0}],
        INT_: [{"period": "2026-05-14", "aum": 200.0}],
        LT: [{"period": "2026-05-14", "aum": 200.0}],
        ULT: [{"period": "2026-05-14", "aum": 100.0}],
    }
    infl = [{"period": "2026-05-15", "aum": 50.0}, {"period": "2026-05-29", "aum": 52.0}, {"period": "2026-06-01", "aum": 53.0},
            {"period": "2026-06-02", "aum": 54.0}, {"period": "2026-07-19", "aum": 55.0}, {"period": "2026-07-20", "aum": 1.0}]
    return served, {"firm49": firm49, "inflectionCustom": infl}


def custom_fixture():
    """The measured Custom Models gap shape (real objects, 2026-10-13): the window before the pool is served (Inflection's series, one missing date
    first, one carried date), then dates where the pool is served (difference) and dates where it is not (Inflection-only would understate)."""
    dates = ["2026-05-14", "2026-05-15", "2026-05-29", "2026-05-30", "2026-06-01", "2026-07-20", "2026-07-28", "2026-07-29", "2026-08-03",
             "2026-08-04", "2026-08-05"]
    n = len(dates)
    gone = 3                       # 2026-05-30 is a carried date: every served array is null

    def keep(v, extra=()):
        return [None if i == gone or i in extra else v for i in range(n)]
    served = {
        "dates": dates,
        "total": [1000.0, 1100.0, 1101.0, None, 1102.0, 1140.0, 1144.0, 1143.0, 1145.0, 1146.0, 1146.5],
        "modelAua": [500.0, 526.0, 527.0, None, 528.0, 540.0, 544.0, 543.0, 545.0, None, 546.0],
        "primary": {k: [None, 100.0, 100.0, None, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0] for k in PRIMARY},
        "otherModels": [None, None, None, None, None, 40.0, None, None, 45.0, None, 46.0],
        "clientSupervised": keep(300.0, extra=(9,)),
        "etfStrategies": keep(5.0),
        "altStrategies": [None] * n,
        "carriedDates": ["2026-05-30"],
    }
    stitch = {
        "firm49": {k: [{"period": "2026-05-14", "aum": 100.0}] for k in PRIMARY},
        # 2026-05-15 has NO Inflection point (before the first value); 07-20 and 07-28 are understated; 07-29 is missing
        "inflectionCustom": [{"period": "2026-05-29", "aum": 27.0}, {"period": "2026-06-01", "aum": 28.0},
                             {"period": "2026-07-20", "aum": 38.0}, {"period": "2026-07-28", "aum": 37.0}],
    }
    return served, stitch


def build_fixtures():
    os_, ost = oracle_fixture()
    bs, bst = boundary_fixture()
    # an oracle served object whose total is NOT the sum of its parts, and whose group values are not cent-round
    fr = json.loads(json.dumps(os_))
    fr["total"][-1] = 123456789.123456
    fr["clientSupervised"][-1] = 98765432.123456
    fr["etfStrategies"][-1] = 11111111.111111
    fr["altStrategies"][-1] = 22222222.222222
    # the same object with the producer's arrays absent (older leaf)
    old = json.loads(json.dumps(bs))
    for k in ("clientSupervised", "etfStrategies", "altStrategies", "carriedDates", "otherModels"):
        old[k] = None
    # a measured zero in a served group
    zero = json.loads(json.dumps(bs))
    zero["clientSupervised"][4] = 0.0
    cs, cst = custom_fixture()
    return {"oracle": [os_, ost], "boundary": [bs, bst], "free": [fr, ost], "old": [old, bst], "zero": [zero, bst], "custom": [cs, cst], "begins": BEGINS}


# ---------------------------------------------------------------------------------------------- bun exercise
BUN_TS = r"""
import { pathToFileURL } from 'node:url'
import { readFileSync } from 'node:fs'
const mod: any = await import(pathToFileURL(process.env.R9_MODULE as string).href)
const fx: any = JSON.parse(readFileSync(process.env.R9_FIX as string, 'utf8'))
const out: any = {}
const need = ['buildGlobalTrendRows', 'trendModeFor', 'globalTrendFootnote', 'trendDetailNoteFor', 'trendPointClass', 'carriedTooltipLabel', 'compositionFootnote']
out.missing = need.filter((n) => typeof mod[n] !== 'function')
out.consts = { SUPPRESSED_FOOTNOTE: mod.SUPPRESSED_FOOTNOTE ?? null, MODELS_BAND_LABEL: mod.MODELS_BAND_LABEL ?? null }
out.legacy = {
  group: typeof mod.groupCustomModelsSeries === 'function', present: typeof mod.presentTrendEntries === 'function',
  note: typeof mod.trendDetailNote === 'function', cust: mod.CUSTOM_MODELS_LABEL ?? null,
}
const safe = (f: () => any) => { try { return { v: f() } } catch (e: any) { return { err: String(e && e.message || e).slice(0, 120) } } }
const build = (name: string, mode: string, withStitch = true) => {
  const [served, stitch] = fx[name]
  const before = JSON.stringify([served, stitch])
  const rows = mod.buildGlobalTrendRows(served, withStitch ? stitch : null, mode, fx.begins)
  return { rows, unchanged: before === JSON.stringify([served, stitch]) }
}
if (out.missing.length === 0) {
  out.o_v1 = safe(() => build('oracle', 'variant1'))
  out.free_v1 = safe(() => build('free', 'variant1'))
  out.o_v2 = safe(() => build('oracle', 'variant2'))
  out.b_v1 = safe(() => build('boundary', 'variant1'))
  out.b_v2 = safe(() => build('boundary', 'variant2'))
  out.b_v2_nostitch = safe(() => build('boundary', 'variant2', false))
  out.old_v1 = safe(() => build('old', 'variant1'))
  out.zero_v1 = safe(() => build('zero', 'variant1'))
  out.c_v1 = safe(() => build('custom', 'variant1'))
  out.c_v2 = safe(() => build('custom', 'variant2'))
  out.fn_v1 = safe(() => mod.globalTrendFootnote(build('boundary', 'variant1').rows, 'variant1'))
  out.fn_v2 = safe(() => mod.globalTrendFootnote(build('boundary', 'variant2').rows, 'variant2'))
  out.fn_v2_clean = safe(() => mod.globalTrendFootnote(build('oracle', 'variant2').rows.filter((r: any) => r.period >= '2026-07-20'), 'variant2'))
  out.mode = safe(() => [mod.trendModeFor(true), mod.trendModeFor(false), mod.trendModeFor(undefined), mod.trendModeFor('yes'), mod.trendModeFor(1), mod.trendModeFor(null)])
  out.note = safe(() => [mod.trendDetailNoteFor('variant1', '2026-05-15', '2024-11-01'), mod.trendDetailNoteFor('variant2', '2026-05-15', '2024-11-01'),
    mod.trendDetailNoteFor('variant2', '2026-05-15', '2026-05-15')])
  out.comp = safe(() => [mod.compositionFootnote('variant1'), mod.compositionFootnote('variant2')])
  out.cls = safe(() => [mod.trendPointClass('measured', ['total']), mod.trendPointClass('interpolated_estimate', ['total']),
    mod.trendPointClass('measured', []), mod.trendPointClass(undefined, [])])
  out.tip = safe(() => [mod.carriedTooltipLabel('Long Term', ['Long Term']), mod.carriedTooltipLabel('Long Term', 'Short Term|Long Term'),
    mod.carriedTooltipLabel('Long Term', []), mod.carriedTooltipLabel('Long Term', ''), mod.carriedTooltipLabel('Long Term', null)])
}
console.log(JSON.stringify(out))
"""


def run_bun(module):
    if not os.path.isfile(module):
        return None, "module not found: " + module
    d = tempfile.mkdtemp(prefix="r9cnp2_")
    try:
        ex = os.path.join(d, "exercise.ts")
        fx = os.path.join(d, "fixtures.json")
        with open(ex, "w", newline="\n", encoding="utf-8") as fh:
            fh.write(BUN_TS)
        with open(fx, "w", newline="\n", encoding="utf-8") as fh:
            json.dump(build_fixtures(), fh)
        env = dict(os.environ)
        env["R9_MODULE"] = module
        env["R9_FIX"] = fx
        try:
            r = subprocess.run(["bun", ex], capture_output=True, text=True, timeout=100, env=env, cwd=d)
        except subprocess.TimeoutExpired:
            return None, "bun exercise timed out"
        line = r.stdout.strip().splitlines()[-1:] or [""]
        try:
            return json.loads(line[0]), ""
        except ValueError:
            tail = (r.stderr or r.stdout).strip().splitlines()[-1:] or [""]
            return None, "exercise rc=%d, no JSON: %s" % (r.returncode, tail[0][:160])
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ---------------------------------------------------------------------------------------------- grading helpers
def rows_of(got, key):
    r = (got or {}).get(key) or {}
    return (r.get("v") or {}).get("rows"), r.get("err")


def by_period(rows):
    return {r["period"]: r for r in rows}


def mm(x):
    return None if x is None else x / M


def close(a, b, tol=0.05):
    return a is not None and b is not None and abs(a - b) <= tol


def no_fn(got, err):
    if got is None:
        return "no result (%s)" % err
    if got.get("missing"):
        return "missing exports: " + ",".join(got["missing"])
    return ""


def oracle_arms(got, err):
    miss = no_fn(got, err)
    arms = []

    def arm(i, ok, why):
        arms.append((i, bool(ok), why if ok else ("FAIL: " + why)))
    legacy = (got or {}).get("legacy") or {}
    arm("C1", legacy.get("group") and legacy.get("present") and legacy.get("note") and legacy.get("cust") == "Custom Models",
        "control: the CN-i-1/CN-i-2 exports (groupCustomModelsSeries, presentTrendEntries, trendDetailNote, CUSTOM_MODELS_LABEL) stay exported")
    if miss:
        for i in ("O1", "O2", "O3", "O4", "O5", "O6"):
            arm(i, False, miss)
        return arms
    rows, e = rows_of(got, "o_v1")
    if not rows:
        for i in ("O1", "O2", "O3", "O4", "O5", "O6"):
            arm(i, False, "buildGlobalTrendRows threw: %s" % e)
        return arms
    P = by_period(rows)
    bad, sums = [], []
    for r in ORACLE:
        d = r[0]
        row = P.get(d)
        if row is None:
            bad.append(d + " missing")
            continue
        got_vals = [mm(row["models"].get(k)) for k in PRIMARY] + [mm(row["custom"]), mm(row["clientSupervised"]), mm(row["etfStrategies"]), mm(row["altStrategies"])]
        for name, a, b in zip(("UST", "ST", "INT", "LT", "ULT", "Custom", "Client", "ETF", "ALT"), got_vals, r[1:10]):
            if not close(a if a is not None else 0.0, b):
                bad.append("%s %s %s vs %s" % (d, name, a, b))
        sums.append((d, sum(v or 0.0 for v in got_vals), r[10]))
    arm("O1", not bad, "all 9 period-end rows match the amended oracle to 0.05 $M (%s)" % ("; ".join(bad[:4]) or "no mismatch"))
    off = [(d, round(s, 2), t) for d, s, t in sums if abs(s - t) > 0.15]
    arm("O2", len(sums) == 9 and not off, "each row's groups sum to its Total within 0.15 $M, the oracle's own 1-dp rounding (off: %s)" % off[:3])
    r1 = P.get("2024-12-31") or {}
    r6 = P.get("2026-06-30") or {}
    arm("O3", r1.get("models", {}).get(UST) is None and close(mm(r1.get("etfStrategies")), 5.8) and r6.get("altStrategies") is None
        and r1.get("altStrategies") is None,
        "ABSENT IS NOT ZERO and never back-filled: UST at 2024-12-31 is null, ETF there is the SMA history 5.8, ALT before 2026-09-30 is null")
    fr, e2 = rows_of(got, "free_v1")
    last = (by_period(fr).get("2026-10-13") if fr else None) or {}
    arm("O4", last.get("total") == 123456789.123456, "the Total is a FIELD READ: it equals the served opal_aggregate_aua exactly, though the groups do not sum to it (%s)" % last.get("total"))
    arm("O5", last.get("clientSupervised") == 98765432.123456 and last.get("etfStrategies") == 11111111.111111 and last.get("altStrategies") == 22222222.222222,
        "Client Supervised, ETF and ALT are read as served, with no arithmetic and no rounding (%s, %s, %s)"
        % (last.get("clientSupervised"), last.get("etfStrategies"), last.get("altStrategies")))
    retired = [k for row in rows for k in row if k in ("otherAua", "nonModel", "clientUnsupervised", "clientUnsup")]
    r9 = P.get("2026-09-30") or {}
    arm("O6", not retired and close(mm(r9.get("custom")), 66.9) and close(mm(r6.get("custom")), 34.3),
        "Client Unsupervised and Other AUA are retired (no field); Custom is the served difference once the pool is held (66.9) and Inflection's own series inside the window (34.3)")
    return arms


def variants_arms(got, err):
    miss = no_fn(got, err)
    ids = ("V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11", "V12")
    arms = []

    def arm(i, ok, why):
        arms.append((i, bool(ok), why if ok else ("FAIL: " + why)))
    if miss:
        return [(i, False, "FAIL: " + miss) for i in ids]
    b1, e1 = rows_of(got, "b_v1")
    b2, e2 = rows_of(got, "b_v2")
    n2, _ = rows_of(got, "b_v2_nostitch")
    if not b1 or not b2:
        return [(i, False, "FAIL: buildGlobalTrendRows threw: %s %s" % (e1, e2)) for i in ids]
    P1, P2 = by_period(b1), by_period(b2)
    # V1: Variant 2 before the boundary: one Models band, no per-model line, no Custom
    pre2 = P2["2026-05-14"]
    pre1 = P1["2026-05-14"]
    arm("V1", pre2["modelsBand"] == 700.0 and all(v is None for v in pre2["models"].values()) and pre2["custom"] is None
        and pre1["modelsBand"] is None and pre1["models"][ST] == 100.0 and pre1["models"][LT] == 200.0,
        "before 2026-05-15 a Variant 2 session draws one Models band (700) and no model line; Variant 1 draws 49F's lines and no band")
    # V2: Custom in the single-firm window
    w2, w1 = P2["2026-06-01"], P1["2026-06-01"]
    arm("V2", w2["custom"] is None and w2["customSuppressed"] is True and w1["custom"] == 53.0 and w1["customSuppressed"] is False,
        "05-15 .. 07-19: Variant 2 suppresses Custom (and flags it); Variant 1 draws Inflection's own series (53)")
    # V3: the demo tenant
    m = (got.get("mode") or {}).get("v") or []
    demo_internal = ("demo" == "opal-capital") or ("Client" == "Dev")      # the page's rule: firmId opal-capital or userType Dev
    ok_mode = len(m) == 6 and m[0] == "variant1" and m[1] == "variant2" and m[2] == "variant2" and m[3] == "variant2" and m[4] == "variant2" and m[5] == "variant2"
    arm("V3", ok_mode and demo_internal is False,
        "demo tenant (firmId demo, not opal-capital, not Dev): internal false -> variant2; only a literal true gives variant1; undefined, 'yes', 1 and null fail closed (%s)" % m)
    # V4: the stitch is OFF for a non-internal session: passing it changes nothing
    arm("V4", n2 is not None and json.dumps(b2, sort_keys=True) == json.dumps(n2, sort_keys=True)
        and all(v is None for r in b2 if r["period"] < BEGINS for v in r["models"].values()),
        "a Variant 2 build with the stitch passed equals one without it: the single-firm series never reach a non-internal row")
    # V5: carried
    c = P1["2026-05-30"]
    keys = set(c["carried"])
    need = {"total", UST, ST, INT_, LT, ULT, "Custom Models", "Client Supervised", "ETF Strategies"}
    arm("V5", need <= keys and c["total"] == 1150.0 and c["models"][LT] == 260.0 and c["clientSupervised"] == 304.0 and c["custom"] == 52.0
        and P1["2026-05-31"]["total"] == 1150.0 and P1["2026-05-29"]["carried"] == [] and P1["2026-06-01"]["carried"] == [],
        "the nine-style no-total dates take the last known value and name every carried group; a served date carries nothing (carried 05-30: %s)" % sorted(keys))
    # V6: roll forward only, and only on a listed date
    pre_first = P1["2025-01-04"]
    gap = P1["2026-06-02"]
    arm("V6", pre_first["models"][UST] is None and "Ultra-Short Term" not in pre_first["carried"] and pre_first["total"] == 800.0 and gap["clientSupervised"] is None
        and "Client Supervised" not in gap["carried"],
        "roll FORWARD only: a carried date before a series' first value stays null; a null on a date not listed in carried_dates is not filled")
    # V7: footnote and the boundary note
    fn1 = (got.get("fn_v1") or {}).get("v")
    fn2 = (got.get("fn_v2") or {}).get("v")
    fn2c = (got.get("fn_v2_clean") or {}).get("v")
    note = (got.get("note") or {}).get("v") or [None, None, None]
    comp = (got.get("comp") or {}).get("v") or [None, None]
    arm("V7", fn1 is None and fn2 == "models held at one firm are in the total and not broken out" and fn2c is None
        and note[0] is None and isinstance(note[1], str) and "May 15, 2026" in note[1] and note[2] is None
        and isinstance(comp[0], str) and "Inflection" in comp[0] and "Cottonwood" in comp[0] and comp[1] is None,
        "footnotes: Variant 2 inside the window only, exact text; none for Variant 1. 'Per-model detail begins' note: Variant 2 only. Composition steps: internal only (got %s | %s | %s)" % (fn2, note, comp))
    # V8: classes and tooltip label
    cls = (got.get("cls") or {}).get("v") or []
    tip = (got.get("tip") or {}).get("v") or []
    arm("V8", cls == ["carried", "interpolated_estimate", "measured", None] and tip == ["Long Term (carried)", "Long Term (carried)", "Long Term", "Long Term", "Long Term"],
        "a carried point carries class 'carried' (the estimate wins); the tooltip names a carried value (%s | %s)" % (cls, tip))
    # V9: no mutation, one row per date in order
    ok9 = (got.get("b_v1") or {}).get("v", {}).get("unchanged") is True and (got.get("o_v2") or {}).get("v", {}).get("unchanged") is True \
        and [r["period"] for r in b1] == sorted(P1) and len(b1) == 11
    arm("V9", ok9, "the served object and the stitch are not mutated; one row per served date, in order")
    # V10: absent is not zero, a measured zero stays
    z, _ = rows_of(got, "zero_v1")
    o, _ = rows_of(got, "old_v1")
    ok10 = bool(z) and by_period(z)["2026-05-29"]["clientSupervised"] == 0.0 and P1["2026-06-02"]["altStrategies"] is None and bool(o) \
        and all(r["clientSupervised"] is None and r["etfStrategies"] is None and r["altStrategies"] is None for r in o) \
        and not {"Client Supervised", "ETF Strategies", "ALT Strategies"} & set(by_period(o)["2026-05-30"]["carried"])
    arm("V10", ok10, "a measured zero stays 0; a missing array (an older leaf) yields nulls and no carried group for it, never 0")
    # V11 / V12: Custom Models rolls forward (Variant 1), on the measured gap shape
    cv1, ce1 = rows_of(got, "c_v1")
    cv2, ce2 = rows_of(got, "c_v2")
    if not cv1 or not cv2:
        arm("V11", False, "buildGlobalTrendRows threw: %s %s" % (ce1, ce2))
        arm("V12", False, "buildGlobalTrendRows threw: %s %s" % (ce1, ce2))
        return arms
    want1 = [None, None, 27.0, 27.0, 28.0, 40.0, 40.0, 40.0, 45.0, 45.0, 46.0]
    have1 = [r["custom"] for r in cv1]
    roll_only_custom = all(cv1[i]["carried"] == ["Custom Models"] for i in (6, 7, 9)) and "Custom Models" in cv1[3]["carried"]         and all(cv1[i]["carried"] == [] for i in (2, 4, 5, 8, 10)) and cv1[9]["clientSupervised"] is None
    arm("V11", have1 == want1 and roll_only_custom,
        "Variant 1: Custom Models carries its last known value on every date after its first (the carried 05-30, the pool-less 07-28 and 07-29, the no-model-AUA 08-04), "
        "not Inflection-only once the pool is served, never before the first value; only Custom is rolled and it is named in row.carried (got %s)" % have1)
    want2 = [None, None, None, None, None, 40.0, None, None, 45.0, None, 46.0]
    have2 = [r["custom"] for r in cv2]
    flags2 = [r["customSuppressed"] for r in cv2]
    arm("V12", have2 == want2 and all("Custom Models" not in r["carried"] for r in cv2) and flags2[1] and flags2[6] and not flags2[9]
        and not any(r["customSuppressed"] for r in cv1) and have1[:2] == [None, None],
        "Variant 2 never rolls Custom (suppressed stays suppressed, flagged where model AUA exists); Variant 1 flags nothing and fills nothing before the first value (got %s)" % have2)
    return arms


# ---------------------------------------------------------------------------------------------- wiring arms
def stripped(page):
    return re.sub(r"import \{[^}]*\} from '@/lib/trendGrouping'", "", norm(page))


def wiring_arms(src):
    page = read(os.path.join(src, "pages", "ModelPortfolios.tsx"))
    proxy = norm(read(os.path.join(src, "api", "portal-proxy.ts")))
    mod = norm(read(os.path.join(src, "lib", "trendGrouping.ts")))
    P = stripped(page)
    full = norm(page)
    arms = []

    def arm(i, ok, why):
        arms.append((i, bool(ok), why if ok else ("FAIL: " + why)))
    arm("W1", re.search(r"buildGlobalTrendRows\(", P) is not None and re.search(r"trendModeFor\(\s*internal\s*\)", P) is not None,
        "the page calls buildGlobalTrendRows and derives the mode as trendModeFor(internal) (the page's own isInternal() || isDev())")
    gated = []
    for firm in ("49financial", "inflection"):
        ok = False
        for m in re.finditer(r"getMdpfAggregateAUATimeSeriesByFirm\(\s*'%s'\s*\)" % firm, P):
            win = P[m.start(): m.start() + 420]
            en = re.search(r"enabled:\s*([^,}]*)", win)
            if en and "internal" in en.group(1) and "global" in en.group(1):
                ok = True
        gated.append(ok)
    arm("W2", all(gated), "the two single-firm reads (49financial, inflection) are enabled only when internal and the scope is global (%s)" % gated)
    gone = [t for t, rx in (("clientChipAt(", r"\bclientChipAt\("), ("otherAua(", r"\botherAua\("), ("etfStrategiesAua(", r"\betfStrategiesAua\("),
                            ("hasGlobalEnterprise", r"\bhasGlobalEnterprise\b"), ("hasClientChips", r"\bhasClientChips\b"),
                            ("clientUnsupAsOf", r"\bclientUnsupAsOf\b"), ("legend Client Unsupervised", r"\{ label: 'Client Unsupervised'")) if re.search(rx, P)]
    arm("W3", not gone, "the as-of Client chips, Other AUA at Global and the old arithmetic are retired from the page (still present: %s)" % (gone or "none"))
    arm("W4", re.search(r"trendDetailNoteFor\(", P) is not None and re.search(r"(?<![A-Za-z])trendDetailNote\(", P) is None
        and re.search(r"globalTrendFootnote\(", P) is not None and "data-trend-footnote" in P
        and re.search(r"compositionFootnote\(", P) is not None and "data-trend-composition" in P,
        "the boundary note goes through trendDetailNoteFor(mode, ...); the footnotes through globalTrendFootnote and compositionFootnote with data-trend-footnote and data-trend-composition elements")
    arm("W5", re.search(r"carriedTooltipLabel\(", P) is not None and re.search(r"trendPointClass\(", P) is not None and CARRIED_LEGEND_RE.search(P) is not None,
        "carried points: the tooltip label, the point class and the legend entry go through the module")
    need = ("client_supervised_aua", "etf_strategies_aua", "alt_strategies_aua", "carried_dates")
    arm("W6", all(re.search(r"\b%s\??:" % k, proxy) for k in need), "portal-proxy.ts types the four new optional fields: " + ", ".join(need))
    raw_mod = read(os.path.join(src, "lib", "trendGrouping.ts"))
    fn_ok = bool(re.search(r"export function buildGlobalTrendRows", mod)) and not re.search(r"^\s*import\s", raw_mod, re.M) and "fetch(" not in raw_mod
    arm("W7", fn_ok, "the module stays pure: exports buildGlobalTrendRows and imports nothing")
    # controls: the approved edits ride the row unchanged
    tree = read(os.path.join(src, "components", "CategoryViewTree.tsx"))
    sm = re.search(r"const trendStitch\b.*?\}, \[internal", P)
    arm("W9", sm is not None and "groupCustomModelsSeries(" in sm.group(0) and "rollBlendsIntoArchetypeSeries(" not in sm.group(0),
        "the stitch's Inflection Custom is the UNROLLED blends: the stitch memo groups the Inflection series with groupCustomModelsSeries and does not roll the blends into the archetypes first")
    arm("C2", "'Client - Opal Unsupervised': PALETTE.lime500" in norm(tree) and "carriedAsOf" in full and "asOfLabel" in full,
        "control: the approved edits are intact (lime Client Unsupervised, the Other Models 'as of' wiring)")
    arms.append(scope_arm(src))
    return arms


CARRIED_LEGEND_RE = re.compile(r"CARRIED_LEGEND_LABEL")


def scope_arm(src):
    def mk(ok, why):
        return ("W8", ok, why if ok else "FAIL: " + why)
    portal = os.path.dirname(src.rstrip("/\\"))
    if not os.path.isdir(os.path.join(portal, ".git")) and not os.path.isfile(os.path.join(portal, ".git")):
        # no git: protected files only (selftest trees)
        return mk(True, "scope: no git beside this src; protected-file arm skipped (selftest tree)")
    try:
        names = subprocess.check_output(["git", "-C", portal, "diff", "--name-only", BASE_COMMIT], text=True).split()
        untracked = subprocess.check_output(["git", "-C", portal, "ls-files", "--others", "--exclude-standard", "src"], text=True).split()
    except (OSError, subprocess.CalledProcessError) as exc:
        return mk(False, "git read failed: %s" % exc)
    extra = [n for n in names + untracked if n not in OWNED and not OWNED_TEST_RE.match(n)]
    moved = [p for p in PROTECTED if p in names]
    mixed = []
    for rel in OWNED:
        with open(os.path.join(portal, *rel.split("/")), "rb") as fh:
            raw = fh.read()
        if raw.count(b"\n") != raw.count(b"\r\n"):
            mixed.append(rel)
    return mk(not extra and not moved and not mixed,
              "scope: only the three owned files (and a trendGrouping test) differ from the base; protected files byte-equal; every line of the owned files CRLF (extra: %s; protected moved: %s; mixed endings: %s)" % (extra[:4], moved, mixed))


def report(name, arms):
    for i, ok, why in arms:
        print("  %-4s %s  %s" % (i, "PASS" if ok else "FAIL", why))
    k = sum(1 for a in arms if a[1])
    print("ROUND 9 CN-P-2 %s: %d of %d arms" % (name, k, len(arms)))
    return k, len(arms)


def run_pure(src):
    got, err = run_bun(os.path.join(src, "lib", "trendGrouping.ts"))
    return got, err


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("oracle", "variants", "wiring", "selftest"):
        print(__doc__)
        return 2
    mode = sys.argv[1]
    if mode == "selftest":
        return selftest()
    src = src_root()
    if mode == "oracle":
        got, err = run_pure(src)
        k, n = report("ORACLE", oracle_arms(got, err))
    elif mode == "variants":
        got, err = run_pure(src)
        k, n = report("VARIANTS", variants_arms(got, err))
    else:
        k, n = report("WIRING", wiring_arms(src))
    return 0 if k == n else 1


def selftest():
    import importlib.util
    spec = importlib.util.spec_from_file_location("mk", os.path.join(HERE, "ref", "make_reference_cn_p_2.py"))
    mk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mk)
    portal = os.path.join(root(), "portal") if not os.environ.get("R9_PORTAL") else os.environ["R9_PORTAL"]
    d = tempfile.mkdtemp(prefix="r9cnp2_self_")
    ok_all = True
    try:
        def arms_for(src):
            got, err = run_pure(src)
            return oracle_arms(got, err) + variants_arms(got, err) + wiring_arms(src)

        def tree(name, mutant=None, ref=True):
            p = os.path.join(d, name)
            mk.build(p, mutant, portal, ref)
            return p
        n_expected = N_ORACLE + N_VARIANTS + N_WIRING
        base = arms_for(tree("base", None, ref=False))
        red = sorted(a[0] for a in base if not a[1])
        green = sorted(a[0] for a in base if a[1])
        print("selftest unpatched base: green (controls)", green, "red", len(red), "of", len(base))
        ok_all &= len(base) == n_expected and set(green) == {"C1", "C2", "W8"}
        ref = arms_for(tree("ref"))
        print("selftest reference tree:", sum(1 for a in ref if a[1]), "of", len(ref))
        for a in ref:
            if not a[1]:
                print("   ref RED:", a[0], a[2][:200])
        ok_all &= len(ref) == n_expected and all(a[1] for a in ref)
        for mut, expect in mk.MUTANTS:
            arms = arms_for(tree("m_" + mut, mut))
            red = sorted(a[0] for a in arms if not a[1])
            hit = all(e in red for e in expect)
            print("selftest mutant %-12s red %s -> %s" % (mut, red, "OK" if hit else "NOT CAUGHT (wanted %s)" % (expect,)))
            ok_all &= hit
    finally:
        shutil.rmtree(d, ignore_errors=True)
    print("ROUND 9 CN-P-2 SELFTEST: %s" % ("OK" if ok_all else "NOT OK"))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
