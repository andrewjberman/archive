"""AMGT_RESAPP round 48, AMGT-ww-4 AC1 -- THE EXPORT'S WORDS COME FROM ONE SERVED DEFINITION THAT MATCHES THE PAGE'S.

CTO ruling W4-S1 (b) (@06d51bce50): the Model line names and the case formula text come from ONE definition that both the page and
`render_pack` read. RESAPP's half: the definition lives server-side and is SERVED; the export reads it. Graded here:
 (1) `scoped_amgt._model_line_names()` == the page's `LINE_NAMES` (portal/src/pages/SecurityAnalysis/modelSheet.ts), parsed from the
     page source at check time -- so the served words and the page's words are the same map today;
 (2) `scoped_amgt._formula_words(f)` == the page's own `formulaInWords(f)` (ModelTab.tsx), EXTRACTED from the page source at check
     time and run in node, on four served formulas;
 (3) the export names every mapped line in words from the served map: each `render_pack._figures_table` row of a mapped mnemonic
     reads `| <MNEMONIC> | <served name> | <rendered> |` -- the mnemonic stays FIRST because it is FWD-30's join key in
     DSGN_AMGTV1's harness (a row's first cell must be one token), which this project does not write; the case line's words wait on that harness.
usage: python <this>   (from the repo root; needs node)"""
import glob
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.getcwd())
from lib.research.api import scoped_amgt as sa  # noqa: E402
from lib.research.print import render_pack as rp  # noqa: E402

PAGE = "portal/src/pages/SecurityAnalysis"
BLOCKS = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round46/checks/fixtures/blocks"
MNEMONIC = re.compile(r"\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b")
FORMULAS = [
    "Bloomberg consensus EPS (FY1, BEST_EPS) x adjusted trailing-median P/E (PX_LAST / IS_COMP_EPS_ADJUSTED)",
    "adjusted consensus EPS (FY1) x adjusted trailing-median P/E (PX_LAST / IS_COMP_EPS_ADJUSTED)",
    "consensus EPS (FY1) x trailing-median P/E",
    "EPS (BEST_EPS) x P/E (PE_RATIO)",
]


def page_line_names():
    src = open(os.path.join(PAGE, "modelSheet.ts"), encoding="utf-8").read()
    body = re.search(r"export const LINE_NAMES[^{]*\{(.*?)\n\}", src, re.S).group(1)
    return dict(re.findall(r"^\s*([A-Z0-9_]+):\s*'([^']*)'", body, re.M))


def page_formula_words(formulas):
    src = open(os.path.join(PAGE, "tabs/ModelTab.tsx"), encoding="utf-8").read()
    fn = re.search(r"function formulaInWords\(formula: string\): string \{(.*?)\n\}", src, re.S).group(1)
    js = "const f=(formula)=>{%s};console.log(JSON.stringify(%s.map(f)))" % (fn, json.dumps(formulas))
    return json.loads(subprocess.run(["node", "-e", js], capture_output=True, text=True, encoding="utf-8", timeout=60).stdout)


def main():
    bad = []
    for fn in ("_model_line_names", "_formula_words"):
        if not hasattr(sa, fn):
            bad.append("scoped_amgt has no %s" % fn)
    if bad:
        for b in bad:
            print("  BAD", b)
        print("THE EXPORT'S WORDS COME FROM ONE SERVED DEFINITION THAT MATCHES THE PAGE'S: NO")
        return 1
    page = page_line_names()
    served = sa._model_line_names()
    print("line names: page %d, served %d" % (len(page), len(served)))
    if served != page:
        bad.append("(1) served map differs from the page's LINE_NAMES: %r" % sorted(set(page.items()) ^ set(served.items()))[:4])
    want = page_formula_words(FORMULAS)
    got = [sa._formula_words(f) for f in FORMULAS]
    if got != want:
        bad.append("(2) formula words differ: served %r page %r" % (got, want))
    for p in sorted(glob.glob(os.path.join(BLOCKS, "*.model_block.json"))):
        block = json.load(open(p, encoding="utf-8"))
        figs = block.get("figures") or []
        text = "\n".join(rp._figures_table(figs))
        mapped = sorted({f.get("mnemonic") for f in figs if f.get("mnemonic") in page})
        wrong = [m for m in mapped if not re.search(r"^\|\s*%s\s*\|\s*%s\s*\|" % (re.escape(m), re.escape(page[m])), text, re.M)]
        print("%s: mapped lines %d, named in words %d" % (os.path.basename(p), len(mapped), len(mapped) - len(wrong)))
        if not mapped or wrong:
            bad.append("(3) %s: rows not named by the served map: %s" % (os.path.basename(p), wrong[:5]))
    for b in bad:
        print("  BAD", b)
    ok = not bad
    print("THE EXPORT'S WORDS COME FROM ONE SERVED DEFINITION THAT MATCHES THE PAGE'S: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
