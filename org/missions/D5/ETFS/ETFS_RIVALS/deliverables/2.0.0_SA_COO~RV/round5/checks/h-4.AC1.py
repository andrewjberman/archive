"""RIV-h-4 AC1 (hop-9 ruling a) -- an ID-CHANGE needs an identifier relation, never equal value alone; CUSIPs are zero-padded to 9
at silver.

Pure, offline:
  - silver: `silver_issuer.parse_capture` on a capture line whose security_cusip is the 8-character `55622104` (BP) yields
    `055622104`;
  - control (G5): a line whose CUSIP is `55622104` on day 1 and `055622104` on day 2 (same quantity and value) never splits into
    an exit plus an entry: equal-after-normalisation CUSIPs ARE an identifier relation, so one ID-CHANGE row (or none, once silver
    has normalised) is right;
  - G5: an exit of `91377B109` and an entry of `74762E102` at EQUAL value (no identifier relation) infer TWO rows, an exit and an
    entry, neither of confidence ID-CHANGE (today: one ID-CHANGE row);
  - control: an unchanged book infers 0 trades."""
import datetime as dt
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def rows(date, book):
    """book: {key: (quantity, price, cusip)} -> canonical_shape-like rows (BASG), one cash line."""
    d = dt.date.fromisoformat(date)
    out = [{"fund_ticker": "BASG", "report_date": d, "dataset_revision": "r1", "position_type": "cash", "security_id": None,
            "raw_identifier": "Cash", "security_cusip": None, "resolution_status": "UNRESOLVED", "quantity": 1000.0,
            "market_value": 1000.0, "weight": 0.02}]
    for k, (q, p, cus) in book.items():
        out.append({"fund_ticker": "BASG", "report_date": d, "dataset_revision": "r1", "position_type": "long",
                    "security_id": None, "raw_identifier": cus, "security_cusip": cus, "resolution_status": "UNRESOLVED",
                    "quantity": float(q), "market_value": float(q) * p, "weight": 0.01})
    return out


BASE = {f"S{i}": (1000 + 10 * i, 10.0 + i, f"00000{i:03d}0") for i in range(8)}


def run(v):
    c.setup_path()
    import pandas as pd
    from rivalfunds import gold_trade_schedule as g
    from rivalfunds import silver_issuer

    hdr_src = c.main_root() / ".runtime" / "amgt-reconn-daily-census-20260929" / "gqgu" / "2026-09-28.txt"
    header = hdr_src.read_bytes().decode("utf-8-sig").splitlines()[0]
    cols = header.split("|")
    vals = {k: "" for k in cols}
    vals.update({"date": "09/28/2026", "fund_ticker": "GQGU", "security_cusip": "55622104", "security_description": "BP PLC",
                 "quantity": "100", "market_value": "1000", "percent_of_net_assets": "1.0", "security_group": "Equity"})
    raw = ("﻿" + header + "\n" + "|".join(vals[k] for k in cols) + "\n").encode("utf-8")
    parsed = silver_issuer.parse_capture(raw)
    cus = (parsed.get("security_cusip") or [None])[0]
    print("silver security_cusip:", repr(cus))
    v.check(cus == "055622104", "silver zero-pads an 8-character CUSIP to 9 (55622104 -> 055622104)")

    b1 = dict(BASE, BP=(500, 40.0, "55622104"))
    b2 = dict(BASE, BP=(500, 40.0, "055622104"))
    t = g.infer_trades(pd.DataFrame(rows("2026-09-28", b1) + rows("2026-09-29", b2)))
    acts = sorted(zip(t["action"].astype(str), t["confidence"].astype(str))) if len(t) else []
    print("normalised-CUSIP book rows (action, confidence):", acts)
    v.check(len(t) <= 1 and "entry" not in {a for a, _ in acts} and all(cf == "ID-CHANGE" for _, cf in acts),
            "control: the same security under 8- and 9-char CUSIPs never splits into an exit plus an entry (an ID-CHANGE or no row)")

    u1 = dict(BASE, UMG=(1000, 25.0, "91377B109"))
    u2 = dict(BASE, PWR=(250, 100.0, "74762E102"))
    t2 = g.infer_trades(pd.DataFrame(rows("2026-09-25", u1) + rows("2026-09-28", u2)))
    acts2 = sorted(t2["action"].astype(str)) if len(t2) else []
    conf2 = set(t2["confidence"].astype(str)) if len(t2) else set()
    print("equal-value rows: actions", acts2, "confidence", sorted(conf2))
    v.check(acts2 == ["entry", "exit"] and "ID-CHANGE" not in conf2,
            "equal value alone infers an exit plus an entry, never an ID-CHANGE")

    t0 = g.infer_trades(pd.DataFrame(rows("2026-09-28", BASE) + rows("2026-09-29", BASE)))
    v.check(len(t0) == 0, "control: an unchanged book infers 0 trades")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
