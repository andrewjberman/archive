"""CONNECTOR SWEEP -- enumeration backbone (read-only). 0.7.0_AE_CloudOps, 2026-07-14.

Enumerates EVERY EventBridge rule (paginated -- the 100-cap lie is known) + every
Scheduler schedule -> targets -> per-ligament evidence for verdicts (a) fires and
(b) target runs, plus the raw material for (c) landed-bytes (env vars name the
deployed write surfaces). Emits JSON. Denominators printed. ZERO writes anywhere.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import boto3

events = boto3.client("events", region_name="us-east-1")
scheduler = boto3.client("scheduler", region_name="us-east-1")
cw = boto3.client("cloudwatch", region_name="us-east-1")
lam = boto3.client("lambda", region_name="us-east-1")

NOW = datetime.now(timezone.utc)
LOOKBACK_H = 50  # > 2 days so a daily cron shows 2 fires

out: dict = {"generated_utc": NOW.isoformat(), "rules": [], "schedules": [], "denominators": {}}

# --- 1. EventBridge rules, fully paginated -------------------------------------
rules = []
token = None
kw: dict = {}
resp: dict = {}
while True:
    kw = {"Limit": 100}
    if token:
        kw["NextToken"] = token
    resp = events.list_rules(**kw)
    rules.extend(resp.get("Rules", []))
    token = resp.get("NextToken")
    if not token:
        break
print(f"DENOMINATOR: EventBridge rules enumerated = {len(rules)} (paginated)")

def rule_fire_sum(rule_name: str) -> float | None:
    try:
        r = cw.get_metric_statistics(
            Namespace="AWS/Events", MetricName="TriggeredRules",
            Dimensions=[{"Name": "RuleName", "Value": rule_name}],
            StartTime=NOW - timedelta(hours=LOOKBACK_H), EndTime=NOW,
            Period=3600, Statistics=["Sum"],
        )
        pts = r.get("Datapoints", [])
        return sum(p["Sum"] for p in pts) if pts else 0.0
    except Exception as exc:
        print(f"WARN: TriggeredRules metric failed for {rule_name}: {exc}")
        return None

def lambda_metrics(fn: str) -> dict:
    o: dict = {}
    for metric in ("Invocations", "Errors"):
        try:
            r = cw.get_metric_statistics(
                Namespace="AWS/Lambda", MetricName=metric,
                Dimensions=[{"Name": "FunctionName", "Value": fn}],
                StartTime=NOW - timedelta(hours=LOOKBACK_H), EndTime=NOW,
                Period=3600, Statistics=["Sum"],
            )
            pts = r.get("Datapoints", [])
            o[metric.lower()] = sum(p["Sum"] for p in pts) if pts else 0.0
        except Exception as exc:
            o[metric.lower()] = None
            print(f"WARN: {metric} failed for {fn}: {exc}")
    return o

def lambda_env(fn: str) -> dict:
    try:
        cfg = lam.get_function_configuration(FunctionName=fn)
        return {
            "env": (cfg.get("Environment") or {}).get("Variables", {}),
            "last_modified": cfg.get("LastModified"),
            "state": cfg.get("State"),
        }
    except Exception as exc:
        return {"error": str(exc)[:120]}

for i, r in enumerate(rules):
    name = r["Name"]
    entry: dict = {
        "name": name,
        "state": r.get("State"),
        "schedule": r.get("ScheduleExpression", ""),
        "pattern": bool(r.get("EventPattern")),
        "targets": [],
    }
    try:
        tg = events.list_targets_by_rule(Rule=name).get("Targets", [])
    except Exception as exc:
        tg = []
        entry["targets_error"] = str(exc)[:120]
    for t in tg:
        arn = t.get("Arn", "")
        tinfo: dict = {"arn": arn}
        if ":function:" in arn:
            fn = arn.split(":function:")[1].split(":")[0]
            tinfo["lambda"] = fn
            tinfo.update(lambda_metrics(fn))
            tinfo.update(lambda_env(fn))
        entry["targets"].append(tinfo)
    if r.get("State") == "ENABLED":
        entry["fired_sum_50h"] = rule_fire_sum(name)
    out["rules"].append(entry)
    if (i + 1) % 25 == 0:
        print(f"progress: {i+1}/{len(rules)} rules verdicted")

# --- 2. EventBridge Scheduler schedules ----------------------------------------
schedules = []
token = None
kw = {}
resp = {}
while True:
    kw = {"MaxResults": 100}
    if token:
        kw["NextToken"] = token
    resp = scheduler.list_schedules(**kw)
    schedules.extend(resp.get("Schedules", []))
    token = resp.get("NextToken")
    if not token:
        break
print(f"DENOMINATOR: Scheduler schedules enumerated = {len(schedules)}")

for s in schedules:
    try:
        d = scheduler.get_schedule(Name=s["Name"], GroupName=s.get("GroupName", "default"))
        arn = (d.get("Target") or {}).get("Arn", "")
        entry = {
            "name": s["Name"],
            "state": d.get("State"),
            "schedule": d.get("ScheduleExpression"),
            "target_arn": arn,
        }
        if ":function:" in arn:
            fn = arn.split(":function:")[1].split(":")[0]
            entry["lambda"] = fn
            entry.update(lambda_metrics(fn))
            entry.update(lambda_env(fn))
        out["schedules"].append(entry)
    except Exception as exc:
        out["schedules"].append({"name": s["Name"], "error": str(exc)[:120]})

out["denominators"] = {
    "eventbridge_rules": len(rules),
    "scheduler_schedules": len(schedules),
    "ligaments_total": len(rules) + len(schedules),
    "rules_enabled": sum(1 for r in out["rules"] if r["state"] == "ENABLED"),
    "rules_disabled": sum(1 for r in out["rules"] if r["state"] == "DISABLED"),
}
print(f"DENOMINATOR: {json.dumps(out['denominators'])}")

path = r"C:\Users\ANDREW~1\AppData\Local\Temp\claude\C--Users-AndrewBerman-Desktop-ajb-workspace\c6fc3652-4910-4d37-8484-81e5fc278ea5\scratchpad\ligament_sweep.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, default=str)
print(f"OK: sweep written to {path}")
