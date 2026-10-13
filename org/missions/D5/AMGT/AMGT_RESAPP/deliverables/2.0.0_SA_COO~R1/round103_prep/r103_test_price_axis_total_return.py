"""integrations/bloomberg/research/tests/test_price_axis_total_return.py -- AMGT-bj-5.

The total-return leg of the research price axis (Andrew-direct 2026-10-13, TWR pricing on every surface): a second request for DAY_TO_DAY_TOT_RETURN_GROSS_DVDS over the last FIVE
trading days, kept write-once beside the PX_LAST history, that can never change the PX_LAST legs, their writes or the script's exit code. Offline: a fake client stands in for blpapi and
`store.bronze_put` is captured; no Bloomberg or AWS call is made.

Run: python -m pytest integrations/bloomberg/research/tests/test_price_axis_total_return.py -q
"""
from __future__ import annotations

import datetime as dt
import inspect
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
for p in (os.path.join(REPO_ROOT, "integrations", "bloomberg", "mcp"), os.path.join(REPO_ROOT, "integrations", "bloomberg", "research"), REPO_ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

import price_axis_pull as pap  # noqa: E402
import price_series_persist as psp  # noqa: E402

TR = "DAY_TO_DAY_TOT_RETURN_GROSS_DVDS"


class FakeBlp:
    def __init__(self, rows_by_security=None, boom=False):
        self.calls = []
        self.rows_by_security = rows_by_security or {}
        self.boom = boom

    def historical_data(self, securities, fields, start, end, periodicity, timeout_s=0.0):
        self.calls.append({"securities": list(securities), "fields": list(fields), "start": start, "end": end, "periodicity": periodicity})
        if self.boom:
            raise RuntimeError("terminal not signed in")
        return {s: self.rows_by_security.get(s, []) for s in securities}


def test_window_is_the_last_five_trading_days_inclusive():
    # Monday 2026-10-12 back through Fri 9, Thu 8, Wed 7, Tue 6
    assert pap.tr_window_start(dt.date(2026, 10, 12)) == dt.date(2026, 10, 6)
    # across Thanksgiving 2026 (Thu 11-26 closed): Fri 11-27, Wed 25, Tue 24, Mon 23, Fri 20
    assert pap.tr_window_start(dt.date(2026, 11, 27)) == dt.date(2026, 11, 20)
    assert pap.TR_WINDOW_TRADING_DAYS == 5


def test_pull_requests_only_the_total_return_field_in_groups_of_twenty():
    securities = ["T%02d US Equity" % i for i in range(45)]
    sec_to_ticker = {s: s.split()[0] for s in securities}
    fake = FakeBlp({
        "T00 US Equity": [{"date": "2026-10-09", TR: 0.4}, {"date": "2026-10-12", TR: -0.2}, {"date": "2026-10-08", TR: None}],
        "T01 US Equity": [],
    })
    out = pap.pull_total_return(fake, securities, sec_to_ticker, dt.date(2026, 10, 6), dt.date(2026, 10, 12))
    assert [len(c["securities"]) for c in fake.calls] == [20, 20, 5]
    assert all(c["fields"] == [TR] and c["start"] == "20261006" and c["end"] == "20261012" and c["periodicity"] == "DAILY" for c in fake.calls)
    assert out == {"T00": [("2026-10-09", 0.4), ("2026-10-12", -0.2)]}  # a row without the field is dropped, a name with none is absent


def test_the_leg_never_raises_and_a_dry_run_persists_nothing(monkeypatch):
    lines = []
    boom = pap.run_total_return_leg(FakeBlp(boom=True), ["A US Equity"], {"A US Equity": "A"}, dt.date(2026, 10, 12), "2026-10-12", False, lines.append)
    assert boom["error"].startswith("RuntimeError") and boom["persisted"] is None
    assert any("WARN: total-return leg could not run" in x for x in lines)

    captured = []
    monkeypatch.setattr(psp, "persist_tr_series", lambda *a, **k: captured.append((a, k)) or {})
    ok_blp = FakeBlp({"A US Equity": [{"date": "2026-10-12", TR: 0.1}]})
    dry = pap.run_total_return_leg(ok_blp, ["A US Equity"], {"A US Equity": "A"}, dt.date(2026, 10, 12), "2026-10-12", True, lines.append)
    assert dry["pulled"] == 1 and dry["persisted"] is None and captured == []


def test_persisted_object_is_write_once_under_its_own_table(monkeypatch):
    from lib.research.harvest import store

    puts = []

    def fake_put(source, table, partition, object_name, body, **kw):
        puts.append((source, table, partition, object_name, body))
        return {"uri": "s3://x/" + table, "put_performed": True, "existed": False}

    monkeypatch.setattr(store, "bronze_put", fake_put)
    receipt = psp.persist_tr_series("2026-10-12", "2026-10-06", "2026-10-12", {"B": [("2026-10-12", 0.2)], "A": [("2026-10-09", 0.1)]}, client=object())
    assert receipt["put_performed"] is True
    source, table, partition, name, body = puts[0]
    assert (source, table, partition, name) == ("bloomberg", "price_history_tot_return", "date=2026-10-12", "daily_5d.json")
    doc = psp.tr_series_doc("2026-10-12", "2026-10-06", "2026-10-12", {"B": [("2026-10-12", 0.2)], "A": [("2026-10-09", 0.1)]})
    assert doc["schema"] == "price_tot_return_series_v1" and doc["field"] == TR and list(doc["series"]) == ["A", "B"]
    assert psp.TABLE != psp.TABLE_TR and psp.OBJECT_NAMES[psp.KIND_DAILY] == "daily_30d.json"  # the PX_LAST history is untouched


def test_the_px_last_leg_and_its_window_are_unchanged():
    src = inspect.getsource(pap.main)
    assert '["PX_LAST"], start_ymd, end_ymd, "DAILY"' in src
    assert pap.WINDOW_DAYS == 30
    # the leg is called AFTER the window step and BEFORE the exit-code logic, and its result is not read
    assert src.index("price_series_persist.run_daily_window_step") < src.index("run_total_return_leg(") < src.index("failed = [p")
    assert "= run_total_return_leg(" not in src
