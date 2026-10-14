"""RIV-xe-3 checks (round 30): `gold_trade_schedule.load_actions` reads the UNION of every pull's actions per security, de-duplicated
on the action's own key, the LATEST pull winning on a key collision (CTO msg 5577; the precondition of RIV-xe-2's incremental pull).

    cd data/etfs/scripts && python -m pytest -q <this file>

Offline: a local sink, no S3. The rule this file pins:
  * an EVENT row (`row_kind == "event"`) is kept from EVERY pull; its key is (`security_id`, `event_type`, `raw_event_type`,
    `ex_date`), a column the frame lacks reading as ""; of several rows with one key the row of the greatest (`as_of`, `revision`)
    pull is kept;
  * a STATUS row (`row_kind == "status"`) follows the rule as it was: kept only when it belongs to the security's LATEST pull;
  * the return is the same triple (rows | None, a label of the revisions read, the object uris); the label joins the sorted
    revisions of the rows returned; an empty store returns (None, None, []).
The live-store arm (DELTA = 0 against today's G5 output) is the issuer's drain act, not a worker criterion.
"""
import datetime as dt
import io

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from rivalfunds import gold_trade_schedule as g
from rivalfunds import homes, sinks

D = "2026-09-29"


def _s(v):
    return "" if pd.isna(v) else str(v)


def _row(sec, et, ex, amount, rev, as_of, kind="event", raw=None):
    r = {"row_kind": kind, "security_id": sec, "event_type": et, "ex_date": dt.date.fromisoformat(ex) if ex else None,
         "amount": amount, "raw_amount": amount, "revision": rev, "as_of": as_of, "record_seq": 0, "status": "OK" if kind == "event" else "NO_RECORDS"}
    if raw is not None:
        r["raw_event_type"] = raw
    return r


def _put(s, name, rows):
    df = pd.DataFrame(rows)
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(df, preserve_index=False), buf)
    s.put(homes.address("rivalfunds", "etfs", "gold", "corporate_actions", f"date={D}", f"{name}.parquet"), buf.getvalue())


def _old_rule(frames):
    """The reader as it was: per security only the rows of its latest pull."""
    df = pd.concat(frames, ignore_index=True)
    key = df["as_of"].astype(str) + "|" + df["revision"].astype(str)
    return df[key == key.groupby(df["security_id"]).transform("max")]


def test_ac1_a_short_incremental_pull_keeps_every_older_action(tmp_path):
    s = sinks.get_sink(f"local:{tmp_path}")
    full = [_row("A US Equity", "split", "2026-03-02", 2.0, "full", dt.date(2026, 9, 1), raw="Stock Split"),
            _row("A US Equity", "cash_div", "2026-06-01", 0.5, "full", dt.date(2026, 9, 1), raw="Regular Cash")]
    short = [_row("A US Equity", "cash_div", "2026-09-25", 0.6, "short", dt.date(2026, 9, 30), raw="Regular Cash")]
    _put(s, "actions-full", full)
    _put(s, "actions-short", short)
    df, label, uris = g.load_actions(s)
    got = sorted((r.event_type, str(r.ex_date)) for r in df.itertuples())
    assert got == [("cash_div", "2026-06-01"), ("cash_div", "2026-09-25"), ("split", "2026-03-02")]   # old rule: only the short pull's row
    assert len(uris) == 2 and "full" in label and "short" in label


def test_ac2_the_same_action_in_two_pulls_appears_once_with_the_latest_pulls_values(tmp_path):
    s = sinks.get_sink(f"local:{tmp_path}")
    # the LATER pull's object sorts FIRST by name: the answer must not depend on listing order
    _put(s, "a-late", [_row("B US Equity", "cash_div", "2026-06-01", 2.0, "late", dt.date(2026, 9, 30), raw="Regular Cash")])
    _put(s, "z-early", [_row("B US Equity", "cash_div", "2026-06-01", 1.0, "early", dt.date(2026, 9, 1), raw="Regular Cash"),
                        # the same date and type but a different raw type is a DIFFERENT action (a special beside a regular)
                        _row("B US Equity", "cash_div", "2026-06-01", 9.0, "early", dt.date(2026, 9, 1), raw="Special Cash")])
    df, label, _ = g.load_actions(s)
    rows = sorted((r.raw_event_type, r.amount, r.revision) for r in df.itertuples())
    assert rows == [("Regular Cash", 2.0, "late"), ("Special Cash", 9.0, "early")]


def test_ac3_status_rows_follow_the_old_rule_and_full_snapshots_read_as_before(tmp_path):
    s = sinks.get_sink(f"local:{tmp_path}")
    first = [_row("C US Equity", "cash_div", "2026-05-01", 1.0, "p1", dt.date(2026, 9, 1), raw="Regular Cash"),
             _row("D US Equity", None, None, None, "p1", dt.date(2026, 9, 1), kind="status"),
             _row("E US Equity", "cash_div", "2026-04-01", 3.0, "p1", dt.date(2026, 9, 1), raw="Regular Cash")]
    second = [_row("C US Equity", "cash_div", "2026-05-01", 1.0, "p2", dt.date(2026, 9, 30), raw="Regular Cash"),
              _row("C US Equity", "cash_div", "2026-08-01", 1.1, "p2", dt.date(2026, 9, 30), raw="Regular Cash"),
              _row("D US Equity", "cash_div", "2026-07-01", 4.0, "p2", dt.date(2026, 9, 30), raw="Regular Cash"),
              _row("E US Equity", None, None, None, "p2", dt.date(2026, 9, 30), kind="status")]
    _put(s, "actions-p1", first)
    _put(s, "actions-p2", second)
    df, _, _ = g.load_actions(s)
    by = {sec: sorted((r.row_kind, _s(r.ex_date), r.revision) for r in df[df["security_id"] == sec].itertuples())
          for sec in ("C US Equity", "D US Equity", "E US Equity")}
    assert by["C US Equity"] == [("event", "2026-05-01", "p2"), ("event", "2026-08-01", "p2")]   # a full snapshot: as before
    assert by["D US Equity"] == [("event", "2026-07-01", "p2")]                                    # its old status row is superseded
    assert by["E US Equity"] == [("event", "2026-04-01", "p1"), ("status", "", "p2")]          # the event stays; the status row is the latest pull's
    # where every later pull is a full snapshot (a superset), the new reader equals the old rule on the rows it keeps
    only_full = [pd.DataFrame([r for r in second if r["security_id"] == "C US Equity"])]
    assert len(_old_rule(only_full)) == 2


def test_ac3_an_empty_store_returns_the_old_triple(tmp_path):
    assert g.load_actions(sinks.get_sink(f"local:{tmp_path}")) == (None, None, [])


def test_ac4_a_void_object_is_not_an_action_row_and_a_voided_action_does_not_come_back(tmp_path):
    """AMENDMENT 1 (row ETFS_RIVALS-D1-W40-S1): the union must honour `actions-void-*` objects as `price_series._voids` does: the
    (void_revision, normalised security_id) pairs they name drop the event rows of that pull, whatever the pull's age."""
    s = sinks.get_sink(f"local:{tmp_path}")
    full = [_row("A US Equity", "split", "2026-03-02", 2.0, "full", dt.date(2026, 9, 1), raw="Stock Split"),
            _row("A US Equity", "cash_div", "2026-06-01", 0.5, "full", dt.date(2026, 9, 1), raw="Regular Cash")]
    short = [_row("A US Equity", "cash_div", "2026-09-25", 0.6, "short", dt.date(2026, 9, 30), raw="Regular Cash")]
    other = [_row("B US Equity", "cash_div", "2026-05-01", 1.0, "full", dt.date(2026, 9, 1), raw="Regular Cash")]
    _put(s, "actions-full", full + other)
    _put(s, "actions-short", short)
    void = pd.DataFrame([{"void_revision": "full", "security_id": "A US Equity", "reason": "a wrong inferred split", "as_of": dt.date(2026, 10, 2)}])
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(void, preserve_index=False), buf)
    s.put(homes.address("rivalfunds", "etfs", "gold", "corporate_actions", f"date={D}", "actions-void-v1.parquet"), buf.getvalue())
    df, label, uris = g.load_actions(s)
    got = sorted((r.security_id, r.event_type, _s(r.ex_date)) for r in df.itertuples())
    # A's two rows of pull "full" are voided; A's short-pull row and B's row stay; the void object contributes no row
    assert got == [("A US Equity", "cash_div", "2026-09-25"), ("B US Equity", "cash_div", "2026-05-01")]
    assert "void_revision" not in df.columns and len(uris) == 3        # the void object is still listed in the lineage
