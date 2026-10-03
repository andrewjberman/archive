"""RIV-e-2 AC2 (W3-S11): a G3 dividend row carries its currency from the response's `DVD_CRNCY` (today `currency` is NULL on
every DVD_HIST_ALL row). A security whose response has no DVD_CRNCY keeps NULL, never a guess (control).
Interface: `enrichment_bloomberg.rows_from_responses(data, as_of, provenance)`, with `DVD_CRNCY` as a per-security scalar beside
the bulk field."""
import datetime as dt
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

REC = {"Declared Date": "2026-01-01", "Ex-Date": "2026-02-01", "Record Date": "2026-02-02", "Payable Date": "2026-02-10",
       "Dividend Amount": 0.5, "Dividend Frequency": "Quarterly", "Dividend Type": "Regular Cash"}


def run(v):
    c.setup_path()
    from rivalfunds import enrichment_bloomberg as e

    data = {"VOD LN Equity": {"DVD_HIST_ALL": [dict(REC)], "DVD_CRNCY": "GBp"},
            "AAPL US Equity": {"DVD_HIST_ALL": [dict(REC)]}}
    rows = e.rows_from_responses(data, dt.date(2026, 10, 1), {"revision": "r"})
    by = {r["security_id"]: r for r in rows}
    print({k: by[k].get("currency") for k in by})
    v.check(by.get("VOD LN Equity", {}).get("currency") == "GBp", "VOD LN's dividend row carries currency GBp from DVD_CRNCY")
    v.check(by.get("AAPL US Equity", {}).get("currency") is None, "control: no DVD_CRNCY in the response leaves currency NULL")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
