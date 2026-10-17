"""ETFS_RIVALS round 32, RIV-za-1 check (issuer-written; the worker does not edit it).

The `held-tr` mode of `rivalfunds.enrichment_bloomberg`: for named (security, trading day) units it asks Bloomberg for PX_LAST and
DAY_TO_DAY_TOT_RETURN_GROSS_DVDS together and lands each date's rows as ONE new timed G4 object whose rows carry
`as_of_source` "held-tr" (never "backfill"), so the rankings read them. Every vendor hook is stubbed, the budget ledger is a temp
dir, the sink is a LocalSink. Nothing here calls Bloomberg, S3 or the network.

Run from data/etfs/scripts:  python -m pytest -q -p no:cacheprovider <this file> -k ac1|ac2|ac3
"""
import datetime as dt
import io
import types

import pyarrow.parquet as pq
import pytest

from rivalfunds import bbg_budget as bb
from rivalfunds import enrichment_bloomberg as eb
from rivalfunds import gold_holding_contribution as hc
from rivalfunds import homes, sinks

D1, D2, D3 = "2026-09-15", "2026-09-16", "2026-09-17"
TR_FIELD = "DAY_TO_DAY_TOT_RETURN_GROSS_DVDS"
UNITS = [{"bloomberg": "A1 US Equity", "dates": [D1, D2]},
         {"bloomberg": "B1 JP Equity", "dates": [D2]}]          # 3 units; B1 has no stored currency
N_UNITS = 3


@pytest.fixture
def env(monkeypatch, tmp_path):
    monkeypatch.setenv(bb.ENV_DIR, str(tmp_path / "ledger"))
    monkeypatch.setattr(eb, "_run_date_et", lambda: dt.date(2026, 10, 17))
    log = []

    def historical(securities, fields, start, end, timeout_s=90.0):
        log.append(("hist", list(securities), list(fields), start, end))
        out = {}
        for x in securities:
            if x == "A1 US Equity" and start == D1:
                out[x] = {D1: {"PX_LAST": 101.0, TR_FIELD: 1.5}, "2026-09-12": {"PX_LAST": 99.0, TR_FIELD: 0.1}}  # one misdated
            else:
                out[x] = {start: {"PX_LAST": 200.0, TR_FIELD: -0.5}}
        return out

    def reference(securities, fields, overrides=None, timeout_s=90.0):
        log.append(("ref", list(securities), list(fields)))
        return {x: {"CRNCY": "JPY"} for x in securities} if list(fields) == ["CRNCY"] else {}

    rec = []
    real_record = bb.record

    def record(mode, rows, batch_id):
        rec.append((mode, int(rows)))
        return real_record(mode, rows, batch_id)

    monkeypatch.setattr(eb, "_blp_historical_data", historical)
    monkeypatch.setattr(eb, "_blp_reference_data", reference)
    monkeypatch.setattr(bb, "record", record)
    root = tmp_path / "sink"
    s = sinks.LocalSink(root)
    # a planted backfill object per date: A1's close only, with its currency, as batch rv-bf365 wrote them
    for d in (D1, D2):
        prov = {"revision": "20261017T040227Z-planted", "produced_at": "2026-10-17T04:02:27Z", "producer_version": "planted",
                "input_manifest": "{}"}
        rows = eb.market_rows({"A1 US Equity": {"PX_LAST": 1.0, "CRNCY": "USD"}}, d, eb.MARKET_SOURCE_HIST, prov, eb.BACKFILL_SOURCE)
        s.put(eb.market_target_uri(d, "20261017T040227Z-planted"), eb._parquet_bytes(eb._market_table(rows)),
              "application/octet-stream")
    # a planted NON-backfill object after the units: A1's stored currency (a backfill row is never a stored currency)
    prov = {"revision": "20260918T110000Z-planted", "produced_at": "2026-09-18T11:00:00Z", "producer_version": "planted",
            "input_manifest": "{}"}
    rows = eb.market_rows({"A1 US Equity": {"PX_LAST": 5.0, "CRNCY": "USD"}}, D3, eb.MARKET_SOURCE_HIST, prov, "historical")
    s.put(eb.market_target_uri(D3, "20260918T110000Z-planted"), eb._parquet_bytes(eb._market_table(rows)), "application/octet-stream")
    return types.SimpleNamespace(log=log, rec=rec, root=root, sink=s, mp=monkeypatch)


def _ev(env, **kw):
    ev = {"mode": "held-tr", "units": UNITS, "batch_id": "t-za1", "sink": f"local:{env.root}", "max_points": 1000}
    ev.update(kw)
    return ev


def _new_rows(env, day):
    pre = homes.address("rivalfunds", "etfs", "gold", "security_market", f"date={day}") + "/"
    objs = [u for u in env.sink.list(pre) if u.endswith(".parquet") and "planted" not in u]
    rows = []
    for u in objs:
        rows += pq.read_table(io.BytesIO(env.sink.get(u))).to_pandas().to_dict("records")
    return objs, rows


# ------------------------------------------------------------------ AC1: the plan, the dry run and the refusal
def test_ac1_dry_run_plans_two_points_per_unit_plus_lookups_and_requests_nothing(env):
    res = eb.handler_entry(_ev(env))                                   # dry_run absent = a dry run
    assert res["status"] == "OK"
    assert res["plan"]["units"] == N_UNITS and res["plan"]["fields"] == ["PX_LAST", TR_FIELD]
    assert res["plan"]["currency_lookups"] == 1                        # B1 only: A1's currency is stored
    assert res["plan"]["points"] == 2 * N_UNITS + 1
    assert env.log == [] and env.rec == []
    assert _new_rows(env, D1)[0] == [] and _new_rows(env, D2)[0] == []


def test_ac1_over_max_points_or_budget_is_refused_before_any_request(env):
    res = eb.handler_entry(_ev(env, max_points=6, dry_run=False))     # 7 points needed
    assert res["status"] == "REFUSED" and env.log == [] and env.rec == []
    env.mp.setattr(bb, "check_points", lambda n, today=None: "refused for test")
    res = eb.handler_entry(_ev(env, dry_run=False))
    assert res["status"] == "REFUSED" and "refused for test" in str(res["detail"]) and env.log == [] and env.rec == []


# ------------------------------------------------------------------ AC2: the live landing
def test_ac2_live_lands_one_timed_object_per_date_with_close_tr_currency_and_its_own_trading_date(env):
    res = eb.handler_entry(_ev(env, dry_run=False))
    assert res["status"] == "OK" and res["landed"] == N_UNITS and res["misdated"] == 1
    hist = [e for e in env.log if e[0] == "hist"]
    assert hist and all(e[2] == ["PX_LAST", TR_FIELD] and e[3] == e[4] for e in hist)   # one trading day per request
    for d, want in ((D1, {"A1 US Equity"}), (D2, {"A1 US Equity", "B1 JP Equity"})):
        objs, rows = _new_rows(env, d)
        assert len(objs) == 1 and eb.rev_mod.capture_time(objs[0]) is not None        # ONE timed object
        assert {r["security_bloomberg"] for r in rows} == want
        for r in rows:
            assert r["as_of_source"] == "held-tr" and str(r["price_date"])[:10] == d
            assert r["px_close"] is not None and r["total_return_index"] is not None
        ccy = {r["security_bloomberg"]: r["currency"] for r in rows}
        assert ccy["A1 US Equity"] == "USD" and ccy.get("B1 JP Equity", "JPY") == "JPY"
    assert sum(n for m, n in env.rec if m == "held-tr") == 2 * N_UNITS + 1


def test_ac2_a_second_identical_run_overwrites_nothing(env):
    eb.handler_entry(_ev(env, dry_run=False))
    first = {u: env.sink.get(u) for d in (D1, D2) for u in _new_rows(env, d)[0]}
    assert len(first) == 2                                             # one object per date landed by the first run
    eb.handler_entry(_ev(env, dry_run=False, batch_id="t-za1-b"))
    for u, b in first.items():
        assert env.sink.get(u) == b                                    # a name is never overwritten


# ------------------------------------------------------------------ AC3: the readers take it, the rankings keep it
def test_ac3_merged_row_takes_the_held_tr_price_group_over_the_backfill_row_and_drop_backfill_keeps_it(env):
    eb.handler_entry(_ev(env, dry_run=False))
    g = hc.g4_rows(env.sink, D1)
    a1 = g[g["security_bloomberg"] == "A1 US Equity"].iloc[0]
    assert a1["as_of_source"] == "held-tr" and float(a1["px_close"]) == 101.0 and float(a1["total_return_index"]) == 1.5
    kept = hc.drop_backfill(g)
    assert "A1 US Equity" in set(kept["security_bloomberg"])
    assert float(kept[kept["security_bloomberg"] == "A1 US Equity"].iloc[0]["total_return_index"]) == 1.5
