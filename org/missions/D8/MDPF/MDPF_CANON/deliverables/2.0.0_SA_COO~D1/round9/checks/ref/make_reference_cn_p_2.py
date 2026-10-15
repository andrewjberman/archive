#!/usr/bin/env python3
"""Scratch reference tree for MDPF_CANON CN-p-2 (2.0.0_SA_COO~D1). NEVER committed to a product path.

Builds a portal `src` tree in a temp directory from the base commit (git -C portal show <base>:src/<path>) for the files the CN-p-2 arms read:
  ref=False  the unpatched base
  ref=True   the base plus a REFERENCE implementation of the order (the pure functions appended to trendGrouping.ts, the four type fields,
             and a text-level sketch of the page wiring: it turns the arms green, it is NOT compile-checked and is not the worker's page)
  mutant     the reference with ONE planted defect, which must turn the arm(s) named in MUTANTS red

  python make_reference_cn_p_2.py <dst_src_dir> [mutant]
  env R9_BASE the base commit (default the TO's); R9_PORTAL the portal repo path

ASCII only. Output files are LF.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("R9_BASE", "f8c7d310dfef6ef5eb68a25f2244ae3245c7a2bf")
FILES = ("lib/trendGrouping.ts", "pages/ModelPortfolios.tsx", "components/CategoryViewTree.tsx", "api/portal-proxy.ts", "api/endpoints/aum.ts",
         "lib/otherModelsAsOf.ts")

# mutant -> arms that must read red
MUTANTS = (
    ("roundfree", ("O5",)),
    ("recompose", ("O4",)),
    ("zeroabsent", ("O3", "V10")),
    ("modetruthy", ("V3",)),
    ("stitchleak", ("V4",)),
    ("nosuppress", ("V2",)),
    ("rollall", ("V6",)),
    ("nocarried", ("V5",)),
    ("footalways", ("V7",)),
    ("estimateloses", ("V8",)),
    ("poolblind", ("O6",)),
    ("mutates", ("V9",)),
    ("compvisible", ("V7",)),
    ("retiredfield", ("O6",)),
    ("w_ungated", ("W2",)),
    ("w_isinternal", ("W1",)),
    ("w_chipcall", ("W3",)),
    ("w_notyped", ("W6",)),
)


def show(portal, rel):
    out = subprocess.check_output(["git", "-C", portal, "show", "%s:src/%s" % (BASE, rel)])
    return out.decode("utf-8").replace("\r\n", "\n")


def helpers(mutant):
    with open(os.path.join(HERE, "cn_p_2_helpers.ts"), encoding="utf-8") as fh:
        t = fh.read()

    def swap(old, new):
        nonlocal t
        assert old in t, "mutant anchor missing: " + old[:50]
        t = t.replace(old, new, 1)
    if mutant == "roundfree":
        swap("clientSupervised: v['Client Supervised'],", "clientSupervised: v['Client Supervised'] === null ? null : toCents(v['Client Supervised'] as number),")
    elif mutant == "recompose":
        swap("total: v.total,", "total: sumPresent([...Object.values(models), v[CUSTOM_MODELS_LABEL], v['Client Supervised'], v['ETF Strategies'], v['ALT Strategies']]),")
    elif mutant == "zeroabsent":
        swap("const finiteOrNull = (v: unknown): Num => (typeof v === 'number' && Number.isFinite(v) ? v : null)",
             "const finiteOrNull = (v: unknown): Num => (typeof v === 'number' && Number.isFinite(v) ? v : 0)")
    elif mutant == "modetruthy":
        swap("(internal === true ? 'variant1' : 'variant2')", "(internal ? 'variant1' : 'variant2')")
    elif mutant == "stitchleak":
        swap("const stitchOn = mode === 'variant1' && stitch !== null && stitch !== undefined", "const stitchOn = stitch !== null && stitch !== undefined")
    elif mutant == "nosuppress":
        swap("else if (mode === 'variant2' && diff !== null) suppressed = true", "else if (mode === 'variant2' && diff !== null) custom = diff")
    elif mutant == "rollall":
        swap("v[key] === null && carriedSet.has(period) && lastKnown", "v[key] === null && lastKnown")
    elif mutant == "nocarried":
        swap("const carriedSet = new Set(served.carriedDates ?? [])", "const carriedSet = new Set<string>()")
    elif mutant == "footalways":
        swap("return rows.some((r) => r.customSuppressed) ? SUPPRESSED_FOOTNOTE : null", "return SUPPRESSED_FOOTNOTE")
    elif mutant == "estimateloses":
        swap("if (existing === 'interpolated_estimate') return existing", "if (existing === 'interpolated_estimate' && carriedKeys.length === 0) return existing")
    elif mutant == "poolblind":
        swap("if (readAt(served.otherModels, i) !== null) custom = diff\n      else if (stitchOn)", "if (stitchOn) custom = infCustom.get(period) ?? null\n      else if (readAt(served.otherModels, i) !== null) custom = diff\n      else if (stitchOn)")
    elif mutant == "mutates":
        swap("const carriedSet = new Set(served.carriedDates ?? [])", "const carriedSet = new Set(served.carriedDates ?? [])\n  ;(served as any).seen = true")
    elif mutant == "compvisible":
        swap("return mode === 'variant1'\n    ?", "return mode !== 'zzz'\n    ?")
    elif mutant == "retiredfield":
        swap("      customSuppressed: suppressed,", "      customSuppressed: suppressed,\n      clientUnsupervised: null,")
    return t


PROXY_FIELDS = """    // CN-p-2 (PRD v2.19 to v2.21): the Global Trend groups, served by the producer cell CN-p-1, aligned to dates[].
    client_supervised_aua?: Array<number | null>
    etf_strategies_aua?: Array<number | null>
    alt_strategies_aua?: Array<number | null>
    carried_dates?: string[]
"""


def patch_proxy(t, mutant):
    anchor = "  partner_custody_total: Array<number | null>\n  by_model: MdpfPartnerSeries['by_model']\n"
    assert anchor in t
    fields = PROXY_FIELDS.replace("    //", "  //").replace("\n    ", "\n  ")
    if mutant == "w_notyped":
        fields = ""
    return t.replace(anchor, anchor + fields, 1)


def patch_page(t, mutant):
    imp = "import { groupCustomModelsSeries, etfStrategiesAua, otherAua, clientChipAt, presentTrendEntries, trendDetailNote } from '@/lib/trendGrouping'"
    assert imp in t
    t = t.replace(imp, "import { groupCustomModelsSeries, presentTrendEntries, buildGlobalTrendRows, trendModeFor, globalTrendFootnote, trendDetailNoteFor, "
                       "trendPointClass, carriedTooltipLabel, CARRIED_LEGEND_LABEL, compositionFootnote } from '@/lib/trendGrouping'")
    # the as-of Client chips, Other AUA memo and the old composition go
    t = re.sub(r"  const hasGlobalEnterprise = useMemo\(\n.*?\n  \)\n", "", t, count=1, flags=re.S)
    t = re.sub(r"  const categoryBlock = .*?const hasClientChips = [^\n]*\n", "", t, count=1, flags=re.S)
    t = re.sub(r"        \.\.\.\(effectiveFirmId === 'global' && hasClientChips\n.*?\n          : \[\]\),\n", "", t, count=1, flags=re.S)
    start = t.index("  const globalTrendBands = (period: string) => {")
    end = t.index("  const { data: scopeAumMetrics")
    gate = "internal" if mutant != "w_ungated" else "true"
    mode_arg = "internal" if mutant != "w_isinternal" else "isInternal()"
    chip = "  const _chip = clientChipAt(null as never, null, null)\n" if mutant == "w_chipcall" else ""
    wiring = f"""  const {{ data: firm49Data }} = useQuery<MdpfPerFirmTimeSeries | null>({{
    queryKey: ['mdpf-per-firm-timeseries', '49financial'],
    queryFn: () => getMdpfAggregateAUATimeSeriesByFirm('49financial'),
    enabled: effectiveFirmId === 'global' && {gate},
    staleTime: 5 * 60 * 1000,
  }})
  const {{ data: inflectionData }} = useQuery<MdpfPerFirmTimeSeries | null>({{
    queryKey: ['mdpf-per-firm-timeseries', 'inflection'],
    queryFn: () => getMdpfAggregateAUATimeSeriesByFirm('inflection'),
    enabled: effectiveFirmId === 'global' && {gate},
    staleTime: 5 * 60 * 1000,
  }})
  const trendMode = trendModeFor({mode_arg})
{chip}  const globalTrendRows = useMemo(() => (globalMdpfData ? buildGlobalTrendRows(null as never, null, trendMode, null) : []), [globalMdpfData, firm49Data, inflectionData, trendMode])
  const globalTrendFootnoteText = globalTrendFootnote(globalTrendRows, trendMode)
  const compositionText = compositionFootnote(trendMode)
  const _carriedProbe = [carriedTooltipLabel('x', null), trendPointClass(undefined, []), CARRIED_LEGEND_LABEL]
  const globalTrendBands = (period: string) => {{
    const row = globalTrendRows.find((r) => r.period === period)
    return {{ total: row?.total ?? null, nonModel: null, sma: row?.etfStrategies ?? null, clientSup: row?.clientSupervised ?? null, clientUnsup: null, alt: row?.altStrategies ?? null }}
  }}

"""
    t = t[:start] + wiring + t[end:]
    t = t.replace("trendDetailNote(globalMdpfData", "trendDetailNoteFor(trendMode, globalMdpfData")
    t = t.replace("{detailNote && (", '{globalTrendFootnoteText && <p data-trend-footnote="true" className="mb-4 text-xs text-white/60">{globalTrendFootnoteText}</p>}\n              {compositionText && <p data-trend-composition="true" className="mb-4 text-xs text-white/60">{compositionText}</p>}\n              {detailNote && (', 1)
    t = re.sub(r"\bhasGlobalEnterprise\b", "false", t)
    t = re.sub(r"\bhasClientChips\b", "false", t)
    return t


def build(dst, mutant=None, portal=None, ref=True):
    portal = portal or os.environ.get("R9_PORTAL") or os.path.join(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip(), "portal")
    for rel in FILES:
        text = show(portal, rel)
        if ref:
            if rel == "lib/trendGrouping.ts":
                text = text.rstrip("\n") + "\n" + helpers(mutant)
            elif rel == "api/portal-proxy.ts":
                text = patch_proxy(text, mutant)
            elif rel == "pages/ModelPortfolios.tsx":
                text = patch_page(text, mutant)
        out = os.path.join(dst, *rel.split("/"))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    build(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None, None, True)
