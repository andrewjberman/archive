#!/usr/bin/env python3
"""MDPF_CANON round 11 cell CN-s-4 (FWD-9 head a, and the demo-tenant wiring 4b) -- check, 2.0.0_SA_COO~D1, 2026-10-16. Not issued.

PRD v2.23 FWD-9 head (a): a non-internal Global session (Variant 2) must never draw the Models band together with the model stack.
In buildGlobalTrendRows the band is set only before per_model_detail_begins, but the carry-forward loop rolls the last known band
onto a carried date AFTER the boundary (row MDPF_CANON-D1-S29). Repair 4a: the Models band is never carried on or after the boundary.
Head (b) demo wiring, repair 4b: the demo tenant session draws Variant 1 (trendModeFor takes a demo flag; the page gates the
Variant 1 stitch on variant1Session = internal || demoTenant instead of bare internal).

  python r11_cn_s_4.py pure       six arms on the exported pure function, run under bun on fixtures (S0, S3, S5 are controls)
  python r11_cn_s_4.py real       five arms on the REAL served Global aggregate (ref/served_global_aggregate_20261015.json), run under bun
  python r11_cn_s_4.py wiring     ten arms: trendModeFor under bun (P1-P4, P4 also with one argument) and the page wiring read as text (W5-W10)
  python r11_cn_s_4.py selftest   issuer only: the base reads where it should, a scratch reference (both repairs) reads green, one planted
                                  mutant per group reddens its arm, then CN-S-4 SELFTEST: OK

Target: <git toplevel>/portal/src, or the directory in env R11_SRC. Output: `ROUND 11 CN-S-4 <MODE>: k of n arms`, exit 0 only when k == n.
Units (real): the served aggregate and the rows are in dollars (USD); R3 tolerance 0.01 dollars. ASCII only.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SERVED = os.path.join(HERE, "ref", "served_global_aggregate_20261015.json")
PRIMARY = ["Ultra-Short Term", "Short Term", "Intermediate Term", "Long Term", "Ultra-Long Term"]
BEGINS = "2026-05-15"
TOL = 0.01
N_PURE, N_REAL, N_WIRING = 6, 5, 10

BUN_TS = r"""
import { pathToFileURL } from 'node:url'
const mod: any = await import(pathToFileURL(process.env.R11_MODULE as string).href)
const fx: any = JSON.parse(process.env.R11_FIX_JSON as string)
const out: any = {}
out.missing = ['buildGlobalTrendRows'].filter((n) => typeof mod[n] !== 'function')
const safe = (f: () => any) => { try { return { v: f() } } catch (e: any) { return { err: String(e && e.message || e).slice(0, 120) } } }
if (out.missing.length === 0) {
  const run = (mode: string) => {
    const before = JSON.stringify(fx.served)
    const rows = mod.buildGlobalTrendRows(fx.served, fx.stitch, mode, fx.begins)
    return { rows, unchanged: before === JSON.stringify(fx.served) }
  }
  out.v1 = safe(() => run('variant1'))
  out.v2 = safe(() => run('variant2'))
}
console.log(JSON.stringify(out))
"""

# REAL: the page's own helpers (pairedProvenanceRead, modelPortfolioColors) build the served object exactly as the page
# does (ModelPortfolios.tsx globalTrendServed memo), then the module builds the rows. Only the lib directory is read.
BUN_REAL_TS = r"""
import { pathToFileURL } from 'node:url'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'
const lib = process.env.R11_LIB as string
const load = (f: string) => import(pathToFileURL(join(lib, f)).href)
const tg: any = await load('trendGrouping.ts')
const pv: any = await load('pairedProvenanceRead.ts')
const mc: any = await load('modelPortfolioColors.ts')
const g: any = JSON.parse(readFileSync(process.env.R11_SERVED as string, 'utf8'))
const out: any = {}
out.missing = ['buildGlobalTrendRows', 'trendModeFor', 'GLOBAL_PRIMARY_LABELS', 'MODELS_BAND_LABEL', 'readGlobalEnterpriseSeries', 'readModelSeries', 'getCanonicalModelName']
  .filter((n) => ((tg[n] ?? pv[n] ?? mc[n]) === undefined))
const safe = (f: () => any) => { try { return { v: f() } } catch (e: any) { return { err: String(e && e.message || e).slice(0, 160) } } }
const served = (): any => {
  const ser = pv.readGlobalEnterpriseSeries(g)
  const primary: Record<string, any[]> = {}
  const gb = g.by_model ?? {}
  for (const key of Object.keys(gb)) {
    if (gb[key].cohort_class === 'sma') continue
    const label = mc.getCanonicalModelName(gb[key].display_name)
    if ((tg.GLOBAL_PRIMARY_LABELS as string[]).includes(label)) primary[label] = pv.readModelSeries(g, key).map((p: any) => p.value)
  }
  return {
    dates: g.dates,
    total: ser.map((p: any) => p.totalAua),
    modelAua: ser.map((p: any) => p.modelAua),
    primary,
    otherModels: 'other_models' in gb ? pv.readModelSeries(g, 'other_models').map((p: any) => p.value) : null,
    clientSupervised: g.client_supervised_aua ?? null,
    etfStrategies: g.etf_strategies_aua ?? null,
    altStrategies: g.alt_strategies_aua ?? null,
    carriedDates: g.carried_dates ?? null,
  }
}
out.begins = g.meta?.by_model_fold?.per_model_detail_begins ?? null
if (out.missing.length === 0) {
  const sv = served()
  const before = JSON.stringify(sv)
  out.v2 = safe(() => tg.buildGlobalTrendRows(sv, null, 'variant2', out.begins))
  out.v1 = safe(() => tg.buildGlobalTrendRows(sv, null, 'variant1', out.begins))
  out.unchanged = JSON.stringify(sv) === before
}
console.log(JSON.stringify(out))
"""

# WIRING: trendModeFor called under bun, pure, on the real module.
BUN_WIRING_TS = r"""
import { pathToFileURL } from 'node:url'
import { join } from 'node:path'
const tg: any = await import(pathToFileURL(join(process.env.R11_LIB as string, 'trendGrouping.ts')).href)
const out: any = {}
out.missing = ['trendModeFor'].filter((n) => typeof tg[n] !== 'function')
const safe = (f: () => any) => { try { return { v: f() } } catch (e: any) { return { err: String(e && e.message || e).slice(0, 160) } } }
if (out.missing.length === 0) {
  out.p1 = safe(() => tg.trendModeFor(false, true))
  out.p2 = safe(() => tg.trendModeFor(true, false))
  out.p3 = safe(() => tg.trendModeFor(false, false))
  out.p4 = safe(() => tg.trendModeFor(true, true))
  out.p4a = safe(() => tg.trendModeFor(true))
  out.p4b = safe(() => tg.trendModeFor(false))
}
console.log(JSON.stringify(out))
"""

# Repairs and planted mutants are text edits of the two files. Each needle must occur exactly the stated number of times.
CARRY_OLD = "if (v[key] === null && rolls && lastKnown[key] !== undefined && lastKnown[key] !== null) {"
CARRY_BAND_NEW = ("if (v[key] === null && rolls && !(key === MODELS_BAND_LABEL && !pre) && lastKnown[key] !== undefined "
                  "&& lastKnown[key] !== null) {")
MODE_OLD = "export const trendModeFor = (internal: boolean): TrendMode => (internal === true ? 'variant1' : 'variant2')"
MODE_NEW = ("export const trendModeFor = (internal: boolean, demo: boolean = false): TrendMode => "
            "(internal === true || demo === true ? 'variant1' : 'variant2')")
PAGE_EDITS = [
    ("  const internal = isInternal() || isDev()\n",
     "  const internal = isInternal() || isDev()\n  const demoTenant = MDPF_GLOBAL_VIEW_FIRMS.has(claims?.firmId ?? '')\n"
     "  const variant1Session = internal || demoTenant\n", 1),
    ("const trendMode = trendModeFor(internal)", "const trendMode = trendModeFor(internal, demoTenant)", 1),
    ("enabled: effectiveFirmId === 'global' && internal,", "enabled: effectiveFirmId === 'global' && variant1Session,", 2),
    ("if (!internal) return null", "if (!variant1Session) return null", 1),
    ("}, [internal, firm49MdpfData, inflectionMdpfData])", "}, [variant1Session, firm49MdpfData, inflectionMdpfData])", 1),
]
GATE_NEW = "enabled: effectiveFirmId === 'global' && variant1Session,"
GATE_OLD = "enabled: effectiveFirmId === 'global' && internal,"


class EditError(Exception):
    pass


def read_text(path):
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8")


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(text.encode("utf-8"))


def sub_exact(text, old, new, count=1):
    crlf = "\r\n" in text
    o = old.replace("\n", "\r\n") if crlf else old
    n = new.replace("\n", "\r\n") if crlf else new
    got = text.count(o)
    if got != count:
        raise EditError("needle found %d times, wanted %d: %s" % (got, count, old[:80]))
    return text.replace(o, n)


def fixture():
    # 05-13 and 05-14 are before the boundary; 05-15 is the boundary date, measured; 05-16 and 05-17 are carried dates (no total, no legs).
    dates = ["2026-05-13", "2026-05-14", "2026-05-15", "2026-05-16", "2026-05-17"]
    n = [None] * 5
    primary = {k: list(n) for k in PRIMARY}
    for i, v in ((2, 10.0),):
        for k in PRIMARY:
            primary[k][i] = v
    total = [100.0, 101.0, 150.0, None, None]
    model_aua = [40.0, 41.0, 50.0, None, None]
    served = {
        "dates": dates, "total": total, "modelAua": model_aua, "primary": primary,
        "otherModels": [None, None, 5.0, None, None],
        "clientSupervised": [30.0, 30.0, 30.0, None, None], "etfStrategies": [20.0, 20.0, 20.0, None, None],
        "altStrategies": [None, None, 50.0, None, None], "carriedDates": ["2026-05-16", "2026-05-17"],
    }
    # the stitch is OFF for variant 2 (non-internal): a null stitch, as the page passes it
    return {"served": served, "stitch": None, "begins": BEGINS}


def run_ts(ts, env_extra):
    d = tempfile.mkdtemp(prefix="r11cns4_")
    try:
        ex = os.path.join(d, "exercise.ts")
        write_text(ex, ts)
        env = dict(os.environ, **env_extra)
        try:
            r = subprocess.run(["bun", ex], capture_output=True, text=True, encoding="utf-8", errors="replace",
                               timeout=100, env=env, cwd=d)
        except subprocess.TimeoutExpired:
            return None, "bun exercise timed out"
        line = (r.stdout.strip().splitlines() or [""])[-1]
        try:
            return json.loads(line), ""
        except ValueError:
            tail = (r.stderr or r.stdout).strip().splitlines()[-1:] or [""]
            return None, "exercise rc=%d, no JSON: %s" % (r.returncode, tail[0][:160])
    finally:
        shutil.rmtree(d, ignore_errors=True)


def src_root():
    if os.environ.get("R11_SRC"):
        return os.environ["R11_SRC"]
    top = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    return os.path.join(top, "portal", "src")


# ---------------------------------------------------------------------------------------------- pure
def run_pure(module):
    if not os.path.isfile(module):
        return None, "module not found: " + module
    return run_ts(BUN_TS, {"R11_MODULE": module, "R11_FIX_JSON": json.dumps(fixture())})


def grade(got, err):
    """Returns a list of (name, ok, detail)."""
    if got is None:
        return [("exercise", False, err)]
    if got.get("missing"):
        return [("exports", False, "missing " + ",".join(got["missing"]))]
    v1 = (got.get("v1") or {}).get("v") or {}
    v2 = (got.get("v2") or {}).get("v") or {}
    r1, r2 = v1.get("rows"), v2.get("rows")
    if not r1 or not r2:
        return [("rows", False, "no rows: %s %s" % ((got.get("v1") or {}).get("err"), (got.get("v2") or {}).get("err")))]
    p2 = {r["period"]: r for r in r2}
    arms = []
    # S0 control: before the boundary Variant 2 still draws the band (the model assets it cannot break out)
    arms.append(("S0 control: before the boundary the band is drawn",
                 p2["2026-05-13"]["modelsBand"] == 40.0 and p2["2026-05-14"]["modelsBand"] == 41.0, "%s %s" % (p2["2026-05-13"]["modelsBand"], p2["2026-05-14"]["modelsBand"])))
    # S1: on a carried date AFTER the boundary the band is null and is not listed as carried
    c = [p2[d] for d in ("2026-05-16", "2026-05-17")]
    arms.append(("S1 the band is not carried after the boundary",
                 all(r["modelsBand"] is None and "Models" not in r["carried"] for r in c),
                 "band %s carried %s" % ([r["modelsBand"] for r in c], [r["carried"] for r in c])))
    # S2: no row draws the band together with any model line
    both = [r["period"] for r in r2 if r["modelsBand"] is not None and any(v is not None for v in r["models"].values())]
    arms.append(("S2 no row draws the band and the stack", not both, "rows with both: %s" % both))
    # S3 control: Variant 1 never draws the band
    arms.append(("S3 control: variant 1 draws no band", all(r["modelsBand"] is None for r in r1), "%s" % [r["modelsBand"] for r in r1]))
    # S4: the repair removes only the band: the five primary lines still carry on the carried dates (Variant 2)
    ok4 = all(p2[d]["models"][k] == 10.0 and k in p2[d]["carried"] for d in ("2026-05-16", "2026-05-17") for k in PRIMARY)
    arms.append(("S4 the primary lines still carry", ok4, "%s" % [p2[d]["models"] for d in ("2026-05-16",)]))
    # S5 control: the served input is not mutated
    arms.append(("S5 control: input not mutated", v1.get("unchanged") is True and v2.get("unchanged") is True, ""))
    return arms


def pure_arms(src):
    got, err = run_pure(os.path.join(src, "lib", "trendGrouping.ts"))
    return grade(got, err)


# ---------------------------------------------------------------------------------------------- real
def real_arms(src):
    got, err = run_ts(BUN_REAL_TS, {"R11_LIB": os.path.join(src, "lib"), "R11_SERVED": SERVED})
    return real_grade(got, err)


def real_grade(got, err):
    if got is None:
        return [("exercise", False, err)]
    if got.get("missing"):
        return [("exports", False, "missing " + ",".join(got["missing"]))]
    v2 = (got.get("v2") or {}).get("v")
    v1 = (got.get("v1") or {}).get("v")
    if not v2 or not v1:
        return [("rows", False, "no rows: %s %s" % ((got.get("v1") or {}).get("err"), (got.get("v2") or {}).get("err")))]
    with open(SERVED, encoding="utf-8") as fh:
        fx = json.load(fh)
    dates = fx["dates"]
    n = len(dates)
    carried = set(fx.get("carried_dates") or [])
    begins = ((fx.get("meta") or {}).get("by_model_fold") or {}).get("per_model_detail_begins")
    raw_total = fx["opal_aggregate_aua"]
    arms = []

    # R0 control: one row per served date, in order, and the module exports exist
    r0 = [r["period"] for r in v2] == dates and len(v1) == n and got.get("missing") == []
    arms.append(("R0 control: one row per served date and the module exports exist", r0,
                 "rows %d of %d served dates" % (len(v2), n)))

    # R1 control: Variant 1 (stitch null) draws no Models band on any row
    b1 = [r["modelsBand"] for r in v1]
    arms.append(("R1 control: variant 1 draws no Models band on any row", all(b is None for b in b1),
                 "%d of %d rows draw a band" % (sum(1 for b in b1 if b is not None), len(b1))))

    # R2: no row draws the Models band together with any model line (the count of offending rows is printed)
    both = [r["period"] for r in v2 if r["modelsBand"] is not None and any(r["models"].get(k) is not None for k in PRIMARY)]
    arms.append(("R2 no row draws the Models band together with any model line", not both,
                 "%d of %d rows draw the band with a model line; first %s" % (len(both), n, both[:3])))

    # R3: on each carried date on or after the boundary, the drawn stack does not exceed the row's Total by more than TOL dollars
    scope = [r for r in v2 if r["period"] in carried and begins is not None and r["period"] >= begins]

    def stack(r):
        parts = [r["modelsBand"]] + [r["models"].get(k) for k in PRIMARY] + [r["custom"], r["clientSupervised"], r["etfStrategies"], r["altStrategies"]]
        return sum(p for p in parts if p is not None)

    over = []
    for r in scope:
        excess = stack(r) - (r["total"] if r["total"] is not None else 0.0)
        if excess > TOL:
            over.append((r["period"], round(excess, 2)))
    arms.append(("R3 no drawn group above the Total on the carried dates from the boundary (dollars, tolerance %.2f)" % TOL,
                 len(scope) > 0 and not over,
                 "%d of %d carried dates from %s exceed the Total; first %s" % (len(over), len(scope), begins, over[:3])))

    # R4 control: every row's total equals the served Total at that date (no arithmetic). LITERAL: the served Total is null on the
    # unmeasured (carried) dates and the module carries the last measured Total there; the arm checks that carry explicitly.
    ok_meas = n_meas = ok_car = n_car = literal = 0
    last = None
    for i, d in enumerate(dates):
        raw = raw_total[i]
        row_t = v2[i]["total"]
        if raw is not None:
            n_meas += 1
            eq = row_t is not None and abs(row_t - raw) < 1e-6
            ok_meas += 1 if eq else 0
            literal += 1 if eq else 0
            last = raw
        else:
            n_car += 1
            literal += 1 if row_t is None else 0
            if row_t == last and "total" in v2[i]["carried"]:
                ok_car += 1
    arms.append(("R4 control: every row's total is the served Total (carried dates: the last measured Total, listed as carried)",
                 ok_meas == n_meas and ok_car == n_car,
                 "measured %d of %d equal the served Total; carried %d of %d carry the last measured Total; literal %d of %d equal (served null on %d dates)"
                 % (ok_meas, n_meas, ok_car, n_car, literal, n, n_car)))
    return arms


# ---------------------------------------------------------------------------------------------- wiring
def norm(text):
    return re.sub(r"\s+", " ", text.replace("\r\n", "\n"))


def wiring_pure_arms(got, err):
    if got is None or got.get("missing"):
        why = err or ("missing " + ",".join(got.get("missing", [])))
        return [(i, False, why) for i in ("P1", "P2", "P3", "P4")]

    def val(k):
        r = got.get(k) or {}
        return r.get("v", "ERR " + str(r.get("err")))
    return [
        ("P1 trendModeFor(false, true) is variant1 (the demo flag reaches the mode)", val("p1") == "variant1", "got %s" % val("p1")),
        ("P2 control: trendModeFor(true, false) is variant1", val("p2") == "variant1", "got %s" % val("p2")),
        ("P3 control: trendModeFor(false, false) is variant2", val("p3") == "variant2", "got %s" % val("p3")),
        ("P4 control: trendModeFor(true, true) is variant1; one argument: trendModeFor(true) variant1, trendModeFor(false) variant2",
         val("p4") == "variant1" and val("p4a") == "variant1" and val("p4b") == "variant2",
         "got %s / %s / %s" % (val("p4"), val("p4a"), val("p4b"))),
    ]


def wiring_text_arms(src):
    N = norm(read_text(os.path.join(src, "pages", "ModelPortfolios.tsx")))
    n_session = N.count("enabled: effectiveFirmId === 'global' && variant1Session")
    n_internal = N.count("enabled: effectiveFirmId === 'global' && internal")
    w5 = "const demoTenant = MDPF_GLOBAL_VIEW_FIRMS.has(claims?.firmId ?? '')" in N
    w6 = "const variant1Session = internal || demoTenant" in N
    w7 = "trendModeFor(internal, demoTenant)" in N
    w8 = n_session == 2 and n_internal == 0
    w9 = re.search(r"const trendStitch = useMemo<[^>]*>\(\(\) => \{ if \(!variant1Session\) return null.*?\}, "
                   r"\[variant1Session, firm49MdpfData, inflectionMdpfData\]\)", N) is not None
    w10 = "const SHOW_BENCHMARK_TOGGLE = internal" in N and "const effectiveFirmId = internal" in N
    return [
        ("W5 the page defines demoTenant from the demo tenant set and the claims firm", w5, "line present: %s" % w5),
        ("W6 the page defines variant1Session = internal || demoTenant", w6, "line present: %s" % w6),
        ("W7 the page derives the mode with trendModeFor(internal, demoTenant)", w7, "call present: %s" % w7),
        ("W8 both single-firm reads gate on variant1Session (2 found), none on bare internal (0 found)", w8,
         "variant1Session gates %d, bare internal gates %d" % (n_session, n_internal)),
        ("W9 the trendStitch memo begins if (!variant1Session) return null and depends on [variant1Session, firm49MdpfData, inflectionMdpfData]",
         w9, "memo shape present: %s" % w9),
        ("W10 control: SHOW_BENCHMARK_TOGGLE = internal and effectiveFirmId = internal are unchanged", w10, "both lines present: %s" % w10),
    ]


def wiring_arms(src):
    got, err = run_ts(BUN_WIRING_TS, {"R11_LIB": os.path.join(src, "lib")})
    return wiring_pure_arms(got, err) + wiring_text_arms(src)


# ---------------------------------------------------------------------------------------------- report
def report(name, arms, n):
    k = 0
    for an, ok, detail in arms:
        k += 1 if ok else 0
        print("  %s %s%s" % ("PASS" if ok else "FAIL", an, "  -- " + str(detail)[:300] if detail else ""))
    print("ROUND 11 CN-S-4 %s: %d of %d arms" % (name, k, n))
    return 0 if k == n else 1


def pure():
    return report("PURE", pure_arms(src_root()), N_PURE)


def real():
    return report("REAL", real_arms(src_root()), N_REAL)


def wiring():
    return report("WIRING", wiring_arms(src_root()), N_WIRING)


def red_of(arms):
    return {a[0].split()[0] for a in arms if not a[1]}


def show(name, arms):
    print("%s: %s" % (name, " ".join("%s=%s" % (a[0].split()[0], "ok" if a[1] else "RED") for a in arms)))


def build_tree(top, src, band=True, mode=True, gate_left=False, carry="repaired"):
    """A scratch copy of the portal src with the repairs applied as text edits (CRLF kept). Mutant flags plant one defect each."""
    lib_src, lib_dst = os.path.join(src, "lib"), os.path.join(top, "src", "lib")
    os.makedirs(lib_dst)
    os.makedirs(os.path.join(top, "src", "pages"))
    for f in sorted(os.listdir(lib_src)):
        if f.endswith(".ts") and not f.endswith(".test.ts") and f != "trendGrouping.ts":
            shutil.copy(os.path.join(lib_src, f), os.path.join(lib_dst, f))
    tg = read_text(os.path.join(lib_src, "trendGrouping.ts"))
    if carry == "none":
        tg = sub_exact(tg, CARRY_OLD, CARRY_OLD.replace("if (v[key]", "if (false && v[key]"))
    elif band:
        tg = sub_exact(tg, CARRY_OLD, CARRY_BAND_NEW)
    if mode:
        tg = sub_exact(tg, MODE_OLD, MODE_NEW)
    write_text(os.path.join(lib_dst, "trendGrouping.ts"), tg)
    page = read_text(os.path.join(src, "pages", "ModelPortfolios.tsx"))
    for old, new, cnt in PAGE_EDITS:
        page = sub_exact(page, old, new, cnt)
    if gate_left:
        if page.count(GATE_NEW) != 2:
            raise EditError("gate needle count is not 2 after the page edits")
        page = page.replace(GATE_NEW, GATE_OLD, 1)
    write_text(os.path.join(top, "src", "pages", "ModelPortfolios.tsx"), page)
    return os.path.join(top, "src")


def selftest():
    import traceback
    src = src_root()
    ok = True
    print("== base: the untouched portal src (%s)" % src)
    base_p, base_r, base_w = pure_arms(src), real_arms(src), wiring_arms(src)
    show("base pure  ", base_p)
    show("base real  ", base_r)
    show("base wiring", base_w)
    bp, br, bw = red_of(base_p), red_of(base_r), red_of(base_w)
    print("base red: pure %s; real %s (R3 %s); wiring %s" % (sorted(bp), sorted(br), "red" if "R3" in br else "green", sorted(bw)))
    ok &= bp == {"S1", "S2"}
    ok &= "R2" in br and br <= {"R2", "R3"}
    ok &= bw == {"P1", "W5", "W6", "W7", "W8", "W9"}
    d = tempfile.mkdtemp(prefix="r11cns4_self_")
    try:
        try:
            ref_src = build_tree(os.path.join(d, "ref"), src)
        except EditError as e:
            print("SELFTEST: cannot apply the reference edits at the base: %s" % e)
            return 2
        print("== scratch reference (both repairs applied in %s)" % ref_src)
        ref_p, ref_r, ref_w = pure_arms(ref_src), real_arms(ref_src), wiring_arms(ref_src)
        show("ref pure  ", ref_p)
        show("ref real  ", ref_r)
        show("ref wiring", ref_w)
        for name, arms, n in (("pure", ref_p, N_PURE), ("real", ref_r, N_REAL), ("wiring", ref_w, N_WIRING)):
            good = len(arms) == n and all(a[1] for a in arms)
            print("reference %s: %d of %d" % (name, sum(1 for a in arms if a[1]), n))
            ok &= good
        print("== planted mutants (one per group)")
        mutants = [
            ("band-carried-again", dict(band=False), real_arms, {"R2"}),
            ("no-carry-at-all", dict(carry="none"), pure_arms, {"S4"}),
            ("trendModeFor-ignores-demo", dict(mode=False), wiring_arms, {"P1"}),
            ("gate-left-on-internal", dict(gate_left=True), wiring_arms, {"W8"}),
        ]
        for name, flags, fn, expect in mutants:
            try:
                mut_src = build_tree(os.path.join(d, "m_" + name), src, **flags)
            except EditError as e:
                print("selftest mutant %s: cannot plant: %s" % (name, e))
                ok = False
                continue
            arms = fn(mut_src)
            red = red_of(arms)
            hit = expect <= red
            print("selftest mutant %-26s red %s -> %s" % (name, sorted(red), "OK" if hit else "NOT CAUGHT (wanted %s)" % sorted(expect)))
            ok &= hit
    except Exception:
        traceback.print_exc()
        ok = False
    finally:
        shutil.rmtree(d, ignore_errors=True)
    print("CN-S-4 SELFTEST: %s" % ("OK" if ok else "NOT OK"))
    return 0 if ok else 1


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    table = {"pure": pure, "real": real, "wiring": wiring, "selftest": selftest}
    if cmd not in table:
        print(__doc__)
        return 2
    return table[cmd]()


if __name__ == "__main__":
    sys.exit(main())
