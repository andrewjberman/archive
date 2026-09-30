"""AMGT_RESAPP round 54, AMGT-ad-4 AC1 -- FWD-30's grader reads an UNRESOLVED header figure's RAW FIGURE, and grades it equal ONLY when
BOTH sides state the unit unresolved AND the digits agree.
On TSM_US_Equity, captured from the DEPLOYED function by the grader's own capture and rendered by its own `render_page_html`, the page's
HEADER CURR_ENTP_VAL cell reads "unit not resolved -- raw figure 71,993,494.73 (TWD)" and the export's value is "71993494.73205896
UNRESOLVED-ON-TSM ..." (the round-53 close: the one NOT_OK fact of 96 names). With the grader's `page_facts_from_html`, `rich_facts` and
`value_diffs` on that fact:
  (0) as captured: the fact reads EQUAL (0 value-difference lines for it);
  (a) PLANT: the page's raw-figure digits changed (71,993,494.73 -> 81,993,494.73), words kept -- the fact must DIFFER;
  (b) CONTROL: the export's unit made RESOLVED (UNRESOLVED... -> MILLIONS) with the page still saying "unit not resolved" -- the fact
      must DIFFER (one side resolved, the other not, is a difference, never an equality).
At the cut the grader reads the page's leading words as the value, so (0) fails.
usage: python <this> --cache <dir outside the repo>   (from the repo root; read-only Invokes)"""
import argparse
import copy
import importlib.util
import sys
from pathlib import Path

SWEEP = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round45/checks/sweep.py"
KEY = "TSM_US_Equity"
FACT = ("HEADER", "CURR_ENTP_VAL")


def lines_for(m, page, rich):
    return [x for x in m.value_diffs(page, rich)[4] if str(FACT) in x]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("sweep", SWEEP)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    d, fx = m.captured(a.cache, KEY, m.load_capture_lib())
    rich_path = next(iter(sorted((Path(d) / "served").glob("*.rich.md"))))
    page = m.page_facts_from_html(m.render_page_html(fx))
    rich = m.rich_facts(Path(rich_path).read_text(encoding="utf-8"), fx)
    pv, rv = (page.get("VALUES") or {}).get(FACT), (rich.get("VALUES") or {}).get(FACT)
    print("page %s | export %s" % (pv, rv))
    if not pv or not rv:
        print("the fact is not carried on both sides")
        print("THE GRADER READS AN UNRESOLVED FIGURE'S RAW DIGITS, BOTH SIDES UNRESOLVED ONLY: NO")
        return 1
    base = lines_for(m, page, rich)
    print("(0) as captured: difference lines %d %s" % (len(base), [x[:160] for x in base]))
    planted = copy.deepcopy(page)
    planted["VALUES"][FACT] = [(t.replace("71,993,494.73", "81,993,494.73"), x) for t, x in pv]
    plant_lines = lines_for(m, planted, rich)
    print("(a) raw-figure plant: difference lines %d" % len(plant_lines))
    control = copy.deepcopy(rich)
    control["VALUES"][FACT] = [(tok, "MILLIONS") for tok, _u in rv]
    control_lines = lines_for(m, page, control)
    print("(b) export-resolved control: difference lines %d" % len(control_lines))
    ok = not base and bool(plant_lines) and bool(control_lines) and any("71,993,494.73" in t for t, _ in pv)
    print("THE GRADER READS AN UNRESOLVED FIGURE'S RAW DIGITS, BOTH SIDES UNRESOLVED ONLY: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
