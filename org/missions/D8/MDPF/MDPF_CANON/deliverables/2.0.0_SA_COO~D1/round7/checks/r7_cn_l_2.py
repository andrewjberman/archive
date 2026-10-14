#!/usr/bin/env python3
"""MDPF_CANON round 7, cell CN-l-2 -- the portal half of the Other Models dated carry (rows D1-W16-S2 / D1-W16-S4).

Issuer's check (2.0.0_SA_COO~D1). Read-only for every worker: never edit this file.

  python r7_cn_l_2.py helper     the pure helper portal/src/lib/otherModelsAsOf.ts: carriedAsOf / asOfLabel (7 arms)
  python r7_cn_l_2.py page       the wiring: type field, import, the card model carries the date, the centre readout draws it (8 arms)
  python r7_cn_l_2.py selftest   proves the arms fail at base and pass on a reference patch (alone and on top of the CN-i-1 reference),
                                 four mutants RED; issuer only

The served half is CN-l-1: the Global aum-metrics `Other Models` by_model row carries "as_of": "YYYY-MM-DD" ONLY when its value is
carried from an earlier pooled date; an absent row stays absent (no card, nothing to draw). The page draws "as of <date>" under the
card value exactly when that date is present and differs from the page's own as-of date, and draws nothing special otherwise.

Anchors are matched by TEXT, never by line number, so the checks hold before and after CN-i-1 (which owns the rest of the page).

Targets (repo root = `git rev-parse --show-toplevel` of the working directory):
  portal/src/lib/otherModelsAsOf.ts   portal/src/pages/ModelPortfolios.tsx   portal/src/api/endpoints/aum.ts
Overrides for the selftest only: R7L2_MODULE, R7L2_PAGE, R7L2_AUM (absolute file paths).

Output: `ROUND 7 <NAME>: k of n arms`, exit 0 only when k == n. ASCII only.
"""
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
N_HELPER = 7
N_PAGE = 8

BUN_TS = r"""
import { pathToFileURL } from 'node:url'
const mod: any = await import(pathToFileURL(process.env.R7L2_MODULE as string).href)
const carried = mod.carriedAsOf as (row: any, page: any) => string | null
const label = mod.asOfLabel as (d: any) => string
const out: string[] = []
const arm = (id: string, ok: boolean, why: string) => out.push(`ARM ${id} ${ok ? 'PASS' : 'FAIL'} ${why}`)

const PAGE = '2026-10-13'
const ROW = '2026-10-09'

// H1 no stamp on the row -> nothing to draw (the pool was present: the value is current)
const h1 = [undefined, null, ''].map((v) => carried(v as any, PAGE))
arm('H1', h1.every((v) => v === null), `absent stamp ${JSON.stringify(h1)} -> null`)

// H2 a stamp equal to the page's own as-of -> nothing special
arm('H2', carried(PAGE, PAGE) === null, 'stamp equal to the page as-of -> null')

// H3 a stamp that differs -> that date, verbatim, in either direction
const a = carried(ROW, PAGE)
const b = carried('2026-10-20', PAGE)
arm('H3', a === ROW && b === '2026-10-20', `earlier ${a}, later ${b}`)

// H4 a malformed stamp is never drawn
const bad = ['10/09/2026', '2026-10-9', 'yesterday', '2026-10-09T00:00:00Z', 20261009, {}, [] , true]
const h4 = bad.map((v) => carried(v as any, PAGE))
arm('H4', h4.every((v) => v === null), `malformed -> ${JSON.stringify(h4)}`)

// H5 the page date unknown: the carried date is still stated (a stamp exists only on a carried row)
const h5 = [carried(ROW, null), carried(ROW, undefined), carried(ROW, '')]
arm('H5', h5.every((v) => v === ROW), `page date unknown -> ${JSON.stringify(h5)}`)

// H6 the label text lives here, once
const l1 = label(ROW)
const l2 = [label(null), label(undefined), label(''), label('bad')]
arm('H6', l1 === 'as of 2026-10-09' && l2.every((v) => v === ''), `label ${JSON.stringify(l1)}, absent/malformed ${JSON.stringify(l2)}`)

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
    module = os.environ.get("R7L2_MODULE") or os.path.join(pr, "lib", "otherModelsAsOf.ts")
    page = os.environ.get("R7L2_PAGE") or os.path.join(pr, "pages", "ModelPortfolios.tsx")
    aum = os.environ.get("R7L2_AUM") or os.path.join(pr, "api", "endpoints", "aum.ts")
    return module, page, aum


def report(name, arms):
    for a in arms:
        print("  %s %s %s" % (a[0], "PASS" if a[1] else "FAIL", a[2]))
    k = sum(1 for a in arms if a[1])
    print("ROUND 7 %s: %d of %d arms" % (name, k, len(arms)))
    return k, len(arms)


def raw(path):
    with open(path, "rb") as f:
        return f.read()


def read(path):
    return raw(path).decode("utf-8").replace("\r\n", "\n")


def run_helper(module):
    if not os.path.isfile(module):
        return [("H0", False, "module not found: " + module)]
    d = tempfile.mkdtemp(prefix="r7cnl2_")
    try:
        ex = os.path.join(d, "exercise.ts")
        with open(ex, "w", newline="\n", encoding="utf-8") as f:
            f.write(BUN_TS)
        env = dict(os.environ)
        env["R7L2_MODULE"] = module
        try:
            r = subprocess.run(["bun", ex], capture_output=True, text=True, timeout=100, env=env, cwd=d)
        except subprocess.TimeoutExpired:
            return [("H0", False, "bun exercise timed out")]
        arms = []
        for line in r.stdout.splitlines():
            m = re.match(r"ARM (H\d) (PASS|FAIL) (.*)", line)
            if m:
                arms.append((m.group(1), m.group(2) == "PASS", m.group(3)))
        if r.returncode != 0 or len(arms) != N_HELPER - 1:
            tail = (r.stderr or r.stdout).strip().splitlines()[-1:] or [""]
            return [("H0", False, "exercise rc=%d arms=%d %s" % (r.returncode, len(arms), tail[0][:160]))]
        text = read(module)
        imports = [ln for ln in text.split("\n") if re.match(r"\s*import\s", ln)]
        ascii_ok = all(ord(c) < 128 for c in text)
        exported = all(re.search(r"export (function|const) %s\b" % n, text) for n in ("carriedAsOf", "asOfLabel"))
        arms.append(("H7", not imports and ascii_ok and exported,
                     "imports %d (must be 0), ascii %s, exports carriedAsOf/asOfLabel %s" % (len(imports), ascii_ok, exported)))
        return arms
    finally:
        shutil.rmtree(d, ignore_errors=True)


def block(text, start_pat, end_pat):
    m = re.search(start_pat, text)
    if not m:
        return None
    e = re.search(end_pat, text[m.end():])
    return text[m.start(): m.end() + (e.start() if e else len(text))]


def run_page(page, aum):
    if not os.path.isfile(page) or not os.path.isfile(aum):
        return [("P0", False, "page or aum.ts not found")]
    text, au = read(page), read(aum)
    arms = []

    # P1 the card model carries the date
    body = block(text, r"interface ModelPortfolio \{", r"\n\}")
    arms.append(("P1", body is not None and re.search(r"carriedAsOf\?:\s*string \| null", body) is not None,
                 "interface ModelPortfolio declares carriedAsOf?: string | null"))

    # P2 the import of both helpers from the one module
    imps = re.findall(r"import \{([^}]*)\} from '[^']*otherModelsAsOf'", text)
    names = set(re.split(r"\s*,\s*", " ".join(imps).strip())) if imps else set()
    arms.append(("P2", {"carriedAsOf", "asOfLabel"} <= names, "imports from otherModelsAsOf: %s" % sorted(names)))

    # P3 the aum-metrics mapping stamps each card from the row's as_of against the page's dataAsOf, and re-runs when dataAsOf moves
    memo = re.search(r"const \{ modelPortfolios \} = useMemo\(\(\) => \{(.*?)\n  \}, \[([^\]]*)\]\)", text, re.S)
    ok3 = False
    why3 = "memo not found"
    if memo:
        mb, deps = memo.group(1), memo.group(2)
        call = re.search(r"carriedAsOf:\s*carriedAsOf\(([^)]*)\)", mb)
        ok3 = bool(call and "as_of" in call.group(1) and "dataAsOf" in call.group(1) and "dataAsOf" in deps)
        why3 = "call args %r, deps [%s]" % (call.group(1) if call else None, deps.strip())
    arms.append(("P3", ok3, "modelPortfolios memo: " + why3))

    # P4 the centre readout draws the label under the value, guarded by the date
    sel = block(text, r"\{selectedPortfolio \? \(", r"\) : \(")
    ok4 = False
    if sel:
        i_val = sel.find("formatCurrency(selectedPortfolio.currentAUM)")
        i_lab = sel.find("asOfLabel(selectedPortfolio.carriedAsOf)")
        guard = re.search(r"selectedPortfolio\.carriedAsOf\s*(&&|\?)", sel)
        ok4 = i_val >= 0 and i_lab > i_val and guard is not None and guard.start() < i_lab and i_lab - guard.start() < 300
    arms.append(("P4", ok4, "centre readout: value then asOfLabel(selectedPortfolio.carriedAsOf), guarded by the date"))

    # P5 the served type carries the field
    ib = block(au, r"export interface MdpfFirmModelMetrics \{", r"\n\}")
    arms.append(("P5", ib is not None and re.search(r"\bas_of\?:\s*string \| null", ib) is not None,
                 "MdpfFirmModelMetrics declares as_of?: string | null"))

    # P6 CONTROL: nothing else the edit stands on moved
    one_site = text.count("formatCurrency(selectedPortfolio.currentAUM)") == 1
    roll = "rollBlendsIntoArchetypeModels(models)" in text
    iface = ib is not None and "model_name: string" in ib and "q3: MdpfNullablePeriodMetrics" in ib
    arms.append(("P6", one_site and roll and iface,
                 "one centre value site %s, blend roll kept %s, MdpfFirmModelMetrics fields kept %s" % (one_site, roll, iface)))

    # P7 CONTROL: the label text lives in the helper only (no 'as of' string literal on a line that names the helpers)
    bad = [ln.strip()[:80] for ln in text.split("\n")
           if re.search(r"carriedAsOf|asOfLabel", ln) and not ln.lstrip().startswith("import")
           and re.search(r"""['"`][^'"`\n]*\bas of\b[^'"`\n]*['"`]""", ln)]
    arms.append(("P7", not bad, "as-of text literals beside the helpers: %d" % len(bad)))

    # P8 CONTROL: line endings stay uniform (both files are CRLF at HEAD)
    def mixed(b):
        crlf = b.count(b"\r\n")
        bare = b.count(b"\n") - crlf
        return crlf > 0 and bare > 0
    mp, ma = mixed(raw(page)), mixed(raw(aum))
    arms.append(("P8", not mp and not ma, "mixed line endings: page %s, aum.ts %s" % (mp, ma)))
    return arms


# ----------------------------------------------------------------------------------------------- selftest reference patch

REF_HELPER = """// MDPF_CANON round 7, CN-l-2 (FWD-3 follow-on): the Other Models card carries its date or says nothing.
// Pure: no import. The served row carries as_of only when its value is carried from an earlier pooled date.
const ISO_DATE = /^\\d{4}-\\d{2}-\\d{2}$/

export function carriedAsOf(rowAsOf: unknown, pageAsOf: string | null | undefined): string | null {
  if (typeof rowAsOf !== 'string' || !ISO_DATE.test(rowAsOf)) return null
  return rowAsOf === pageAsOf ? null : rowAsOf
}

export function asOfLabel(d: unknown): string {
  return typeof d === 'string' && ISO_DATE.test(d) ? `as of ${d}` : ''
}
"""


def patch_page(src):
    s = src.replace("import { useAuth } from '@/hooks/useAuth'",
                    "import { useAuth } from '@/hooks/useAuth'\nimport { carriedAsOf, asOfLabel } from '@/lib/otherModelsAsOf'", 1)
    s = s.replace("  accountCount: number\n  metrics: MetricsPeriod[]\n}",
                  "  accountCount: number\n  carriedAsOf?: string | null\n  metrics: MetricsPeriod[]\n}", 1)
    s = s.replace("        accountCount: m.account_count ?? 0,\n        metrics: allNull",
                  "        accountCount: m.account_count ?? 0,\n        carriedAsOf: carriedAsOf(m.as_of, dataAsOf),\n        metrics: allNull", 1)
    s = s.replace("    return { modelPortfolios: rollBlendsIntoArchetypeModels(models) }\n  }, [scopeAumMetrics])",
                  "    return { modelPortfolios: rollBlendsIntoArchetypeModels(models) }\n  }, [scopeAumMetrics, dataAsOf])", 1)
    s = s.replace("                                    {formatCurrency(selectedPortfolio.currentAUM)}\n"
                  "                                  </span>\n",
                  "                                    {formatCurrency(selectedPortfolio.currentAUM)}\n"
                  "                                  </span>\n"
                  "                                  {selectedPortfolio.carriedAsOf && (\n"
                  "                                    <span style={{ fontSize: 11, color: 'rgba(255,255,255,0.6)' }}>\n"
                  "                                      {asOfLabel(selectedPortfolio.carriedAsOf)}\n"
                  "                                    </span>\n"
                  "                                  )}\n", 1)
    return s


def patch_aum(src):
    return src.replace("  account_count?: number | null\n  series_start?: string | null\n  q0: MdpfNullablePeriodMetrics",
                       "  account_count?: number | null\n  /** CN-l-1: set only when the value is carried from an earlier pooled date. */\n"
                       "  as_of?: string | null\n  series_start?: string | null\n  q0: MdpfNullablePeriodMetrics", 1)


def write_crlf(path, text):
    with open(path, "wb") as f:
        f.write(text.replace("\n", "\r\n").encode("utf-8"))


def load_cn_i_1():
    p = os.path.join(HERE, "r7_cn_i_1.py")
    spec = importlib.util.spec_from_file_location("r7_cn_i_1_for_l2", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cmd_selftest():
    mod, page, aum = targets()
    d = tempfile.mkdtemp(prefix="r7cnl2_st_")
    ok_all = True

    def expect(label, arms, want_k):
        nonlocal ok_all
        k = sum(1 for a in arms if a[1])
        good = (k == want_k)
        ok_all = ok_all and good
        print("  SELFTEST %s %s: %d (want %d) [%s]" % ("OK" if good else "FAIL", label, k, want_k,
                                                       ",".join(a[0] for a in arms if not a[1]) or "-"))
        return arms

    try:
        base_page, base_aum = read(page), read(aum)
        if "carriedAsOf" in base_page:
            print("SELFTEST: the page already carries the edit; the base arms cannot be exercised here")
            return 2
        hm = os.path.join(d, "otherModelsAsOf.ts")
        with open(hm, "w", newline="\n", encoding="utf-8") as f:
            f.write(REF_HELPER)

        # base
        expect("helper at base (module absent)", run_helper(os.path.join(d, "absent.ts")), 0)
        expect("page at base (P6, P7, P8 are controls)", run_page(page, aum), 3)

        # reference
        expect("helper reference", run_helper(hm), N_HELPER)
        pp, pa = os.path.join(d, "page.tsx"), os.path.join(d, "aum.ts")
        write_crlf(pp, patch_page(base_page))
        write_crlf(pa, patch_aum(base_aum))
        ref = run_page(pp, pa)
        expect("page reference", ref, N_PAGE)

        # on top of CN-i-1's reference patch: the anchors of the two cells do not overlap
        try:
            i1 = load_cn_i_1()
            write_crlf(pp, patch_page(i1.patch_page(base_page)))
            expect("page reference on top of the CN-i-1 reference", run_page(pp, pa), N_PAGE)
        except Exception as exc:  # noqa: BLE001 -- a failed import must read as a failed arm
            ok_all = False
            print("  SELFTEST FAIL chained CN-i-1 reference: %s: %s" % (type(exc).__name__, str(exc)[:120]))

        # mutants
        good_page = patch_page(base_page)
        muts = {
            "label_in_page (the text built in the page)": (
                good_page.replace("{asOfLabel(selectedPortfolio.carriedAsOf)}", "{`as of ${selectedPortfolio.carriedAsOf}`}", 1), "P7", None),
            "no_dep (dataAsOf missing from the memo deps)": (good_page.replace("[scopeAumMetrics, dataAsOf]", "[scopeAumMetrics]", 1), "P3", None),
            "unguarded (the label drawn on every card)": (
                good_page.replace("{selectedPortfolio.carriedAsOf && (", "{(", 1), "P4", None),
            "lf_line (one bare LF in a CRLF file)": (good_page, "P8", "lf"),
        }
        for name, (txt, want_red, mode) in muts.items():
            mp = os.path.join(d, "mut.tsx")
            write_crlf(mp, txt)
            if mode == "lf":
                b = raw(mp)
                with open(mp, "wb") as f:
                    f.write(b.replace(b"\r\n", b"\n", 1))
            arms = run_page(mp, pa)
            red = [a[0] for a in arms if not a[1]]
            good = (want_red in red) and set(red) <= {want_red, "P4"}
            ok_all = ok_all and good
            print("  SELFTEST %s mutant %s: red %s (want %s among them; P4 may follow when the call is replaced)"
                  % ("OK" if good else "FAIL", name, red, want_red))

        # a helper mutant: a malformed stamp drawn
        mh = os.path.join(d, "mut_helper.ts")
        with open(mh, "w", newline="\n", encoding="utf-8") as f:
            f.write(REF_HELPER.replace("typeof rowAsOf !== 'string' || !ISO_DATE.test(rowAsOf)", "rowAsOf == null || rowAsOf === ''"))
        hr = run_helper(mh)
        red = [a[0] for a in hr if not a[1]]
        good = ("H4" in red)
        ok_all = ok_all and good
        print("  SELFTEST %s helper mutant (malformed stamp drawn): red %s (want H4 among them)" % ("OK" if good else "FAIL", red))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    print("SELFTEST: %s" % ("OK" if ok_all else "FAIL"))
    return 0 if ok_all else 1


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("helper", "page", "selftest"):
        print("usage: r7_cn_l_2.py helper|page|selftest")
        return 2
    sub = sys.argv[1]
    if sub == "selftest":
        return cmd_selftest()
    module, page, aum = targets()
    if sub == "helper":
        k, n = report("CN-L-2 HELPER", run_helper(module))
        return 0 if k == N_HELPER else 1
    k, n = report("CN-L-2 PAGE", run_page(page, aum))
    return 0 if k == N_PAGE else 1


if __name__ == "__main__":
    sys.exit(main())
