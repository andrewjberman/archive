"""twin_writer_census.py -- EG-s-11: which bd-49f twin WRITES the served slices.

READ-ONLY census on the APPLIED plane (live AWS reads) plus the served objects, per
ETFS_GUARDRAIL.TO-EG-s-11.which-49f-twin-writes-the-served-slices.md. No invoke, no write.

NEVER#1: only opal-data-etfs (the aggregation bucket, daily/49financial/ prefix and each
function's own configuration) is read here. No opal-data-assets/schwab/* or any firm-bucket
read is performed by this script.

Prints, in order:
  1. the live functions whose name starts with "bd-49f-etf-ownership" (list-functions, paginated,
     counted client-side).
  2. for each live one: configuration (OUTPUT_PREFIX env, LastModified, CodeSha256), the
     EventBridge rules targeting it, and the newest CloudWatch log events matching "OK: wrote"
     in /aws/lambda/<fn> over the last 3 days (filter-log-events, MANUALLY paginated via
     nextToken -- a single un-paginated call returns only ONE matching event per page despite
     --limit 20, a coverage trap named in this project's channel as ETFS_GUARDRAIL-W2-S3).
  3. the three newest served slices under s3://opal-data-etfs/daily/49financial/ with their
     LastModified and, from the object body, source_artifact + source_as_of.
  4. ONE line "WRITER=<function-name> EVIDENCE=<n log lines within 5 min of a served slice's
     LastModified>" (or "WRITER=UNDETERMINED" with the reason), and one line per twin
     "TWIN=<name> LIVE=<bool> SCHEDULED=<rules> LAST_WROTE=<ts or none>".
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta, timezone

import boto3
from botocore.exceptions import ClientError

TWIN_NAMES = ["bd-49f-etf-ownership-daily", "bd-49f-etf-ownership-daily-canonical"]
LOG_PREFIX = "/aws/lambda/"
SERVED_BUCKET = "opal-data-etfs"
SERVED_PREFIX = "daily/49financial/"
WROTE_PATTERN = '"OK: wrote"'
WROTE_KEY_RE = re.compile(r"OK: wrote s3://[^ ]+/(daily/49financial/[^ ]+\.json)")

lam = boto3.client("lambda")
ev = boto3.client("events")
logs = boto3.client("logs")
s3 = boto3.client("s3")


def list_matching_functions() -> list[str]:
    names = []
    paginator = lam.get_paginator("list_functions")
    pages = 0
    for page in paginator.paginate():
        pages += 1
        for fn in page.get("Functions", []):
            if fn["FunctionName"].startswith("bd-49f-etf-ownership"):
                names.append(fn["FunctionName"])
    print("STEP1: list-functions prefix='bd-49f-etf-ownership' -- %d page(s) scanned, %d match(es): %s"
          % (pages, len(names), ",".join(sorted(names))))
    return sorted(names)


def get_config(fn_name: str) -> dict | None:
    try:
        cfg = lam.get_function_configuration(FunctionName=fn_name)
        out = {
            "FunctionName": cfg["FunctionName"],
            "LastModified": cfg.get("LastModified"),
            "CodeSha256": cfg.get("CodeSha256"),
            "OUTPUT_PREFIX": (cfg.get("Environment", {}) or {}).get("Variables", {}).get("OUTPUT_PREFIX"),
            "FunctionArn": cfg.get("FunctionArn"),
        }
        print("CONFIG %s: LastModified=%s CodeSha256=%s OUTPUT_PREFIX=%s"
              % (fn_name, out["LastModified"], out["CodeSha256"], out["OUTPUT_PREFIX"]))
        return out
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "?")
        print("CONFIG %s: NOT LIVE (%s)" % (fn_name, code))
        return None


def rules_for(fn_arn: str) -> list[str]:
    try:
        resp = ev.list_rule_names_by_target(TargetArn=fn_arn)
        rules = resp.get("RuleNames", [])
        print("RULES for %s: %s" % (fn_arn, ",".join(rules) if rules else "(none)"))
        return rules
    except ClientError as exc:
        print("RULES for %s: ERROR (%s)" % (fn_arn, exc.response.get("Error", {}).get("Code", "?")))
        return []


def wrote_events(fn_name: str, start_ms: int) -> list[dict]:
    """Manually paginated -- a single filter-log-events call with --limit returns only ONE
    matching event per internal response page despite the limit, a coverage trap (see module
    docstring). Followed here to the true end (empty page, no nextToken)."""
    log_group = LOG_PREFIX + fn_name
    events: list[dict] = []
    token = None
    pages = 0
    try:
        while True:
            kwargs = dict(logGroupName=log_group, startTime=start_ms, filterPattern=WROTE_PATTERN, limit=20)
            if token:
                kwargs["nextToken"] = token
            resp = logs.filter_log_events(**kwargs)
            pages += 1
            page_events = resp.get("events", [])
            events.extend(page_events)
            token = resp.get("nextToken")
            if not token or not page_events:
                break
            if pages > 20:  # bound: never loop unbounded
                print("WARN: wrote_events(%s) stopped after 20 pages (bound)" % fn_name)
                break
    except ClientError as exc:
        print("LOGS %s: ERROR (%s)" % (fn_name, exc.response.get("Error", {}).get("Code", "?")))
        return []
    print("LOGS %s: %d page(s) followed (manual nextToken), %d 'OK: wrote' event(s) in the 3-day window"
          % (fn_name, pages, len(events)))
    for e in events:
        print("  LOGEVT %s %s %s" % (fn_name, e["timestamp"], e["message"].strip()[:160]))
    return events


def newest_served_slices(n: int = 3) -> list[dict]:
    paginator = s3.get_paginator("list_objects_v2")
    objs = []
    pages = 0
    for page in paginator.paginate(Bucket=SERVED_BUCKET, Prefix=SERVED_PREFIX):
        pages += 1
        objs.extend(page.get("Contents", []))
    objs.sort(key=lambda o: o["LastModified"])
    newest = objs[-n:] if len(objs) >= n else objs
    print("STEP3: s3 list-objects-v2 s3://%s/%s -- %d page(s), %d object(s) total, %d newest shown"
          % (SERVED_BUCKET, SERVED_PREFIX, pages, len(objs), len(newest)))
    out = []
    for o in newest:
        body = s3.get_object(Bucket=SERVED_BUCKET, Key=o["Key"])["Body"].read()
        rows = json.loads(body)
        row0 = rows[0] if isinstance(rows, list) and rows else {}
        rec = {
            "Key": o["Key"],
            "LastModified": o["LastModified"],
            "source_artifact": row0.get("source_artifact"),
            "source_as_of": row0.get("source_as_of"),
        }
        print("SLICE %s LastModified=%s source_artifact=%s source_as_of=%s"
              % (rec["Key"], rec["LastModified"], rec["source_artifact"], rec["source_as_of"]))
        out.append(rec)
    return out


def main() -> int:
    now = datetime.now(timezone.utc)
    start_ms = int((now - timedelta(days=3)).timestamp() * 1000)
    print("WINDOW: last 3 days, start=%s (%d ms) end=now (%s)" % (
        (now - timedelta(days=3)).isoformat(), start_ms, now.isoformat()))

    list_matching_functions()

    configs: dict[str, dict] = {}
    rule_map: dict[str, list[str]] = {}
    log_events: dict[str, list[dict]] = {}
    for name in TWIN_NAMES:
        cfg = get_config(name)
        if cfg is not None:
            configs[name] = cfg
            rule_map[name] = rules_for(cfg["FunctionArn"])
            log_events[name] = wrote_events(name, start_ms)
        else:
            rule_map[name] = []
            log_events[name] = []

    slices = newest_served_slices(3)

    # WRITER determination: which live function's "OK: wrote" event names a slice key that
    # matches a served object, with the log timestamp within 5 minutes of the object's
    # LastModified.
    writer = None
    evidence_count = 0
    reason = None
    served_keys = {s["Key"]: s["LastModified"] for s in slices}
    for name, evs in log_events.items():
        matches = 0
        for e in evs:
            m = WROTE_KEY_RE.search(e["message"])
            if not m:
                continue
            key = m.group(1)
            if key not in served_keys:
                continue
            evt_ts = datetime.fromtimestamp(e["timestamp"] / 1000.0, tz=timezone.utc)
            obj_ts = served_keys[key]
            if abs((evt_ts - obj_ts).total_seconds()) <= 300:
                matches += 1
        if matches > 0:
            if writer is not None and writer != name:
                writer = None
                reason = "MULTIPLE functions show matching evidence (%s and %s)" % (writer, name)
                evidence_count = 0
                break
            writer = name
            evidence_count = matches

    if writer:
        print("WRITER=%s EVIDENCE=%d" % (writer, evidence_count))
    else:
        print("WRITER=UNDETERMINED REASON=%s" % (reason or "no live function's 'OK: wrote' log line names a served key within 5 minutes of that object's LastModified"))

    for name in TWIN_NAMES:
        cfg = configs.get(name)
        live = cfg is not None
        rules = rule_map.get(name) or []
        evs = log_events.get(name) or []
        last_wrote = max((e["timestamp"] for e in evs), default=None)
        last_wrote_str = datetime.fromtimestamp(last_wrote / 1000.0, tz=timezone.utc).isoformat() if last_wrote else "none"
        print("TWIN=%s LIVE=%s SCHEDULED=%s LAST_WROTE=%s"
              % (name, live, ",".join(rules) if rules else "(none)", last_wrote_str))

    return 0


if __name__ == "__main__":
    sys.exit(main())
