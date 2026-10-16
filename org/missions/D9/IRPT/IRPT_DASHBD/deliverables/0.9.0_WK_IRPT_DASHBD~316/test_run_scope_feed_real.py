"""Tests for run_scope_feed_real.py (IRPT_DASHBD round 129, cell DB-i-16, worker 0.9.0_WK_IRPT_DASHBD~316).

Every row here is SYNTHETIC: account ids are invented, the factors and values are round numbers, and nothing is read from
S3 or from the checker's fixtures. The reader is a local fake with a read counter; the out_dir lives in pytest's temp area.
Run: python -I -m pytest -q <this file>
"""
import datetime as dt
import importlib.util
import json
import re
from pathlib import Path

import pandas
import pytest

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "run_scope_feed_real.py"
_spec = importlib.util.spec_from_file_location("run_scope_feed_real_under_test", str(SCRIPT))
rs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rs)

FIRM = "FIRM-SYNTH"
RECORD_KEYS = {"status", "contract_version", "partitions_read", "s3_reads", "calendar_days_read", "calendar_days_incomplete",
               "rows_present", "rows_absent", "absent_by_reason", "accounts_in_feed", "accounts_mapped", "accounts_unmapped",
               "trading_days_unaccounted", "market_value_eod_claim_counts", "boundary", "chain", "method_version_used",
               "out_dir_private"}
COLUMNS = ["pull_date", "day", "account_id", "status", "reason_class", "daily_factor", "start_market_value",
           "end_market_value", "source"]


class FakeReader:
    """GET-only fake over {partition name: frame} for the scope_account_returns table, with a read counter."""

    def __init__(self, tables):
        self.tables = tables
        self.reads = 0

    def list_partitions(self, table_uri):
        self.reads += 1
        assert table_uri == rs.TABLE_URI
        return sorted(self.tables)

    def read_parquet(self, uri):
        self.reads += 1
        assert uri.endswith("/data.parquet")
        return self.tables[uri.split("/")[-2]]

    def latest_partition(self, table_uri):
        names = self.list_partitions(table_uri)
        return names[-1], self.read_parquet(table_uri + "/" + names[-1] + "/data.parquet")


def _row(account, day, factor=None, start=None, end=None, status="RETURNED", reason=None):
    return {"day": day, "account_id": account, "status": status, "reason_class": reason, "daily_factor": factor,
            "start_market_value": start, "end_market_value": end, "source": "orion_scope"}


def _partition(rows):
    """One date partition per day, pull_date equal to the day, as the feed writes it."""
    by_day = {}
    for r in rows:
        full = {c: None for c in COLUMNS}
        full.update(r)
        full["pull_date"] = r["day"]
        by_day.setdefault(r["day"], []).append(full)
    return {"date=%s" % d: pandas.DataFrame(v, columns=COLUMNS) for d, v in sorted(by_day.items())}


def _weekdays(first, last):
    a, b = dt.date.fromisoformat(first), dt.date.fromisoformat(last)
    out, d = [], a
    while d <= b:
        if d.weekday() < 5:
            out.append(d.isoformat())
        d += dt.timedelta(days=1)
    return out


def _small_feed():
    """Mon 2026-07-06 to Fri 2026-07-10: two mapped accounts (4001, 4002) and one unmapped (4009); every day RETURNED."""
    days = ["2026-07-06", "2026-07-07", "2026-07-08", "2026-07-09", "2026-07-10"]
    rows = []
    for acct, base in (("4001", 100.0), ("4002", 200.0), ("4009", 300.0)):
        for i, d in enumerate(days):
            last = i == len(days) - 1
            rows.append(_row(acct, d, factor=1.001, start=base + i, end=(base + 50.0) if last else None))
    return _partition(rows)


def _run(reader, out, dim_ids=("4001", "4002"), max_reads=400):
    return rs.run_real(reader, str(out), list(dim_ids), _weekdays, FIRM, 0, max_reads)


def _chain_fixture(first, n_days, account="6001", drop_table_day=None):
    """n_days calendar days from first, one account with a RETURNED factor every day; the table holds one PRESENT row per
    trading day (weekday) carrying the product of the factors since the previous trading day. drop_table_day omits one."""
    start = dt.date.fromisoformat(first)
    days = [(start + dt.timedelta(days=i)).isoformat() for i in range(n_days)]
    factor = {d: 1.0 + (((i * 7) % 11) - 5) * 0.0004 for i, d in enumerate(days)}
    trading = [d for d in days if dt.date.fromisoformat(d).weekday() < 5]
    silver_rows = [_row(account, d, factor=factor[d], start=100.0) for d in days]
    table, prev = [], None
    for t in trading:
        span = [d for d in days if (prev is None or d > prev) and d <= t]
        prod = 1.0
        for d in span:
            prod *= factor[d]
        if t != drop_table_day:
            table.append({"row_status": "PRESENT", "source_account_id": int(account), "business_date": t,
                          "total_return_daily": prod - 1.0})
        prev = t
    return _partition(silver_rows), table, trading, days[0], days[-1]


def test_run_real_ran_record_keys_and_counts(tmp_path):
    reader = FakeReader(_small_feed())
    out = tmp_path / "out"
    rec = _run(reader, out, dim_ids=("4001", "4002", "4003"))
    assert rec["status"] == "RAN"
    assert set(rec) == RECORD_KEYS
    assert rec["partitions_read"] == 5 and rec["calendar_days_read"] == 5 and rec["calendar_days_incomplete"] == 0
    assert rec["rows_present"] == 10 and rec["rows_absent"] == 5
    assert rec["accounts_in_feed"] == 3 and rec["accounts_mapped"] == 2 and rec["accounts_unmapped"] == 1
    assert rec["trading_days_unaccounted"] == 0
    assert rec["absent_by_reason"] == {"UNMAPPED_ACCOUNT": 5}
    assert rec["market_value_eod_claim_counts"] == {"inferred": 8, "measured": 2}
    assert rec["s3_reads"] == 6 and reader.reads == 6
    assert rec["method_version_used"] == 0 and rec["out_dir_private"] is True
    assert rec["boundary"] == {"pairs": 0, "pairs_equal": 0, "max_rel_diff_bp": None}
    assert rec["chain"]["status"] == "WINDOW_TOO_SHORT" and rec["chain"]["window_calendar_days"] == 5
    assert (out / "run_record.json").is_file()


def test_no_silver_yet_reads_once_and_writes_nothing(tmp_path):
    reader = FakeReader({})
    out = tmp_path / "out"
    rec = _run(reader, out)
    assert rec == {"status": "NO_SILVER_YET", "partitions_listed": 0, "s3_reads": 1}
    assert reader.reads == 1
    assert not out.exists()


def test_stopped_at_cap_makes_only_the_list(tmp_path):
    reader = FakeReader(_small_feed())
    out = tmp_path / "out"
    rec = _run(reader, out, max_reads=3)
    assert rec == {"status": "STOPPED_AT_CAP", "partitions_listed": 5, "s3_reads": 1}
    assert reader.reads == 1
    assert not out.exists()


def test_non_empty_out_dir_is_refused_with_nothing_read_back(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    (out / "stray.txt").write_text("x", encoding="ascii")
    reader = FakeReader(_small_feed())
    with pytest.raises(ValueError):
        _run(reader, out)
    assert sorted(p.name for p in out.iterdir()) == ["stray.txt"]


def test_zero_row_partitions_return_no_rows_and_write_nothing(tmp_path):
    empty = pandas.DataFrame(columns=COLUMNS)
    reader = FakeReader({"date=2026-07-06": empty, "date=2026-07-07": empty})
    out = tmp_path / "out"
    rec = _run(reader, out)
    assert rec == {"status": "NO_ROWS", "partitions_listed": 2, "s3_reads": 3}
    assert not out.exists()


def test_boundary_measure_equal_unequal_nan_and_missing_neighbours():
    rows = [
        _row("5001", "2026-07-06", factor=1.0, start=100.0, end=101.0),
        _row("5001", "2026-07-07", factor=1.0, start=101.0, end=103.0),
        _row("5001", "2026-07-08", factor=1.0, start=105.0, end=None),
        _row("5002", "2026-07-06", factor=1.0, start=10.0, end=float("nan")),
        _row("5002", "2026-07-07", factor=1.0, start=50.0, end=60.0),
        _row("5003", "2026-07-06", factor=1.0, start=10.0, end=10.0),
        _row("5004", "2026-07-06", factor=1.0, start=10.0, end=10.0),
        _row("5004", "2026-07-07", factor=None, start=None, end=None, status="ABSENT", reason="NO_FEED_ROW"),
        _row("5005", "2026-07-06", factor=1.0, start=10.0, end=10.0),
        _row("5005", "2026-07-07", factor=1.0, start=float("nan"), end=20.0),
    ]
    pairs, equal, worst = rs.measure_boundary(_partition(rows))
    # 5001: (07-06, 07-07) diff 0 (equal); (07-07, 07-08) diff 2 on start 105 = 190.476... bp -> 190.48.
    # 5002: NaN end on 07-06 -> no pair. 5003: no 07-07 row. 5004: ABSENT neighbour. 5005: NaN start on 07-07.
    assert (pairs, equal, worst) == (2, 1, 190.48)


def test_boundary_measure_with_no_end_values_is_none():
    rows = [_row("5001", "2026-07-06", factor=1.0, start=100.0, end=None),
            _row("5001", "2026-07-07", factor=1.0, start=101.0, end=None)]
    assert rs.measure_boundary(_partition(rows)) == (0, 0, None)


def test_chain_check_ok_on_a_299_day_window():
    silver, table, trading, start, end = _chain_fixture("2026-01-05", 299)
    res = rs.chain_check(table, silver, trading, start, end)
    assert res["status"] == "OK" and res["window_calendar_days"] == 299
    assert res["accounts_checked"] == 1 and res["accounts_matching"] == 1
    assert res["max_abs_diff_bp"] is not None and res["max_abs_diff_bp"] <= 1e-6


def test_chain_check_mismatch_on_an_altered_row():
    silver, table, trading, start, end = _chain_fixture("2026-01-05", 299)
    bad = [dict(r) for r in table]
    bad[10]["total_return_daily"] += 0.001
    res = rs.chain_check(bad, silver, trading, start, end)
    assert res["status"] == "MISMATCH" and res["accounts_checked"] == 1 and res["accounts_matching"] == 0
    assert res["max_abs_diff_bp"] > 1e-6


def test_chain_check_window_too_short_under_238_and_accepts_238():
    silver, table, trading, start, end = _chain_fixture("2026-01-05", 237)
    short = rs.chain_check(table, silver, trading, start, end)
    assert short == {"status": "WINDOW_TOO_SHORT", "window_calendar_days": 237, "accounts_checked": 0,
                     "accounts_matching": 0, "max_abs_diff_bp": None}
    silver, table, trading, start, end = _chain_fixture("2026-01-05", 238)
    assert rs.chain_check(table, silver, trading, start, end)["status"] == "OK"


def test_chain_check_no_complete_account_when_a_trading_day_is_missing():
    silver, table, trading, start, end = _chain_fixture("2026-01-05", 299, drop_table_day="2026-03-02")
    res = rs.chain_check(table, silver, trading, start, end)
    assert res == {"status": "NO_COMPLETE_ACCOUNT", "window_calendar_days": 299, "accounts_checked": 0,
                   "accounts_matching": 0, "max_abs_diff_bp": None}


def test_record_is_whitelisted_ascii_and_carries_no_date_or_eight_digit_run(tmp_path):
    reader = FakeReader(_small_feed())
    rec = _run(reader, tmp_path / "out")
    text = json.dumps(rec, sort_keys=True, indent=2)
    assert set(rec) == RECORD_KEYS
    assert text.isascii()
    assert re.search(r"\d{4}-\d{2}-\d{2}", text) is None and "date=" not in text
    assert re.search(r"\d{8,}", text) is None


def test_mutant_window_floor_changed_to_five_days_is_detected():
    """Mutant: the 238-day floor is changed to 5 in the script's own source text, executed as a module with the real
    __file__, and the 7-day case must then read differently (the original reads WINDOW_TOO_SHORT)."""
    source = SCRIPT.read_text(encoding="ascii")
    assert source.count("MIN_WINDOW_DAYS = 238") == 1
    mutated = source.replace("MIN_WINDOW_DAYS = 238", "MIN_WINDOW_DAYS = 5")
    ns = {"__file__": str(SCRIPT), "__name__": "mutant_run_scope_feed_real"}
    exec(compile(mutated, str(SCRIPT), "exec"), ns)
    silver, table, trading, start, end = _chain_fixture("2026-01-05", 7)
    original = rs.chain_check(table, silver, trading, start, end)
    mutant = ns["chain_check"](table, silver, trading, start, end)
    assert original["status"] == "WINDOW_TOO_SHORT"
    assert mutant["status"] == "OK" and mutant != original
