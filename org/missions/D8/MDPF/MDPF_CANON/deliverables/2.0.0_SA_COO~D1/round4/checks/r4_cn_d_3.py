#!/usr/bin/env python3
"""MDPF_CANON round 4, cell CN-d-3 -- the Global trend stack meets the line (W8-S3).

Issuer's check (2.0.0_SA_COO~D1). Read-only for every worker: never edit this file.

  python r4_cn_d_3.py reader     the paired reader carries the two additive series as FIELD READS (4 arms)
  python r4_cn_d_3.py page       the page mounts the two bands for Global only, with no client arithmetic (5 arms)
  python r4_cn_d_3.py selftest   proves the arms can fail (base, mutants) and pass (a reference patch); issuer only

Targets: <repo root>/portal/src/lib/pairedProvenanceRead.ts and <repo root>/portal/src/pages/ModelPortfolios.tsx,
where <repo root> is `git rev-parse --show-toplevel` of the working directory. Overrides for the selftest only:
R4_MODULE, R4_PAGE (absolute file paths). The provenance guard arm always runs against <repo root>/portal.

Output: `ROUND 4 <NAME>: k of n arms`, exit 0 only when k == n. ASCII only.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

BUN_TS = r"""
import { pathToFileURL } from 'node:url'
const mod: any = await import(pathToFileURL(process.env.R4_MODULE as string).href)
const read = mod.readGlobalEnterpriseSeries as (s: unknown) => any[]
const out: string[] = []
const arm = (id: string, ok: boolean, why: string) => out.push(`ARM ${id} ${ok ? 'PASS' : 'FAIL'} ${why}`)

// Synthetic series (no client figure): 12 dates, one whole-day gap (i=8), additive on 5 dates.
const N = 12
const dates = Array.from({ length: N }, (_, i) => `2026-09-${String(i + 1).padStart(2, '0')}`)
const model: Array<number | null> = Array.from({ length: N }, (_, i) => 1000 + 10 * i)
const nm: Array<number | null> = Array.from({ length: N }, (_, i) => 200 + i)
const sma: Array<number | null> = Array.from({ length: N }, () => null)
const tax: Array<number | null> = Array.from({ length: N }, () => null)
for (const i of [3, 4, 5]) sma[i] = 7.5
for (const i of [4, 5]) tax[i] = 2.25
const oaa: Array<number | null> = model.map((m, i) => Math.round(((m as number) + (nm[i] as number) + (sma[i] ?? 0) + (tax[i] ?? 0)) * 100) / 100)
for (const a of [model, nm, oaa]) a[8] = null
const series = { dates, opal_aggregate_aua: oaa, model_aua: model, non_model_aua: nm, sma_additive_aua: sma, tax_additive_aua: tax }
const pts = read(series)

arm('R1', pts.length === N && pts.every((p, i) => p.smaAdditiveAua === sma[i] && p.taxAdditiveAua === tax[i]),
  `field read of both additive series over ${pts.length} dates (additive on ${sma.filter((v) => v != null).length} + ${tax.filter((v) => v != null).length})`)

const bare = read({ dates, opal_aggregate_aua: oaa, model_aua: model, non_model_aua: nm })
arm('R2', bare.length === N && bare.every((p) => p.smaAdditiveAua === null && p.taxAdditiveAua === null),
  'a series with no additive fields reads null on every date (never 0, never undefined)')

let valid = 0
let bad = 0
for (const p of pts) {
  if (p.totalAua == null) continue
  valid += 1
  const sum = (p.modelAua ?? 0) + (p.nonModelAua ?? 0) + (p.smaAdditiveAua ?? 0) + (p.taxAdditiveAua ?? 0)
  if (Math.abs(p.totalAua - sum) > 0.011) bad += 1
}
arm('R3', valid === 11 && bad === 0, `identity total == model + non_model + sma_additive + tax_additive on ${valid} valued dates, ${bad} failing`)

arm('R4', pts.every((p, i) => p.totalAua === oaa[i] && p.modelAua === model[i] && p.nonModelAua === nm[i]),
  'total, model and non-model still read straight through (control)')
console.log(out.join('\n'))
"""


def root():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if r.returncode != 0:
        print("ERROR: not in a git worktree")
        sys.exit(2)
    return r.stdout.strip()


def paths():
    pr = os.path.join(root(), "portal")
    module = os.environ.get("R4_MODULE") or os.path.join(pr, "src", "lib", "pairedProvenanceRead.ts")
    page = os.environ.get("R4_PAGE") or os.path.join(pr, "src", "pages", "ModelPortfolios.tsx")
    return pr, module, page


def run_reader(module):
    if not os.path.isfile(module):
        return [("R0", False, "module not found: " + module)]
    d = tempfile.mkdtemp(prefix="r4cnd3_")
    try:
        ex = os.path.join(d, "exercise.ts")
        with open(ex, "w", newline="\n") as f:
            f.write(BUN_TS)
        env = dict(os.environ)
        env["R4_MODULE"] = module
        try:
            r = subprocess.run(["bun", ex], capture_output=True, text=True, timeout=100, env=env, cwd=d)
        except subprocess.TimeoutExpired:
            return [("R0", False, "bun exercise timed out")]
        arms = []
        for line in r.stdout.splitlines():
            m = re.match(r"ARM (R\d) (PASS|FAIL) (.*)", line)
            if m:
                arms.append((m.group(1), m.group(2) == "PASS", m.group(3)))
        if r.returncode != 0 or len(arms) != 4:
            tail = (r.stderr or r.stdout).strip().splitlines()[-1:] or [""]
            return [("R0", False, "exercise rc=%d arms=%d %s" % (r.returncode, len(arms), tail[0][:160]))]
        return arms
    finally:
        shutil.rmtree(d, ignore_errors=True)


def run_page(page, portal_real):
    if not os.path.isfile(page):
        return [("P0", False, "page not found: " + page)]
    with open(page, encoding="utf-8", newline="") as f:
        text = f.read()
    lines = text.split("\n")
    arms = []

    # P1: STACK_SERIES carries both band keys AFTER non_model.
    m = re.search(r"const STACK_SERIES[^=]*=\s*\[(.*?)\n\]", text, re.S)
    keys = re.findall(r"key:\s*'([^']+)'", m.group(1)) if m else []
    ok1 = ("non_model" in keys and "sma_additive" in keys and "tax_additive" in keys
           and keys.index("sma_additive") > keys.index("non_model")
           and keys.index("tax_additive") > keys.index("non_model"))
    arms.append(("P1", ok1, "STACK_SERIES keys %s" % keys))

    # P2: both row builders (two `const nmKey = keyForModel('Non-Model')` sites) read both fields within 30 lines.
    sites = [i for i, ln in enumerate(lines) if re.search(r"const nmKey = keyForModel\('Non-Model'\)", ln)]
    hits = []
    for i in sites:
        block = "\n".join(lines[i:i + 31])
        hits.append(("smaAdditiveAua" in block) and ("taxAdditiveAua" in block))
    arms.append(("P2", len(sites) == 2 and all(hits), "row builders %d, each reads both fields: %s" % (len(sites), hits)))

    # P3: field-read law -- both fields appear (>= 2 each) and no arithmetic touches either.
    n_s = len(re.findall(r"\bsmaAdditiveAua\b", text))
    n_t = len(re.findall(r"\btaxAdditiveAua\b", text))
    arith = []
    for ln in lines:
        if "AdditiveAua" not in ln:
            continue
        code = re.sub(r"//.*$", "", ln)
        code = re.sub(r"'[^']*'|\"[^\"]*\"|`[^`]*`", "''", code)
        if re.search(r"\s[-+*/]\s", code):
            arith.append(ln.strip()[:80])
    arms.append(("P3", n_s >= 2 and n_t >= 2 and not arith,
                 "smaAdditiveAua x%d, taxAdditiveAua x%d, arithmetic hits %d" % (n_s, n_t, len(arith))))

    # P4: control -- the provenance read guard stays green on the real portal tree.
    try:
        r = subprocess.run(["node", "scripts/provenance-read-guard.mjs"], capture_output=True, text=True,
                           timeout=100, cwd=portal_real)
        arms.append(("P4", r.returncode == 0 and r.stdout.lstrip().startswith("OK:"),
                     "provenance-read-guard rc=%d (control)" % r.returncode))
    except (subprocess.TimeoutExpired, OSError) as e:
        arms.append(("P4", False, "provenance-read-guard did not run: %s" % e))

    # P5: both stack mounts gate the bands to Global (the `show` expression names the additive keys and isPerFirm).
    shows = []
    for i, ln in enumerate(lines):
        if re.search(r"const show = ", ln):
            blk = []
            for ln2 in lines[i:i + 9]:
                blk.append(ln2)
                if re.search(r"const (modelColor|color|interpMonths)\b", ln2):
                    break
            b = "\n".join(blk).lower()
            shows.append("additive" in b and "isperfirm" in b)
    arms.append(("P5", len(shows) == 2 and all(shows), "stack mounts %d, each gates the bands: %s" % (len(shows), shows)))
    return arms


def report(name, arms):
    for a in arms:
        print("  %s %s %s" % (a[0], "PASS" if a[1] else "FAIL", a[2]))
    k = sum(1 for a in arms if a[1])
    print("ROUND 4 %s: %d of %d arms" % (name, k, len(arms)))
    return k, len(arms)


def cmd_reader():
    _, module, _ = paths()
    k, n = report("BAND-READER", run_reader(module))
    return 0 if k == n else 1


def cmd_page():
    pr, _, page = paths()
    k, n = report("BAND-PAGE", run_page(page, pr))
    return 0 if k == n else 1


def patch_module(src):
    s = src.replace(
        "  non_model_aua?: Array<number | null>\n  by_model?:",
        "  non_model_aua?: Array<number | null>\n  sma_additive_aua?: Array<number | null>\n"
        "  tax_additive_aua?: Array<number | null>\n  by_model?:", 1)
    s = s.replace("  nonModelAua: number | null\n}",
                  "  nonModelAua: number | null\n  smaAdditiveAua: number | null\n  taxAdditiveAua: number | null\n}", 1)
    s = s.replace("    nonModelAua: nm?.[i] ?? null,\n",
                  "    nonModelAua: nm?.[i] ?? null,\n    smaAdditiveAua: series.sma_additive_aua?.[i] ?? null,\n"
                  "    taxAdditiveAua: series.tax_additive_aua?.[i] ?? null,\n", 1)
    return s


def patch_page(src):
    s = src.replace("  { key: 'non_model',    label: 'Non-Model' },\n]",
                    "  { key: 'non_model',    label: 'Non-Model' },\n  { key: 'sma_additive', label: 'Additive SMA sleeves' },\n"
                    "  { key: 'tax_additive', label: 'Tax-Managed SMA' },\n]", 1)
    sites = [("aggregateItem.period", 1), ("period", 2)]
    out = []
    lines = s.split("\n")
    n = 0
    for ln in lines:
        out.append(ln)
        if "const nmKey = keyForModel('Non-Model')" in ln:
            var = sites[n][0]
            n += 1
            ind = ln[:len(ln) - len(ln.lstrip())]
            out.append(ind + "dataPoint['sma_additive'] = !timeSeriesData.isPerFirm ? "
                       "(globalEnterpriseByPeriod.get(%s)?.smaAdditiveAua ?? null) : null" % var)
            out.append(ind + "dataPoint['tax_additive'] = !timeSeriesData.isPerFirm ? "
                       "(globalEnterpriseByPeriod.get(%s)?.taxAdditiveAua ?? null) : null" % var)
    s = "\n".join(out)
    s = re.sub(
        r"(\? \(timeSeriesData\.isPerFirm \|\| hasGlobalEnterprise\)\n)([ \t]*): trendModelOrder\.includes\(s\.label\)",
        lambda m: (m.group(1) + m.group(2) + ": (s.key === 'sma_additive' || s.key === 'tax_additive')\n"
                   + m.group(2) + "  ? (!timeSeriesData.isPerFirm && hasGlobalEnterprise)\n"
                   + m.group(2) + "  : trendModelOrder.includes(s.label)"),
        s)
    return s


def cmd_selftest():
    pr, module, page = paths()
    bad = []
    with open(module, encoding="utf-8", newline="") as f:
        msrc = f.read().replace("\r\n", "\n")   # the portal files are CRLF; the patches are written on LF text
    with open(page, encoding="utf-8", newline="") as f:
        psrc = f.read().replace("\r\n", "\n")
    d = tempfile.mkdtemp(prefix="r4cnd3_self_")
    try:
        def put(name, text):
            p = os.path.join(d, name)
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(text)
            return p
        ref_m = put("ref_module.ts", patch_module(msrc))
        mut_m = put("mut_module.ts", patch_module(msrc).replace(
            "series.sma_additive_aua?.[i] ?? null", "series.sma_additive_aua?.[i] ?? 0"))
        ref_p = put("ref_page.tsx", patch_page(psrc))
        mut_p = put("mut_page.tsx", patch_page(psrc).replace(
            "globalEnterpriseByPeriod.get(aggregateItem.period)?.smaAdditiveAua ?? null",
            "(globalEnterpriseByPeriod.get(aggregateItem.period)?.smaAdditiveAua ?? 0) + "
            "(globalEnterpriseByPeriod.get(aggregateItem.period)?.taxAdditiveAua ?? 0)", 1))
        cases = [
            ("reader base", lambda: run_reader(module), "base"),
            ("reader reference", lambda: run_reader(ref_m), "all"),
            ("reader mutant (null coalesced to 0)", lambda: run_reader(mut_m), "notall"),
            ("page base", lambda: run_page(page, pr), "base"),
            ("page reference", lambda: run_page(ref_p, pr), "all"),
            ("page mutant (client sum of the two fields)", lambda: run_page(mut_p, pr), "notall"),
        ]
        for label, fn, want in cases:
            arms = fn()
            k = sum(1 for a in arms if a[1])
            n = len(arms)
            print("%-44s %d of %d" % (label, k, n))
            if want == "all" and k != n:
                bad.append(label)
            if want == "notall" and k == n:
                bad.append(label)
            if want == "base" and k == n:
                bad.append(label)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    print("SELFTEST: %s" % ("ok" if not bad else "FAILED " + ", ".join(bad)))
    return 0 if not bad else 1


def main():
    sub = sys.argv[1] if len(sys.argv) > 1 else ""
    fn = {"reader": cmd_reader, "page": cmd_page, "selftest": cmd_selftest}.get(sub)
    if fn is None:
        print("usage: r4_cn_d_3.py reader|page|selftest")
        return 2
    return fn()


if __name__ == "__main__":
    sys.exit(main())
