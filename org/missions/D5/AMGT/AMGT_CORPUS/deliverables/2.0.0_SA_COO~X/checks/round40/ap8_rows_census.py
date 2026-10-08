"""AMGT_CORPUS round 40, CRPS-ap-8 FWD-20 (ruling 2) -- the census of shown / refused / absent / unmapped over the Model sheet's
rows for every covered name with a block, against a portal tree's OWN row specs.

Read-only and offline: it reads the row specs from `<portal>/src/pages/SecurityAnalysis/modelSheet.ts` (the three lists the
sheet is built from: FINANCIAL_SUMMARY_ROWS, MARGIN_HISTORY_ROWS, V3_LINE_ROWS) and the capture `ap8_rows_capture.json`
(ap8_rows_capture.py: per name, the fiscal-year mnemonics the /thesis payload carries a value for, and those whose figures the
served check face REFUSES by the page's own join).

  python ap8_rows_census.py <portal root>

Per row, per name: unmapped (the spec names no field), refused (a figure of that field is refused: the page draws the row's
refusal sentence), shown (at least one fiscal-year value), else absent (the page draws the row's absent reason). A row whose
field is a forecast line (BEST_*) reads absent here: the capture holds fiscal-year figures only, and the page fills its E
columns from the served forecast figures.
"""
import collections
import json
import os
import re
import sys


def specs(portal):
    with open(os.path.join(portal, "src", "pages", "SecurityAnalysis", "modelSheet.ts"), encoding="utf-8") as fh:
        text = fh.read()
    out = []
    for name in ("FINANCIAL_SUMMARY_ROWS", "MARGIN_HISTORY_ROWS", "V3_LINE_ROWS"):
        start = text.index("export const %s" % name)
        body = text[start:text.index("]\n", start)]
        for m in re.finditer(r"\{\s*label:\s*'([^']*)'(?:,\s*mnemonic:\s*(?:'([^']*)'|null))?", body):
            out.append((name, m.group(1), m.group(2)))
    return out


def main(argv):
    portal = argv[0]
    rows = specs(portal)
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "ap8_rows_capture.json"), encoding="utf-8") as fh:
        cap = json.load(fh)
    keys = cap["keys"]
    total = collections.Counter()
    per_row = collections.defaultdict(collections.Counter)
    for key, got in keys.items():
        have = set(got["fiscal_mnemonics"])
        refused = set(got["refused_mnemonics"])
        for group, label, mnem in rows:
            state = ("unmapped" if not mnem else "refused" if mnem in refused else "shown" if mnem in have else "absent")
            total[state] += 1
            per_row[(group, label, mnem)][state] += 1
    print("capture: %s" % cap.get("_note", "")[:160])
    print("rows %d (%s) x names %d = cells %d" % (len(rows), ", ".join("%s %d" % (g, sum(1 for r in rows if r[0] == g))
          for g in ("FINANCIAL_SUMMARY_ROWS", "MARGIN_HISTORY_ROWS", "V3_LINE_ROWS")), len(keys), len(rows) * len(keys)))
    print("CENSUS shown %d refused %d absent %d unmapped %d" % (total["shown"], total["refused"], total["absent"], total["unmapped"]))
    for (group, label, mnem), c in sorted(per_row.items(), key=lambda kv: -kv[1]["absent"]):
        if c["absent"] or c["refused"] or c["unmapped"]:
            print("  %-22s %-44s %-28s shown %3d refused %3d absent %3d unmapped %3d" % (
                group[:22], label[:44], str(mnem)[:28], c["shown"], c["refused"], c["absent"], c["unmapped"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
