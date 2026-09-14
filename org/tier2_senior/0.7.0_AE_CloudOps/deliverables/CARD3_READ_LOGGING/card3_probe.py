#!/usr/bin/env python3
"""card3_probe.py -- the one script the card3-read-logging criteria name.

Order: org/tier2_senior/0.7.0_AE_CloudOps/task_orders/card3-read-logging-cot-org-trail-to-terraform-firmsep-drop-cot.md
Author: 0.7.0_AE_CloudOps.

READ-ONLY. It lists and reads CloudTrail log objects, calls cloudtrail DescribeTrails / LookupEvents and
s3 GetBucketLocation, and compares local JSON captures. It writes nothing anywhere.

Output contract: ONE line on stdout per call. Diagnostics (what was scanned, sample events) go to stderr.

  events --bucket B --since ISO [--until ISO] [--detail N] [--show-principal SUBSTR]
      -> DATA_EVENTS bucket=B n=<int> first=<eventTime|none>
      Reads the DELIVERED log objects of opal-organization-trail (its S3BucketName from describe-trails),
      keeping records with eventCategory=Data, eventName=GetObject, requestParameters.bucketName == B and
      since <= eventTime < until (until defaults to now). It refuses to read opal-served-key-write-trail's
      bucket and it never counts a write.
  order --since ISO
      -> ORDER putrule=<t|none> puteventselectors=<t|none> rule_first=<true|false|unknown>
      From cloudtrail lookup-events (management events): the earliest successful PutRule on
      FIRMSEP-s3-direct-access-bypass and the earliest successful PutEventSelectors on
      opal-organization-trail at or after --since. unknown when either one is not found -- a missing
      event is not a pass.
  same-rule RULE_PRE RULE_POST TARGETS_PRE TARGETS_POST
      -> RULE_UNCHANGED_EXCEPT_BUCKETS=<true|false>
      Every describe-rule field, the event pattern with its detail.requestParameters.bucketName list
      removed, and the list-targets-by-rule document.
  same-trail SELECTORS_PRE SELECTORS_POST TRAIL_PRE TRAIL_POST
      -> TRAIL_UNCHANGED_EXCEPT_READ_VALUES=<true|false>
      Everything in get-event-selectors except the ReadOnly selector's DataResources[].Values, and the
      whole describe-trails document.

The two comparisons are canonical-JSON byte comparisons (keys sorted, no whitespace): CRLF and
indentation from the CLI shim are not a difference, and every value is. A bare file name that does not
exist in the working directory is looked up next to this script, so the order's invocations run from the
workspace root.
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

TRAIL = "opal-organization-trail"
RULE = "FIRMSEP-s3-direct-access-bypass"
SERVED_KEY_TRAIL_BUCKET = "opal-served-key-write-trail-logs"
HOME_REGION = "us-east-1"
# A log file's name carries the minute it was written, which is after every event inside it, so a file
# stamped before --since cannot hold an event at or after --since (5 minutes of slack for clock skew).
# Delivery lags an event by up to about 15 minutes, so files up to 20 minutes past --until are read.
SLACK_BEFORE = timedelta(minutes=5)
SLACK_AFTER = timedelta(minutes=20)
HERE = os.path.dirname(os.path.abspath(__file__))


def parse_ts(value: str) -> datetime:
    s = value.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def fmt_ts(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def resolve(path: str) -> str:
    if os.path.exists(path):
        return path
    beside = os.path.join(HERE, path)
    if os.path.exists(beside):
        return beside
    raise SystemExit(f"ERROR: file not found: {path} (also looked in {HERE})")


def load_json(path: str):
    with open(resolve(path), encoding="utf-8-sig") as fh:
        return json.load(fh)


def trail_record(ct) -> dict:
    trails = ct.describe_trails(trailNameList=[TRAIL]).get("trailList", [])
    if len(trails) != 1:
        raise SystemExit(f"ERROR: describe-trails returned {len(trails)} trail(s) for {TRAIL}")
    return trails[0]


def file_stamp(key: str):
    # <acct>_CloudTrail_<region>_20260913T2330Z_<random>.json.gz
    for part in key.rsplit("/", 1)[-1].split("_"):
        if len(part) == 14 and part[8] == "T" and part.endswith("Z"):
            try:
                return datetime.strptime(part, "%Y%m%dT%H%MZ").replace(tzinfo=timezone.utc)
            except ValueError:
                return None
    return None


def cmd_events(args) -> int:
    import boto3

    since = parse_ts(args.since)
    until = parse_ts(args.until) if args.until else datetime.now(timezone.utc)
    if until <= since:
        print("ERROR: --until must be after --since", file=sys.stderr)
        return 2
    ct = boto3.client("cloudtrail", region_name=HOME_REGION)
    s3 = boto3.client("s3", region_name=HOME_REGION)
    trail = trail_record(ct)
    log_bucket = trail["S3BucketName"]
    if log_bucket == SERVED_KEY_TRAIL_BUCKET:
        raise SystemExit("ERROR: refusing to read the served-key write trail's bucket")
    account = trail["TrailARN"].split(":")[4]
    prefix = (trail.get("S3KeyPrefix") or "").strip("/")
    prefix = prefix + "/" if prefix else ""
    region = s3.get_bucket_location(Bucket=args.bucket).get("LocationConstraint") or "us-east-1"

    lo, hi = since - SLACK_BEFORE, until + SLACK_AFTER
    keys = []
    day = lo.date()
    pager = s3.get_paginator("list_objects_v2")
    while day <= hi.date():
        day_prefix = f"{prefix}AWSLogs/{account}/CloudTrail/{region}/{day:%Y/%m/%d}/"
        for page in pager.paginate(Bucket=log_bucket, Prefix=day_prefix):
            for obj in page.get("Contents", []):
                stamp = file_stamp(obj["Key"])
                if stamp is not None and lo <= stamp <= hi:
                    keys.append(obj["Key"])
        day += timedelta(days=1)

    def scan(key: str):
        body = s3.get_object(Bucket=log_bucket, Key=key)["Body"].read()
        records = json.loads(gzip.decompress(body)).get("Records", [])
        hits = []
        for rec in records:
            if rec.get("eventCategory") != "Data" or rec.get("eventName") != "GetObject":
                continue
            if rec.get("readOnly") is False:
                continue
            params = rec.get("requestParameters") or {}
            if params.get("bucketName") != args.bucket:
                continue
            if since <= parse_ts(rec["eventTime"]) < until:
                ident = rec.get("userIdentity") or {}
                hits.append((rec["eventTime"], ident.get("arn", "?"), rec.get("userAgent", "?"), params.get("key", "?")))
        return len(records), hits

    total = 0
    hits = []
    with ThreadPoolExecutor(max_workers=16) as pool:
        for count, found in pool.map(scan, keys):
            total += count
            hits.extend(found)
    hits.sort()
    print(f"SCANNED log_bucket={log_bucket} region_folder={region} files={len(keys)} records={total} "
          f"window=[{fmt_ts(since)},{fmt_ts(until)})", file=sys.stderr)
    for h in hits[: args.detail]:
        print(f"EVENT eventTime={h[0]} principal={h[1]} userAgent={h[2]} key={h[3]}", file=sys.stderr)
    if args.show_principal:
        for h in hits:
            if args.show_principal in h[1]:
                print(f"MATCH eventTime={h[0]} principal={h[1]} userAgent={h[2]} key={h[3]}", file=sys.stderr)
    print(f"DATA_EVENTS bucket={args.bucket} n={len(hits)} first={hits[0][0] if hits else 'none'}")
    return 0


def earliest(ct, event_name: str, match, since: datetime, until: datetime):
    found = []
    pager = ct.get_paginator("lookup_events")
    attrs = [{"AttributeKey": "EventName", "AttributeValue": event_name}]
    for page in pager.paginate(LookupAttributes=attrs, StartTime=since, EndTime=until):
        for ev in page.get("Events", []):
            detail = json.loads(ev.get("CloudTrailEvent") or "{}")
            if detail.get("errorCode"):
                continue
            if match(detail):
                found.append(detail.get("eventTime"))
    return min(found) if found else None


def cmd_order(args) -> int:
    import boto3

    since = parse_ts(args.since)
    until = datetime.now(timezone.utc)
    ct = boto3.client("cloudtrail", region_name=HOME_REGION)

    def is_rule(d: dict) -> bool:
        return (d.get("requestParameters") or {}).get("name") == RULE

    def is_trail(d: dict) -> bool:
        name = (d.get("requestParameters") or {}).get("trailName") or ""
        return name == TRAIL or name.endswith(":trail/" + TRAIL)

    putrule = earliest(ct, "PutRule", is_rule, since, until)
    selectors = earliest(ct, "PutEventSelectors", is_trail, since, until)
    if putrule and selectors:
        first = "true" if parse_ts(putrule) < parse_ts(selectors) else "false"
    else:
        first = "unknown"
    print(f"ORDER putrule={putrule or 'none'} puteventselectors={selectors or 'none'} rule_first={first}")
    return 0


def strip_rule(rule: dict):
    fields = dict(rule)
    pattern = json.loads(fields.pop("EventPattern", "{}"))
    params = (pattern.get("detail") or {}).get("requestParameters")
    if isinstance(params, dict):
        params.pop("bucketName", None)
    return fields, pattern


def cmd_same_rule(args) -> int:
    pre_fields, pre_pattern = strip_rule(load_json(args.rule_pre))
    post_fields, post_pattern = strip_rule(load_json(args.rule_post))
    diffs = []
    if canon(pre_fields) != canon(post_fields):
        diffs.append("describe-rule fields")
    if canon(pre_pattern) != canon(post_pattern):
        diffs.append("event pattern with bucketName removed")
    if canon(load_json(args.targets_pre)) != canon(load_json(args.targets_post)):
        diffs.append("list-targets-by-rule")
    for d in diffs:
        print(f"DIFF {d}", file=sys.stderr)
    print(f"RULE_UNCHANGED_EXCEPT_BUCKETS={'false' if diffs else 'true'}")
    return 0


def strip_selectors(doc: dict) -> dict:
    out = json.loads(json.dumps(doc))
    for sel in out.get("EventSelectors", []):
        if sel.get("ReadWriteType") == "ReadOnly":
            for res in sel.get("DataResources", []):
                res.pop("Values", None)
    return out


def cmd_same_trail(args) -> int:
    diffs = []
    if canon(strip_selectors(load_json(args.selectors_pre))) != canon(strip_selectors(load_json(args.selectors_post))):
        diffs.append("get-event-selectors outside the ReadOnly Values")
    if canon(load_json(args.trail_pre)) != canon(load_json(args.trail_post)):
        diffs.append("describe-trails")
    for d in diffs:
        print(f"DIFF {d}", file=sys.stderr)
    print(f"TRAIL_UNCHANGED_EXCEPT_READ_VALUES={'false' if diffs else 'true'}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="card3-read-logging probe (read-only)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ev = sub.add_parser("events")
    ev.add_argument("--bucket", required=True)
    ev.add_argument("--since", required=True)
    ev.add_argument("--until")
    ev.add_argument("--detail", type=int, default=0)
    ev.add_argument("--show-principal", default="")
    ev.set_defaults(fn=cmd_events)

    od = sub.add_parser("order")
    od.add_argument("--since", required=True)
    od.set_defaults(fn=cmd_order)

    sr = sub.add_parser("same-rule")
    for name in ("rule_pre", "rule_post", "targets_pre", "targets_post"):
        sr.add_argument(name)
    sr.set_defaults(fn=cmd_same_rule)

    st = sub.add_parser("same-trail")
    for name in ("selectors_pre", "selectors_post", "trail_pre", "trail_post"):
        st.add_argument(name)
    st.set_defaults(fn=cmd_same_trail)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
