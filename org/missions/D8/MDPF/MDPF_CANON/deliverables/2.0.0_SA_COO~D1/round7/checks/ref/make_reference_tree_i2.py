#!/usr/bin/env python3
"""Scratch reference tree for MDPF_CANON CN-i-2 (2.0.0_SA_COO~D1). NEVER committed to a product path.

Builds a portal `src` tree in a temp directory: the six files the CN-i-2 arms read, taken from the candidate branch
(git -C portal show <ref>:src/<path>), with the repair applied (a reference implementation of the order) or with one
planted defect (a mutant). The arms must read the reference green, the unpatched base red where the order demands a
change, and every mutant red on the arm that names it.

  python make_reference_tree_i2.py <dst_src_dir> [mutant]       mutant: colour | dropzero | equalnote | band | nonote | nometa
  env R8_BASE_REF  the base ref (default cand/dell1/mdpf-canon-aua-trend-groups-and-as-of); R8_PORTAL the portal repo path

ASCII only.
"""
import os
import subprocess
import sys

BASE_REF = os.environ.get("R8_BASE_REF", "cand/dell1/mdpf-canon-aua-trend-groups-and-as-of")
FILES = ("lib/trendGrouping.ts", "pages/ModelPortfolios.tsx", "components/CategoryViewTree.tsx", "api/portal-proxy.ts",
         "lib/chartColors.ts", "lib/modelPortfolioColors.ts", "pages/ModelPortfolios.taxsma-color.test.ts")

HELPERS = '''
/**
 * CN-i-2 (PRD v2.18): the Trend tooltip lists a series only where it HAS a value on the hovered date. ABSENT IS NOT ZERO:
 * null, undefined, '' and a non-finite value drop; a measured 0 (number or numeric string) and a negative stay.
 * Returns a new array in the input order and never mutates the input.
 */
export function presentTrendEntries<T extends { value?: unknown }>(entries: ReadonlyArray<T>): T[] {
  return entries.filter((e) => {
    const v = e.value
    if (v === null || v === undefined || v === '') return false
    return Number.isFinite(Number(v))
  })
}

const ISO_DATE = /^\\d{4}-\\d{2}-\\d{2}$/

/**
 * CN-i-2 (PRD v2.18, FWD-9 clause (2)): the sentence the Trend states when it draws dates before the served object's
 * meta.by_model_fold.per_model_detail_begins. Null unless both dates are ISO and the first drawn period is BEFORE the boundary.
 */
export function trendDetailNote(begins: string | null | undefined, firstPeriod: string | null | undefined): string | null {
  if (typeof begins !== 'string' || typeof firstPeriod !== 'string') return null
  if (!ISO_DATE.test(begins) || !ISO_DATE.test(firstPeriod)) return null
  if (!(firstPeriod < begins)) return null
  const shown = new Date(begins + 'T12:00:00').toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
  return `Per-model detail begins ${shown}; earlier model assets are in the Total and are not broken out.`
}
'''


def show(portal, path):
    r = subprocess.run(["git", "-C", portal, "show", "%s:src/%s" % (BASE_REF, path)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("git show failed for %s: %s" % (path, r.stderr.decode("utf-8", "replace")[:200]))
    return r.stdout.decode("utf-8").replace("\r\n", "\n")


def sub(text, old, new, label):
    if text.count(old) != 1:
        raise SystemExit("anchor not unique for %s: %d" % (label, text.count(old)))
    return text.replace(old, new)


def build(dst, mutant=None, portal="portal"):
    for rel in FILES:
        text = show(portal, rel)
        if rel == "components/CategoryViewTree.tsx":
            new = ("  // CN-i-2 (D1-W18-S7): lime500, not orange500 -- orange500 is the locked Ultra-Short Term hex (CIEDE2000 0.0 on the Trend);\n"
                   "  // lime500 is dE00 20.6 or more from every other Trend colour and 19.9 from every other row of this table.\n"
                   "  'Client - Opal Unsupervised': PALETTE.lime500,\n")
            if mutant != "colour":
                text = sub(text, "  'Client - Opal Unsupervised': PALETTE.orange500,\n", new, "L1_COLOR")
        elif rel == "lib/trendGrouping.ts":
            body = HELPERS
            if mutant == "dropzero":
                body = body.replace("return Number.isFinite(Number(v))", "return Boolean(Number(v)) && Number.isFinite(Number(v))")
            if mutant == "equalnote":
                body = body.replace("if (!(firstPeriod < begins)) return null", "if (!(firstPeriod <= begins)) return null")
            text = text.rstrip("\n") + "\n" + body
        elif rel == "api/portal-proxy.ts":
            if mutant != "nometa":
                anchor = "    // MDPF_REVAMP.S5: producer-DECLARED honest-None days"
                new = ("    // CN-i-2 (PRD v2.18): the Global fold's boundary, served in meta.by_model_fold.\n"
                       "    by_model_fold?: { min_firms?: number; per_model_detail_begins?: string; statement?: string }\n")
                if text.count(anchor) == 1:
                    text = sub(text, anchor, new + anchor, "meta")
                else:
                    text = sub(text, "    slice: string\n", "    slice: string\n" + new, "meta-slice")
        elif rel == "pages/ModelPortfolios.tsx":
            text = sub(text, "import { groupCustomModelsSeries, etfStrategiesAua, otherAua, clientChipAt } from '@/lib/trendGrouping'",
                       "import { groupCustomModelsSeries, etfStrategiesAua, otherAua, clientChipAt, presentTrendEntries, trendDetailNote } from '@/lib/trendGrouping'",
                       "import")
            text = sub(text, "    const buckets = payload.filter((entry) => entry.dataKey !== 'interp_total')",
                       "    const buckets = presentTrendEntries(payload.filter((entry) => entry.dataKey !== 'interp_total'))", "tooltip")
            if mutant != "nonote":
                text = sub(text, "          const endDateDisplay = latestTransactionDate.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })\n",
                           "          const endDateDisplay = latestTransactionDate.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })\n"
                           "          const detailNote = isGlobalSI\n"
                           "            ? trendDetailNote(globalMdpfData?.meta?.by_model_fold?.per_model_detail_begins, earliestPeriodStr)\n"
                           "            : null\n", "detailNote")
                text = sub(text, "                  : `Rolling 1-year ${assetLbl.short} growth from ${startDateDisplay} to ${endDateDisplay}.`}\n              </p>\n",
                           "                  : `Rolling 1-year ${assetLbl.short} growth from ${startDateDisplay} to ${endDateDisplay}.`}\n              </p>\n"
                           "              {detailNote && (\n"
                           "                <p data-trend-detail-note=\"true\" className=\"-mt-3 mb-4 text-xs text-white/60\">{detailNote}</p>\n"
                           "              )}\n", "noteJsx")
            if mutant == "band":
                text = sub(text, "  { key: 'non_model',    label: 'Other AUA' },\n",
                           "  { key: 'detail_withheld', label: 'Models (detail withheld)' },\n  { key: 'non_model',    label: 'Other AUA' },\n", "band")
        out = os.path.join(dst, *rel.split("/"))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    return dst


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    build(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None, os.environ.get("R8_PORTAL", "portal"))
    print("built", sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "(reference)")
