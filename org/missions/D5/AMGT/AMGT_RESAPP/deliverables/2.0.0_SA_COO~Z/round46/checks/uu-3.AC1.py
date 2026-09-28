"""AMGT_RESAPP round 46, AMGT-uu-3 AC1 -- THE BASE CASE ON THE ADJUSTED BASIS, EACH INPUT CARRYING ITS BASIS, THE VALUE PRINTED AS A VALUE.

Over three pinned STORED model blocks (round46/checks/fixtures/blocks, read 2026-09-28 ~21:4xZ; their landed base case is the
pre-ruling GAAP-P/E construction), the served adapter `scoped_amgt._model_cases(block)` must answer, per name:
  (1) base SERVED, and base.inputs.consensus_eps.basis == the block's own BEST_EPS FY1 forecast figure's `basis` object;
  (2) base.inputs.trailing_median_pe is ADJUSTED: its `window` is exactly the closed fiscal years (<= history_window
      .latest_closed_fiscal_year, and < consensus_eps.fiscal_year) carrying BOTH a PX_LAST and an IS_COMP_EPS_ADJUSTED
      fiscal_year_line_item with EPS > 0, joined on fiscal_year; its `value` == median((PX_LAST_y / f) / IS_COMP_EPS_ADJUSTED_y)
      over that window (rel 1e-9), f as in (3), so the multiple is dimensionless; it carries a `basis` object naming both
      mnemonics;
  (3) base.value == consensus_eps.value x trailing_median_pe.value x f (rel 1e-9), f = the block's own landed unit factor
      (landed value / (landed eps x landed pe)); base.formula contains "adjusted";
  (4) upside and downside are byte-identical to the ruled ABSENT objects the block serves today;
  (5) render_pack._model_case_line("Base", base, CRNCY) prints the value with exactly two decimals.
usage: python <this>   (from the repo root)"""
import glob
import json
import os
import re
import statistics
import sys

sys.path.insert(0, os.getcwd())
from lib.research.api import scoped_amgt as sa  # noqa: E402
from lib.research.print import render_pack  # noqa: E402

FX = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round46/checks/fixtures/blocks"
RULED = {"status": "ABSENT", "reason": "methodology to be discussed with Andrew"}


def close(a, b):
    return a is not None and b is not None and abs(a - b) <= 1e-9 * max(1.0, abs(b))


def fig(block, mnemonic, scope, fy=None):
    for f in block.get("figures") or []:
        if f.get("mnemonic") == mnemonic and f.get("scope") == scope and (fy is None or str(f.get("fiscal_year")) == str(fy)):
            return f
    return None


def check(path):
    block = json.load(open(path, encoding="utf-8"))
    key = os.path.basename(path).split(".")[0]
    bad = []
    landed = (block.get("cases") or {}).get("base") or {}
    li = landed.get("inputs") or {}
    f = landed["value"] / (li["consensus_eps"]["value"] * li["trailing_median_pe"]["value"])
    out = sa._model_cases(block)
    base = out.get("base") or {}
    if base.get("status") != "SERVED":
        return key, ["base not SERVED: %s" % json.dumps(base)[:160]]
    inp = base.get("inputs") or {}
    eps = inp.get("consensus_eps") or {}
    best = next((x for x in block["figures"] if x.get("mnemonic") == "BEST_EPS" and x.get("scope") == "forecast"
                 and str(x.get("fiscal_year")) == str(eps.get("fiscal_year"))), None)
    if not isinstance(eps.get("basis"), dict) or best is None or eps.get("basis") != best.get("basis"):
        bad.append("(1) consensus_eps.basis %s != BEST_EPS FY1 basis" % json.dumps(eps.get("basis"))[:80])
    last_closed = int(block["history_window"]["latest_closed_fiscal_year"])
    fy1 = int(eps.get("fiscal_year") or li["consensus_eps"]["fiscal_year"])
    years, ratios = [], []
    for y in range(2000, last_closed + 1):
        if y >= fy1:
            continue
        px, ae = fig(block, "PX_LAST", "fiscal_year_line_item", y), fig(block, "IS_COMP_EPS_ADJUSTED", "fiscal_year_line_item", y)
        if px and ae and isinstance(px.get("value"), (int, float)) and isinstance(ae.get("value"), (int, float)) and ae["value"] > 0:
            years.append(str(y))
            ratios.append((px["value"] / f) / ae["value"])  # dimensionless: a minor-unit quote (GBp) is brought to the EPS unit
    pe = inp.get("trailing_median_pe") or {}
    want = statistics.median(ratios) if ratios else None
    if [str(w) for w in (pe.get("window") or [])] != years:
        bad.append("(2) window %s != adjusted-qualifying years %s" % (pe.get("window"), years))
    if not close(pe.get("value"), want):
        bad.append("(2) trailing_median_pe %s != median(PX/adjEPS) %s" % (pe.get("value"), want))
    b = json.dumps(pe.get("basis") or "")
    if not ("PX_LAST" in b and "IS_COMP_EPS_ADJUSTED" in b):
        bad.append("(2) trailing_median_pe.basis names neither/one mnemonic: %s" % b[:100])
    if not close(base.get("value"), (eps.get("value") or 0) * (pe.get("value") or 0) * f):
        bad.append("(3) base.value %s != eps x pe x f" % base.get("value"))
    if "adjusted" not in str(base.get("formula") or "").lower():
        bad.append("(3) formula lacks 'adjusted': %r" % base.get("formula"))
    for side in ("upside", "downside"):
        if out.get(side) != RULED:
            bad.append("(4) %s moved: %s" % (side, json.dumps(out.get(side))[:120]))
    crncy = (fig(block, "CRNCY", "header") or {}).get("value")
    line = render_pack._model_case_line("Base", base, crncy)
    m = re.match(r"^Base case: SERVED -- (-?\d+)(\.\d+)?\b", line)
    if not m or m.group(2) is None or len(m.group(2)) != 3:
        bad.append("(5) value not printed with two decimals: %r" % line[:90])
    print("%s: pe %s over %d years; base %s; line %r" % (key, pe.get("value"), len(years), base.get("value"), line[:80]))
    return key, bad


def main():
    paths = sorted(glob.glob(os.path.join(FX, "*.model_block.json")))
    fails = 0
    for p in paths:
        key, bad = check(p)
        for b in bad:
            print("  FAIL %s %s" % (key, b))
        fails += bool(bad)
    print("ADJUSTED BASE CASE, BASIS CARRIED, VALUE PRINTED: %d of %d names" % (len(paths) - fails, len(paths)))
    return 0 if paths and not fails else 1


if __name__ == "__main__":
    sys.exit(main())
