"""p199 PROBE (issuer 2.0.0_SA_COO~D2, IRPT_DASHBD round 150, cell DB-b-333): the issuer's own behaviour tests of the Cottonwood late-posting reader, written into the
worker's tree as data/assets/scripts/gold/irpt_reporting/tests/test_p199_probe.py by the checker `p199_cot_late_window.py`, run there with pytest and deleted. Synthetic data and fakes only; no network.

What a correct reader does (CTO rulings after dell1's finding, msg 7612): the fact_transactions silver partitions are ROLLING pulls, so one trade appears in many partitions and a day's trades can first
post in a LATER partition. A day's flows are read from the partitions from the window's first day through the 14th trading day after its last day, each TransactionID counted ONCE (the later partition's
copy replaces an earlier one); a day whose own partition is absent is still present when rows dated that day exist in that window; a scheduled fire rewrites, through the existing rewrite path, the
landed day 14 trading days before each day it owes.
"""
import importlib.util
import sys
from pathlib import Path

import pyarrow as pa
import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
sys.path.insert(0, str(ROOT / "lib"))
import trading_calendar as tc  # noqa: E402

MODULE = ROOT / "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py"
_spec = importlib.util.spec_from_file_location("cbd_p199_probe", str(MODULE))
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)

HANDLER_DIR = ROOT / "infra/aws/lambda/investor-reporting/account-return-daily"
sys.path.insert(0, str(HANDLER_DIR))
_hspec = importlib.util.spec_from_file_location("handler_p199_probe", str(HANDLER_DIR / "handler.py"))
h = importlib.util.module_from_spec(_hspec)
_hspec.loader.exec_module(h)

ACCT = "AB12345678C"
OTHER = "AB87654321D"
D, PREV = "2026-07-14", "2026-07-13"
AFTER = [x.isoformat() for x in tc.trading_days_between(D, "2026-09-30")][1:]   # AFTER[0] is the first trading day after D; AFTER[13] the 14th
FLOOR = "2026-07-10"


def alloc(pairs):
    return pa.table({"AccountID": [a for a, _v in pairs], "Account Market Value": [v for _a, v in pairs]})


def tx(rows):
    """rows: (TransactionID, AccountID, Trade Date, External Flow, Transaction Type, Market Value)."""
    cols = ["TransactionID", "AccountID", "Trade Date", "External Flow", "Transaction Type", "Market Value"]
    if not rows:
        return pa.table({c: pa.array([], pa.float64() if c == "Market Value" else pa.string()) for c in cols})
    return pa.table({c: [r[i] for r in rows] for i, c in enumerate(cols)})


class Reader:
    def __init__(self, allocations, transactions):
        self.allocations, self.transactions, self.read_days = allocations, transactions, []
        self.reads = 0  # the adapter's census reads this counter

    def list_partitions(self, table):
        return sorted((self.allocations if table == "fact_allocations" else self.transactions).keys())

    def read_parquet(self, table, day):
        self.reads += 1
        if table == "fact_transactions":
            self.read_days.append(day)
        return (self.allocations if table == "fact_allocations" else self.transactions)[day]


def contribution(tid, trade=D, mv=100.0, acct=ACCT):
    return (tid, acct, trade, "Contribution", "Cash Deposit", mv)


def window_reader(per_partition, alloc_days=None):
    allocations = alloc_days or {PREV: alloc([(ACCT, 1000.0), (OTHER, 500.0)]), D: alloc([(ACCT, 1200.0), (OTHER, 510.0)])}
    return Reader(allocations, {day: tx(rows) for day, rows in per_partition.items()})


def flow_of(reader):
    rows, _summary = m.derive(reader, {ACCT, OTHER}, PREV, D)
    return {r["account_id"]: r for r in rows if r["business_date"] == D}


def test_a_trade_repeated_in_twelve_rolling_partitions_counts_once():
    reader = window_reader({day: [contribution("T1")] for day in AFTER[:12]})
    assert flow_of(reader)[ACCT]["external_flow"] == pytest.approx(100.0)


def test_the_later_partitions_copy_of_a_transaction_replaces_an_earlier_one():
    per = {AFTER[0]: [contribution("T1", mv=50.0)], AFTER[1]: [contribution("T1", mv=50.0)]}
    per.update({day: [contribution("T1", mv=80.0)] for day in AFTER[2:6]})
    assert flow_of(window_reader(per))[ACCT]["external_flow"] == pytest.approx(80.0)


def test_a_trade_that_first_posts_late_inside_the_window_counts():
    per = {day: [contribution("T1")] for day in AFTER[:12]}
    per[AFTER[6]] = [contribution("T1"), contribution("T2", mv=25.0)]
    per.update({day: [contribution("T1"), contribution("T2", mv=25.0)] for day in AFTER[7:12]})
    assert flow_of(window_reader(per))[ACCT]["external_flow"] == pytest.approx(125.0)


def test_a_partition_after_the_fourteenth_trading_day_is_neither_read_nor_counted():
    per = {day: [contribution("T1")] for day in AFTER[:14]}
    per[AFTER[14]] = [contribution("T1"), contribution("T3", mv=999.0)]
    reader = window_reader(per)
    assert flow_of(reader)[ACCT]["external_flow"] == pytest.approx(100.0)
    assert AFTER[14] not in reader.read_days and AFTER[13] in reader.read_days


def test_the_flows_of_two_accounts_are_each_deduplicated():
    per = {day: [contribution("T1"), contribution("T9", mv=40.0, acct=OTHER)] for day in AFTER[:10]}
    got = flow_of(window_reader(per))
    assert got[ACCT]["external_flow"] == pytest.approx(100.0) and got[OTHER]["external_flow"] == pytest.approx(40.0)


def test_a_day_with_no_partition_of_its_own_is_present_when_rows_dated_it_post_later():
    per = {PREV: [], AFTER[0]: [contribution("T1")]}
    reader = window_reader({**per})
    assert D not in reader.list_partitions("fact_transactions")
    assert m.presence_hold(reader, D) is None


def test_a_day_with_rows_dated_it_only_beyond_the_window_is_held():
    reader = window_reader({PREV: [], AFTER[14]: [contribution("T1")]})
    held = m.presence_hold(reader, D)
    assert isinstance(held, str) and held.startswith("HOLD") and "fact_transactions" in held


def test_a_day_with_no_partition_and_no_rows_dated_it_is_held():
    held = m.presence_hold(window_reader({PREV: [], AFTER[0]: [contribution("T1", trade=PREV)]}), D)
    assert isinstance(held, str) and held.startswith("HOLD") and "fact_transactions" in held


def test_a_day_with_its_own_partition_is_present():
    assert m.presence_hold(window_reader({D: []}), D) is None


def test_run_day_derives_a_day_whose_own_partition_is_absent():
    reader = window_reader({AFTER[0]: [contribution("T1")], AFTER[1]: [contribution("T1")]})
    out = m.run_day(reader, None, D, upload=False)
    assert out["held"] is False and out["rows"] == 2


def test_a_day_written_early_then_rewritten_at_the_full_window_matches_the_full_window_value():
    early = window_reader({AFTER[0]: [contribution("T1")]})
    late = {day: [contribution("T1")] for day in AFTER[:3]}
    late.update({day: [contribution("T1"), contribution("T2", mv=25.0)] for day in AFTER[3:14]})
    full = window_reader(late)
    assert flow_of(early)[ACCT]["external_flow"] == pytest.approx(100.0)
    got = flow_of(full)[ACCT]
    assert got["external_flow"] == pytest.approx(125.0)          # the independent sum of the two distinct TransactionIDs
    assert got["total_return_daily"] == pytest.approx((1200.0 - 125.0) / 1000.0 - 1.0)


# ------------------------------------------------------------------------------------------------ the scheduled fire's settle

class S3:
    """list_objects_v2 answers a Delimiter LIST from the landed days and a plain LIST from the keys planted or put; put_object records."""

    def __init__(self, landed_days, existing_keys):
        self.landed, self.existing, self.puts = landed_days, list(existing_keys), []

    def list_objects_v2(self, **kw):
        if "Delimiter" in kw:
            return {"CommonPrefixes": [{"Prefix": "%sdate=%s/" % (kw["Prefix"], d)} for d in self.landed], "IsTruncated": False}
        keys = sorted(k for k in self.existing + [k for k in self.puts] if k.startswith(kw["Prefix"]))
        return {"KeyCount": len(keys), "Contents": [{"Key": k} for k in keys], "IsTruncated": False}

    def put_object(self, Bucket, Key, Body, **kw):
        self.puts.append(Key)
        return {}


def back_of(day, n=14):
    return [x.isoformat() for x in tc.trading_days_between(__import__("datetime").date.fromisoformat(day) - __import__("datetime").timedelta(days=3 * n), day)][-(n + 1)]


def test_settle_days_names_the_day_fourteen_trading_days_before_each_owed_day():
    bucket, prefix = m.gold_prefix()
    owed = "2026-08-04"
    back = back_of(owed)
    assert back >= FLOOR
    assert h.settle_days(S3([back], []), [owed]) == [back]
    assert h.settle_days(S3([], []), [owed]) == []                                  # the day is not landed: nothing to settle
    early = back_of("2026-07-20")
    assert early < FLOOR
    assert h.settle_days(S3([back, early], []), ["2026-07-20"]) == []               # 14 trading days back is before the floor, though it is landed
    assert h.settle_days(S3([back], []), [owed, back]) == []                        # a day that is itself owed is not settled
    assert h.settle_days(S3([back], []), [owed, owed]) == [back]


def fire_fixtures(monkeypatch, owed_day, back_day):
    prev_owed = tc.prev_trading_day(owed_day).isoformat()
    prev_back = tc.prev_trading_day(back_day).isoformat()
    allocations = {FLOOR: alloc([(ACCT, 900.0)]), prev_back: alloc([(ACCT, 1000.0)]), back_day: alloc([(ACCT, 1010.0)]),
                   prev_owed: alloc([(ACCT, 1100.0)]), owed_day: alloc([(ACCT, 1120.0)])}
    transactions = {d: tx([]) for d in allocations}
    transactions[owed_day] = tx([("T1", ACCT, owed_day, "None", "Dividend", 1.0)])
    reader = Reader(allocations, transactions)
    bucket, prefix = m.gold_prefix()
    key = lambda d: "%sdate=%s/data.parquet" % (prefix, d)  # noqa: E731
    s3 = S3([back_day], [key(back_day)])
    monkeypatch.setattr(h, "owed_days", lambda newest, today, max_days=h.MAX_DAYS_PER_FIRE: [owed_day])
    monkeypatch.setattr(h, "newest_landed_day", lambda s3_, b, p: prev_owed)
    monkeypatch.setattr(h, "emit_transactions", lambda s3_, reader_, days, upload: ({}, {}))
    return s3, reader


def test_a_scheduled_fire_rewrites_the_day_fourteen_trading_days_back(monkeypatch):
    owed = "2026-08-04"
    back = back_of(owed)
    s3, reader = fire_fixtures(monkeypatch, owed, back)
    out = h.lambda_handler({}, s3=s3, reader=reader)
    assert out["days"] == [owed] and sorted(out["settled"]) == [back] and out["settle_failed"] == {}
    assert out["settled"][back]["held"] is False
    assert any("date=%s/" % back in k for k in s3.puts) and any("date=%s/" % owed in k for k in s3.puts)
    assert all(("date=%s/" % back in k) or ("date=%s/" % owed in k) for k in s3.puts)         # no other day was written


def test_a_dry_scheduled_fire_writes_nothing_and_still_names_the_settled_day(monkeypatch):
    owed = "2026-08-04"
    back = back_of(owed)
    s3, reader = fire_fixtures(monkeypatch, owed, back)
    out = h.lambda_handler({"dry_run": True}, s3=s3, reader=reader)
    assert s3.puts == [] and sorted(out["settled"]) == [back]


def test_an_explicit_day_event_settles_nothing(monkeypatch):
    owed = "2026-08-04"
    back = back_of(owed)
    s3, reader = fire_fixtures(monkeypatch, owed, back)
    out = h.lambda_handler({"day": owed}, s3=s3, reader=reader)
    assert "settled" not in out or out["settled"] == {}
    assert not any("date=%s/" % back in k for k in s3.puts)


def test_a_failing_settle_never_changes_the_returns_result(monkeypatch):
    owed = "2026-08-04"
    back = back_of(owed)
    s3, reader = fire_fixtures(monkeypatch, owed, back)
    clean = h.lambda_handler({"dry_run": True}, s3=s3, reader=reader)
    real = h.cbd.run_day

    def broken(rd, s3_, day, **kw):
        if kw.get("rewrite"):
            raise RuntimeError("planted")
        return real(rd, s3_, day, **kw)
    monkeypatch.setattr(h.cbd, "run_day", broken)
    out = h.lambda_handler({"dry_run": True}, s3=s3, reader=reader)
    assert out["results"] == clean["results"] and out["ok"] is True
    assert list(out["settle_failed"]) == [back] and "planted" in out["settle_failed"][back]
