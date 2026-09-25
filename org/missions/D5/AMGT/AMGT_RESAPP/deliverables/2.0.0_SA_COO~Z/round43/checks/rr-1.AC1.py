"""AMGT_RESAPP round 43, AMGT-rr-1 AC1 -- the five no-block names of the LIVE research library (AMD, GOOGL, LLY, PWR, UNH)
each have a landed Model block the served reader returns, with fiscal-year rows and figures. A read.
usage (repo root): PYTHONPATH="$(pwd)" python <this>"""
import sys

from lib.research.api import scoped_amgt as sa

KEYS = ["AMD_US_Equity", "GOOGL_US_Equity", "LLY_US_Equity", "PWR_US_Equity", "UNH_US_Equity"]
landed = 0
for key in KEYS:
    block = sa.read_model_block(key) or {}
    fy = block.get("fiscal_year_row_count") or len(block.get("fiscal_years") or [])
    figs = len(block.get("figures") or [])
    ok = bool(block) and fy > 0 and figs > 0
    landed += ok
    print("%s block=%s fy_rows=%s figures=%s raw_stamp=%s %s" % (
        key, "yes" if block else "NO", fy, figs, block.get("raw_stamp_used"), "OK" if ok else "MISSING"))
print("model blocks landed: %d of %d" % (landed, len(KEYS)))
sys.exit(0 if landed == len(KEYS) else 1)
