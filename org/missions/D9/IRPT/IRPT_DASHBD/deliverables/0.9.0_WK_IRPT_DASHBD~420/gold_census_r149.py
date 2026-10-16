"""IRPT_DASHBD round 149, TO DB-c-29, worker 0.9.0_WK_IRPT_DASHBD~420 -- the gold coverage census (a TEST READ, not a serve, not a production run).

Read only: S3 list_objects_v2 with Delimiter "/" on the prefix of each of the two 49 Financial gold tables, region us-east-1.
No object is opened and no object is written. The prefix is built with lib/opal_naming.py address(), cut at the table folder.

Usage: python gold_census_r149.py <worktree_root>      (plain python, not -I: lib/trading_calendar.py needs the user site packages)

Prints ONE JSON line: {"gold": {table: {partitions, first_date, last_date, absent_trading_days, runs}}, "reads": {...}}.
It prints no key, no bucket name, no account identifier and no series value. A refused call prints its error code only.
"""
import datetime as dt
import json
import re
import sys
from pathlib import Path

FIRM = "49financial"
TABLES = ("account_return_daily", "holdings_performance_daily")
DATE_FOLDER = re.compile(r"date=(\d{4}-\d{2}-\d{2})/$")


def error_code(exc):
    response = getattr(exc, "response", None)
    if isinstance(response, dict):
        code = response.get("Error", {}).get("Code")
        if code:
            return str(code)
    return type(exc).__name__


def main(argv):
    root = Path(argv[0]).resolve()
    sys.path.insert(0, str(root))
    import boto3
    import lib.opal_naming as naming
    import lib.trading_calendar as cal

    s3 = boto3.client("s3", region_name="us-east-1")
    reads = {"s3_list_calls": 0, "list_errors": []}
    gold = {}
    for table in TABLES:
        uri = naming.address("irpt", FIRM, "gold", table, "date=2000-01-01", "data.parquet")
        bucket, key = re.match(r"s3://([^/]+)/(.*)$", uri).groups()
        prefix = key[: key.index("date=")]
        prefix = prefix[: prefix.index(table) + len(table)] + "/"
        have = set()
        try:
            for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
                reads["s3_list_calls"] += 1
                for folder in page.get("CommonPrefixes", []):
                    hit = DATE_FOLDER.search(folder["Prefix"])
                    if hit:
                        have.add(hit.group(1))
        except Exception as exc:  # noqa: BLE001 -- a refused read is recorded, never repaired
            reads["list_errors"].append(error_code(exc))
            gold[table] = {"NOT_ESTABLISHED": "list refused: " + error_code(exc)}
            continue
        days = sorted(have)
        if not days:
            gold[table] = {"NOT_ESTABLISHED": "no date partition listed"}
            continue
        first, last = days[0], days[-1]
        window = [d.isoformat() for d in cal.trading_days_between(dt.date.fromisoformat(first), dt.date.fromisoformat(last))]
        absent = [d for d in window if d not in have]
        index = {d: i for i, d in enumerate(window)}
        runs = []
        for d in absent:
            if runs and index[d] == index[runs[-1]["end"]] + 1:
                runs[-1]["end"] = d
                runs[-1]["trading_days"] += 1
            else:
                runs.append({"start": d, "end": d, "trading_days": 1})
        gold[table] = {
            "partitions": len(days),
            "first_date": first,
            "last_date": last,
            "absent_trading_days": absent,
            "runs": runs,
        }
    print(json.dumps({"gold": gold, "reads": reads}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
