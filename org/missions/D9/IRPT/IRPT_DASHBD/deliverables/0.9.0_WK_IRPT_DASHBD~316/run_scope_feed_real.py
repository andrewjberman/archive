"""IRPT_DASHBD round 129, workstream B-IN (issuer 2.0.0_SA_COO~I2), cell DB-i-16 -- the first-real-row RUN script.

Reads the Scope feed's silver table (scope_account_returns) through the round-108 GET-only reader, hands the partitions to
the round-127 wrapper (inflection_scope_feed_run.run) with a PRIVATE local output directory, and returns counts only:
the Orion boundary measure (startValue(t+1) against endValue(t)) and a chain check over a 238-to-365-day window.
When the silver does not exist yet the result is NO_SILVER_YET (one LIST, nothing written); a read cap gives
STOPPED_AT_CAP (the LIST only, nothing written). No write call, no vendor call, no secret: the reader is GET-only and
the only files written are the private directory the wrapper fills and the record file named on the command line.

The chain check compares the table's chained PRESENT rows with the product of the silver's own daily factors (a
consistency check of the adapter and the wrapper on real rows). It is NOT a comparison with Orion's reported period
return: that needs a vendor call and a window the backfill provides, and is outside this script.

Usage: python -I run_scope_feed_real.py --out-dir <absent or empty private dir> --record <record.json>
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import pandas
import pyarrow.parquet as pq


def _find_root() -> Path:
    here = Path(__file__).resolve()
    for anc in here.parents:
        if (anc / "lib" / "trading_calendar.py").is_file() and (anc / "data").is_dir():
            return anc
    raise SystemExit("repo root not found above this file")


ROOT = _find_root()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "data" / "assets" / "scripts" / "gold" / "irpt_reporting" / "adapters"))
from lib import trading_calendar as tc  # noqa: E402
import inflection_account_dim as iad  # noqa: E402
import inflection_account_return_daily as iar  # noqa: E402
import inflection_scope_feed_run as wrap  # noqa: E402

TABLE_URI = iar.ORION_SILVER + "scope_account_returns"
MIN_WINDOW_DAYS = 238
CHAIN_SPAN_DAYS = 364
MATCH_BP = 1e-6
EQUAL_TOL = 0.005


def _num(value):
    """A cell as a float, or None for a null, NaN or non-numeric cell."""
    if value is None:
        return None
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    return None if x != x else x


def _key(account_id, day):
    return (str(int(account_id)), str(day))


def _next_day(day):
    return (dt.date.fromisoformat(day) + dt.timedelta(days=1)).isoformat()


def measure_boundary(silver):
    """(pairs, pairs_equal, max_rel_diff_bp) over the feed rows of every partition in silver (a dict of frames).

    A pair: a RETURNED row on day d with a non-null end_market_value and a RETURNED row for the same account on d + 1
    with a non-null start_market_value. diff = |end(d) - start(d+1)|; equal when diff <= 0.005; the relative difference
    is diff / max(|start(d+1)|, 1e-9) in basis points; max_rel_diff_bp is None when there are no pairs.
    """
    rows = {}
    for frame in silver.values():
        for row in frame.to_dict("records"):
            rows[_key(row["account_id"], row["day"])] = row
    pairs = equal = 0
    worst = None
    for (account, day), row in rows.items():
        if row.get("status") != "RETURNED":
            continue
        end = _num(row.get("end_market_value"))
        after = rows.get((account, _next_day(day)))
        if end is None or after is None or after.get("status") != "RETURNED":
            continue
        start = _num(after.get("start_market_value"))
        if start is None:
            continue
        diff = abs(end - start)
        rel = diff / max(abs(start), 1e-9) * 1e4
        pairs += 1
        if diff <= EQUAL_TOL:
            equal += 1
        worst = rel if worst is None or rel > worst else worst
    return pairs, equal, (None if worst is None else round(worst, 2))


def chain_check(table_rows, silver, trading_days, start, end):
    """The table's chained PRESENT rows against the silver's own daily factors, per account whose PRESENT rows cover
    every trading day of trading_days inside [start, end]. start and end are ISO days."""
    window_days = (dt.date.fromisoformat(end) - dt.date.fromisoformat(start)).days + 1
    if window_days < MIN_WINDOW_DAYS:
        return {"status": "WINDOW_TOO_SHORT", "window_calendar_days": window_days, "accounts_checked": 0,
                "accounts_matching": 0, "max_abs_diff_bp": None}
    window = [t for t in trading_days if start <= t <= end]
    factors = {}
    for frame in silver.values():
        for row in frame.to_dict("records"):
            if row.get("status") != "RETURNED":
                continue
            factor = _num(row.get("daily_factor"))
            if factor is not None:
                factors[_key(row["account_id"], row["day"])] = factor
    present = {}
    for row in table_rows:
        if row.get("row_status") == "PRESENT":
            account = str(int(row["source_account_id"]))
            present.setdefault(account, {})[str(row["business_date"])] = float(row["total_return_daily"])
    diffs = []
    for account in sorted(present, key=int):
        own = present[account]
        if not window or any(t not in own for t in window):
            continue
        table_chain = 1.0
        for t in window:
            table_chain *= 1.0 + own[t]
        silver_chain = 1.0
        day = dt.date.fromisoformat(start)
        last = dt.date.fromisoformat(window[-1])
        while day <= last:
            silver_chain *= factors.get((account, day.isoformat()), 1.0)
            day += dt.timedelta(days=1)
        diffs.append(abs(table_chain - silver_chain) * 1e4)
    if not diffs:
        return {"status": "NO_COMPLETE_ACCOUNT", "window_calendar_days": window_days, "accounts_checked": 0,
                "accounts_matching": 0, "max_abs_diff_bp": None}
    matching = sum(1 for d in diffs if d <= MATCH_BP)
    return {"status": "OK" if matching == len(diffs) else "MISMATCH", "window_calendar_days": window_days,
            "accounts_checked": len(diffs), "accounts_matching": matching, "max_abs_diff_bp": round(max(diffs), 9)}


def _partition_rows(out_dir):
    rows = []
    for part in sorted(Path(out_dir).glob("date=*")):
        rows.extend(pq.read_table(str(part / "data.parquet")).to_pylist())
    return rows


def run_real(reader, out_dir, dim_ids, trading_days_fn, firm, method_version, max_reads=400):
    """The first-real-row run: list, read, call the round-127 wrapper into out_dir, measure, return counts only."""
    parts = reader.list_partitions(TABLE_URI)
    if not parts:
        return {"status": "NO_SILVER_YET", "partitions_listed": 0, "s3_reads": reader.reads}
    if 1 + len(parts) > max_reads:
        return {"status": "STOPPED_AT_CAP", "partitions_listed": len(parts), "s3_reads": reader.reads}
    silver = {name: reader.read_parquet(TABLE_URI + "/" + name + "/data.parquet") for name in parts}
    days = sorted({str(d) for frame in silver.values() for d in frame["day"]})
    if not days:
        return {"status": "NO_ROWS", "partitions_listed": len(parts), "s3_reads": reader.reads}
    tdays = list(trading_days_fn(days[0], days[-1]))
    dim = pandas.DataFrame({"account_id": [str(a) for a in dim_ids]})
    run_record = wrap.run(silver, dim, tdays, firm, method_version, str(out_dir))
    pairs, equal, worst = measure_boundary(silver)
    end = min(days[-1], (dt.date.fromisoformat(days[0]) + dt.timedelta(days=CHAIN_SPAN_DAYS)).isoformat())
    chain = chain_check(_partition_rows(out_dir), silver, tdays, days[0], end)
    return {
        "status": "RAN",
        "contract_version": run_record["contract_version"],
        "partitions_read": len(parts),
        "s3_reads": reader.reads,
        "calendar_days_read": run_record["calendar_days_read"],
        "calendar_days_incomplete": run_record["calendar_days_incomplete"],
        "rows_present": run_record["rows_present"],
        "rows_absent": run_record["rows_absent"],
        "absent_by_reason": run_record["absent_by_reason"],
        "accounts_in_feed": run_record["accounts_in_feed"],
        "accounts_mapped": run_record["accounts_mapped"],
        "accounts_unmapped": run_record["accounts_unmapped"],
        "trading_days_unaccounted": run_record["trading_days_unaccounted"],
        "market_value_eod_claim_counts": run_record["market_value_eod_claim_counts"],
        "boundary": {"pairs": pairs, "pairs_equal": equal, "max_rel_diff_bp": worst},
        "chain": chain,
        "method_version_used": method_version,
        "out_dir_private": True,
    }


def _trading_days_iso(first, last):
    return [d.isoformat() for d in tc.trading_days_between(first, last)]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run the Scope feed's silver through the round-127 wrapper into a private "
                                                 "directory and print counts only.")
    parser.add_argument("--out-dir", required=True, help="a private directory: absent, or empty")
    parser.add_argument("--record", required=True, help="the record file to write (ASCII JSON)")
    args = parser.parse_args(argv)
    reader = iad.InflectionSilverReader()
    _name, holdings = reader.latest_partition(iar.ORION_SILVER + "fact_positions")
    _name, roster = reader.latest_partition(iar.ORION_SILVER + "fact_assets")
    dim_ids = iad.build_account_dim(holdings, roster).column("account_id").to_pylist()
    record = run_real(reader, args.out_dir, dim_ids, _trading_days_iso, iad.FIRM, 0)
    Path(args.record).write_bytes((json.dumps(record, indent=2, sort_keys=True) + "\n").encode("ascii"))
    print("status: %s" % record["status"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
