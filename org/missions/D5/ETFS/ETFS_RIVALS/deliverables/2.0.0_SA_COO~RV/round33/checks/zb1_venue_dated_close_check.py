"""ETFS_RIVALS round 33, RIV-zb-1 check (issuer-written; the worker does not edit it).

The G4 market pull for a PAST partition D takes the price group (px_close, total_return_index) ONLY from the historical request
dated D, asked for PX_LAST and DAY_TO_DAY_TOT_RETURN_GROSS_DVDS alone; it never files the current-value (reference) PX_LAST under a
past partition. Descriptive fields still come from the reference request, for every security. Rows Z-S85 / D1-S21. Every vendor
hook is stubbed; the sink is a LocalSink.

Run from data/etfs/scripts:  python -m pytest -q -p no:cacheprovider <this file> -k ac1|ac2|ac3
"""
import datetime as dt
import io

import pyarrow.parquet as pq

from rivalfunds import enrichment_bloomberg as e
from rivalfunds import homes, sinks

RUN = dt.date(2026, 10, 16)
D = "2026-10-15"
US, JP, HK = "ADBE US Equity", "7203 JP Equity", "992 HK Equity"   # HK: no close dated D (its venue was shut)
PRICE_FIELDS = ["PX_LAST", "DAY_TO_DAY_TOT_RETURN_GROSS_DVDS"]


def _rows(sink, date):
    s = sinks.get_sink(sink)
    out = []
    for u in s.list(homes.address("rivalfunds", "etfs", "gold", "security_market", f"date={date}") + "/"):
        if u.endswith(".parquet"):
            out += pq.read_table(io.BytesIO(s.get(u))).to_pylist()
    return {r["security_bloomberg"]: r for r in out}


def _pin(monkeypatch, hist):
    calls = {"hist": [], "ref": []}
    monkeypatch.setattr(e, "_run_date_et", lambda: RUN)

    def historical(secs, fields, start, end, **k):
        calls["hist"].append((list(secs), list(fields), start, end))
        return hist(secs, start)

    def reference(secs, fields, overrides=None, timeout_s=0):
        calls["ref"].append((list(secs), list(fields)))
        return {x: {"PX_LAST": 99.0, "DAY_TO_DAY_TOT_RETURN_GROSS_DVDS": 9.9, "GICS_SECTOR_NAME": "Tech", "CRNCY": "XXX"} for x in secs}

    monkeypatch.setattr(e, "_blp_historical_data", historical)
    monkeypatch.setattr(e, "_blp_reference_data", reference)
    return calls


def _answer(secs, start):
    got = {US: {start: {"PX_LAST": 10.0, "DAY_TO_DAY_TOT_RETURN_GROSS_DVDS": 1.0}},
           JP: {start: {"PX_LAST": 20.0, "DAY_TO_DAY_TOT_RETURN_GROSS_DVDS": -2.0}}, HK: {}}
    return {x: got.get(x, {}) for x in secs}


def _run(tmp_path, date=D, mode="market"):
    sink = f"local:{tmp_path}"
    r = e.handler_entry({"mode": mode, "date": date, "securities": [US, JP, HK], "batch_id": "zb1", "sink": sink})
    return r, sink


# ------------------------------------------------------------------ AC1: the past partition's price group is the dated historical answer
def test_ac1_past_partition_price_group_comes_only_from_the_historical_answer_dated_d(tmp_path, monkeypatch):
    calls = _pin(monkeypatch, _answer)
    r, sink = _run(tmp_path)
    assert r["status"] == "OK"
    assert calls["hist"] and all(f == PRICE_FIELDS and s == D and t == D for _, f, s, t in calls["hist"])
    rows = _rows(sink, D)
    assert (rows[US]["px_close"], rows[US]["total_return_index"]) == (10.0, 1.0)
    assert (rows[JP]["px_close"], rows[JP]["total_return_index"]) == (20.0, -2.0)
    for k in (US, JP):
        assert rows[k]["as_of_source"] == "historical" and str(rows[k]["price_date"])[:10] == D
        assert rows[k]["as_of"] == dt.date.fromisoformat(D)
    assert rows[HK]["px_close"] is None and rows[HK]["total_return_index"] is None   # never the 99.0 snapshot
    assert rows[HK]["as_of_source"] == "pull"
    assert r["detail"]["as_of_source_counts"] == {"historical": 2, "pull": 1}


def test_ac1_descriptive_fields_still_come_from_the_reference_request_for_every_security(tmp_path, monkeypatch):
    calls = _pin(monkeypatch, _answer)
    _, sink = _run(tmp_path)
    asked = {x for secs, _ in calls["ref"] for x in secs}
    assert {US, JP, HK} <= asked
    rows = _rows(sink, D)
    assert all(rows[k]["gics_sector"] == "Tech" for k in (US, JP, HK))
    assert rows[US]["currency"] == "XXX" and rows[HK]["currency"] == "XXX"


# ------------------------------------------------------------------ AC2: a misdated or failed historical answer never prices the partition
def test_ac2_a_historical_value_dated_otherwise_is_not_this_dates_close(tmp_path, monkeypatch):
    _pin(monkeypatch, lambda secs, start: {x: {"2026-10-16": {"PX_LAST": 55.0, "DAY_TO_DAY_TOT_RETURN_GROSS_DVDS": 5.0}} for x in secs})
    _, sink = _run(tmp_path)
    rows = _rows(sink, D)
    assert all(rows[k]["px_close"] is None and rows[k]["as_of_source"] == "pull" for k in (US, JP, HK))


def test_ac2_a_failed_historical_request_lands_descriptors_and_no_close(tmp_path, monkeypatch):
    calls = _pin(monkeypatch, _answer)
    monkeypatch.setattr(e, "_blp_historical_data", lambda *a, **k: (_ for _ in ()).throw(TimeoutError("blp down")))
    r, sink = _run(tmp_path)
    rows = _rows(sink, D)
    assert r["status"] == "OK" and r["detail"]["historical_request_failures"] >= 1
    assert all(rows[k]["px_close"] is None and rows[k]["gics_sector"] == "Tech" for k in (US, JP, HK))
    assert calls["ref"]


# ------------------------------------------------------------------ AC3: the run-date partition is unchanged; daily mode takes the same rule
def test_ac3_run_date_partition_still_takes_the_current_pull_and_asks_no_history(tmp_path, monkeypatch):
    calls = _pin(monkeypatch, _answer)
    r, sink = _run(tmp_path, date=RUN.isoformat())
    rows = _rows(sink, RUN.isoformat())
    assert r["status"] == "OK" and calls["hist"] == [] and rows[US]["px_close"] == 99.0 and rows[US]["as_of_source"] == "pull"


def test_ac3_daily_mode_past_partition_takes_the_same_rule(tmp_path, monkeypatch):
    _pin(monkeypatch, _answer)
    monkeypatch.setattr(e, "_daily_dividends", lambda event, s, date, batch_id, produced_at, out: out("OK", detail={}))
    r, sink = _run(tmp_path, mode="daily")
    rows = _rows(sink, D)
    assert r["market"]["status"] == "OK"
    assert rows[JP]["px_close"] == 20.0 and rows[HK]["px_close"] is None
