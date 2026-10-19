"""Read-only: the object versions of the eight Cottonwood gold day keys that TO-DB-b-332 would have rewritten (IRPT_DASHBD, issuer 2.0.0_SA_COO~D2).

For each of the eight day keys prints the number of versions, the LastModified of the newest version, and whether the newest version is older than the ledger's open time (2026-10-17T15:00:54Z). Counts and times only:
no row, account or value is read. Usage: python -I <this file> [--out <json>]
"""
import datetime
import json
import sys
from pathlib import Path

import boto3

BUCKET, PREFIX = "opal-data-cottonwood", "irpt/cottonwood/gold/account_return_daily/"
DAYS = ["2026-07-22", "2026-07-23", "2026-07-27", "2026-07-28", "2026-07-29", "2026-07-30", "2026-08-03", "2026-08-04"]
OPEN_UTC = datetime.datetime(2026, 10, 17, 15, 0, 54, tzinfo=datetime.timezone.utc)
VERSIONS_AT_OPEN = 2  # the packet's before reads: each of the eight days held 2 versions


def main():
    s3 = boto3.client("s3", region_name="us-east-1")
    out = {"claim": "measured", "bucket_prefix": PREFIX, "ledger_open_utc": OPEN_UTC.strftime("%Y-%m-%dT%H:%M:%SZ"), "versions_at_open_per_packet": VERSIONS_AT_OPEN, "days": {}}
    for d in DAYS:
        key = "%sdate=%s/data.parquet" % (PREFIX, d)
        vs = [v for v in s3.list_object_versions(Bucket=BUCKET, Prefix=key).get("Versions", []) if v["Key"] == key]
        vs.sort(key=lambda v: v["LastModified"], reverse=True)
        newest = vs[0]["LastModified"] if vs else None
        out["days"][d] = {"versions": len(vs), "newest_last_modified": newest.strftime("%Y-%m-%dT%H:%M:%SZ") if newest else None, "newest_before_open": bool(newest and newest < OPEN_UTC),
                          "after_open": sum(1 for v in vs if v["LastModified"] >= OPEN_UTC)}
    out["all_unchanged_since_open"] = all(v["versions"] == VERSIONS_AT_OPEN and v["after_open"] == 0 for v in out["days"].values())
    text = json.dumps(out, indent=1)
    if "--out" in sys.argv:
        Path(sys.argv[sys.argv.index("--out") + 1]).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
