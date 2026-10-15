"""RIV-ya-1 checks (round 31): where a Bloomberg (MEASURED) corporate-action row and an inferred (INFERRED) row name the same
(security_id, event_type, ex_date), the Bloomberg row wins in BOTH readers and the inferred row is dropped and COUNTED.
Authority: CTO half ledger/NEVER_WIDEN_R30_DEPLOY_CTO_HALF.md condition C1 (msg 5612); Andrew 2026-10-15 "Call bbd5: yes fix only round now".

    cd data/etfs/scripts && python -m pytest -q <this file>

Offline: a local sink and in-memory frames, no S3, no vendor call. The rule this file pins:
  * G5 reader `gold_trade_schedule.load_actions(s)`: of the EVENT rows that share (normalised security_id, event_type, ex_date) where at
    least one has claim == "MEASURED" and another has claim == "INFERRED", the INFERRED rows leave BEFORE the union is returned
    (their raw_event_type differs, so the union's own key never collapsed them). The returned frame carries the count of rows
    dropped in `df.attrs["precedence_dropped"]` (an int, 0 when none); the (rows, label, uris) triple is unchanged. A frame with
    no `claim` column behaves exactly as before and carries precedence_dropped 0.
  * chart reader `price_series.series(...)`: the same rule over the actions frame before the splits are applied, so a Bloomberg
    split and an inferred split of the SAME ex_date apply ONCE (the Bloomberg row) whatever the two ratios are (the old
    (ex_date, ratio) de-dup only collapsed equal ratios); each key's result carries "precedence_dropped": <int> (0 when none).
  * one inferred row with NO Bloomberg row for its key is applied, as the union intends; a different event_type or a different
    ex_date is a different key; two MEASURED rows are never dropped by this rule.
"""
import datetime as dt
import io

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from rivalfunds import gold_canonical_shape as g1mod
from rivalfunds import gold_trade_schedule as g
from rivalfunds import homes, price_series, sinks

D = "2026-10-01"
D1, D2 = dt.date(2026, 9, 1), dt.date(2026, 9, 2)


def _row(sec, et, ex, ratio, rev, as_of, claim, raw, url=None):
    r = {"row_kind": "event", "security_id": sec, "event_type": et, "ex_date": dt.date.fromisoformat(ex), "ratio": ratio,
         "revision": rev, "as_of": as_of, "record_seq": 0, "status": "OK", "raw_event_type": raw, "claim": claim,
         "source_url": url}
    return r


def _put(s, name, rows):
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(homes.address("rivalfunds", "etfs", "gold", "corporate_actions", f"date={D}", f"{name}.parquet"), buf.getvalue())


def _key(r):
    return (r.security_id, r.event_type, str(r.ex_date), r.claim)


def test_ac1_g5_a_bloomberg_split_beats_an_inferred_split_of_the_same_key_and_the_drop_is_counted(tmp_path):
    s = sinks.get_sink(f"local:{tmp_path}")
    bbg = [_row("A US Equity", "split", "2026-03-02", 2.0, "bbg1", dt.date(2026, 10, 1), "MEASURED", "Stock Split"),
           _row("A US Equity", "cash_div", "2026-06-01", 0.5, "bbg1", dt.date(2026, 10, 1), "MEASURED", "Regular Cash"),
           # two MEASURED rows of one key (a special beside a regular) are never touched by the rule
           _row("C US Equity", "cash_div", "2026-06-01", None, "bbg1", dt.date(2026, 10, 1), "MEASURED", "Regular Cash"),
           _row("C US Equity", "cash_div", "2026-06-01", None, "bbg1", dt.date(2026, 10, 1), "MEASURED", "Special Cash")]
    inferred = [_row("A US Equity", "split", "2026-03-02", 4.0, "inf1", dt.date(2026, 10, 10), "INFERRED", "stock split 4-for-1", "https://x/1"),
                # (b) an inferred split with NO vendor row for its key is applied
                _row("B US Equity", "split", "2026-04-01", 3.0, "inf1", dt.date(2026, 10, 10), "INFERRED", "stock split 3-for-1", "https://x/2"),
                # a different ex_date for the same security and type is a different key: kept
                _row("A US Equity", "split", "2026-05-05", 5.0, "inf1", dt.date(2026, 10, 10), "INFERRED", "stock split 5-for-1", "https://x/3"),
                # a different event_type on a Bloomberg key's date is a different key: kept
                _row("A US Equity", "cash_div", "2026-03-02", 0.1, "inf1", dt.date(2026, 10, 10), "INFERRED", "special dividend", "https://x/4")]
    _put(s, "actions-bbg1", bbg)
    _put(s, "actions-inferred-inf1", inferred)
    df, label, uris = g.load_actions(s)
    got = sorted(_key(r) for r in df.itertuples())
    assert got == sorted([("A US Equity", "split", "2026-03-02", "MEASURED"), ("A US Equity", "cash_div", "2026-06-01", "MEASURED"),
                          ("C US Equity", "cash_div", "2026-06-01", "MEASURED"), ("C US Equity", "cash_div", "2026-06-01", "MEASURED"),
                          ("B US Equity", "split", "2026-04-01", "INFERRED"), ("A US Equity", "split", "2026-05-05", "INFERRED"),
                          ("A US Equity", "cash_div", "2026-03-02", "INFERRED")])
    assert df.attrs["precedence_dropped"] == 1
    assert len(uris) == 2 and "bbg1" in label


def test_ac1_g5_control_without_a_claim_column_or_without_a_vendor_row_the_reader_is_as_it_was(tmp_path):
    s = sinks.get_sink(f"local:{tmp_path}")
    old = [{k: v for k, v in _row("A US Equity", "split", "2026-03-02", 2.0, "p1", dt.date(2026, 9, 1), "MEASURED", "Stock Split").items()
            if k not in ("claim", "source_url")}]
    _put(s, "actions-p1", old)
    df, _, _ = g.load_actions(s)
    assert len(df) == 1 and df.attrs["precedence_dropped"] == 0
    s2 = sinks.get_sink(f"local:{tmp_path}/two")
    _put(s2, "actions-inferred-only", [_row("B US Equity", "split", "2026-04-01", 3.0, "i", dt.date(2026, 10, 10), "INFERRED", "3-for-1", "u")])
    df2, _, _ = g.load_actions(s2)
    assert len(df2) == 1 and df2.attrs["precedence_dropped"] == 0
    assert g.load_actions(sinks.get_sink(f"local:{tmp_path}/empty")) == (None, None, [])


def _g1(keys):
    cols = [f.name for f in g1mod.SCHEMA]
    return pd.DataFrame([{**{c: None for c in cols}, "fund_id": "TXUE", "fund_ticker": "TXUE", "report_date": d, "security_id": k,
                          "raw_identifier": k, "quantity": 10.0, "market_value": 1000.0, "is_cash_line": False}
                         for k in keys for d in (D1, D2)], columns=cols)


def _g4(key):
    return pd.DataFrame([{"security_id": key, "date": d, "px_close": 10.0, "currency": "USD"} for d in (D1, D2)],
                        columns=["security_id", "date", "px_close", "currency"])


def _act(rows):
    return pd.DataFrame(rows, columns=["security_id", "event_type", "ratio", "ex_date", "claim", "source_url", "revision"])


def _series(rows):
    return price_series.series(_g4("A"), _g1(["A"]), ["A"], D1, D2, actions=_act(rows))["A"]


def test_ac2_chart_a_bloomberg_split_beats_an_inferred_split_of_the_same_ex_date_whatever_the_ratios(tmp_path):
    ex = dt.date(2026, 9, 2)
    out = _series([("A", "split", 4.0, ex, "MEASURED", None, "bbg1"), ("A", "split", 2.0, ex, "INFERRED", "https://x", "inf1")])
    assert [(r["ratio"], r["claim"]) for r in out["adjustment"]] == [(4.0, "MEASURED")]   # the old de-dup kept BOTH (the ratios differ)
    assert out["precedence_dropped"] == 1
    same = _series([("A", "split", 4.0, ex, "INFERRED", "https://x", "inf1"), ("A", "split", 4.0, ex, "MEASURED", None, "bbg1")])
    assert [(r["ratio"], r["claim"]) for r in same["adjustment"]] == [(4.0, "MEASURED")] and same["precedence_dropped"] == 1


def test_ac2_chart_control_an_inferred_split_alone_applies_and_a_second_date_is_a_second_event():
    ex = dt.date(2026, 9, 2)
    alone = _series([("A", "split", 2.0, ex, "INFERRED", "https://x", "inf1")])
    assert [(r["ratio"], r["claim"]) for r in alone["adjustment"]] == [(2.0, "INFERRED")] and alone["precedence_dropped"] == 0
    # two MEASURED rows are never dropped by this rule; the same-ratio de-dup of the old reader is unchanged
    two = _series([("A", "split", 2.0, ex, "MEASURED", None, "b1"), ("A", "split", 2.0, ex, "MEASURED", None, "b2")])
    assert len(two["adjustment"]) == 1 and two["precedence_dropped"] == 0
    none = _series([])
    assert none["adjustment"] == [] and none["precedence_dropped"] == 0
