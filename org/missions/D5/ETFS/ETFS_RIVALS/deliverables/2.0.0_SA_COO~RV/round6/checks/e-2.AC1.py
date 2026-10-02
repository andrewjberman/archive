"""RIV-e-2 AC1 (W3-S11, round-4 ruling 5): `DVD_CRNCY` joins the dividend request inside the worded rivalfunds pull. The
OFFLINE plan mode (no Bloomberg session, nothing written) lists it beside `DVD_HIST_ALL`.
Interface: `enrichment_bloomberg.handler_entry({"mode": "plan", "securities": [...], "date": ...})["plan"]["fields"]`."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import enrichment_bloomberg as e

    r = e.handler_entry({"mode": "plan", "securities": ["VOD LN Equity", "AAPL US Equity"], "date": "2026-10-01"})
    fields = list((r.get("plan") or {}).get("fields") or [])
    print("status:", r.get("status"), "| plan fields:", fields)
    v.check(r.get("status") == "OK" and "DVD_HIST_ALL" in fields, "control: the plan still requests DVD_HIST_ALL")
    v.check("DVD_CRNCY" in fields, "the plan requests DVD_CRNCY")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
