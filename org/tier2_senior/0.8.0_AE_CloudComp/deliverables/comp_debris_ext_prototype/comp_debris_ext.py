#!/usr/bin/env python3
"""comp-debris extension PROTOTYPE -- past Lambda to the AWS-resource plane (NFRA decommission research).

Validates COMP_DEBRIS_EXTENSION_DESIGN_20260717.md against LIVE AWS. This is a PROTOTYPE in the
0.8.0_AE_CloudComp research lane -- the production build lands in comp_debris.py at the ANY_EXEC
engine home (org/modules/graph/), separately staffed. Read-only, advisory, NEVER deletes.

THE ARCHITECTURE PROVEN HERE: one classify(), N adapters. The band logic + the three refinements
are resource-type-AGNOSTIC and reused VERBATIM by IMPORTING comp_debris.classify / BANDS / _HELD_RX.
Each per-type adapter contributes ONLY its signal -- (last_activity_day, created_day, read_ok,
signal_basis) -- and the central classify() assigns the band. Adding a type = adding an adapter,
never touching the invariants.

SIGNALS (grounded live 2026-07-17; see the design doc):
  DYNAMODB_TABLE : CW ConsumedRead+WriteCapacityUnits (Sum, daily)      -- mirrors Lambda exactly
  S3_BUCKET      : CW NumberOfObjects delta (AllStorageTypes, daily)    -- write-cold, FREE + always-on;
                   read-activity is BLIND (accepted per Andrew 2026-07-17) -> signal_basis says so
  EC2_INSTANCE   : CW CPUUtilization + NetworkIn (idle = both under floor) -- idle != stopped; fuzzy
  EVENT_RULE     : CW AWS/Events Invocations per RuleName (Sum, daily)  -- never-fired = cold wiring

HONESTY CONTROLS (design sec.4): per-row signal_basis; UNKNOWN-is-a-band (blind read never "cold");
never-active split by creation age; hold-aware (_HELD_RX). The T-1/trading-calendar control (design
sec.4.5) is NOTED as a production requirement for pipeline/data buckets -- this prototype flags it,
does not yet fold lib/trading_calendar (see --self-test note + design open-Q3).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

# Reuse the LOAD-BEARING invariant logic by importing the exec-home engine (read-only import).
_HERE = Path(__file__).resolve()
_REPO = _HERE.parents[5]  # comp_debris_ext_prototype -> deliverables -> serial -> tier2_senior -> org -> REPO
_ENGINE_DIR = _REPO / "org" / "modules" / "graph"
if str(_ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(_ENGINE_DIR))
import comp_debris as cd  # noqa: E402  (classify, BANDS, _HELD_RX -- reused verbatim)

# EC2 idle floors (design open-Q1: a runner between scheduled jobs is idle-but-not-dead ->
# a low-signal EC2 is a PURPOSE-REVIEW candidate, never a clean reap). Conservative defaults.
EC2_CPU_FLOOR = 2.0        # avg %CPU below this on a day = "not actively computing"
EC2_NETIN_FLOOR = 1_000_000  # bytes/day NetworkIn below this = "not actively serving"


# ---- CloudWatch GetMetricData batching (design sec.5: <=500 queries/call) -----------------
def _cw(region: str):
    import boto3
    return boto3.client("cloudwatch", region_name=region)


def _get_metric_data(cw, queries: list, days: int) -> dict:
    """queries: [{id, namespace, metric, dims:[{Name,Value}], stat}]. Returns {id: [(day, value)]}.
    Batches <=500 per GetMetricData call and paginates NextToken. Daily period."""
    end = dt.datetime.now(dt.timezone.utc)
    start = end - dt.timedelta(days=days)
    out: dict[str, list] = {}
    for i in range(0, len(queries), 500):
        chunk = queries[i:i + 500]
        mdq = [{
            "Id": q["id"],
            "MetricStat": {
                "Metric": {"Namespace": q["namespace"], "MetricName": q["metric"],
                           "Dimensions": q["dims"]},
                "Period": 86400, "Stat": q["stat"],
            },
            "ReturnData": True,
        } for q in chunk]
        token = None
        while True:
            kw = {"MetricDataQueries": mdq, "StartTime": start, "EndTime": end,
                  "ScanBy": "TimestampAscending"}
            if token:
                kw["NextToken"] = token
            resp = cw.get_metric_data(**kw)
            for r in resp.get("MetricDataResults", []):
                series = list(zip([t for t in r.get("Timestamps", [])], r.get("Values", [])))
                out.setdefault(r["Id"], []).extend(series)
            token = resp.get("NextToken")
            if not token:
                break
    return out


def _last_nonzero_day(series: list) -> str | None:
    """last day with a nonzero value -> ISO date, else None. (Sum-metric activity signal.)"""
    days = [(ts.date(), v) for ts, v in series if (v or 0) > 0]
    return max(days)[0].isoformat() if days else None


def _last_change_day(series: list) -> str | None:
    """last day a value DIFFERS from the prior day -> ISO date (the write/delete signal for a
    level-metric like NumberOfObjects), else None if flat/insufficient."""
    s = sorted(series, key=lambda x: x[0])
    last = None
    for k in range(1, len(s)):
        if s[k][1] != s[k - 1][1]:
            last = s[k][0].date()
    return last.isoformat() if last else None


# ---- adapters: each returns records [{rtype, name, created, hist, signal_basis}] ----------
def adapt_dynamodb(region: str, days: int) -> list:
    import boto3
    ddb = boto3.client("dynamodb", region_name=region)
    cw = _cw(region)
    tables, tok = [], None
    while True:
        kw = {"ExclusiveStartTableName": tok} if tok else {}
        r = ddb.list_tables(**kw)
        tables += r.get("TableNames", [])
        tok = r.get("LastEvaluatedTableName")
        if not tok:
            break
    meta = {}
    for t in tables:
        try:
            d = ddb.describe_table(TableName=t)["Table"]
            meta[t] = d.get("CreationDateTime")
        except Exception:  # noqa: BLE001
            meta[t] = None
    queries = []
    for i, t in enumerate(tables):
        for m in ("ConsumedReadCapacityUnits", "ConsumedWriteCapacityUnits"):
            queries.append({"id": f"d{i}_{m[8:12].lower()}", "namespace": "AWS/DynamoDB",
                            "metric": m, "dims": [{"Name": "TableName", "Value": t}], "stat": "Sum"})
    data = _get_metric_data(cw, queries, days)
    recs = []
    for i, t in enumerate(tables):
        series = data.get(f"d{i}_read", []) + data.get(f"d{i}_writ", [])
        last = _last_nonzero_day(series)
        created = meta[t].astimezone(dt.timezone.utc).isoformat() if meta.get(t) else ""
        recs.append({"rtype": "DYNAMODB_TABLE", "name": t, "created": created,
                     "hist": {"read": True, "last_invoked_day": last,
                              "total": int(sum(v for _, v in series))},
                     "signal_basis": "cw-capacity(read+write)"})
    return recs


def adapt_s3(region: str, days: int) -> list:
    import boto3
    s3 = boto3.client("s3", region_name=region)
    cw = _cw(region)
    buckets = s3.list_buckets().get("Buckets", [])
    queries = []
    for i, b in enumerate(buckets):
        queries.append({"id": f"s{i}", "namespace": "AWS/S3", "metric": "NumberOfObjects",
                        "dims": [{"Name": "BucketName", "Value": b["Name"]},
                                 {"Name": "StorageType", "Value": "AllStorageTypes"}], "stat": "Average"})
    data = _get_metric_data(cw, queries, days)
    recs = []
    for i, b in enumerate(buckets):
        series = data.get(f"s{i}", [])
        last = _last_change_day(series)  # last WRITE/DELETE day (level-metric change)
        created = b["CreationDate"].astimezone(dt.timezone.utc).isoformat() if b.get("CreationDate") else ""
        # read-blindness accepted (Andrew 2026-07-17): signal_basis states the write-only basis.
        recs.append({"rtype": "S3_BUCKET", "name": b["Name"], "created": created,
                     "hist": {"read": bool(series), "last_invoked_day": last,
                              "total": None},
                     "signal_basis": "storage-delta(write-only; READ-UNKNOWN)"})
    return recs


def adapt_ec2(region: str, days: int) -> list:
    import boto3
    ec2 = boto3.client("ec2", region_name=region)
    cw = _cw(region)
    insts = []
    for resv in ec2.describe_instances().get("Reservations", []):
        for ins in resv.get("Instances", []):
            insts.append(ins)
    queries = []
    for i, ins in enumerate(insts):
        iid = ins["InstanceId"]
        queries.append({"id": f"e{i}_cpu", "namespace": "AWS/EC2", "metric": "CPUUtilization",
                        "dims": [{"Name": "InstanceId", "Value": iid}], "stat": "Average"})
        queries.append({"id": f"e{i}_net", "namespace": "AWS/EC2", "metric": "NetworkIn",
                        "dims": [{"Name": "InstanceId", "Value": iid}], "stat": "Sum"})
    data = _get_metric_data(cw, queries, days)
    recs = []
    for i, ins in enumerate(insts):
        iid = ins["InstanceId"]
        cpu = data.get(f"e{i}_cpu", [])
        net = data.get(f"e{i}_net", [])
        # a day is ACTIVE if CPU over floor OR NetworkIn over floor.
        active_days = {ts.date() for ts, v in cpu if (v or 0) >= EC2_CPU_FLOOR}
        active_days |= {ts.date() for ts, v in net if (v or 0) >= EC2_NETIN_FLOOR}
        last = max(active_days).isoformat() if active_days else None
        lt = ins.get("LaunchTime")
        created = lt.astimezone(dt.timezone.utc).isoformat() if lt else ""
        recs.append({"rtype": "EC2_INSTANCE", "name": ins.get("InstanceId"), "created": created,
                     "hist": {"read": bool(cpu or net), "last_invoked_day": last, "total": None},
                     "signal_basis": f"cw-cpu>={EC2_CPU_FLOOR}%|netin>={EC2_NETIN_FLOOR}b (idle!=stopped -> PURPOSE-REVIEW)"})
    return recs


def adapt_events(region: str, days: int) -> list:
    import boto3
    ev = boto3.client("events", region_name=region)
    cw = _cw(region)
    rules, tok = [], None
    while True:
        kw = {"NextToken": tok} if tok else {}
        r = ev.list_rules(**kw)
        rules += [rr["Name"] for rr in r.get("Rules", [])]
        tok = r.get("NextToken")
        if not tok:
            break
    queries = [{"id": f"r{i}", "namespace": "AWS/Events", "metric": "Invocations",
                "dims": [{"Name": "RuleName", "Value": n}], "stat": "Sum"} for i, n in enumerate(rules)]
    data = _get_metric_data(cw, queries, days)
    recs = []
    for i, n in enumerate(rules):
        series = data.get(f"r{i}", [])
        last = _last_nonzero_day(series)
        # EventBridge has no rule-creation API -> creation UNKNOWN (honest: a never-fired rule with
        # unknown creation is UNKNOWN, not cold). Production seeds it from the graph snapshot_ts.
        recs.append({"rtype": "EVENT_RULE", "name": n, "created": "",
                     "hist": {"read": True, "last_invoked_day": last,
                              "total": int(sum(v for _, v in series))},
                     "signal_basis": "cw-events-invocations (creation UNKNOWN -> graph-seed in prod)"})
    return recs


ADAPTERS = {"ddb": adapt_dynamodb, "s3": adapt_s3, "ec2": adapt_ec2, "events": adapt_events}


# ---- the multi-type ledger (reuses cd.classify + cd._HELD_RX -- the invariants) ------------
def ext_ledger(records: list, now_date, days: int, hot_days: int) -> dict:
    held, classified = [], []
    for rec in records:
        if cd._HELD_RX.search(rec["name"]):
            held.append(f"{rec['rtype']}:{rec['name']}")
            continue
        row = {"name": rec["name"], "last_modified": rec["created"]}
        band = cd.classify(row, rec["hist"], now_date, days, hot_days)
        band["rtype"] = rec["rtype"]
        band["signal_basis"] = rec["signal_basis"]
        classified.append(band)
    by_band = {b: [c for c in classified if c["band"] == b] for b in cd.BANDS}
    reap = sorted(by_band["COLD-DORMANT"], key=lambda c: -c.get("dormant_days", 0))
    return {"window_days": days, "hot_days": hot_days, "n_total": len(records),
            "n_held_excluded": len(held), "held_excluded": sorted(held),
            "counts": {b: len(by_band[b]) for b in cd.BANDS},
            "reap_rank_cold_dormant": reap,
            "purpose_review_stillborn_or_guard": by_band["STILLBORN-OR-GUARD"],
            "too_young": by_band["TOO-YOUNG"], "unknown": by_band["UNKNOWN"], "hot": by_band["HOT"]}


def _render(led: dict) -> str:
    L = ["comp-debris-ext (PROTOTYPE) -- multi-type coldest-first ledger (ADVISORY; NEVER deletes; hold-aware)",
         "  window %dd (hot %dd) | %d resources | %d held EXCLUDED | per-row SIGNAL BASIS shown"
         % (led["window_days"], led["hot_days"], led["n_total"], led["n_held_excluded"]),
         "  bands: " + " ".join("%s=%d" % (b, led["counts"][b]) for b in cd.BANDS),
         "",
         "  REAP RANK -- COLD-DORMANT only (dormancy AFTER activity; coldest first):"]
    if not led["reap_rank_cold_dormant"]:
        L.append("    (none dormant-after-activity in window)")
    for c in led["reap_rank_cold_dormant"][:30]:
        L.append("    %4dd  %-16s %-40s last=%s  [%s]"
                 % (c.get("dormant_days", 0), c["rtype"], c["name"], c.get("last_invoked"), c["signal_basis"]))
    sob = led["purpose_review_stillborn_or_guard"]
    if sob:
        L += ["", "  PURPOSE REVIEW -- STILLBORN-OR-GUARD (%d): older than window, zero activity" % len(sob)]
        for c in sob[:20]:
            L.append("    %-16s %-40s created=%s  [%s]" % (c["rtype"], c["name"], c["created"], c["signal_basis"]))
    if led["counts"]["UNKNOWN"]:
        L += ["", "  UNKNOWN (%d): blind read / no creation date -- NOT cold (see signal_basis)." % led["counts"]["UNKNOWN"]]
    L += ["", "  NOTE: T-1/trading-calendar (design sec.4.5) is a PROD requirement for pipeline/data buckets --",
          "  a data bucket write-cold over a weekend is CORRECT T-1, not cold. This prototype does NOT yet",
          "  fold lib/trading_calendar; do not reap a data bucket off a wall-clock window."]
    return "\n".join(L)


# ---- offline self-test: band mutants per type (no AWS) ------------------------------------
def _self_test() -> int:
    print("=== comp-debris-ext --self-test (offline band mutants; reuses cd.classify) ===")
    now = dt.date(2026, 7, 17)
    days, hot = 30, 7
    def iso(d):
        return "%sT00:00:00+00:00" % d
    records = [
        # DDB dormant-after-activity -> COLD-DORMANT (reap)
        {"rtype": "DYNAMODB_TABLE", "name": "ddb-cold", "created": iso("2026-01-01"),
         "hist": {"read": True, "last_invoked_day": "2026-06-20", "total": 5}, "signal_basis": "cw-capacity"},
        # S3 never-written-in-window + OLD -> STILLBORN-OR-GUARD (never cold)
        {"rtype": "S3_BUCKET", "name": "s3-flat-old", "created": iso("2025-01-01"),
         "hist": {"read": True, "last_invoked_day": None, "total": None}, "signal_basis": "storage-delta"},
        # S3 within-window creation, no writes -> TOO-YOUNG
        {"rtype": "S3_BUCKET", "name": "s3-new", "created": iso("2026-07-10"),
         "hist": {"read": True, "last_invoked_day": None, "total": None}, "signal_basis": "storage-delta"},
        # EC2 blind (metric read failed) -> UNKNOWN, never cold
        {"rtype": "EC2_INSTANCE", "name": "ec2-blind", "created": iso("2026-01-01"),
         "hist": {"read": False, "error": "AccessDenied"}, "signal_basis": "cw-cpu"},
        # HELD name -> excluded entirely
        {"rtype": "LAMBDA", "name": "inf-gold-trigger", "created": iso("2026-01-01"),
         "hist": {"read": True, "last_invoked_day": None, "total": 0}, "signal_basis": "cw-invocations"},
        # EventBridge hot -> HOT
        {"rtype": "EVENT_RULE", "name": "rule-hot", "created": iso("2026-01-01"),
         "hist": {"read": True, "last_invoked_day": "2026-07-16", "total": 900}, "signal_basis": "cw-events"},
    ]
    led = ext_ledger(records, now, days, hot)
    ok = []
    def ck(name, cond, detail=""):
        ok.append(cond)
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    reap = {c["name"] for c in led["reap_rank_cold_dormant"]}
    ck("ddb_dormant_is_reap", reap == {"ddb-cold"} and led["reap_rank_cold_dormant"][0]["dormant_days"] == 27, f"reap={reap}")
    ck("s3_flat_old_is_stillborn",
       any(c["name"] == "s3-flat-old" for c in led["purpose_review_stillborn_or_guard"]) and "s3-flat-old" not in reap)
    ck("s3_new_is_too_young", any(c["name"] == "s3-new" for c in led["too_young"]) and "s3-new" not in reap)
    ck("ec2_blind_is_unknown", any(c["name"] == "ec2-blind" for c in led["unknown"]) and "ec2-blind" not in reap)
    ck("held_excluded", "LAMBDA:inf-gold-trigger" in led["held_excluded"]
       and all("inf-gold-trigger" not in {c["name"] for c in led[k]}
               for k in ("reap_rank_cold_dormant", "purpose_review_stillborn_or_guard", "unknown", "too_young", "hot")))
    ck("event_hot_is_hot", any(c["name"] == "rule-hot" for c in led["hot"]) and "rule-hot" not in reap)
    ck("signal_basis_on_every_row", all(c.get("signal_basis") for c in led["reap_rank_cold_dormant"] + led["hot"]))
    good = all(ok)
    print("\n" + ("OK: multi-type never-active!=cold, UNKNOWN-band, hold-aware, signal-basis-per-row -- all held"
                  if good else "ERROR: comp-debris-ext self-test FAILED"))
    return 0 if good else 1


def main() -> int:
    ap = argparse.ArgumentParser(prog="comp-debris-ext",
                                 description="comp-debris extension PROTOTYPE (S3/DDB/EC2/EventBridge). Advisory; NEVER deletes.")
    ap.add_argument("--types", default="ddb,s3,ec2,events", help="comma list: ddb,s3,ec2,events")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--hot-days", type=int, default=7)
    ap.add_argument("--region", default=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass
    if args.self_test:
        return _self_test()
    records = []
    for t in [x.strip() for x in args.types.split(",") if x.strip()]:
        if t not in ADAPTERS:
            sys.stderr.write(f"unknown type '{t}' (known: {','.join(ADAPTERS)})\n")
            continue
        try:
            records += ADAPTERS[t](args.region, args.days)
        except Exception as e:  # noqa: BLE001 -- an adapter read failure is surfaced, never assumed-cold
            sys.stderr.write(f"adapter {t} failed: {str(e)[:120]}\n")
    now_date = dt.datetime.now(dt.timezone.utc).date()
    led = ext_ledger(records, now_date, args.days, args.hot_days)
    led["region"] = args.region
    print(json.dumps(led, indent=1, default=str) if args.json else _render(led))
    return 0


if __name__ == "__main__":
    sys.exit(main())
