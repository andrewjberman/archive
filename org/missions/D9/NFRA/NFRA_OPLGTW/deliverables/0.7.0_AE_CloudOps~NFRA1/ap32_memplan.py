#!/usr/bin/env python
"""OG-ap-32 Phase A: the HOST MEMORY PLAN input. READ-ONLY. How much resident memory does the page read of OG-en-17 hold per dated partition?
  python ap32_memplan.py <out.json>  -> RUNNER (uploads itself to S3, runs once over SSM, Rule 12); python ap32_memplan.py --host -> HOST program.
The OG-en-17 page read returns the rows of ALL its partitions at once (_read_partitions builds a list of (partition, rows) for up to 60 partitions before the fence runs).
This measures, for each of transactions and fees, the process resident-memory growth of reading the newest 8 partitions the same way (ctx.read_rows with the adapter's own
columns, 16 workers, rows RETAINED), converts it to MB per partition, and projects it to a 60-partition page. A monitor aborts at 60 percent host memory used (far below the
85 percent bound, and the page is only 8 files). Seconds, MB, percentages and counts only; no value is printed."""
from __future__ import annotations

import io
import json
import os
import sys
import threading
import time
import traceback

ROOT = "/opt/opal-gateway"
N = 8
ABORT_PCT = 60.0


def mem_used_pct():
    d = {}
    for ln in open("/proc/meminfo"):
        k, v = ln.split(":", 1)
        d[k] = int(v.split()[0])
    return 100.0 * (1.0 - d["MemAvailable"] / d["MemTotal"]), d["MemTotal"] // 1024, d["MemAvailable"] // 1024


def rss_mb():
    for ln in open("/proc/self/status"):
        if ln.startswith("VmRSS:"):
            return int(ln.split()[1]) / 1024.0
    return 0.0


def host() -> dict:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    with open(os.path.join(ROOT, ".env"), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v)
    from concurrent.futures import ThreadPoolExecutor
    from app import client_core as cc
    from app import client_adapter_bd49f as bd
    ctx = cc._new_ctx()
    bd.bind_firms()
    segment = bd._firm(ctx, "49financial")
    out = {"partitions_per_sample": N, "abort_pct": ABORT_PCT}
    pct0, total_mb, avail_mb = mem_used_pct()
    out["host"] = {"mem_total_mb": total_mb, "mem_available_mb_before": avail_mb, "mem_used_pct_before": round(pct0, 1)}
    peak = [0.0]
    stop = threading.Event()
    abort = threading.Event()

    def watch():
        while not stop.is_set():
            p = mem_used_pct()[0]
            peak[0] = max(peak[0], p)
            if p > ABORT_PCT:
                abort.set()
            time.sleep(0.2)
    threading.Thread(target=watch, daemon=True).start()
    for table in ("fees", "transactions"):
        columns = bd.TXN_COLUMNS if table == "transactions" else bd.FEE_READ_COLUMNS
        prefix = bd._live_prefix(ctx, segment, table)
        parts = bd._partitions(ctx, prefix)[-N:]
        rss0 = rss_mb()
        t0 = time.monotonic()
        with ThreadPoolExecutor(16) as ex:
            got = list(ex.map(lambda p: ctx.read_rows(prefix, p, columns=list(columns)), parts))
        wall = time.monotonic() - t0
        rss_hold = rss_mb()                       # rows still referenced by `got`: what a page holds
        rows = [len(g) for g in got]
        kept = sum(len([r for r in g if str(r.get("account_id") or "").startswith(bd.ACCOUNT_PREFIX)]) for g in got)
        per_part = (rss_hold - rss0) / len(parts)
        out[table] = {"partitions": len(parts), "rows_total": sum(rows), "rows_per_partition_avg": sum(rows) // len(parts), "rows_kept_by_the_fence": kept,
                      "wall_seconds": round(wall, 2), "rss_mb_before": round(rss0, 1), "rss_mb_holding_rows": round(rss_hold, 1),
                      "rss_growth_mb_per_partition": round(per_part, 1), "projected_rss_growth_mb_for_60_partitions": round(per_part * 60, 1),
                      "projected_host_used_pct_at_60": round(pct0 + 100.0 * per_part * 60 / total_mb, 1)}
        del got
        if abort.is_set():
            out["aborted_on_memory"] = True
            break
    stop.set()
    out["peak_host_mem_used_pct_during_sampling"] = round(peak[0], 1)
    out["host"]["mem_used_pct_after"] = round(mem_used_pct()[0], 1)
    return out


def runner(outp: str) -> None:
    import boto3
    instance, bucket, key = "i-07dccb1615503ac99", "opal-313476888478-lambda-artifacts", "ec2/opal-gateway/ap32_memplan.py"
    boto3.client("s3").put_object(Bucket=bucket, Key=key, Body=io.open(os.path.abspath(__file__), "rb").read())
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/ap32_memplan.py && aws s3 cp s3://%s/%s /tmp/ap32_memplan.py --region us-east-1 >/dev/null && "
           "/opt/opal-gateway/.venv/bin/python /tmp/ap32_memplan.py --host" % (bucket, key))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=600)["Command"]["CommandId"]
    inv = None
    for _ in range(150):
        time.sleep(4)
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    if "AP32_MEM" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP32_MEM", 1)[1].strip())
    doc["ssm_command_id"] = cid
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))


if __name__ == "__main__":
    if "--host" in sys.argv:
        print("AP32_MEM")
        try:
            print(json.dumps(host(), separators=(",", ":"), default=str))
        except Exception:
            print(json.dumps({"fatal": traceback.format_exc()[-900:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1])
