"""P-2 window, leg A2 (packet @855fdad77c, CTO batch 222): rewrite every landed account_return_daily partition over the declared
population on method_version 2, oldest first, in chunks of at most 25 trading days, through the DEPLOYED gold Lambda's
backfill mode (reporting-gold/handler.py run_backfill). Never extends the gold: the end is the newest landed day.

Usage:
  python p2_backfill_driver.py --plan                 # print the chunks and the denominator; invokes nothing
  python p2_backfill_driver.py --run [--from N]       # invoke chunk by chunk, verify each, stop at the first failure
Resumable: a chunk whose every day's manifest already reads method_version 2 is skipped (printed SKIP).
Each chunk is verified on the served artifact, never the Lambda's own report:
  every day's manifest reads method_version 2 and rows == the invoke's reported rows for that day;
  every served account present on that day before the window (P2_SERVED6) is still present.
"""
import io
import json
import sys
from pathlib import Path

import boto3
import pyarrow.parquet as pq
from botocore.config import Config

ROOT = Path(__file__).resolve().parents[8]
sys.path.insert(0, str(ROOT))
from lib import trading_calendar  # noqa: E402

BUCKET = "opal-data-49financial"
PREFIX = "irpt/49financial/gold/account_return_daily/"
FUNCTION = "irpt-49f-reporting-gold-lambda"
CHUNK = 25
def _REAL(token):
    """Resolve an acct# token to the real account id at run time from the private evidence dir (outside the repo)."""
    import json as _json
    import os as _os
    d = _os.environ.get("IRPT_PRIVATE_EVIDENCE_DIR")
    if not d:
        raise SystemExit("REFUSE: IRPT_PRIVATE_EVIDENCE_DIR is not set; this historical script needs the private account map")
    p = _os.path.join(d, "account_map_49financial.json")
    if not _os.path.isfile(p):
        raise SystemExit("REFUSE: account_map_49financial.json is absent from IRPT_PRIVATE_EVIDENCE_DIR")
    with open(p, encoding="utf-8") as fh:
        m = _json.load(fh)
    if token not in m:
        raise SystemExit("REFUSE: token %s is not in the account map" % token)
    return m[token]


P2_SERVED6 = {_REAL("acct#08137b81"), _REAL("acct#89d0916a"), _REAL("acct#f08ffd13"), _REAL("acct#6b914f88"), _REAL("acct#ffa615d2"), _REAL("acct#d0cf6c92")}

s3 = boto3.client("s3")
lam = boto3.client("lambda", config=Config(read_timeout=960, connect_timeout=30, retries={"max_attempts": 0}))


def landed_days():
    days = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX, Delimiter="/"):
        days += [c["Prefix"].split("date=")[1].rstrip("/") for c in page.get("CommonPrefixes", [])]
    return sorted(days)


def manifest(day):
    return json.loads(s3.get_object(Bucket=BUCKET, Key=PREFIX + "date=%s/manifest.json" % day)["Body"].read())


def accounts(day):
    body = s3.get_object(Bucket=BUCKET, Key=PREFIX + "date=%s/data.parquet" % day)["Body"].read()
    return set(pq.read_table(io.BytesIO(body), columns=["account_id"]).column("account_id").to_pylist())


def chunks():
    days = landed_days()
    cal = [str(d) for d in trading_calendar.trading_days_between(days[0], days[-1])]
    if cal != days:
        sys.exit("BLOCKED: landed days (%d) != trading days %s..%s (%d): the backfill would refuse a day with no row"
                 % (len(days), days[0], days[-1], len(cal)))
    return [days[i:i + CHUNK] for i in range(0, len(days), CHUNK)], days


def main():
    plan, days = chunks()
    print("DENOMINATOR: %d landed days %s..%s = %d chunks of <= %d" % (len(days), days[0], days[-1], len(plan), CHUNK))
    if "--plan" in sys.argv:
        for i, c in enumerate(plan):
            print("  chunk %2d: %s..%s (%d days)" % (i, c[0], c[-1], len(c)))
        return
    start = int(sys.argv[sys.argv.index("--from") + 1]) if "--from" in sys.argv else 0
    for i, c in enumerate(plan[start:], start):
        if all(manifest(d).get("method_version") == 2 for d in c):
            print("SKIP chunk %d %s..%s: every day already method_version 2" % (i, c[0], c[-1]))
            continue
        before = {d: accounts(d) & P2_SERVED6 for d in c}
        ev = {"backfill": {"start": c[0], "end": c[-1]}, "accounts": "population"}
        r = lam.invoke(FunctionName=FUNCTION, InvocationType="RequestResponse", Payload=json.dumps(ev).encode())
        body = json.loads(r["Payload"].read() or b"null")
        if r.get("FunctionError") or not isinstance(body, dict) or not body.get("rows"):
            sys.exit("FAIL chunk %d %s..%s: FunctionError=%s body=%s" % (i, c[0], c[-1], r.get("FunctionError"),
                                                                        json.dumps(body)[:600]))
        bad = []
        for d in c:
            m = manifest(d)
            if m.get("method_version") != 2 or m.get("rows") != body["rows"].get(d):
                bad.append("%s manifest mv=%s rows=%s reported=%s" % (d, m.get("method_version"), m.get("rows"),
                                                                     body["rows"].get(d)))
            lost = before[d] - accounts(d)
            if lost:
                bad.append("%s served accounts lost %s" % (d, sorted(lost)))
        if bad:
            sys.exit("FAIL chunk %d verify:\n  " % i + "\n  ".join(bad[:20]))
        print("OK chunk %2d %s..%s: %d days rewritten, rows %d..%d, method_version 2, served accounts kept"
              % (i, c[0], c[-1], len(c), min(body["rows"].values()), max(body["rows"].values())))
    print("DONE: %d chunks" % len(plan))


if __name__ == "__main__":
    main()
