#!/usr/bin/env python
"""OG-ap-35 Phase A step 1 (usage): how many times has her principal used the download operation since her grant's activation? READ-ONLY. Counts only.

Two audit sources, both under s3://opal-mcp-audit (the gateway's AUDIT_S3_BUCKET), every retained day from the grant's first activation to now:
  A  audit/dt=<day>/*.jsonl            app/audit.py records: tool, principal ("<tid>/<oid>"), outcome, ts. The operation download_filtered is the tool schwab_prepare_download.
  B  audit/schwab/dt=<day>/*.json      app/schwab_audit.py records: principal_hash (a salted sha256 of the lower-cased principal key), operation, event_type, ts.
Her principal is resolved in-process from X/ag1_identities.json (off-repo) and never printed. Denominators and a positive control are printed: the scan must see her principal's
other records and the tool's records for any principal, or a zero would read as 'never used' with an instrument that cannot see.
usage: python ag1_usage.py   (from the repo root of the worktree)"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import boto3

BUCKET = "opal-mcp-audit"
REGION = "us-east-1"
W = os.path.join("org", "missions", "D9", "NFRA", "NFRA_OPLGTW", "deliverables", "0.7.0_AE_CloudOps~NFRA1")
TOOL = "schwab_prepare_download"
DL_OPS = ("schwab_prepare_download", "download_filtered", "download_start")
WORKERS = 32


def x_dir() -> str:
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    return os.path.join(base, "opal", "og-salt", "ag1")


def digest(value: str) -> str:
    return "sha256:" + hashlib.sha256(("opal-schwab-audit|principal|%s" % value.strip().lower()).encode("utf-8")).hexdigest()


def main() -> int:
    ident = json.load(io.open(os.path.join(x_dir(), "ag1_identities.json"), encoding="utf-8"))
    key = ("%s/%s" % (ident["alyssa_tid"], ident["alyssa_oid"])).lower()
    pdigest = digest(key)
    before = json.load(io.open(os.path.join(W, "AG1_BEFORE_state.json"), encoding="utf-8"))
    start_iso = before["alyssa_grant_timeline"]["first_activation_at"]
    dl_added = before["alyssa_grant_timeline"]["download_filtered_added_at"]
    start_day = dt.date.fromisoformat(start_iso[:10])
    today = dt.datetime.now(dt.timezone.utc).date()
    days = [(start_day + dt.timedelta(days=i)).isoformat() for i in range((today - start_day).days + 1)]
    s3 = boto3.client("s3", region_name=REGION, config=boto3.session.Config(max_pool_connections=64, retries={"max_attempts": 8}))

    def list_prefix(prefix):
        keys, token = [], None
        while True:
            kw = {"Bucket": BUCKET, "Prefix": prefix}
            if token:
                kw["ContinuationToken"] = token
            r = s3.list_objects_v2(**kw)
            keys += [o["Key"] for o in r.get("Contents", [])]
            if not r.get("IsTruncated"):
                return keys
            token = r["NextContinuationToken"]

    def read(k):
        try:
            body = s3.get_object(Bucket=BUCKET, Key=k)["Body"].read().decode("utf-8", "replace")
            return k, body, None
        except Exception as exc:
            return k, None, type(exc).__name__

    res = {"window_start": start_iso, "download_filtered_added_at": dl_added, "window_end_day": today.isoformat(), "days_listed": len(days), "sources": {}}
    for name, tmpl in (("A_general_lake", "audit/dt=%s/"), ("B_schwab_prefix", "audit/schwab/dt=%s/")):
        keys = []
        for d in days:
            keys += list_prefix(tmpl % d)
        stats = {"objects_listed": len(keys), "objects_read": 0, "read_errors": 0, "malformed": 0, "records": 0,
                 "her_records": 0, "her_download_calls": 0, "her_download_calls_since_added": 0, "her_download_ok": 0, "her_download_denied": 0,
                 "any_principal_download_calls": 0, "last_download_use": None, "her_other_tools_distinct": set()}
        errs = []
        with ThreadPoolExecutor(WORKERS) as ex:
            for k, body, err in ex.map(read, keys):
                if err:
                    stats["read_errors"] += 1
                    errs.append(err)
                    continue
                stats["objects_read"] += 1
                for line in body.splitlines():
                    if not line.strip():
                        continue
                    try:
                        rec = json.loads(line)
                    except ValueError:
                        stats["malformed"] += 1
                        continue
                    stats["records"] += 1
                    ts = str(rec.get("ts") or "")
                    if name == "A_general_lake":
                        tool = rec.get("tool")
                        mine = str(rec.get("principal") or "").lower() == key
                        is_dl = tool == TOOL
                    else:
                        tool = rec.get("operation")
                        mine = rec.get("principal_hash") == pdigest
                        is_dl = tool in DL_OPS and rec.get("event_type") in ("release_authorized", "delivery_finished", "denied")
                    if is_dl:
                        stats["any_principal_download_calls"] += 1
                    if mine:
                        stats["her_records"] += 1
                        if not is_dl and tool:
                            stats["her_other_tools_distinct"].add(str(tool))
                        if is_dl and ts >= start_iso:
                            stats["her_download_calls"] += 1
                            if dl_added and ts >= dl_added:
                                stats["her_download_calls_since_added"] += 1
                            outcome = str(rec.get("outcome") or rec.get("decision") or "")
                            if outcome in ("ok", "authorized", "allow"):
                                stats["her_download_ok"] += 1
                            elif outcome in ("denied", "deny"):
                                stats["her_download_denied"] += 1
                            if stats["last_download_use"] is None or ts > stats["last_download_use"]:
                                stats["last_download_use"] = ts
        stats["her_other_tools_distinct"] = len(stats["her_other_tools_distinct"])
        stats["read_error_kinds"] = sorted(set(errs))
        res["sources"][name] = stats
        print("  %s: %s" % (name, {k: v for k, v in stats.items()}))
    a, b = res["sources"]["A_general_lake"], res["sources"]["B_schwab_prefix"]
    res["positive_control"] = {"her_principal_seen_in_general_lake": a["her_records"] > 0, "tool_seen_for_any_principal_in_general_lake": a["any_principal_download_calls"] > 0,
                               "her_principal_seen_in_schwab_prefix": b["her_records"] > 0}
    res["download_filtered_calls_since_grant"] = a["her_download_calls"] + b["her_download_calls"]
    res["download_filtered_calls_since_grant_by_source"] = {"general_lake_tool_records": a["her_download_calls"], "schwab_prefix_events": b["her_download_calls"]}
    res["download_filtered_calls_since_added_to_grant"] = a["her_download_calls_since_added"] + b["her_download_calls_since_added"]
    res["last_use"] = max([x for x in (a["last_download_use"], b["last_download_use"]) if x] or [None]) if (a["last_download_use"] or b["last_download_use"]) else None
    with io.open(os.path.join(W, "AG1_usage.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print("  USAGE: since grant %s, since download added %s, last use %s; control %s" % (res["download_filtered_calls_since_grant"], res["download_filtered_calls_since_added_to_grant"], res["last_use"], res["positive_control"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
