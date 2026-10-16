"""DB-c-22 (IRPT_DASHBD TO-DB-c-22, round 145): the Cottonwood coverage census. READ ONLY.

Usage (from the worktree root, plain python, not -I):  python <this file> <repo_root>

Reads: S3 list_objects_v2 (CommonPrefixes under each gold table root and the Black Diamond silver
fact_allocations root), get_object for parquet footers (num_rows) and for the account_id / coverage
columns of the newest partitions. No put, delete, create, invoke or secret read. Counts only; no
identifier value is written anywhere. Writes exactly two files in this folder: the record JSON.
"""
import collections
import datetime as dt
import io
import json
import re
import sys
from pathlib import Path

import boto3
import pyarrow.parquet as pq

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
HERE = Path(__file__).resolve().parent
RECORD = HERE / "COTTONWOOD_COVERAGE_CENSUS_R145.json"
BUCKET = "opal-data-cottonwood"
TABLES = ("filled_report_values", "account_return_daily", "holdings_performance_daily", "account_dim")

# Words are measured-claim prose only: no account id, no household id, no long digit run.
WORDS = json.loads((HERE / "census_words_r145.json").read_text(encoding="utf-8")) if (HERE / "census_words_r145.json").is_file() else {}

COUNTS = collections.Counter()


def _count(model=None, **kwargs):
    name = getattr(model, "name", "")
    if name == "ListObjectsV2":
        COUNTS["list"] += 1
    elif name == "HeadObject":
        COUNTS["head"] += 1
    elif name == "GetObject":
        COUNTS["get"] += 1
    else:
        COUNTS["other:" + str(name)] += 1


def now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


s3 = boto3.client("s3", region_name="us-east-1")
s3.meta.events.register("before-call.s3", _count)

sys.path.insert(0, str(ROOT))
import lib.opal_naming as naming  # noqa: E402
import lib.trading_calendar as tc  # noqa: E402


def gold_root(table):
    u = naming.address("irpt", "cottonwood", "gold", table, "date=2000-01-03", "data.parquet")
    b, k = re.match(r"s3://([^/]+)/(.*)$", u).groups()
    return b, k[: k.index("date=")]


def silver_root():
    code = ("import json,sys; sys.path.insert(0,'infra/aws/lambda/investor-reporting/account-dim-cot'); "
            "import lambda_function as L; print(json.dumps(L.silver_locations('2000-01-03')))")
    import subprocess
    r = subprocess.run([sys.executable, "-c", code], cwd=str(ROOT), capture_output=True, text=True, timeout=100)
    assert r.returncode == 0, r.stderr[-300:]
    b, k = json.loads(r.stdout.strip().splitlines()[-1])["fact_allocations"]
    return b, k[: -len("date=2000-01-03/data.parquet")]


def list_parts(bucket, prefix):
    """Partition dates from a delimiter listing (CommonPrefixes). A common prefix implies >= 1 key beneath it."""
    dates, other = set(), []
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        for cp in pg.get("CommonPrefixes", []):
            m = re.search(r"date=(\d{4}-\d{2}-\d{2})/$", cp["Prefix"])
            if m:
                dates.add(m.group(1))
            else:
                other.append(cp["Prefix"])
    return sorted(dates), other


def absent_runs(first, last, have):
    days = [str(x) for x in tc.trading_days_between(dt.date.fromisoformat(first), dt.date.fromisoformat(last))]
    have = set(have)
    absent = [d for d in days if d not in have]
    idx = {d: i for i, d in enumerate(days)}
    runs = []
    for d in absent:
        if runs and idx[d] == idx[runs[-1]["end"]] + 1:
            runs[-1]["end"] = d
            runs[-1]["trading_days"] += 1
        else:
            runs.append({"start": d, "end": d, "trading_days": 1})
    return days, absent, runs


def footer_rows(bucket, prefix, day):
    keys = []
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, day)):
        keys += [o["Key"] for o in pg.get("Contents", []) if o["Key"].endswith(".parquet")]
    if not keys:
        return None
    total = 0
    for k in keys:
        body = s3.get_object(Bucket=bucket, Key=k)["Body"].read()
        total += pq.ParquetFile(io.BytesIO(body)).metadata.num_rows
    return total


def column_of(bucket, key, col):
    body = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
    t = pq.read_table(io.BytesIO(body), columns=[col])
    return t.column(col).to_pylist()


def main():
    rec = {"claim": "measured", "pushed": False, "deployed": False, "round": 145, "to": "IRPT_DASHBD.TO-DB-c-22",
           "serial": "0.9.0_WK_IRPT_DASHBD~414", "tables": {}}

    # 1. tables
    per_table_dates = {}
    for t in TABLES:
        b, pfx = gold_root(t)
        dates, other = list_parts(b, pfx)
        read_utc = now()
        assert dates, "no partition for " + t
        days, absent, runs = absent_runs(dates[0], dates[-1], dates)
        per_table_dates[t] = dates
        rec["tables"][t] = {
            "partitions": len(dates),
            "first_date": dates[0],
            "last_date": dates[-1],
            "absent_trading_days": absent,
            "runs": runs,
            "trading_days_in_span": len(days),
            "non_partition_prefixes": len(other),
            "read_utc": read_utc,
        }
        print("TABLE", t, "partitions", len(dates), "first", dates[0], "last", dates[-1],
              "absent", len(absent), "runs", len(runs), "read_utc", read_utc, flush=True)

    fr = per_table_dates["filled_report_values"]
    floor = fr[0]

    # 2. floor: silver fact_allocations footer reads over every silver partition
    sb, sp = silver_root()
    sdates, _other = list_parts(sb, sp)
    trading_set = {str(x) for x in tc.trading_days_between(dt.date.fromisoformat(sdates[0]), dt.date.fromisoformat(sdates[-1]))}
    srows = {}
    for d in sdates:
        srows[d] = footer_rows(sb, sp, d)
    silver_read_utc = now()
    empties = [d for d in sdates if srows[d] == 0]
    nonempty_after = [d for d in sdates if srows[d] and empties and d > empties[-1]]
    first_empty = empties[0] if empties else None
    last_empty = empties[-1] if empties else None
    rec["floor"] = {
        "date": floor,
        "evidence_words": WORDS.get("floor_evidence", "TBD"),
        "silver_empty": {
            "table": "fact_allocations",
            "first_empty": first_empty,
            "last_empty": last_empty,
            "count": len(empties),
            "scanned": len(sdates),
            "unscanned_or_no_parquet": [d for d in sdates if srows[d] is None],
            "partitions_in_first_to_last_empty_span": sum(1 for d in sdates if first_empty and last_empty and first_empty <= d <= last_empty),
            "empty_in_first_to_last_empty_span": sum(1 for d in sdates if first_empty and last_empty and first_empty <= d <= last_empty and srows[d] == 0),
            "nonempty_partitions_before_first_empty": sum(1 for d in sdates if first_empty and d < first_empty and srows[d]),
            "empty_dates": [d for d in sdates if srows[d] == 0],
            "empty_on_trading_days": sum(1 for d in empties if d in trading_set),
            "empty_on_non_trading_days": sum(1 for d in empties if d not in trading_set),
            "nonempty_on_trading_days_in_span": sum(1 for d in sdates if first_empty and first_empty <= d <= last_empty and srows[d] and d in trading_set),
            "trading_days_in_span_with_silver_partition": sum(1 for d in sdates if first_empty and first_empty <= d <= last_empty and d in trading_set),
            "first_nonempty_after": nonempty_after[0] if nonempty_after else None,
            "read_utc": silver_read_utc,
        },
    }
    print("SILVER scanned", len(sdates), "empty", len(empties), "first_empty", first_empty,
          "last_empty", last_empty, "first_nonempty_after", rec["floor"]["silver_empty"]["first_nonempty_after"],
          "read_utc", silver_read_utc, flush=True)
    print("FLOOR", floor, flush=True)

    # 3. twelve-day gap: the run between the last pre-2026-07 account_return_daily partition and the floor
    arr = rec["tables"]["account_return_daily"]
    pre = [d for d in per_table_dates["account_return_daily"] if d < "2026-07-01"]
    last_pre = pre[-1] if pre else None
    gap_runs = [q for q in arr["runs"] if last_pre and q["start"] > last_pre and q["end"] < floor]
    twelve = [q for q in arr["runs"] if q["trading_days"] == 12]
    if gap_runs and gap_runs[0]["trading_days"] == 12:
        rec["twelve_day_gap"] = {"table": "account_return_daily", "start": gap_runs[0]["start"],
                                 "end": gap_runs[0]["end"], "trading_days": 12, "found": True}
    else:
        rec["twelve_day_gap"] = {"found": False, "words": WORDS.get("gap_words", "TBD"),
                                 "last_pre_july_partition": last_pre,
                                 "run_between_last_pre_july_and_floor": gap_runs[0] if gap_runs else None,
                                 "runs_of_exactly_12_trading_days_anywhere": twelve}
    print("GAP", json.dumps(rec["twelve_day_gap"], sort_keys=True)[:600], flush=True)

    # 4. account histories (counts only)
    ad_b, ad_p = gold_root("account_dim")
    hp_b, hp_p = gold_root("holdings_performance_daily")
    ad_last = per_table_dates["account_dim"][-1]
    hp_last = per_table_dates["holdings_performance_daily"][-1]
    ad_accts = {str(v).strip() for v in column_of(ad_b, "%sdate=%s/data.parquet" % (ad_p, ad_last), "account_id") if v is not None}
    hp_floor = {str(v).strip() for v in column_of(hp_b, "%sdate=%s/data.parquet" % (hp_p, floor), "account_id") if v is not None}
    hp_new = {str(v).strip() for v in column_of(hp_b, "%sdate=%s/data.parquet" % (hp_p, hp_last), "account_id") if v is not None}
    rec["account_histories"] = {
        "accounts_in_account_dim": len(ad_accts),
        "accounts_with_holdings_on_the_floor_day": len(hp_floor),
        "accounts_first_seen_after_floor": len(hp_new - hp_floor),
        "account_forms_note": "column account_id in account_dim and holdings_performance_daily; compared as str(value).strip(); "
                              "newest account_dim partition %s; newest holdings partition %s; floor-day partition %s"
                              % (ad_last, hp_last, floor),
        "read_utc": now(),
    }
    print("ACCTS", rec["account_histories"]["accounts_in_account_dim"],
          rec["account_histories"]["accounts_with_holdings_on_the_floor_day"],
          rec["account_histories"]["accounts_first_seen_after_floor"], flush=True)

    # 5. coverage vocabulary: newest partition, the column that carries the coverage state
    fr_b, fr_p = gold_root("filled_report_values")
    arr_b, arr_p = gold_root("account_return_daily")
    fr_vals = column_of(fr_b, "%sdate=%s/data.parquet" % (fr_p, fr[-1]), "absent_kind")
    arr_vals = column_of(arr_b, "%sdate=%s/data.parquet" % (arr_p, arr["last_date"]), "day_quality")
    rec["coverage_vocabulary"] = {
        "column": WORDS.get("vocab_column", "day_quality"),
        "table": WORDS.get("vocab_table", "account_return_daily"),
        "values": dict(collections.Counter("<null>" if v is None else str(v) for v in arr_vals)),
        "alternates_measured": {
            "filled_report_values.absent_kind": dict(collections.Counter("<null>" if v is None else str(v) for v in fr_vals)),
        },
        "words": WORDS.get("vocab_words", "TBD"),
        "read_utc": now(),
    }

    rec["reads"] = {"s3_list_calls": COUNTS["list"], "s3_head_calls": COUNTS["head"], "s3_get_calls": COUNTS["get"],
                    "other_s3_calls": {k: v for k, v in COUNTS.items() if k.startswith("other")},
                    "writes": 0, "invokes": 0}
    rec["record_written_utc"] = now()
    RECORD.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="ascii")
    print("RECORD", RECORD.name, "reads", rec["reads"], flush=True)


if __name__ == "__main__":
    main()
