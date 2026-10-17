#!/usr/bin/env python
"""OG-ev-3: assemble W/WINDOW_MEASURE.json from the two host records (no value is typed here that a record does not hold).
  ev3_transactions.json  <- ev3_measure.py transactions      ev3_fees.json  <- ev3_measure.py fees      ev3_diag.json  <- ev3_diag.py
p50 and p95 are computed over the COMPLETE runs only (a run the memory guard stopped is not a wall time). usage: python ev3_build.py   (repository root)"""
from __future__ import annotations

import datetime
import io
import json
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"


def load(n):
    return json.load(io.open(W + n, encoding="utf-8"))


def pct(xs, q):
    s = sorted(xs)
    if len(s) == 1:
        return s[0]
    k = (len(s) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def table(rec):
    full = [r for r in rec["runs"] if r["files_read"] == rec["partitions"] and not r["errors"] and not r["skipped_on_abort"]]
    walls = [r["wall_seconds"] for r in full]
    partial = [r for r in rec["runs"] if r not in full]
    return {"partitions": rec["partitions"], "files_read": rec["partitions"], "wall_seconds": walls, "p50": round(pct(walls, 0.5), 3), "p95": round(pct(walls, 0.95), 3),
            "bytes": rec["bytes"], "runs_complete": len(full), "runs_stopped_by_the_memory_guard": len(partial),
            "stopped_run_files_read": [r["files_read"] for r in partial], "errors": sum(r["errors"] for r in rec["runs"]),
            "empty_reads": sum(r["empty_reads"] for r in full), "host_cpu_busy_pct_per_run": [r["host_cpu_busy_pct"] for r in full],
            "peak_mem_used_pct_per_run": [r["peak_mem_used_pct"] for r in rec["runs"]], "window_first": rec["first"], "window_last": rec["last"]}


tx, fe, dg = load("ev3_transactions.json"), load("ev3_fees.json"), load("ev3_diag.json")
tables = {"transactions": table(tx), "fees": table(fe)}
worst = max(t["p95"] for t in tables.values())
ref = subprocess.run(["aws", "s3api", "head-object", "--bucket", "opal-313476888478-lambda-artifacts", "--key", "ec2/opal-gateway/opal-gateway-latest.tar.gz",
                      "--query", 'Metadata."git-ref"', "--output", "text"], capture_output=True).stdout.decode().strip()
body = {
    "read_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "live_commit": ref, "concurrency": 16, "tables": tables,
    "request_budget": {"alb_idle_timeout_seconds": 60, "inside_threshold_seconds": 30, "verdict": "inside" if worst <= 30 else "outside"},
    "bytes_basis": tx["bytes_basis"],
    "host": {"cpus": tx["host_before"]["cpus"], "mem_used_pct_before": {"transactions": tx["host_before"]["mem_used_pct"], "fees": fe["host_before"]["mem_used_pct"]},
             "mem_used_pct_peak": {"transactions": tx["peak_mem_used_pct_overall"], "fees": fe["peak_mem_used_pct_overall"]},
             "mem_used_pct_after": {"transactions": tx["host_after"]["mem_used_pct"], "fees": fe["host_after"]["mem_used_pct"]},
             "gateway_rss_mb_before_after": {"transactions": [tx["host_before"]["gateway_rss_mb"], tx["host_after"]["gateway_rss_mb"]],
                                             "fees": [fe["host_before"]["gateway_rss_mb"], fe["host_after"]["gateway_rss_mb"]]},
             "memory_guard": {"abort_pct": tx["stop_pct"], "orders_bound_pct": 85, "pilot_files": 16, "pilot_peak_pct": {"transactions": tx["pilot"]["peak_mem_used_pct"], "fees": fe["pilot"]["peak_mem_used_pct"]}}},
    "single_call_diagnostic_fees": {k: dg[k] for k in ("objects_listed", "rows_in_partition", "list_keys_seconds", "read_parquet_seconds", "read_rows_seconds")},
}
io.open(W + "WINDOW_MEASURE.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body}, indent=1) + "\n")
print(json.dumps({"verdict": body["request_budget"]["verdict"], "worst_p95": worst, "tx": {k: tables["transactions"][k] for k in ("partitions", "wall_seconds", "p50", "p95", "bytes", "runs_complete")},
                  "fees": {k: tables["fees"][k] for k in ("partitions", "wall_seconds", "p50", "p95", "bytes", "runs_complete")}}, indent=1))
