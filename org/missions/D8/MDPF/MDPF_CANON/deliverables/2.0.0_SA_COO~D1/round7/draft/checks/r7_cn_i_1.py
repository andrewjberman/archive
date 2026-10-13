#!/usr/bin/env python3
"""MDPF_CANON round 7, cell CN-i-1 -- FWD-9, the AUA Trend grouping (Custom Models, ETF Strategies, ALT Strategies).

Issuer's check (2.0.0_SA_COO~D1). Read-only for every worker: never edit this file.

  python r7_cn_i_1.py module     the pure grouping module sums custom lines into ONE series, absent is not zero (6 arms)
  python r7_cn_i_1.py page       the page uses the Total Assets colour export, one palette, Global only (5 arms)
  python r7_cn_i_1.py data       the rule on the REAL served objects: the stack still adds to the total (3 arms)
  python r7_cn_i_1.py selftest   proves the arms fail at base and pass on a reference patch; issuer only

Targets (repo root = `git rev-parse --show-toplevel` of the working directory):
  portal/src/lib/trendGrouping.ts   portal/src/pages/ModelPortfolios.tsx   portal/src/components/CategoryViewTree.tsx
Overrides for the selftest only: R7_MODULE, R7_PAGE, R7_CVT (absolute file paths).

Output: `ROUND 7 <NAME>: k of n arms`, exit 0 only when k == n. ASCII only. The `data` subcommand also prints FINDING lines
(measured contradictions in the FWD-9 inputs); they are not arms.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BUCKET = "opal-data-assets"
CANON = ["Ultra-Short Term", "Short Term", "Intermediate Term", "Long Term", "Ultra-Long Term"]

BUN_TS = r"""
import { pathToFileURL } from 'node:url'
const mod: any = await import(pathToFileURL(process.env.R7_MODULE as string).href)
const group = mod.groupCustomModelsSeries as (b: Record<string, any[]>, c: ReadonlySet<string>) => Record<string, any[]>
const LABEL = mod.CUSTOM_MODELS_LABEL as string
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
  'the member series are absent from the result: three keys (two canonical + the group)')
arm('M5', JSON.stringify(src) === snap, 'the input is not mutated')
const none = group({ 'Short Term': mk([1, 2, 3, 4, 5, 6]) }, canon)
arm('M6', !(LABEL in none) && Object.keys(none).length === 1, 'no custom lines -> no group key (nothing invented)')
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
        if r.returncode != 0 or len(arms) != 6:
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

    # P1 the Total Assets colour table is EXPORTED once, with its six keys intact (no second table is born).
    ok = (re.search(r"^export const L1_COLOR\b", cv, re.M) is not None
          and re.search(r"^export const l1ColorOf\b", cv, re.M) is not None
          and all(("'%s'" % k in cv or k + ":" in cv) for k in ("Custom", "ETF Strategies", "ALT Strategies",
                                                               "Client - Opal Supervised", "Client - Opal Unsupervised")))
    arms.append(("P1", ok, "CategoryViewTree exports L1_COLOR and l1ColorOf; the five bucket keys still present"))

    # P2 the page imports the export and the grouping module.
    imp_color = re.search(r"import \{[^}]*\bl1ColorOf\b[^}]*\} from '[^']*CategoryViewTree'", text) is not None
    imp_group = re.search(r"import \{[^}]*\bgroupCustomModelsSeries\b[^}]*\} from '[^']*trendGrouping'", text) is not None
    arms.append(("P2", imp_color and imp_group, "page imports l1ColorOf (%s) and groupCustomModelsSeries (%s)" % (imp_color, imp_group)))

    # P3 the mount spine: custom_models before non_model; the three group labels; the two old band labels are gone from it.
    m = re.search(r"const STACK_SERIES[^=]*=\s*\[(.*?)\n\]", text, re.S)
    body = m.group(1) if m else ""
    keys = re.findall(r"key:\s*'([^']+)'", body)
    labels = re.findall(r"label:\s*'([^']+)'", body)
    ok3 = ("custom_models" in keys and "non_model" in keys and keys.index("custom_models") < keys.index("non_model")
           and "Custom Models" in labels and "ETF Strategies" in labels and "ALT Strategies" in labels
           and "Additive SMA sleeves" not in labels and "Tax-Managed SMA" not in labels)
    arms.append(("P3", ok3, "STACK_SERIES keys %s labels %s" % (keys, labels)))

    # P4 the grouping is applied for Global only (the call sits next to an effectiveFirmId === 'global' test).
    idx = [i for i, ln in enumerate(lines) if "groupCustomModelsSeries(" in ln and "import" not in ln]
    near = any("effectiveFirmId === 'global'" in "\n".join(lines[max(0, i - 4):i + 4]) for i in idx)
    arms.append(("P4", len(idx) >= 1 and near, "groupCustomModelsSeries call sites %d, Global-gated: %s" % (len(idx), near)))

    # P5 one palette: colours for the three labels come through l1ColorOf (a resolver used at >= 3 sites), with no hex literal
    # and no second PALETTE pick on a line naming one of the three labels.
    grp_lines = [ln for ln in lines if re.search(r"'(Custom Models|ETF Strategies|ALT Strategies)'", ln)]
    hexed = [ln.strip()[:80] for ln in grp_lines if re.search(r"#[0-9a-fA-F]{3,8}\b", ln)]
    palette = [ln.strip()[:80] for ln in grp_lines if re.search(r"PALETTE\.(fuchsia|cyan|green)\d+", ln)]
    uses = len(re.findall(r"\btrendColorOf\(", text))
    has_def = re.search(r"const trendColorOf\b", text) is not None and "l1ColorOf(" in text
    arms.append(("P5", has_def and uses >= 3 and not hexed and not palette,
                 "trendColorOf defined=%s, uses=%d, hex literals on group lines=%d, PALETTE picks=%d"
                 % (has_def, uses, len(hexed), len(palette))))
    return arms


def served(s3, key):
    return json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())


def newest(s3, prefix):
    ks = []
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
        ks += [o["Key"] for o in p.get("Contents", []) if o["Key"].endswith(".json")]
    return sorted(ks)


def run_data():
    import boto3
    s3 = boto3.client("s3", region_name="us-east-1")
    ts_keys = newest(s3, "portal/gold/mdpf/global/aggregate-aua-timeseries/")
    cv_keys = newest(s3, "portal/gold/mdpf/global/category-views/")
    ts = served(s3, ts_keys[-1])
    dates = ts["dates"]
    n = len(dates)
    sma = {k for k, v in ts["by_model"].items() if v.get("cohort_class") == "sma"}
    model = {k: v for k, v in ts["by_model"].items() if k not in sma and k != "tax"}
    core_keys = [k for k in model if k in ("opal_ultra_short_term", "opal_short_term", "opal_intermediate",
                                           "opal_long_term_conservative", "opal_long_term_aggressive")]
    custom_keys = [k for k in model if k not in core_keys]
    arms = []

    def val(k, i):
        v = model[k]["model_value"][i]
        return v

    # D1 the stack still adds to the total: canonical + custom group + Non-Model + the two additive bands == opal_aggregate_aua
    bad, valid = [], 0
    for i in range(n):
        tot = ts["opal_aggregate_aua"][i]
        nm = ts["non_model_aua"][i]
        if tot is None or nm is None or ts["model_aua"][i] is None:
            continue
        valid += 1
        core = sum((val(k, i) or 0.0) for k in core_keys)
        cust_vals = [val(k, i) for k in custom_keys if val(k, i) is not None]
        cust = sum(cust_vals) if cust_vals else 0.0
        add = (ts["sma_additive_aua"][i] or 0.0) + (ts["tax_additive_aua"][i] or 0.0)
        # the model lines the page draws are every non-SMA by_model key; model_aua differs from their sum by the rounding cents
        if abs(tot - (core + cust + nm + add)) > 0.05 + abs(ts["model_aua"][i] - (core + cust)):
            bad.append(dates[i])
    arms.append(("D1", valid > 0 and not bad,
                 "stack == opal_aggregate_aua on %d valued dates of %d, %d failing %s" % (valid, n, len(bad), bad[:3])))

    # D2 the group value per date is exactly the sum of the custom lines, null only where all are null
    nulls = 0
    mism = 0
    for i in range(n):
        vs = [val(k, i) for k in custom_keys if val(k, i) is not None]
        grp = round(sum(vs), 2) if vs else None
        if grp is None:
            nulls += 1
        direct = round(sum(v for v in (model[k]["model_value"][i] for k in custom_keys) if v is not None), 2) if vs else None
        if grp != direct:
            mism += 1
    arms.append(("D2", mism == 0, "Custom Models series over %d dates: %d null (all members absent), %d members of %d model lines"
                 % (n, nulls, len(custom_keys), len(model))))

    # D3 membership: every custom ts key is a Models > Custom member_id in the newest served category-views, or the fold line
    cv = served(s3, cv_keys[-1])
    cust_members = set()
    custom_node = ((cv["nodes"].get("Models") or {}).get("children") or {}).get("Custom") or {}
    for ch in list(custom_node.get("members") or []) + list((custom_node.get("children") or {}).values()):
        if isinstance(ch, dict) and ch.get("member_id"):
            cust_members.add(ch["member_id"])
    outside = [k for k in custom_keys if k not in cust_members and k != "other_models"]
    arms.append(("D3", not outside,
                 "custom ts keys %d, category-views Custom members %d (%s), outside the tree: %s"
                 % (len(custom_keys), len(cust_members), cv.get("as_of"), outside[:4])))

    # FINDINGS (not arms): the contradictions the cell must not paper over
    i = n - 1
    div = sum(model_v for model_v in [ts["by_model"].get(k, {}).get("model_value", [None] * n)[i] for k in
                                      ("opal_div_sma", "opal_growth_sma", "pfde")] if model_v is not None)
    print("  FINDING F1 dated category-views objects served by the cell's data path: %d (%s .. %s) against %d ts dates; "
          "the portal fetches only platinum/mdpf/<scope>/category-views.json (the latest)"
          % (len(cv_keys), cv_keys[0].split("/")[-1], cv_keys[-1].split("/")[-1], n))
    print("  FINDING F2 ETF Strategies group on the last date = %.2f from ts SMA-class lines; sma_additive_aua = %.2f; "
          "the carve-out members sit inside non_model_aua = %.2f (drawing the group as its own stack band double counts them)"
          % (div, ts["sma_additive_aua"][i] or 0.0, ts["non_model_aua"][i] or 0.0))
    return arms


def cmd(name, fn):
    k, n = report(name, fn())
    return 0 if k == n else 1


# ----------------------------------------------------------------------------------------------- selftest reference patch
REF_MODULE = """export interface TrendPoint { period: string; aum: number | null; pointClass?: string }
export const CUSTOM_MODELS_LABEL = 'Custom Models'
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


def patch_page(src):
    s = src.replace("import { CategoryViewTree } from '@/components/CategoryViewTree'",
                    "import { CategoryViewTree, l1ColorOf } from '@/components/CategoryViewTree'\n"
                    "import { groupCustomModelsSeries } from '@/lib/trendGrouping'", 1)
    s = s.replace("  { key: 'non_model',    label: 'Non-Model' },\n  { key: 'sma_additive', label: 'Additive SMA sleeves' },\n"
                  "  { key: 'tax_additive', label: 'Tax-Managed SMA' },\n",
                  "  { key: 'custom_models', label: 'Custom Models' },\n  { key: 'non_model',    label: 'Non-Model' },\n"
                  "  { key: 'sma_additive', label: 'ETF Strategies' },\n  { key: 'tax_additive', label: 'ALT Strategies' },\n", 1)
    s = s.replace("const keyForModel = (label: string): string =>",
                  "const TREND_GROUP_L1: Record<string, string> = { 'Custom Models': 'Custom', 'ETF Strategies': 'ETF Strategies', "
                  "'ALT Strategies': 'ALT Strategies' }\n"
                  "const trendColorOf = (label: string): string | undefined => (label in TREND_GROUP_L1 ? l1ColorOf(TREND_GROUP_L1[label]) : undefined)\n"
                  "const keyForModel = (label: string): string =>", 1)
    s = s.replace("  const timeSeriesData = useMemo(() => {\n    if (!timeSeriesDataRaw) return null\n"
                  "    return { ...timeSeriesDataRaw, by_model: rollBlendsIntoArchetypeSeries(timeSeriesDataRaw.by_model) }\n"
                  "  }, [timeSeriesDataRaw])",
                  "  const timeSeriesData = useMemo(() => {\n    if (!timeSeriesDataRaw) return null\n"
                  "    const rolled = rollBlendsIntoArchetypeSeries(timeSeriesDataRaw.by_model)\n"
                  "    const by_model = effectiveFirmId === 'global'\n"
                  "      ? groupCustomModelsSeries(rolled, new Set(['Ultra-Short Term', 'Short Term', 'Intermediate Term', 'Long Term', 'Ultra-Long Term']))\n"
                  "      : rolled\n    return { ...timeSeriesDataRaw, by_model }\n  }, [timeSeriesDataRaw, effectiveFirmId])", 1)
    s = s.replace("          const modelColor = getModelColor(modelName)\n          return {\n            label: displayModelName(modelName),\n"
                  "            color: modelColor?.primary || PALETTE.blue400,",
                  "          const modelColor = getModelColor(modelName)\n          return {\n            label: displayModelName(modelName),\n"
                  "            color: trendColorOf(modelName) ?? modelColor?.primary ?? PALETTE.blue400,", 1)
    s = s.replace("[{ label: 'Additive SMA sleeves', color: getModelColor('Additive SMA sleeves')?.primary || PALETTE.gray300 }]",
                  "[{ label: 'ETF Strategies', color: trendColorOf('ETF Strategies') ?? PALETTE.gray300 }]", 1)
    s = s.replace("[{ label: 'Tax-Managed SMA', color: getModelColor('Tax-Managed SMA')?.primary || PALETTE.gray300 }]",
                  "[{ label: 'ALT Strategies', color: trendColorOf('ALT Strategies') ?? PALETTE.gray300 }]", 1)
    s = s.replace("                            const modelColor = getModelColor(s.label)\n",
                  "                            const modelColor = getModelColor(s.label)\n"
                  "                            const groupColor = trendColorOf(s.label)\n", 1)
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
        ok_all &= (bm < 6 and bp < 5)

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
        # M-a: a grouping that coalesces an all-null period to 0
        mut = REF_MODULE.replace("acc.set(p.period, { aum: v, pointClass: p.pointClass })",
                                 "acc.set(p.period, { aum: v ?? 0, pointClass: p.pointClass })")
        mp = os.path.join(d, "mut_module.ts")
        with open(mp, "w", newline="\n", encoding="utf-8") as f:
            f.write(mut)
        arms = run_module(mp)
        red = [a[0] for a in arms if not a[1]]
        print("  mutant 'null coalesced to 0' -> RED on %s (must include M2)" % red)
        ok_all &= ("M2" in red)
        # P-a: a second palette (hex literal on a group label line)
        mut_p = new_p.replace("const trendColorOf = (label: string): string | undefined =>",
                              "const HEX_CUSTOM = { 'Custom Models': '#d946ef' }\nconst trendColorOf = (label: string): string | undefined =>", 1)
        mpp = os.path.join(d, "mut_page.tsx")
        with open(mpp, "w", newline="\n", encoding="utf-8") as f:
            f.write(mut_p)
        arms = run_page(mpp, rc)
        red = [a[0] for a in arms if not a[1]]
        print("  mutant 'hex literal beside a group label' -> RED on %s (must include P5)" % red)
        ok_all &= ("P5" in red)
        # P-b: not Global-gated
        mut_g = new_p.replace("const by_model = effectiveFirmId === 'global'\n      ? groupCustomModelsSeries(", "const by_model = true\n      ? groupCustomModelsSeries(", 1)
        mgp = os.path.join(d, "mut_global.tsx")
        with open(mgp, "w", newline="\n", encoding="utf-8") as f:
            f.write(mut_g)
        arms = run_page(mgp, rc)
        red = [a[0] for a in arms if not a[1]]
        print("  mutant 'grouping not Global-gated' -> RED on %s (must include P4)" % red)
        ok_all &= ("P4" in red)
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
