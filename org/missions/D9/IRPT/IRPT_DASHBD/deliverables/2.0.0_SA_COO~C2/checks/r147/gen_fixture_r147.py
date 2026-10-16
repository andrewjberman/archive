"""IRPT_DASHBD round 147, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- the fixture generator for cell DB-c-25 (FWD-10 cell (a)).

The three series documents are produced by the CONTRACT'S WRITER (infra/aws/lambda/investor-reporting/reporting-publish/publisher.py
build_series, series contract 0.3.0) over made-up rows (account SYNTH-A, invented values) and the real trading calendar
(lib/trading_calendar.py). Nothing here is hand-written series JSON.

  series-unreported-days.json   the source reported every trading day from 2026-07-10 to 2026-08-14 EXCEPT 2026-07-14, 2026-07-15 and 2026-08-05
  series-no-statement.json      the same rows, no `present_dates` (the pair is absent: no statement is made)
  series-unreported-empty.json  the source reported every trading day (the pair is present and the list is [])

Usage: python <this file> <repo_root> <output_dir>      writes the three files, compact JSON + one newline; prints one line per file.
Plain `python`, NOT `-I` (lib/trading_calendar needs the user site packages).
"""
import datetime as dt
import json
import sys
from pathlib import Path

FIRST = dt.date(2026, 7, 10)
LAST = dt.date(2026, 8, 14)
UNREPORTED = ("2026-07-14", "2026-07-15", "2026-08-05")
NAMES = ("series-unreported-days.json", "series-no-statement.json", "series-unreported-empty.json")


def row(date, value, ret):
    """One synthetic gold row; a null return is NOT_MEASURABLE, a present return is TWR (the contract's pairing). Income is null (the method separates none)."""
    return {"account_id": "SYNTH-A", "business_date": date, "market_value_eod": value,
            "total_return_daily": ret, "return_basis": "NOT_MEASURABLE" if ret is None else "TWR",
            "day_quality": "MEASURED", "external_flow": 0.0, "income_received": None,
            "holdings_price_return": None, "method_version": 1, "history_scope": "PARTIAL_HISTORY"}


def main(argv):
    root, out_dir = Path(argv[0]).resolve(), Path(argv[1])
    sys.path.insert(0, str(root / "infra" / "aws" / "lambda" / "investor-reporting" / "reporting-publish"))
    sys.path.insert(0, str(root))
    import publisher as p  # noqa: E402
    from lib import trading_calendar as tc  # noqa: E402

    days = [d.isoformat() for d in tc.trading_days_between(FIRST, LAST)]
    present = [d for d in days if d not in UNREPORTED]
    rows = [row(d, 1000.0 + 1.5 * i, None if i == 0 else 0.001) for i, d in enumerate(present)]
    docs = (
        p.build_series(rows, present_dates=present, calendar=tc),
        p.build_series(rows),
        p.build_series([row(d, 1000.0 + 1.5 * i, None if i == 0 else 0.001) for i, d in enumerate(days)], present_dates=days, calendar=tc),
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, doc in zip(NAMES, docs):
        raw = json.dumps(doc, separators=(",", ":"), allow_nan=False, sort_keys=False) + "\n"
        (out_dir / name).write_bytes(raw.encode("utf-8"))
        print("%s bytes=%d unreported=%s" % (name, len(raw), doc.get("unreported_trading_days", "ABSENT")))
    assert docs[0]["unreported_trading_days"] == list(UNREPORTED), docs[0]["unreported_trading_days"]
    assert "unreported_trading_days" not in docs[1] and docs[2]["unreported_trading_days"] == []
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
