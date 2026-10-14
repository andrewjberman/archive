"""RIV-xe-1 checks (round 30): the enrichment leg (1) runs on TRADING days only and (2) reads the standing request's queue state before
a history-owed draw and fails closed (analysis ruling; CTO msg 4568; row D1-S2; round-22 ADDENDUM 7, condition 1).

    cd data/etfs/scripts && python -m pytest -q <this file>

Offline: no S3, no Bloomberg. The rule this file pins:
  GATE   `enrichment_bloomberg.main(argv)`: with NO `--date` and `--mode` in (`daily`, `market`), when `_run_date_et()` is not a trading day
         by `lib.trading_calendar.is_trading_day`, it prints ONE line beginning `SKIP:` and returns 0 WITHOUT calling `handler_entry`.
         An explicit `--date` run, any other mode, and a trading day are not gated.
  READER `_queue_state() -> str`: `data.mdpf.scripts.demque.standing.read_state("ETFS_RIVALS-HISTORY-OWED-DAILY")`, imported lazily; any
         exception (an ImportError included) returns "unreadable". In `_history_owed(mode="ask", ...)`, after the owed set is computed and
         BEFORE any stored-currency read or Bloomberg request: state `active` proceeds as before; any other state asks ZERO (no `_blp_call`),
         prints ONE `HISTORY OWED:` line naming the state, and returns asked 0, carried = owed, `refused` naming the state.
         `print` mode does not read the state.
"""
import datetime as dt

import pandas as pd
import pytest

from rivalfunds import bbg_budget, history_owed, sinks
from rivalfunds import enrichment_bloomberg as eb

SAT, SUN, LABOR_DAY, TUE = dt.date(2026, 10, 10), dt.date(2026, 10, 11), dt.date(2026, 9, 7), dt.date(2026, 10, 13)


@pytest.fixture
def leg(monkeypatch):
    calls = []
    monkeypatch.setattr(eb, "handler_entry", lambda ev, context=None: calls.append(ev) or {"status": "OK", "outputs": [], "detail": None})
    return calls


def _run(monkeypatch, capsys, day, argv):
    monkeypatch.setattr(eb, "_run_date_et", lambda: day)
    rc = eb.main(argv)
    return rc, [ln for ln in capsys.readouterr().out.splitlines() if ln.strip()]


@pytest.mark.parametrize("day", [SAT, SUN, LABOR_DAY])
def test_ac1_a_non_trading_day_prints_one_skip_line_and_exits_zero_without_the_leg(monkeypatch, capsys, leg, day):
    for mode in ("daily", "market"):
        rc, lines = _run(monkeypatch, capsys, day, ["--mode", mode])
        assert rc == 0 and len(lines) == 1 and lines[0].startswith("SKIP:")
    assert leg == []                                   # the leg never ran


def test_ac1_a_trading_day_an_explicit_date_and_other_modes_are_not_gated(monkeypatch, capsys, leg):
    rc, lines = _run(monkeypatch, capsys, TUE, ["--mode", "daily"])
    assert rc == 0 and len(leg) == 1 and not any(ln.startswith("SKIP:") for ln in lines)
    rc, lines = _run(monkeypatch, capsys, SAT, ["--mode", "daily", "--date", "2026-10-09"])
    assert len(leg) == 2 and leg[1]["date"] == "2026-10-09" and not any(ln.startswith("SKIP:") for ln in lines)
    _run(monkeypatch, capsys, SAT, ["--mode", "plan-market"])
    assert len(leg) == 3                               # plan-market is offline QA: not gated


def test_ac1_the_calendar_is_the_source_not_a_typed_list(monkeypatch, capsys, leg):
    from lib import trading_calendar as tc
    monkeypatch.setattr(tc, "is_trading_day", lambda d: False)       # a Tuesday the calendar calls closed
    rc, lines = _run(monkeypatch, capsys, TUE, ["--mode", "daily"])
    assert rc == 0 and len(lines) == 1 and lines[0].startswith("SKIP:") and leg == []


# ----------------------------------------------------------------------------------------------------------- the queue-state reader
@pytest.fixture
def owed(monkeypatch, tmp_path):
    asked = []
    df = pd.DataFrame([{"security_id": "A US Equity", "security_bloomberg": "A US Equity", "date": "2026-10-09", "funds": "TXUE"},
                       {"security_id": "B US Equity", "security_bloomberg": "B US Equity", "date": "2026-10-09", "funds": "TXUE"}])
    monkeypatch.setattr(history_owed, "owed", lambda s, day, *a, **k: df)
    monkeypatch.setattr(eb, "_stored_currencies", lambda *a, **k: {})
    monkeypatch.setattr(bbg_budget, "check_points", lambda n: None)
    monkeypatch.setattr(bbg_budget, "record", lambda *a, **k: None)
    monkeypatch.setattr(eb, "_blp_call", lambda fn, *a, **k: asked.append(fn.__name__) or {})
    return sinks.get_sink(f"local:{tmp_path}"), asked


def _ask(s, capsys):
    res = eb._history_owed("ask", {}, s, "2026-10-09", "b1", "2026-10-13T11:00:00Z")
    return res, [ln for ln in capsys.readouterr().out.splitlines() if ln.startswith("HISTORY OWED:")]


def test_ac2_an_active_queue_state_draws_as_before(monkeypatch, capsys, owed):
    s, asked = owed
    monkeypatch.setattr(eb, "_queue_state", lambda: "active")
    res, lines = _ask(s, capsys)
    assert asked and res["mode"] == "ask" and "refused" not in res and len(lines) == 1


@pytest.mark.parametrize("state", ["paused", "stopped", "unreadable", "banana"])
def test_ac2_any_other_state_draws_zero_and_names_the_state(monkeypatch, capsys, owed, state):
    s, asked = owed
    monkeypatch.setattr(eb, "_queue_state", lambda: state)
    res, lines = _ask(s, capsys)
    assert asked == []                                                    # not one Bloomberg call, a currency lookup included
    assert res["asked"] == 0 and res["carried"] == res["owed"] == 2 and state in res["refused"]
    assert len(lines) == 1 and state in lines[0]


def test_ac2_the_reader_fails_closed_and_print_mode_does_not_read_it(monkeypatch, capsys, owed):
    s, asked = owed
    import data.mdpf.scripts.demque.standing as standing
    monkeypatch.setattr(standing, "read_state", lambda request_id, s3=None: (_ for _ in ()).throw(OSError("denied")))
    assert eb._queue_state() == "unreadable"
    seen = []
    monkeypatch.setattr(standing, "read_state", lambda request_id, s3=None: seen.append(request_id) or "paused")
    assert eb._queue_state() == "paused" and seen == ["ETFS_RIVALS-HISTORY-OWED-DAILY"]
    monkeypatch.setattr(eb, "_queue_state", lambda: (_ for _ in ()).throw(AssertionError("print mode must not read the state")))
    res = eb._history_owed("print", {}, s, "2026-10-09", "b1", "2026-10-13T11:00:00Z")
    assert res["mode"] == "print" and asked == []
