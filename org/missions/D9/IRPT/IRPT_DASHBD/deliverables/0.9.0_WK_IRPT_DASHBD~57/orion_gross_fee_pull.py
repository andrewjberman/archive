"""IRPT_DASHBD TO-DB-b-76 -- READ-ONLY pull of Orion's GROSS performance and fee figures for the Inflection window.

Order exception (law 4d77a9c3ea, Andrew @669ab7d677): read-only calls to Orion's query API with the credential read from
its secret (s3://<legacy bucket>/orion/jwt/current.json) for the call only. The credential is held in memory, never
printed, never written, never committed. Every call is a GET, or the POST that RUNS a saved report (the same Generate
call the production pulls make); nothing is created, edited or deleted in Orion. Bloomberg is not touched.

Four runs of Orion's own saved queries, all over the source's Rolling 3-Year window ending --end:
  perf_gross    "Performance Dim", the performance option object overridden to feeMethod "Gross Of Fees"
                (PATH_DISCOVERY.md:124: gross vs net is a query-level option, not a path)
  perf_net      "Performance Dim" unchanged (Net of Fees) -- the control against the landed twr_value
  unified       "Unified Account Dim": Activity.Value with activityOptionId 11 (Advisory Fees Paid), per account
  billing       "Billing Dim": Billing.FeeAmount and Asset.IncludedInBilling per account

Output: CSVs in --scratch (they hold account names and are never committed). The adapter reads them.

Usage (repo root): python <this file> --end 2026-10-08 --scratch .scratch --bucket <legacy bucket from the registry alias>
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import sys
import time
import uuid
from pathlib import Path

import boto3
import requests

BASE = "https://api.cloud.orionadvisor.com"
JWT_KEY = "orion/jwt/current.json"
DATABASE_ID = 4698
MIN_JWT_MINUTES = 30


def headers(token, content_type=None):
    h = {
        "Authorization": "Session " + token,
        "App": "OrionConnect",
        "AppPath": "/reports/dataqueries/querybuilder",
        "BrowserSessionId": str(uuid.uuid4()),
        "Origin": BASE,
        "Referer": BASE + "/orionconnectapp/",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/147.0.0.0 Safari/537.36",
    }
    if content_type:
        h["Content-Type"] = content_type
    return h


def read_token(bucket):
    meta = json.loads(boto3.client("s3", region_name="us-east-1").get_object(Bucket=bucket, Key=JWT_KEY)["Body"].read())
    left = dt.datetime.fromisoformat(meta["expires_at_iso"].replace("Z", "+00:00")) - dt.datetime.now(dt.timezone.utc)
    if left < dt.timedelta(minutes=MIN_JWT_MINUTES):
        raise SystemExit("REFUSED: the Orion session token has %s left (< %d minutes)" % (left, MIN_JWT_MINUTES))
    print("OK: token read, %s remaining (value not printed)" % left)
    return meta["jwt"]


def generate_body(verbose, query, end, fee_method=None):
    start = dt.date(end.year - 3, end.month, end.day) + dt.timedelta(days=1)
    required = []
    for opt in verbose["requiredOptions"]:
        opt = dict(opt)
        if opt.get("$type") == "select-entity":
            opt["entity"] = "Database"
            opt["entityIds"] = []
        elif opt.get("$type") == "daterange":
            opt["start"] = {"date": "%d/%d/%d" % (start.month, start.day, start.year), "expression": "-3y+1d", "dateSource": "Static"}
            opt["end"] = {"date": "%d/%d/%d" % (end.month, end.day, end.year), "expression": "0d", "dateSource": "Static"}
        required.append(opt)
    if fee_method:
        perf = [o for c in verbose["additionalOptions"] if c["category"] == "Performance Options"
                for o in c["options"] if o["id"] == "performance 1"][0]
        perf = copy.deepcopy(perf)
        perf["feeMethod"] = fee_method
        perf["prompt"] = "Always"
        required.append(perf)
    return {"id": query["id"], "queryType": "Excel", "databaseIdList": [DATABASE_ID],
            "category": query.get("category") or "Sample Queries", "name": query["name"],
            "description": query.get("description") or "", "requiredOptions": required,
            "deliveryOptions": [{"id": "delivery-method", "$type": "delivery-method", "storageType": "DirectDownload",
                                 "reportFormat": "Csv", "combinationMethod": "Aggregate"}]}


def run_report(token, body):
    r = requests.post("%s/api/v1/Reporting/Envision/ExcelReports/%s/Generate" % (BASE, body["id"]),
                      headers=headers(token, "application/json;charset=UTF-8"), json=body, timeout=300)
    if r.status_code != 201:
        raise SystemExit("REFUSED: generate %s: %s" % (r.status_code, r.text[:300]))
    loc = r.headers["Location"]
    loc = loc if loc.startswith("https://") else BASE + loc
    deadline = time.time() + 400
    while time.time() < deadline:
        g = requests.get(loc, headers=headers(token), timeout=60)
        if g.status_code == 200 and g.content:
            return g.content
        if g.status_code not in (200, 202, 204):
            raise SystemExit("REFUSED: poll %s: %s" % (g.status_code, g.text[:300]))
        time.sleep(5)
    raise SystemExit("REFUSED: poll timeout")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--end", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--bucket", required=True)
    args = ap.parse_args()
    end = dt.date.fromisoformat(args.end)
    scratch = Path(args.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    token = read_token(args.bucket)
    catalog = requests.get(BASE + "/api/v1/Reporting/Envision/ExcelReports", headers=headers(token), timeout=30).json()
    runs = [("perf_gross", "Performance Dim", "Gross Of Fees"), ("perf_net", "Performance Dim", None),
            ("unified", "Unified Account Dim", None), ("billing", "Billing Dim", None)]
    manifest = {}
    for label, name, fee_method in runs:
        query = [q for q in catalog if q.get("name") == name][0]
        verbose = requests.get("%s/api/v1/Reporting/Envision/ExcelReports/Verbose/%s" % (BASE, query["id"]),
                               headers=headers(token), params={"expand": "all"}, timeout=30).json()
        for attempt in (1, 2, 3):  # Orion answers 400 "was not primed before use" intermittently; the same call then succeeds
            try:
                content = run_report(token, generate_body(verbose, query, end, fee_method))
                break
            except SystemExit as exc:
                if attempt == 3 or "not primed" not in str(exc):
                    raise
                print("WARN: %s attempt %d refused as not primed; retrying" % (label, attempt))
                time.sleep(10)
        (scratch / ("orion_%s.csv" % label)).write_bytes(content)
        manifest[label] = {"query": name, "fee_method_override": fee_method, "bytes": len(content),
                           "rows": max(0, len(content.decode("utf-8", errors="replace").splitlines()) - 1)}
        print("OK: %s <- %s%s: %d rows" % (label, name, " (feeMethod %s)" % fee_method if fee_method else "", manifest[label]["rows"]))
    (scratch / "orion_pull_manifest.json").write_text(json.dumps({"end": args.end, "runs": manifest}, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
