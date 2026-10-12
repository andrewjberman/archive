"""RIV-xd-1 checks (round 29): a dramatic move PLANTED in a scratch sink is found by the lookup and ADJUSTED on the page of the same
day -- the series the chart reads, and the published chart object -- with a control (no lookup: a gap) and no S3.

    cd data/etfs/scripts && python -m pytest -q <this file>

Offline: a LocalSink holds synthetic gold; `search` is injected; nothing is served and no vendor is called.
AC1 (series level) and AC2 (the page's own chart object, the real neighbour: publish_page.handler_entry).
"""
import datetime as dt
import io
import json

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from rivalfunds import dramatic_move as dm
from rivalfunds import gold_holding_contribution as hc
from rivalfunds import guardrails, homes, price_series, publish_page, sinks
from rivalfunds.tests import test_p2_page_grouped_by_fund as tp2

DAY = "2026-10-08"            # a Thursday: hc.as_of(DAY) is 2026-10-07, the date the page's series ends on
K = "TKOMY_US_Equity"
NAME = "Tokio Marine Holdings Inc"
CLOSES = [("2026-10-01", 50.5), ("2026-10-02", 49.93), ("2026-10-05", 49.59), ("2026-10-06", 50.5), ("2026-10-07", 3.33)]
BIG = "the price moved more than threefold in one day and no corporate action is on file"


def _put_g4(s, rows, key=K, name=NAME):
    for d, px in rows:
        t = pa.table({"security_id": pa.array([key], pa.string()), "date": pa.array([dt.date.fromisoformat(d)], pa.date32()),
                      "px_close": pa.array([float(px)], pa.float64()), "currency": pa.array(["USD"], pa.string()),
                      "security_name": pa.array([name], pa.string())})
        buf = io.BytesIO()
        pq.write_table(t, buf)
        stamp = d.replace("-", "") + "T100000Z"
        s.put(homes.address("rivalfunds", "etfs", "gold", "security_market", f"date={d}", f"market-{stamp}-aaaaaaaaaaaa.parquet"),
              buf.getvalue())


def _search(name, url="https://example.test/tkm", effective="October 7, 2026"):
    """The injected search. `effective` MUST be the move's own date: the lookup takes the ex-date a result names within 30 days
    of the move, and a row ex-dated after the page's as-of date is (correctly) not applied by that page."""
    def search(q):
        if name in q and "stock split" in q:
            return [{"title": f"{name} announces 15-for-1 stock split", "url": url,
                     "snippet": f"{name} will conduct a 15-for-1 stock split effective {effective}."}]
        return []
    return search


def test_ac1_a_find_is_read_by_the_page_of_the_day_it_was_found(tmp_path):
    s = sinks.LocalSink(str(tmp_path / "with_lookup"))
    _put_g4(s, CLOSES)
    rep = dm.run_for_day(DAY, s, search=_search(NAME))
    assert rep["candidates"] == 1 and rep["written"] == 1 and rep["failed"] == 0
    asof = dt.date.fromisoformat(hc.as_of(DAY))
    assert asof == dt.date(2026, 10, 7)
    out = price_series.load(s, [K], dt.date(2026, 10, 1), asof)[K]   # the call publish_page._build_charts makes
    assert [(a["event_type"], a["ratio"], a["ex_date"], a["claim"], a["source_url"]) for a in out["adjustment"]] == \
        [("split", 15.0, "2026-10-07", "INFERRED", "https://example.test/tkm")]
    vals = [p[1] for p in out["points"] if p[1] is not None]
    assert len(vals) == 5 and max(vals) / min(vals) < 1.1 and out["gaps"] == []
    # CONTROL: the same closes with no lookup run leave the move a gap with the stated reason
    c = sinks.LocalSink(str(tmp_path / "no_lookup"))
    _put_g4(c, CLOSES)
    ctl = price_series.load(c, [K], dt.date(2026, 10, 1), asof)[K]
    assert ctl["adjustment"] == [] and ctl["gaps"] and ctl["gaps"][0]["reason"] == BIG
    # a second run reads the stored row back and searches nothing
    q = []
    again = dm.run_for_day(DAY, s, search=lambda x: q.append(x) or [])
    assert again["candidates"] == 0 and again["calls"] == 0 and q == []


@pytest.fixture
def spec(tmp_path, monkeypatch):
    monkeypatch.setenv("RIVALFUNDS_PRODUCE_A1", "1")
    monkeypatch.setenv(guardrails.OVERRIDE_ENV, json.dumps({"min_resolved_fraction": 0.0}))
    sp = f"local:{tmp_path}"
    s = sinks.get_sink(sp)
    for step, d in enumerate(("2026-09-25", "2026-09-28", tp2.DAY)):
        tp2._put(s, d, {"TXUE": (tp2._book(step), "bloomberg", 0.1 * step), "BASG": (tp2._book(step), "issuer", 0.1 * step)})
    from rivalfunds import gold_trade_schedule
    assert gold_trade_schedule.handler_entry({"date": tp2.DAY, "mode": "replay", "batch_id": "g", "sink": sp})["status"] == "OK"
    return sp


PLANT_KEY, PLANT_NAME = "S00", "Name S00"     # a security the p2 fixture's TXUE dialog carries (its chart object lists S00..S09)
PLANT_DAY = "2026-09-30"                      # hc.as_of(PLANT_DAY) is 2026-09-29, the last date the chart's series reads


def _plant(s):
    asof = hc.as_of(PLANT_DAY)
    assert asof == "2026-09-29"
    _put_g4(s, [("2026-09-24", 150.0), ("2026-09-25", 151.0), ("2026-09-28", 149.0), (asof, 10.0)], key=PLANT_KEY, name=PLANT_NAME)


def _chart(spec, day=PLANT_DAY):
    return json.loads(sinks.get_sink(spec).get(homes.page(day, "charts/TXUE.json")))["securities"][PLANT_KEY]


def test_ac2_control_the_planted_move_with_no_lookup_is_a_gap_on_the_published_chart(spec):
    _plant(sinks.get_sink(spec))
    publish_page.handler_entry(tp2._ev(spec, day=PLANT_DAY))
    sec = _chart(spec)
    assert sec["adjustment"] == [] and any(g["reason"] == BIG for g in sec["gaps"])


def test_ac2_the_published_chart_object_carries_the_find(spec):
    s = sinks.get_sink(spec)
    _plant(s)
    rep = dm.run_for_day(PLANT_DAY, s, search=_search(PLANT_NAME, "https://example.test/planted", "September 29, 2026"))
    assert rep["written"] == 1 and rep["failed"] == 0
    publish_page.handler_entry(tp2._ev(spec, day=PLANT_DAY))      # the sweep's order: the lookup, then the day's publish
    sec = _chart(spec)
    assert [(a["event_type"], a["ratio"], a["claim"], a["source_url"]) for a in sec["adjustment"]] ==         [("split", 15.0, "INFERRED", "https://example.test/planted")]
    assert sec["adjustment"][0]["ex_date"] == "2026-09-29"
    drawn = [p for p in sec["points"] if p[0] >= "2026-09-24" and p[1] is not None]
    assert len(drawn) >= 4 and max(p[1] for p in drawn) / min(p[1] for p in drawn) < 1.2
