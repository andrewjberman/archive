"""AMGT_RESAPP round 47, AMGT-vv-1 AC1 -- THE RULE'S VALUE IS A "HISTORICAL-MULTIPLE REFERENCE" WHOSE FORMULA NAMES EACH INPUT AS
ITS BASIS OBJECT DOES; THE VALUES DO NOT MOVE.

CTO round-46 analysis ruling 1 (@0e405cc330) + the anchor ruling (org/tier1_exec/1.0.0_SA_CTO/deliverables/
CTO_RULING_RESAPP_BASE_CASE_ANCHOR_20260929.md, ruling 2). Over three pinned STORED model blocks (round46/checks/fixtures/blocks)
plus one block with no `cases` key, `scoped_amgt._model_cases(block)` must answer per name:
(1) base.formula == "Bloomberg consensus EPS (FY1, BEST_EPS) x adjusted trailing-median P/E (PX_LAST / IS_COMP_EPS_ADJUSTED)";
(2) base.label == "Historical-multiple reference" (SERVED and ABSENT alike);
(3) base.value == the value served before this cell (pinned below), exactly;
(4) upside/downside the ruled ABSENT object, with no label;
(5) render_pack._model_case_line("Base", base, CRNCY) begins "Historical-multiple reference: SERVED -- " and never "Base case".
usage: python <this>   (from the repo root)"""
import glob
import json
import os
import sys

sys.path.insert(0, os.getcwd())
from lib.research.api import scoped_amgt as sa  # noqa: E402

FX = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round46/checks/fixtures/blocks"
WANT = "Bloomberg consensus EPS (FY1, BEST_EPS) x adjusted trailing-median P/E (PX_LAST / IS_COMP_EPS_ADJUSTED)"
RULED = {"status": "ABSENT", "reason": "methodology to be discussed with Andrew"}
LABEL = "Historical-multiple reference"
PINNED = {"AMD_US_Equity": 415.64057358490567, "GOOGL_US_Equity": 511.6099296044653, "RKT_LN_Equity": 5941.776539489737}


def main():
    from lib.research.print import render_pack
    ok = 0
    paths = sorted(glob.glob(os.path.join(FX, "*.model_block.json")))
    for p in paths:
        key = os.path.basename(p).split(".")[0]
        block = json.load(open(p, encoding="utf-8"))
        out = sa._model_cases(block)
        base, bad = out.get("base") or {}, []
        if base.get("formula") != WANT:
            bad.append("formula %r" % base.get("formula"))
        if base.get("label") != LABEL:
            bad.append("label %r" % base.get("label"))
        if base.get("value") != PINNED[key]:
            bad.append("value moved %r -> %r" % (PINNED[key], base.get("value")))
        if out.get("upside") != RULED or out.get("downside") != RULED:
            bad.append("upside/downside moved")
        crncy = next((f.get("value") for f in block.get("figures") or []
                      if f.get("scope") == "header" and f.get("mnemonic") == "CRNCY"), None)
        line = render_pack._model_case_line("Base", base, crncy)
        if not line.startswith(LABEL + ": SERVED -- ") or "Base case" in line:
            bad.append("export line %r" % line[:70])
        print("%s: %s" % (key, "OK" if not bad else "; ".join(bad)))
        ok += not bad
    absent = sa._model_cases({"figures": []}).get("base") or {}
    a_ok = absent.get("status") == "ABSENT" and absent.get("label") == LABEL
    print("no-cases block: base %s label %r -> %s" % (absent.get("status"), absent.get("label"), "OK" if a_ok else "BAD"))
    n = len(paths) + 1
    ok += a_ok
    print("THE RULE'S VALUE IS A LABELLED REFERENCE, FORMULA BASIS-TRUE, VALUES UNMOVED: %d of %d" % (ok, n))
    return 0 if paths and ok == n else 1


if __name__ == "__main__":
    sys.exit(main())
