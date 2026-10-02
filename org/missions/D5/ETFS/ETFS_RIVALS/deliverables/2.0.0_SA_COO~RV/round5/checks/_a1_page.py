"""Shared fixture for the RIV-pg-1 checks (issuer-written): the test_p2 page fixture plus the four amendment-A1 tables for TXUE,
a planted AI account for the benchmark SCHY, and a census with one missing input; then one publish. Returns (result, html)."""
import io
import json

import _common as c

DAY = "2026-09-30"


def _put(s, table, rev, rows):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq

    from rivalfunds import homes
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(homes.address("rivalfunds", "etfs", "gold", table, f"date={DAY}", f"{table}-{rev}.parquet"), buf.getvalue())


def publish():
    c.setup_path()
    from rivalfunds import publish_page

    spec, s, _ = c.page_fixture()
    rev = "20260930T020000Z-cccccccccccc"
    hc = []
    for p in ("MTD", "QTD", "YTD", "R30"):
        for i, (b, v) in enumerate((("S1", 0.012), ("S2", -0.004))):
            hc.append({"fund_id": "TXUE", "role": "rival", "period": p, "period_start": "2026-09-01", "period_end": DAY,
                       "axis": "security", "bucket": b, "security_name": f"Name {b}", "contribution": v, "price_coverage": "full",
                       "n_days_priced": 21, "n_days_period": 21, "rank_best": i + 1, "rank_worst": 2 - i, "n_ranked": 2,
                       "n_missing": 1, "claim": "INFERRED", "revision": rev})
        hc.append({"fund_id": "TXUE", "role": "rival", "period": p, "period_start": "2026-09-01", "period_end": DAY,
                   "axis": "sector", "bucket": "Energy", "security_name": None, "contribution": 0.008, "price_coverage": "full",
                   "n_days_priced": 21, "n_days_period": 21, "rank_best": 1, "rank_worst": 1, "n_ranked": 1, "n_missing": 0,
                   "claim": "INFERRED", "revision": rev})
    _put(s, "holding_contribution", rev, hc)
    _put(s, "buying_trend", rev, [{"fund_id": "TXUE", "role": "rival", "window_start": "2026-01-02", "window_end": DAY,
                                   "n_trading_days": 188, "axis": "security", "bucket": "S1", "security_name": "Name S1",
                                   "net_notional_base": 3000.0, "n_windows": 3, "lean": "into", "rank": 1, "reading": "tilt",
                                   "trend_mark": "+ + + 0 0 0 0 0 0", "n_refused_windows": 0, "claim": "INFERRED", "revision": rev}])
    acct = {"run_id": "runP", "item_id": "1", "kind": "activity_30d", "text": "TXUE added 3000 of Name S1.", "observed": "[]",
            "inferred": "[]", "cited_rows": json.dumps([{"table": "buying_trend", "key": "S1", "revision": rev, "value": 3000.0}]),
            "invalidation": "a reversal", "input_vintages": json.dumps({"fear_greed": "2026-09-30"}), "web_reads": "[]",
            "grounding": "PASS", "grounding_reason": None, "model_version": "stub", "prompt_version": "v1",
            "input_manifest": "{}", "produced_at": "2026-09-30T02:00:00Z"}
    _put(s, "research_hypotheses", "runP", [dict(acct, fund_id="TXUE"), dict(acct, fund_id="SCHY")])
    _put(s, "input_census", rev, [{"date": DAY, "input_kind": "price", "subject": "S9", "fund_id": "TXUE", "role": "rival",
                                   "status": "missing", "as_of": None, "location": "fixture", "reason": "no G4 row", "revision": rev}])
    r = publish_page.handler_entry({"date": DAY, "mode": "daily", "batch_id": "a1pg", "sink": spec})
    from rivalfunds import homes
    try:
        html = s.get(homes.page(DAY, "index.html")).decode("utf-8")
    except Exception:  # noqa: BLE001 -- an unpublished page reads as empty and the checks fail on it
        html = ""
    return r, html
