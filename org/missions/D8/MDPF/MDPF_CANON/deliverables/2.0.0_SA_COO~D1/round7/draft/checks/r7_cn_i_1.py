#!/usr/bin/env python3
"""MDPF_CANON round 7, cell CN-i-1 -- FWD-9 (PRD v2.15), the AUA Trend grouping.

Issuer's check (2.0.0_SA_COO~D1). Read-only for every worker: never edit this file.

  python r7_cn_i_1.py module     the pure module: custom group, ETF carve-out sum, true-remainder Other AUA, as-of-only chip (9 arms)
  python r7_cn_i_1.py page       the page wiring: one palette, ALT stays vermilion, chips as-of only, no second fetch (8 arms)
  python r7_cn_i_1.py data       the rules on the REAL served objects: the stack adds to the total to the cent (5 arms)
  python r7_cn_i_1.py selftest   proves the arms fail at base and pass on a reference patch, four mutants RED; issuer only

Targets (repo root = `git rev-parse --show-toplevel` of the working directory):
  portal/src/lib/trendGrouping.ts   portal/src/pages/ModelPortfolios.tsx   portal/src/components/CategoryViewTree.tsx
  portal/src/pages/ModelPortfolios.taxsma-color.test.ts (read only: the vermilion pin must stand)
Overrides for the selftest only: R7_MODULE, R7_PAGE, R7_CVT (absolute file paths).

Output: `ROUND 7 <NAME>: k of n arms`, exit 0 only when k == n. ASCII only. The `data` subcommand also prints the per-date residual summary.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BUCKET = "opal-data-assets"
CORE = ("opal_ultra_short_term", "opal_short_term", "opal_intermediate", "opal_long_term_conservative", "opal_long_term_aggressive")
CARVE = ("opal_div_sma", "opal_growth_sma")
CLIENT_SUP = "Client - Opal Supervised"
CLIENT_UNSUP = "Client - Opal Unsupervised"
N_MODULE = 9
N_PAGE = 8

BUN_TS = r"""
import { pathToFileURL } from 'node:url'
const mod: any = await import(pathToFileURL(process.env.R7_MODULE as string).href)
const group = mod.groupCustomModelsSeries as (b: Record<string, any[]>, c: ReadonlySet<string>) => Record<string, any[]>
const LABEL = mod.CUSTOM_MODELS_LABEL as string
const etf = mod.etfStrategiesAua as (sma: number | null, carve: Array<number | null>) => number | null
const other = mod.otherAua as (nm: number | null, carve: Array<number | null>, clients: Array<number | null> | null) => number | null
const chip = mod.clientChipAt as (period: string, asOf: string | null | undefined, v: number | null | undefined) => number | null
const out: string[] = []
const arm = (id: string, ok: boolean, why: string) => out.push(`ARM ${id} ${ok ? 'PASS' : 'FAIL'} ${why}`)

const N = 6
const periods = Array.from({ length: N }, (_, i) => `2026-09-${String(i + 1).padStart(2, '0')}`)
const mk = (vals: Array<number | null>) => periods.map((p, i) => ({ period: p, aum: vals[i] }))
const canon = new Set(['Short Term', 'Intermediate Term'])
const src: Record<string, any[]> = {
  'Short Term': mk([10, 11, 12, 13, 14, 15]),
  'Intermediate Term': mk([20, 21, 22, 23, 24, 25]),
  'Opal Fixed Income': mk([1.25, null, 3.5, null, 5, 6]),
  'Other Models': mk([2, null, 4, null, null, 7.75]),
}
const snap = JSON.stringify(src)
const g = group(src, canon)

const c = g[LABEL]
const exp = [3.25, null, 7.5, null, 5, 13.75]
arm('M1', LABEL === 'Custom Models' && Array.isArray(c) && c.length === N && c.every((p, i) => p.period === periods[i] && p.aum === exp[i]),
  `the custom lines sum into ONE series '${LABEL}' on ${N} periods (3 periods hand-checked)`)
arm('M2', Array.isArray(c) && c[1].aum === null && c[3].aum === null,
  'a period where every member is null reads null, never 0')
arm('M3', g['Short Term'] === src['Short Term'] && g['Intermediate Term'] === src['Intermediate Term'],
  'the canonical series pass through untouched (same arrays)')
arm('M4', !('Opal Fixed Income' in g) && !('Other Models' in g) && Object.keys(g).length === 3,
  'the member series (the fold line included) are absent from the result: three keys (two canonical + the group)')
arm('M5', JSON.stringify(src) === snap, 'the input is not mutated')
const none = group({ 'Short Term': mk([1, 2, 3, 4, 5, 6]) }, canon)
arm('M6', !(LABEL in none) && Object.keys(none).length === 1, 'no custom lines -> no group key (nothing invented)')
arm('M7', typeof etf === 'function' && etf(0.41, [17.1, 4.0]) === 21.51 && etf(null, [null, null]) === null && etf(null, [17.1, null]) === 17.1
  && etf(0.41, [null, null]) === 0.41,
  'ETF Strategies = pfde plus the two carve-out lines, null only where all three are null (21.51 hand-checked)')
const o1 = typeof other === 'function' ? other(306.35, [17.1, 4.02], null) : undefined
const o2 = typeof other === 'function' ? other(306.35, [17.1, 4.02], [285.23, 0]) : undefined
const o3 = typeof other === 'function' ? other(10, [10.004], null) : undefined
arm('M8', typeof other === 'function' && o1 === 285.23 && o2 === null && other(null, [1], [2]) === null && o3 === null
  && !Object.is(o3, -0) && other(10, [11], null) === -1,
  'Other AUA = non_model minus carve-outs minus the Client chips; a zero or sub-cent remainder draws nothing (never -0); a real negative stays')
arm('M9', typeof chip === 'function' && chip('2026-10-12', '2026-10-12', 5) === 5 && chip('2026-10-09', '2026-10-12', 5) === null
  && chip('2026-10-12', '2026-10-12', null) === null && chip('2026-10-12', null, 5) === null && chip('2026-10-12', '2026-10-12', 0) === 0,
  'a Client chip carries its value only on the object as-of date; absent elsewhere; a measured zero stays 0')
console.log(out.join('\n'))
"""


def root():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if r.returncode != 0:
        print("ERROR: not in a git worktree")
        sys.exit(2)
    return r.stdout.strip()


def targets():
    pr = os.path.join(root(), "portal", "src")
    module = os.environ.get("R7_MODULE") or os.path.join(pr, "lib", "trendGrouping.ts")
    page = os.environ.get("R7_PAGE") or os.path.join(pr, "pages", "ModelPortfolios.tsx")
    cvt = os.environ.get("R7_CVT") or os.path.join(pr, "components", "CategoryViewTree.tsx")
    return module, page, cvt


def report(name, arms):
    for a in arms:
        print("  %s %s %s" % (a[0], "PASS" if a[1] else "FAIL", a[2]))
    k = sum(1 for a in arms if a[1])
    print("ROUND 7 %s: %d of %d arms" % (name, k, len(arms)))
    return k, len(arms)


def run_module(module):
    if not os.path.isfile(module):
        return [("M0", False, "module not found: " + module)]
    d = tempfile.mkdtemp(prefix="r7cni1_")
    try:
        ex = os.path.join(d, "exercise.ts")
        with open(ex, "w", newline="\n", encoding="utf-8") as f:
            f.write(BUN_TS)
        env = dict(os.environ)
        env["R7_MODULE"] = module
        try:
            r = subprocess.run(["bun", ex], capture_output=True, text=True, timeout=100, env=env, cwd=d)
        except subprocess.TimeoutExpired:
            return [("M0", False, "bun exercise timed out")]
        arms = []
        for line in r.stdout.splitlines():
            m = re.match(r"ARM (M\d) (PASS|FAIL) (.*)", line)
            if m:
                arms.append((m.group(1), m.group(2) == "PASS", m.group(3)))
        if r.returncode != 0 or len(arms) != N_MODULE:
            tail = (r.stderr or r.stdout).strip().splitlines()[-1:] or [""]
            return [("M0", False, "exercise rc=%d arms=%d %s" % (r.returncode, len(arms), tail[0][:160]))]
        return arms
    finally:
        shutil.rmtree(d, ignore_errors=True)


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n")


def run_page(page, cvt):
    if not os.path.isfile(page) or not os.path.isfile(cvt):
        return [("P0", False, "page or CategoryViewTree not found")]
    text = read(page)
    cv = read(cvt)
    lines = text.split("\n")
    arms = []

    # P1 the Total Assets colour table is EXPORTED once, with its keys intact (no second table is born).
    ok = (re.search(r"^export const L1_COLOR\b", cv, re.M) is not None
          and re.search(r"^export const l1ColorOf\b", cv, re.M) is not None
          and all(("'%s'" % k in cv or k + ":" in cv) for k in ("Custom", "ETF Strategies", "ALT Strategies", CLIENT_SUP, CLIENT_UNSUP)))
    arms.append(("P1", ok, "CategoryViewTree exports L1_COLOR and l1ColorOf; the five bucket keys still present"))

    # P2 the page imports the export and the pure functions.
    imp_color = re.search(r"import \{[^}]*\bl1ColorOf\b[^}]*\} from '[^']*CategoryViewTree'", text) is not None
    imp_pure = re.search(r"import \{[^}]*\bgroupCustomModelsSeries\b[^}]*\} from '[^']*trendGrouping'", text) is not None
    imp_more = all(re.search(r"import \{[^}]*\b%s\b[^}]*\} from '[^']*trendGrouping'" % fn, text) is not None
                   for fn in ("etfStrategiesAua", "otherAua", "clientChipAt"))
    arms.append(("P2", imp_color and imp_pure and imp_more,
                 "page imports l1ColorOf (%s), groupCustomModelsSeries (%s), etfStrategiesAua/otherAua/clientChipAt (%s)"
                 % (imp_color, imp_pure, imp_more)))

    # P3 the mount spine: the six group keys before non_model's label 'Other AUA'; the old band labels are gone.
    m = re.search(r"const STACK_SERIES[^=]*=\s*\[(.*?)\n\]", text, re.S)
    body = m.group(1) if m else ""
    keys = re.findall(r"key:\s*'([^']+)'", body)
    labels = re.findall(r"label:\s*'([^']+)'", body)
    need_k = ("custom_models", "sma_additive", "tax_additive", "client_supervised", "client_unsupervised", "non_model")
    need_l = ("Custom Models", "ETF Strategies", "ALT Strategies", "Client Supervised", "Client Unsupervised", "Other AUA")
    ok3 = (all(k in keys for k in need_k) and all(lb in labels for lb in need_l)
           and keys.index("custom_models") < keys.index("non_model")
           and "Additive SMA sleeves" not in labels and "Tax-Managed SMA" not in labels and "Non-Model" not in labels)
    arms.append(("P3", ok3, "STACK_SERIES keys %s labels %s" % (keys, labels)))

    # P4 the custom grouping applies at EVERY scope the page offers (PRD: "at Global and at each firm scope"): the call is not gated on Global.
    idx = [i for i, ln in enumerate(lines) if "groupCustomModelsSeries(" in ln and "import" not in ln]
    gated = any("effectiveFirmId === 'global'" in "\n".join(lines[max(0, i - 3):i + 1]) for i in idx)
    arms.append(("P4", len(idx) >= 1 and not gated, "groupCustomModelsSeries call sites %d, gated on Global: %s" % (len(idx), gated)))

    # P5 one palette for Custom, ETF and the two Client chips: resolved through l1ColorOf, used at >= 3 sites, with no hex literal and
    # no PALETTE.fuchsia/cyan/amber/orange pick on a line naming one of those labels.
    names = r"'(Custom Models|ETF Strategies|Client Supervised|Client Unsupervised)'"
    grp_lines = [ln for ln in lines if re.search(names, ln)]
    hexed = [ln.strip()[:80] for ln in grp_lines if re.search(r"#[0-9a-fA-F]{3,8}\b", ln)]
    palette = [ln.strip()[:80] for ln in grp_lines if re.search(r"PALETTE\.(fuchsia|cyan|amber|orange)\d+", ln)]
    uses = len(re.findall(r"\btrendColorOf\(", text))
    has_def = re.search(r"const trendColorOf\b", text) is not None and "l1ColorOf(" in text
    arms.append(("P5", has_def and uses >= 3 and not hexed and not palette,
                 "trendColorOf defined=%s, uses=%d, hex literals on group lines=%d, PALETTE picks=%d"
                 % (has_def, uses, len(hexed), len(palette))))

    # P6 ALT stays vermilion500 on the Trend (Andrew-direct 2026-10-01; the pin test stands): the ALT band resolves through
    # getModelColor('Tax-Managed SMA'), l1ColorOf is never asked for 'ALT Strategies', and the pin test file is untouched in content.
    alt_ok = re.search(r"getModelColor\('Tax-Managed SMA'\)", text) is not None
    alt_l1 = re.search(r"TREND_GROUP_L1[^\n]*'ALT Strategies'\s*:", text) is not None or "l1ColorOf('ALT Strategies')" in text
    pin = os.path.join(os.path.dirname(os.path.abspath(page)), "ModelPortfolios.taxsma-color.test.ts")
    pin_ok = (not os.path.isfile(pin)) or ("vermilion500" in read(pin))
    arms.append(("P6", alt_ok and not alt_l1 and pin_ok,
                 "ALT via getModelColor('Tax-Managed SMA')=%s, ALT asked of l1ColorOf=%s, pin test still names vermilion500=%s"
                 % (alt_ok, alt_l1, pin_ok)))

    # P7 the Client chips ride the page's EXISTING category-views query (no second fetch) and are as-of only.
    fetches = len(re.findall(r"\bgetCategoryViewsByFirm\(", text))
    chip_uses = len(re.findall(r"\bclientChipAt\(", text))
    reads_obj = ("categoryViews" in text) and (CLIENT_SUP in text) and (CLIENT_UNSUP in text)
    arms.append(("P7", fetches == 1 and chip_uses >= 2 and reads_obj,
                 "getCategoryViewsByFirm call sites %d (must stay 1), clientChipAt uses %d, reads the Client nodes of the served object: %s"
                 % (fetches, chip_uses, reads_obj)))

    # P8 the fold's pooled line is never its own series: no 'Other Models' label in the mount list or a colour table entry.
    other_models = [ln.strip()[:80] for ln in lines if re.search(r"label:\s*'Other Models'", ln)]
    arms.append(("P8", not other_models, "'Other Models' series labels in the page: %d" % len(other_models)))
    return arms


def served(s3, key):
    return json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())


def keys_under(s3, prefix):
    ks = []
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
        ks += [o["Key"] for o in p.get("Contents", []) if o["Key"].endswith(".json")]
    return sorted(ks)


def run_data():
    import boto3
    s3 = boto3.client("s3", region_name="us-east-1")
    ts_keys = keys_under(s3, "portal/gold/mdpf/global/aggregate-aua-timeseries/")
    cv_keys = keys_under(s3, "portal/gold/mdpf/global/category-views/")
    ts = served(s3, ts_keys[-1])
    dates = ts["dates"]
    n = len(dates)
    bm = ts["by_model"]
    sma = {k for k, v in bm.items() if v.get("cohort_class") == "sma"}
    model = {k: v for k, v in bm.items() if k not in sma}
    custom_keys = [k for k in model if k not in CORE]
    fold = (ts.get("meta") or {}).get("by_model_fold")
    arms = []

    def at(k, i):
        arr = (bm.get(k) or {}).get("model_value") or []
        return arr[i] if i < len(arr) else None

    def num(x):
        return 0.0 if x is None else float(x)

    # D1 the stack adds to the total TO THE CENT: custom group + canonical + ETF (pfde + carve-outs) + ALT (tax_additive_aua)
    # + Other AUA (non_model_aua - carve-outs) == opal_aggregate_aua, allowing only model_aua's own published rounding gap
    # (<= 0.02) and, on a FOLDED object, the fold's suppressed dates (below the total by the suppressed amount, never drawn).
    bad, valid, exact, rounding, exempt = [], 0, 0, 0, 0
    worst = 0.0
    for i in range(n):
        tot, nm = ts["opal_aggregate_aua"][i], ts["non_model_aua"][i]
        ma = ts["model_aua"][i]
        if tot is None or nm is None or ma is None:
            continue
        valid += 1
        lines_sum = sum(num(at(k, i)) for k in model)
        carve = sum(num(at(k, i)) for k in CARVE)
        etf = num(ts["sma_additive_aua"][i]) + carve
        alt = num(ts["tax_additive_aua"][i])
        other = nm - carve
        stack = lines_sum + etf + alt + other
        gap = round(tot - stack, 2)
        worst = max(worst, abs(gap))
        if abs(gap) < 0.005:
            exact += 1
        elif abs(gap) <= 0.02 + abs(round(ma - lines_sum, 2)):
            rounding += 1
        elif fold is not None and gap > 0:
            exempt += 1
        else:
            bad.append((dates[i], gap))
    arms.append(("D1", valid > 0 and not bad,
                 "stack == opal_aggregate_aua on %d valued dates of %d: exact %d, model_aua rounding gap %d, fold-suppressed %d, "
                 "failing %d %s; worst residual %.2f" % (valid, n, exact, rounding, exempt, len(bad), bad[:3], worst)))

    # D2 the group value per date is exactly the sum of the custom lines (the fold line included), null only where all are null
    nulls = 0
    for i in range(n):
        vs = [at(k, i) for k in custom_keys if at(k, i) is not None]
        if not vs:
            nulls += 1
    arms.append(("D2", True, "Custom Models series over %d dates: %d null (every member absent), %d custom lines of %d model lines"
                 % (n, nulls, len(custom_keys), len(model))))

    # D3 membership: every custom ts key is a Models > Custom member id in the newest served category-views, or the fold line
    cv = served(s3, cv_keys[-1])
    cust_members = set()
    custom_node = (((cv["nodes"].get("Models") or {}).get("children") or {}).get("Custom")) or {}
    for ch in list(custom_node.get("members") or []) + list((custom_node.get("children") or {}).values()):
        if isinstance(ch, dict) and ch.get("member_id"):
            cust_members.add(ch["member_id"])
    outside = [k for k in custom_keys if k not in cust_members and k != "other_models"]
    arms.append(("D3", not outside, "custom ts keys %d, category-views Custom members %d (%s), outside the tree: %s"
                 % (len(custom_keys), len(cust_members), cv.get("as_of"), outside[:4])))

    # D4 the carve-outs are EXACT served members: on every dated category-views object, compared against the time series OF THAT SAME
    # DATE (a newer object restates its history, so the newest ts is the wrong comparand for a dated chip), non_model_aua minus
    # (Supervised + Unsupervised) equals opal_div_sma + opal_growth_sma to the cent (the CVO's 21-23M gap).
    eq, tot_dated, miss, gaps = 0, 0, [], []
    rem_zero, rem_other = 0, 0
    for k in cv_keys:
        d = k.split("/")[-1].replace(".json", "")
        c = served(s3, k)
        try:
            t_d = served(s3, "portal/gold/mdpf/global/aggregate-aua-timeseries/%s.json" % d)
        except Exception:                                    # noqa: BLE001 -- an absent same-date ts object is counted, not hidden
            miss.append(d)
            continue
        ao = c.get("as_of")
        if ao not in t_d["dates"]:
            miss.append(d)
            continue
        i = t_d["dates"].index(ao)
        bmd = t_d["by_model"]
        cl = (c["nodes"].get("Client") or {}).get("children") or {}
        sup = (cl.get(CLIENT_SUP) or {}).get("aum")
        uns = (cl.get(CLIENT_UNSUP) or {}).get("aum")
        nm = t_d["non_model_aua"][i]
        if sup is None or uns is None or nm is None:
            miss.append(d)
            continue
        tot_dated += 1
        carve = 0.0
        for x in CARVE:
            arr = (bmd.get(x) or {}).get("model_value") or []
            carve += num(arr[i] if i < len(arr) else None)
        rem = round(nm - num(sup) - num(uns) - carve, 2)
        gaps.append(abs(rem))
        if abs(rem) <= 0.02:
            eq += 1
        if abs(rem) < 0.005:
            rem_zero += 1
        else:
            rem_other += 1
    arms.append(("D4", tot_dated > 0 and eq == tot_dated,
                 "Client gap == carve-outs to the cent on %d of %d dated category-views dates (%d without a same-date ts object); "
                 "worst difference %.2f" % (eq, tot_dated, len(miss), max(gaps) if gaps else -1)))

    # D5 on a dated date Other AUA is the true remainder: it is zero (so it draws nothing) wherever the carve-outs explain the gap
    arms.append(("D5", tot_dated > 0 and rem_other == 0,
                 "Other AUA on dated dates: zero on %d, nonzero on %d of %d; on the %d undated ts dates it is the single series "
                 "non_model_aua minus the carve-outs" % (rem_zero, rem_other, tot_dated, n - tot_dated)))
    return arms


def cmd(name, fn):
    k, n = report(name, fn())
    return 0 if k == n else 1


# ----------------------------------------------------------------------------------------------- selftest reference patch
REF_MODULE = """export interface TrendPoint { period: string; aum: number | null; pointClass?: string }
export const CUSTOM_MODELS_LABEL = 'Custom Models'
const cents = (x: number): number => Math.round(x * 100) / 100
function sumPresent(values: ReadonlyArray<number | null | undefined>): number | null {
  let any = false
  let s = 0
  for (const v of values) {
    if (v === null || v === undefined) continue
    any = true
    s += v
  }
  return any ? cents(s) : null
}
export function etfStrategiesAua(smaAdditive: number | null, carveOuts: ReadonlyArray<number | null>): number | null {
  return sumPresent([smaAdditive, ...carveOuts])
}
export function otherAua(
  nonModelAua: number | null,
  carveOuts: ReadonlyArray<number | null>,
  clients: ReadonlyArray<number | null> | null,
): number | null {
  if (nonModelAua === null) return null
  const r = cents(nonModelAua - (sumPresent(carveOuts) ?? 0) - (clients ? (sumPresent(clients) ?? 0) : 0))
  return Math.abs(r) < 0.005 ? null : r
}
export function clientChipAt(period: string, asOf: string | null | undefined, value: number | null | undefined): number | null {
  if (!asOf || period !== asOf) return null
  return value === null || value === undefined ? null : value
}
export function groupCustomModelsSeries(
  byModel: Record<string, TrendPoint[]>,
  canonical: ReadonlySet<string>,
): Record<string, TrendPoint[]> {
  const out: Record<string, TrendPoint[]> = {}
  const members: string[] = []
  for (const k of Object.keys(byModel)) {
    if (canonical.has(k)) out[k] = byModel[k]
    else members.push(k)
  }
  if (members.length === 0) return out
  const acc = new Map<string, { aum: number | null; pointClass?: string }>()
  const order: string[] = []
  for (const k of members) {
    for (const p of byModel[k]) {
      const v = p.aum ?? null
      const cur = acc.get(p.period)
      if (!cur) {
        order.push(p.period)
        acc.set(p.period, { aum: v, pointClass: p.pointClass })
        continue
      }
      if (v !== null) cur.aum = cur.aum === null ? v : Math.round((cur.aum + v) * 100) / 100
      if (cur.pointClass !== 'interpolated_estimate' && p.pointClass !== undefined) cur.pointClass = p.pointClass
    }
  }
  out[CUSTOM_MODELS_LABEL] = order.map((period) => ({ period, aum: acc.get(period)!.aum, pointClass: acc.get(period)!.pointClass }))
  return out
}
"""


def patch_cvt(src):
    s = src.replace("const L1_COLOR: Readonly<Record<string, string>> = {", "export const L1_COLOR: Readonly<Record<string, string>> = {", 1)
    s = s.replace("const l1ColorOf = (key: string): string =>", "export const l1ColorOf = (key: string): string =>", 1)
    return s


NEW_STACK = """const STACK_SERIES: ReadonlyArray<{ key: string; label: string }> = [
  { key: 'ust',          label: 'Ultra-Short Term' },
  { key: 'st',           label: 'Short Term' },
  { key: 'int',          label: 'Intermediate Term' },
  { key: 'lt',           label: 'Long Term' },
  { key: 'ult',          label: 'Ultra-Long Term' },
  { key: 'custom_models', label: 'Custom Models' },
  { key: 'sma_additive', label: 'ETF Strategies' },
  { key: 'tax_additive', label: 'ALT Strategies' },
  { key: 'client_supervised', label: 'Client Supervised' },
  { key: 'client_unsupervised', label: 'Client Unsupervised' },
  { key: 'non_model',    label: 'Other AUA' },
]"""


def patch_page(src):
    s = src.replace("import { CategoryViewTree } from '@/components/CategoryViewTree'",
                    "import { CategoryViewTree, l1ColorOf } from '@/components/CategoryViewTree'\n"
                    "import { groupCustomModelsSeries, etfStrategiesAua, otherAua, clientChipAt } from '@/lib/trendGrouping'", 1)
    s = re.sub(r"const STACK_SERIES[^=]*=\s*\[.*?\n\]", lambda m: NEW_STACK, s, count=1, flags=re.S)
    s = s.replace("const keyForModel = (label: string): string =>",
                  "const TREND_GROUP_L1: Record<string, string> = { 'Custom Models': 'Custom', 'ETF Strategies': 'ETF Strategies', "
                  "'Client Supervised': 'Client - Opal Supervised', 'Client Unsupervised': 'Client - Opal Unsupervised' }\n"
                  "const trendColorOf = (label: string): string | undefined => (label in TREND_GROUP_L1 ? l1ColorOf(TREND_GROUP_L1[label]) : undefined)\n"
                  "const ALT_TREND_COLOR = getModelColor('Tax-Managed SMA')?.primary ?? PALETTE.gray300\n"
                  "const keyForModel = (label: string): string =>", 1)
    s = s.replace("  const timeSeriesData = useMemo(() => {\n    if (!timeSeriesDataRaw) return null\n"
                  "    return { ...timeSeriesDataRaw, by_model: rollBlendsIntoArchetypeSeries(timeSeriesDataRaw.by_model) }\n"
                  "  }, [timeSeriesDataRaw])",
                  "  const timeSeriesData = useMemo(() => {\n    if (!timeSeriesDataRaw) return null\n"
                  "    const rolled = rollBlendsIntoArchetypeSeries(timeSeriesDataRaw.by_model)\n"
                  "    const by_model = groupCustomModelsSeries(rolled, new Set(['Ultra-Short Term', 'Short Term', 'Intermediate Term', 'Long Term', 'Ultra-Long Term']))\n"
                  "    return { ...timeSeriesDataRaw, by_model }\n  }, [timeSeriesDataRaw])", 1)
    s = s.replace("          const modelColor = getModelColor(modelName)\n          return {\n            label: displayModelName(modelName),\n"
                  "            color: modelColor?.primary || PALETTE.blue400,",
                  "          const modelColor = getModelColor(modelName)\n          return {\n            label: displayModelName(modelName),\n"
                  "            color: trendColorOf(modelName) ?? modelColor?.primary ?? PALETTE.blue400,", 1)
    s = s.replace("[{ label: 'Additive SMA sleeves', color: getModelColor('Additive SMA sleeves')?.primary || PALETTE.gray300 }]",
                  "[{ label: 'ETF Strategies', color: trendColorOf('ETF Strategies') ?? PALETTE.gray300 }]", 1)
    s = s.replace("[{ label: 'Tax-Managed SMA', color: getModelColor('Tax-Managed SMA')?.primary || PALETTE.gray300 }]",
                  "[{ label: 'ALT Strategies', color: ALT_TREND_COLOR }]", 1)
    # the data-point build: the new series, appended as a block (the reference only needs the wiring text the arms read)
    s += ("\n// reference wiring for the arms\n"
          "const clientSup = clientChipAt(period, categoryViews?.as_of, categoryViews?.nodes?.Client?.children?.['Client - Opal Supervised']?.aum)\n"
          "const clientUnsup = clientChipAt(period, categoryViews?.as_of, categoryViews?.nodes?.Client?.children?.['Client - Opal Unsupervised']?.aum)\n"
          "const etfValue = etfStrategiesAua(addPt?.smaAdditiveAua ?? null, [divSma, growthSma])\n"
          "const otherValue = otherAua(nonModel, [divSma, growthSma], [clientSup, clientUnsup])\n"
          "const legendFor = (l: string) => trendColorOf(l)\n"
          "const legendSup = trendColorOf('Client Supervised')\nconst legendUnsup = trendColorOf('Client Unsupervised')\n")
    return s


def cmd_selftest():
    mod, page, cvt = targets()
    ok_all = True
    d = tempfile.mkdtemp(prefix="r7cni1_ref_")
    try:
        print("-- base (the tree as it is)")
        base_m = run_module(mod)
        base_p = run_page(page, cvt)
        bm = sum(1 for a in base_m if a[1])
        bp = sum(1 for a in base_p if a[1])
        print("  base module %d of %d, page %d of %d (must be below full)" % (bm, len(base_m), bp, len(base_p)))
        ok_all &= (bm < N_MODULE and bp < N_PAGE)

        print("-- reference patch (scratch copies; the product tree is never written)")
        rm = os.path.join(d, "trendGrouping.ts")
        with open(rm, "w", newline="\n", encoding="utf-8") as f:
            f.write(REF_MODULE)
        rp = os.path.join(d, "ModelPortfolios.tsx")
        rc = os.path.join(d, "CategoryViewTree.tsx")
        src_p = read(page)
        src_c = read(cvt)
        new_p = patch_page(src_p)
        new_c = patch_cvt(src_c)
        if new_p == src_p or new_c == src_c:
            print("  SELFTEST FAIL: a reference patch anchor did not match the target (page changed=%s, cvt changed=%s)"
                  % (new_p != src_p, new_c != src_c))
            return 1
        with open(rp, "w", newline="\n", encoding="utf-8") as f:
            f.write(new_p)
        with open(rc, "w", newline="\n", encoding="utf-8") as f:
            f.write(new_c)
        km, nm_ = report("MODULE (reference)", run_module(rm))
        kp, np_ = report("PAGE (reference)", run_page(rp, rc))
        ok_all &= (km == nm_ and kp == np_)

        print("-- mutants")

        def write(name, text):
            p = os.path.join(d, name)
            with open(p, "w", newline="\n", encoding="utf-8") as f:
                f.write(text)
            return p

        # a: a grouping that coalesces an all-null period to 0
        mp = write("mut_module.ts", REF_MODULE.replace("acc.set(p.period, { aum: v, pointClass: p.pointClass })",
                                                      "acc.set(p.period, { aum: v ?? 0, pointClass: p.pointClass })"))
        red = [a[0] for a in run_module(mp) if not a[1]]
        print("  mutant 'null coalesced to 0' -> RED on %s (must include M2)" % red)
        ok_all &= ("M2" in red)
        # b: a second palette (hex literal beside a group label)
        mpp = write("mut_page.tsx", new_p.replace("const trendColorOf = (label: string): string | undefined =>",
                                                  "const HEX_CUSTOM = { 'Custom Models': '#d946ef' }\nconst trendColorOf = (label: string): string | undefined =>", 1))
        red = [a[0] for a in run_page(mpp, rc) if not a[1]]
        print("  mutant 'hex literal beside a group label' -> RED on %s (must include P5)" % red)
        ok_all &= ("P5" in red)
        # c: the grouping gated on Global again (the earlier draft's reading; the PRD says every scope)
        mgp = write("mut_global.tsx", new_p.replace(
            "    const by_model = groupCustomModelsSeries(rolled,",
            "    const by_model = effectiveFirmId === 'global' ? groupCustomModelsSeries(rolled,", 1)
                    .replace("'Long Term', 'Ultra-Long Term']))\n    return { ...timeSeriesDataRaw, by_model }",
                             "'Long Term', 'Ultra-Long Term'])) : rolled\n    return { ...timeSeriesDataRaw, by_model }", 1))
        red = [a[0] for a in run_page(mgp, rc) if not a[1]]
        print("  mutant 'grouping gated on Global' -> RED on %s (must include P4)" % red)
        ok_all &= ("P4" in red)
        # d: ALT recoloured from Total Assets (green400) against Andrew's 2026-10-01 vermilion pin
        malt = write("mut_alt.tsx", new_p.replace(
            "const ALT_TREND_COLOR = getModelColor('Tax-Managed SMA')?.primary ?? PALETTE.gray300",
            "const ALT_TREND_COLOR = l1ColorOf('ALT Strategies')", 1))
        red = [a[0] for a in run_page(malt, rc) if not a[1]]
        print("  mutant 'ALT recoloured from Total Assets' -> RED on %s (must include P6)" % red)
        ok_all &= ("P6" in red)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    print("ROUND 7 SELFTEST: %s" % ("OK" if ok_all else "FAIL"))
    return 0 if ok_all else 1


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("module", "page", "data", "selftest"):
        print(__doc__)
        return 2
    sub = sys.argv[1]
    if sub == "module":
        m, _, _ = targets()
        return cmd("GROUP-MODULE", lambda: run_module(m))
    if sub == "page":
        _, p, c = targets()
        return cmd("GROUP-PAGE", lambda: run_page(p, c))
    if sub == "data":
        return cmd("GROUP-DATA", run_data)
    return cmd_selftest()


if __name__ == "__main__":
    sys.exit(main())
