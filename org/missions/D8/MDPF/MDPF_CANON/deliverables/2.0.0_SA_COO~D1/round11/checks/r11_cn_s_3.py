#!/usr/bin/env python3
"""MDPF_CANON round 11 cell CN-s-3 (the Cottonwood AUM Trend upgrade) -- mechanical check, 2.0.0_SA_COO~D1, 2026-10-16. Not issued.
Written by 0.9.0_WK_MDPF_CANON~r11k3 from the CRO spec (MDPF_CANON_COTTONWOOD_AUM_TREND_UPGRADE_SPEC_20261015.md) and the issuer's draft oracle
(draft/checks/r11_cn_s_3_oracle.py). The module under test is written by the cell; this file only tests it.

  python r11_cn_s_3.py pure       seven arms on buildCottonwoodTrendRows, run under bun on the served Cottonwood object
  python r11_cn_s_3.py selftest   issuer only: base red (module absent), a scratch reference green, seven planted mutants each reddening its named arm

Inputs (all derived, none hardcoded):
  module    <src>/lib/cottonwoodTrend.ts, where <src> = env R11_SRC or <git toplevel>/portal/src
  fixture   env R11_FIXTURE or <git toplevel>/org/missions/.../checks/ref/served_cottonwood_aggregate_20261015.json (read as served)
  spec      env R11_SPEC or the CRO spec; the month-end table is parsed from it at run time (the worktree's sparse checkout omits org/tier1_exec,
            so the default falls back to the main checkout found through git's common dir)

Conventions (read from the fixture and the spec, not assumed):
  - rows are the TOTAL-BEARING dates from the first total on through the as-of date; the served dates without a total are excluded
    (the spec counts 89 rows through 2026-10-14 on the same basis; the draft oracle's derive() skips them too).
  - a primary model with a null model_value on a measured date is printed 0.0 by the spec table, so P3 reads null as 0.0; the module must still
    keep null (P6 checks the null identity on every row).
  - the interpolated class runs from the first total to meta.composed_backfill.first_measured_date (exclusive).

Output: `ROUND 11 CN-S-3 PURE: k of n arms`, exit 0 only when k == n. ASCII only.
"""
import collections
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

M = 1000000.0
SUM_TOL = 0.005
CELL_TOL = 0.05
CLS = ("measured", "interpolated", "carried")
PRIMARY = (
    ("Ultra-Short Term", "opal_ultra_short_term"),
    ("Short Term", "opal_short_term"),
    ("Intermediate Term", "opal_intermediate"),
    ("Long Term", "opal_long_term_conservative"),
    ("Ultra-Long Term", "opal_long_term_aggressive"),
)
LABELS = [p[0] for p in PRIMARY]
FIXTURE_REL = ("org", "missions", "D8", "MDPF", "MDPF_CANON", "deliverables", "2.0.0_SA_COO~D1", "round11", "checks", "ref",
               "served_cottonwood_aggregate_20261015.json")
SPEC_REL = ("org", "tier1_exec", "4.0.0_SA_CRO", "deliverables", "MDPF_CANON_COTTONWOOD_AUM_TREND_UPGRADE_SPEC_20261015.md")
NAMES = (
    "P0 control: module exists and exports buildCottonwoodTrendRows",
    "P1 window: first row is the first total-bearing date; rows and cls follow the rule",
    "P2 partition: primaries + custom + other = total on every row (+-$0.005); no group negative",
    "P3 month-end oracle at the spec's five period ends (+-$0.05M per cell)",
    "P4 the absent-model-leg dates are carried at the last measured leg, total kept",
    "P5 Other at 2026-06-30 equals the spec value (+-$0.05M)",
    "P6 control: input not mutated; no served null turned into 0",
)
N_ARMS = len(NAMES)

BUN_TS = r"""
import { pathToFileURL } from 'node:url'
import { readFileSync } from 'node:fs'
const mod: any = await import(pathToFileURL(process.env.R11_MODULE as string).href)
const fx: any = JSON.parse(readFileSync(process.env.R11_FIX as string, 'utf8'))
const enc = (_k: string, v: any) => (v === undefined ? '__undef__' : (typeof v === 'number' && !Number.isFinite(v) ? '__nonfinite__' : v))
const out: any = { missing: ['buildCottonwoodTrendRows'].filter((n) => typeof mod[n] !== 'function') }
if (out.missing.length === 0) {
  const before = JSON.stringify(fx, enc)
  try {
    out.rows = mod.buildCottonwoodTrendRows(fx)
  } catch (e: any) {
    out.err = String((e && e.message) || e).slice(0, 160)
  }
  out.unchanged = before === JSON.stringify(fx, enc)
}
console.log(JSON.stringify(out, enc))
"""

# Scratch reference for the issuer's selftest only: a faithful implementation of the rule, written here so selftest needs no cell code.
REF_TS = r"""
export type CottonwoodTrendRow = {
  period: string
  total: number | null
  primary: { 'Ultra-Short Term': number | null; 'Short Term': number | null; 'Intermediate Term': number | null; 'Long Term': number | null; 'Ultra-Long Term': number | null }
  custom: number | null
  other: number | null
  cls: 'measured' | 'interpolated' | 'carried'
}

const PRIMARY: Array<[string, string]> = [
  ['Ultra-Short Term', 'opal_ultra_short_term'],
  ['Short Term', 'opal_short_term'],
  ['Intermediate Term', 'opal_intermediate'],
  ['Long Term', 'opal_long_term_conservative'],
  ['Ultra-Long Term', 'opal_long_term_aggressive'],
]

const num = (x: any): number | null => (typeof x === 'number' && Number.isFinite(x) ? x : null)

export function buildCottonwoodTrendRows(raw: any): CottonwoodTrendRow[] {
  const dates: string[] = raw.dates
  const total: any[] = raw.partner_custody_total
  const modelAua: any[] = raw.model_aua
  const firstMeasured: string = raw.meta.composed_backfill.first_measured_date
  const first = total.findIndex((t) => num(t) !== null)
  const rows: CottonwoodTrendRow[] = []
  if (first < 0) return rows
  let lastMeasured: number | null = null
  for (let i = 0; i < dates.length; i++) {
    const measuredLeg = num(modelAua[i]) !== null
    if (measuredLeg) lastMeasured = i
    const t = num(total[i])
    if (i < first || t === null) continue
    const s = lastMeasured
    const primary: any = {}
    let five = 0
    for (const [label, key] of PRIMARY) {
      const v = s === null ? null : num(raw.by_model[key].model_value[s])
      primary[label] = v
      five += v === null ? 0 : v
    }
    const ma = s === null ? null : num(modelAua[s])
    const custom = ma === null ? null : ma - five
    const other = ma === null ? null : t - ma
    const cls: 'measured' | 'interpolated' | 'carried' = !measuredLeg ? 'carried' : dates[i] < firstMeasured ? 'interpolated' : 'measured'
    rows.push({ period: dates[i], total: t, primary, custom, other, cls })
  }
  return rows
}
"""


def num(x):
    return float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) else None


def is_num(x):
    return num(x) is not None


def close(a, b, tol=SUM_TOL):
    return is_num(a) and is_num(b) and abs(a - b) <= tol


def same(a, b):
    return (a is None and b is None) or close(a, b)


def git(*args):
    return subprocess.check_output(["git"] + list(args), text=True, timeout=60).strip()


def toplevel():
    return git("rev-parse", "--show-toplevel")


def src_root():
    return os.environ.get("R11_SRC") or os.path.join(toplevel(), "portal", "src")


def fixture_path():
    return os.environ.get("R11_FIXTURE") or os.path.join(toplevel(), *FIXTURE_REL)


def spec_path():
    if os.environ.get("R11_SPEC"):
        return os.environ["R11_SPEC"]
    top = toplevel()
    common = os.path.abspath(os.path.join(top, git("rev-parse", "--git-common-dir")))
    cands = [os.path.join(top, *SPEC_REL), os.path.join(os.path.dirname(common), *SPEC_REL)]
    for c in cands:
        if os.path.isfile(c):
            return c
    return cands[-1]


def scratch_base():
    base = os.path.join(toplevel(), ".scratch")
    os.makedirs(base, exist_ok=True)
    return base


def read_oracle(path):
    """Month-end rows of the spec's oracle table: (period end, [UST, ST, INT, LT, ULT, Custom, Other, Total] in $M)."""
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            cells = [c.strip() for c in line.strip().split("|")]
            if len(cells) != 11 or cells[0] or cells[10]:
                continue
            m = re.match(r"^(\d{4}-\d{2}-\d{2})", cells[1])
            if not m:
                continue
            try:
                vals = [float(c) for c in cells[2:10]]
            except ValueError:
                continue
            out.append((m.group(1), vals))
    return out


def load_context():
    fx = fixture_path()
    with open(fx, encoding="utf-8") as fh:
        raw = json.load(fh)
    dates, total, ma = raw["dates"], raw["partner_custody_total"], raw["model_aua"]
    n = len(dates)
    first = next(i for i, t in enumerate(total) if is_num(t))
    fm = raw["meta"]["composed_backfill"]["first_measured_date"]
    src_of, last = [], None
    for i in range(n):
        if is_num(ma[i]):
            last = i
        src_of.append(last)
    window = [i for i in range(first, n) if is_num(total[i])]
    absent = [i for i in window if not is_num(ma[i])]
    absent_set = set(absent)
    expected = []
    for i in window:
        s = src_of[i]
        prim = {lab: (num(raw["by_model"][key]["model_value"][s]) if s is not None else None) for lab, key in PRIMARY}
        ma_s = num(ma[s]) if s is not None else None
        five = sum(v or 0.0 for v in prim.values())
        t = num(total[i])
        cls = "carried" if i in absent_set else ("interpolated" if dates[i] < fm else "measured")
        expected.append({"period": dates[i], "total": t, "prim": prim,
                         "custom": None if ma_s is None else ma_s - five,
                         "other": None if ma_s is None else t - ma_s, "cls": cls})
    nm = raw.get("non_model_aua") or []
    exc_obj = ((raw.get("meta") or {}).get("channel_participation") or {}).get("exceptions") or {}
    sp = spec_path()
    try:
        oracle, oerr = read_oracle(sp), ""
    except OSError as e:
        oracle, oerr = None, str(e)[:120]
    return {
        "fixture": fx, "n_served": n, "first_total": dates[first], "served_from": dates[first:],
        "expected": expected, "absent": [dates[i] for i in absent], "exceptions": sorted(exc_obj),
        "first_measured": fm, "nm_first": next((dates[i] for i, v in enumerate(nm) if is_num(v)), None),
        "spec": sp, "oracle": oracle, "oerr": oerr,
    }


def run_bun(module, fixture):
    if not os.path.isfile(module):
        return None, "module absent: " + module
    d = tempfile.mkdtemp(prefix="r11cns3_", dir=scratch_base())
    try:
        ex = os.path.join(d, "exercise.ts")
        with open(ex, "w", newline="\n", encoding="utf-8") as fh:
            fh.write(BUN_TS)
        env = dict(os.environ, R11_MODULE=module, R11_FIX=fixture)
        try:
            r = subprocess.run(["bun", ex], capture_output=True, text=True, timeout=100, env=env, cwd=d)
        except subprocess.TimeoutExpired:
            return None, "bun exercise timed out"
        except OSError as e:
            return None, "bun not runnable: %s" % str(e)[:120]
        line = (r.stdout.strip().splitlines() or [""])[-1]
        try:
            out = json.loads(line)
        except ValueError:
            tail = (r.stderr or r.stdout).strip().splitlines()[-1:] or [""]
            return None, "exercise rc=%d, no JSON: %s" % (r.returncode, tail[0][:160])
        return out, ""
    finally:
        shutil.rmtree(d, ignore_errors=True)


def p1(ctx, rows, got):
    exp = ctx["expected"]
    want_p = [e["period"] for e in exp]
    got_p = [r.get("period") for r in rows]
    want_c = [e["cls"] for e in exp]
    got_c = [r.get("cls") for r in rows]
    ok = got_p == want_p and got_c == want_c
    return ok, ("rows %d want %d; first %s want %s; served from %s = %d dates, %d without a total; cls got %s want %s"
                % (len(got_p), len(want_p), got_p[0] if got_p else None, want_p[0], ctx["first_total"], len(ctx["served_from"]),
                   len(ctx["served_from"]) - len(want_p), dict(collections.Counter(got_c)), dict(collections.Counter(want_c))))


def p2(ctx, rows, got):
    total_by = {e["period"]: e["total"] for e in ctx["expected"]}
    bad = []
    for r in rows:
        if not isinstance(r, dict):
            bad.append(("?", "not an object"))
            continue
        pr = r.get("primary")
        if not isinstance(pr, dict) or set(pr.keys()) != set(LABELS):
            bad.append((r.get("period"), "primary keys"))
            continue
        vals = [pr[lab] for lab in LABELS]
        if not (all(v is None or is_num(v) for v in vals) and is_num(r.get("total")) and is_num(r.get("custom"))
                and is_num(r.get("other")) and r.get("cls") in CLS):
            bad.append((r.get("period"), "shape"))
            continue
        s = sum(v or 0.0 for v in vals) + r["custom"] + r["other"] - r["total"]
        neg = min([v for v in vals if v is not None] + [r["custom"], r["other"]]) < -SUM_TOL
        tot_off = abs(r["total"] - total_by[r["period"]]) > SUM_TOL
        if abs(s) > SUM_TOL or neg or tot_off:
            bad.append((r["period"], "sum off %.4f" % s if abs(s) > SUM_TOL else ("negative" if neg else "total not served")))
    return not bad, "%d of %d rows partition exactly; bad %s" % (len(rows) - len(bad), len(rows), bad[:5])


def p3(ctx, rows, got):
    if ctx["oracle"] is None:
        return False, "spec unreadable: %s %s" % (ctx["spec"], ctx["oerr"])
    table = ctx["oracle"]
    if len(table) != 5:
        return False, "spec table holds %d period-end rows, not 5" % len(table)
    misses, cells = [], 0
    for end, want in table:
        cand = [r for r in rows if r.get("period") <= end]
        if not cand:
            misses.append((end, "no row"))
            continue
        r = max(cand, key=lambda x: x["period"])
        try:
            g = [(r["primary"][lab] or 0.0) / M for lab in LABELS] + [r["custom"] / M, r["other"] / M, r["total"] / M]
        except (TypeError, KeyError):
            misses.append((end, r.get("period"), "null or shape"))
            continue
        cells += len(g)
        if any(abs(g[j] - want[j]) > CELL_TOL for j in range(len(g))):
            misses.append((end, r["period"], [round(x, 2) for x in g], want))
    return not misses, "%d period ends, %d cells compared, misses %s" % (len(table), cells, misses[:2])


def p4(ctx, rows, got):
    absent = sorted(ctx["absent"])
    exp_by = {e["period"]: e for e in ctx["expected"]}
    got_by = {r.get("period"): r for r in rows}
    got_carried = sorted(r.get("period") for r in rows if r.get("cls") == "carried")
    set_ok = got_carried == absent and ctx["exceptions"] == absent
    bad = []
    for d in absent:
        g, e = got_by.get(d), exp_by[d]
        if g is None:
            bad.append((d, "no row"))
            continue
        if not (g.get("cls") == "carried" and close(g.get("total"), e["total"])
                and all(same(g["primary"][lab], e["prim"][lab]) for lab in LABELS)
                and close(g.get("custom"), e["custom"]) and close(g.get("other"), e["other"])):
            bad.append((d, "differs from the last measured leg"))
    return set_ok and not bad, ("%d of %d absent-leg dates carried at the last measured leg with the measured total; carried set == absent set %s"
                                " (meta exceptions %d); bad %s" % (len(absent) - len(bad), len(absent), set_ok, len(ctx["exceptions"]), bad[:3]))


def p5(ctx, rows, got):
    if ctx["oracle"] is None:
        return False, "spec unreadable"
    spec_row = [w for e, w in ctx["oracle"] if e == "2026-06-30"]
    if not spec_row:
        return False, "no 2026-06-30 row in the spec table"
    want_other = spec_row[0][6]
    hit = [r for r in rows if r.get("period") == "2026-06-30"]
    if not hit:
        return False, "no 2026-06-30 row"
    v = hit[0].get("other")
    if not is_num(v):
        return False, "other is %r" % (v,)
    return abs(v / M - want_other) <= CELL_TOL, "other %.2f $M, spec %.1f $M (+-0.05)" % (v / M, want_other)


def p6(ctx, rows, got):
    unchanged = got.get("unchanged") is True
    exp_by = {e["period"]: e for e in ctx["expected"]}
    nulls, bad = 0, []
    for r in rows:
        e = exp_by.get(r.get("period"))
        if e is None:
            bad.append((r.get("period"), "no expected row"))
            continue
        for lab in LABELS:
            want_null = e["prim"][lab] is None
            nulls += 1 if want_null else 0
            if (r["primary"][lab] is None) != want_null:
                bad.append((r["period"], lab, r["primary"][lab]))
    return unchanged and not bad, "input unchanged %s; served-null cells %d; null identity bad %s" % (unchanged, nulls, bad[:3])


CHECKS = (p1, p2, p3, p4, p5, p6)


def guarded(fn, ctx, rows, got):
    try:
        return fn(ctx, rows, got)
    except Exception as e:  # a shape or key error is a red arm, not a crash
        return False, "error %s: %s" % (type(e).__name__, str(e)[:100])


def run_arms(src, ctx):
    """Returns (arms, exercised). exercised is True when the module loaded and returned a row list."""
    module = os.path.join(src, "lib", "cottonwoodTrend.ts")
    got, err = run_bun(module, ctx["fixture"])
    rows = None
    if got is not None and not got.get("missing") and isinstance(got.get("rows"), list):
        rows = got["rows"]
    if got is None:
        p0 = (False, err)
    elif got.get("missing"):
        p0 = (False, "missing " + ",".join(got["missing"]) + " in " + module)
    else:
        p0 = (True, "exports buildCottonwoodTrendRows from " + module + ("" if rows is not None else "; no rows: %s" % (got.get("err") or "rows not a list")))
    arms = [(NAMES[0], p0[0], p0[1])]
    for idx, fn in enumerate(CHECKS, start=1):
        if rows is None:
            why = err or ("missing " + ",".join(got.get("missing") or []) if got else "") or (got or {}).get("err") or "no rows"
            arms.append((NAMES[idx], False, "no module output: " + str(why)))
        else:
            ok, detail = guarded(fn, ctx, rows, got)
            arms.append((NAMES[idx], ok, detail))
    return arms, rows is not None


def report(arms, label):
    k = 0
    for name, ok, detail in arms:
        k += 1 if ok else 0
        print("  %s %s  -- %s" % ("PASS" if ok else "FAIL", name, str(detail)[:240]))
    print("ROUND 11 CN-S-3 %s: %d of %d arms" % (label, k, len(arms)))
    return k


def pure():
    try:
        ctx = load_context()
    except (OSError, ValueError, KeyError, StopIteration) as e:
        print("  fixture unreadable: %s" % str(e)[:160])
        print("ROUND 11 CN-S-3 PURE: 0 of %d arms" % N_ARMS)
        return 1
    print("  fixture %s: served dates %d, from %s %d, total-bearing rows %d" % (
        ctx["fixture"], ctx["n_served"], ctx["first_total"], len(ctx["served_from"]), len(ctx["expected"])))
    print("  spec %s: oracle rows read %s" % (ctx["spec"], len(ctx["oracle"]) if ctx["oracle"] is not None else ctx["oerr"]))
    arms, _ = run_arms(src_root(), ctx)
    k = report(arms, "PURE")
    return 0 if k == N_ARMS else 1


def write_module(src, text):
    os.makedirs(os.path.join(src, "lib"), exist_ok=True)
    with open(os.path.join(src, "lib", "cottonwoodTrend.ts"), "w", newline="\n", encoding="utf-8") as fh:
        fh.write(text)


def mutate(text, pairs):
    for old, new in pairs:
        n = text.count(old)
        if n != 1:
            raise ValueError("needle found %d times: %s" % (n, old[:70]))
        text = text.replace(old, new)
    return text


MUTANTS = (
    ("M1 Other drawn from non_model_aua", "P5",
     [("const other = ma === null ? null : t - ma", "const other = num(raw.non_model_aua[i])")]),
    ("M2 carried dates left absent", "P4",
     [("const s = lastMeasured", "const s = measuredLeg ? lastMeasured : null")]),
    ("M3 window starts at first model date", "P1",
     [("const first = total.findIndex((t) => num(t) !== null)", "const first = modelAua.findIndex((m) => num(m) !== null)"),
      ("if (i < first || t === null) continue", "if (i < first) continue")]),
    ("M4 sums broken by $0.02", "P2",
     [("const other = ma === null ? null : t - ma", "const other = ma === null ? null : t - ma + 0.02")]),
    ("M5 a group negative", "P2",
     [("const custom = ma === null ? null : ma - five", "const custom = ma === null ? null : (dates[i] === '2026-09-30' ? -1 : ma - five)")]),
    ("M6 input mutated", "P6",
     [("export function buildCottonwoodTrendRows(raw: any): CottonwoodTrendRow[] {",
       "export function buildCottonwoodTrendRows(raw: any): CottonwoodTrendRow[] {\n  raw.__r11_touched = true")]),
    ("M7 absent primary written as 0", "P6",
     [("primary[label] = v", "primary[label] = v ?? 0")]),
)


def selftest():
    ctx = load_context()
    base_src = src_root()
    base_mod = os.path.join(base_src, "lib", "cottonwoodTrend.ts")
    base_present = os.path.isfile(base_mod)
    base_arms, _ = run_arms(base_src, ctx)
    base_k = sum(1 for a in base_arms if a[1])
    base_ok = (not base_present) and base_k == 0
    print("SELFTEST 1 base: module %s at %s; %d of %d arms red" % ("PRESENT" if base_present else "ABSENT", base_mod, N_ARMS - base_k, N_ARMS))
    print("  base red: %s" % ", ".join(a[0].split()[0] for a in base_arms if not a[1]))
    scratch = tempfile.mkdtemp(prefix="r11cns3self_", dir=scratch_base())
    good_mut = True
    ref_ok = False
    try:
        ref_src = os.path.join(scratch, "ref", "src")
        write_module(ref_src, REF_TS)
        ref_arms, ref_ex = run_arms(ref_src, ctx)
        ref_k = sum(1 for a in ref_arms if a[1])
        ref_ok = ref_ex and ref_k == N_ARMS
        print("SELFTEST 2 scratch reference: %d of %d arms; exercised %s" % (ref_k, N_ARMS, ref_ex))
        for i, (label, named, pairs) in enumerate(MUTANTS, start=1):
            try:
                text = mutate(REF_TS, pairs)
            except ValueError as e:
                print("SELFTEST 3.%d %s: NOT BUILT (%s)" % (i, label, e))
                good_mut = False
                continue
            msrc = os.path.join(scratch, "mut%d" % i, "src")
            write_module(msrc, text)
            arms, ex = run_arms(msrc, ctx)
            red = [a[0].split()[0] for a in arms if not a[1]]
            hit = named in red and ex
            good_mut = good_mut and hit
            print("SELFTEST 3.%d %s: named %s red %s; exercised %s; red %s" % (i, label, named, named in red, ex, red))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    good = base_ok and ref_ok and good_mut
    print("CN-S-3 SELFTEST: %s" % ("OK" if good else "NOT OK"))
    return 0 if good else 1


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd not in ("pure", "selftest"):
        print(__doc__)
        sys.exit(2)
    sys.exit(pure() if cmd == "pure" else selftest())
