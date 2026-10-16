#!/usr/bin/env python
"""OG-ev-3: READ-ONLY measurement of the full 13-month 49F read on the gateway host at concurrency 16. One file, two roles:
  python ev3_measure.py <table> <out.json>   -> the RUNNER (repository root): uploads itself to S3, runs once over SSM (Rule 12), writes <out.json>
  python ev3_measure.py --host <table>       -> the HOST program (on i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python)

For one table (transactions | fees): through the installed adapter's own read path -- ctx.read_rows(prefix, part, columns=...) with the adapter's own column list
(TXN_COLUMNS, FEE_READ_COLUMNS) -- read EVERY dated partition of the 13-month window ending at the newest partition (the adapter's own _window_plan supplies the list),
ThreadPoolExecutor(16), 5 runs, the cold first run counted. Rows are read and counted, never kept or printed.
GUARDS: a memory monitor samples /proc/meminfo every 0.25 s during every read; a PILOT of 16 partitions at the real concurrency runs first and the measurement does not start
if its peak used memory passes 70 percent; any sample above 80 percent aborts the run (the order's bound is 85; the host has no swap, so the margin is deliberate).
BYTES are the sum of the S3 object sizes of the files read (compressed parquet as stored), not the bytes after column pruning.
Output: seconds, counts, bytes, percentages. No key, account id, amount or name."""
from __future__ import annotations

import io
import json
import os
import sys
import threading
import time
import traceback

ROOT = "/opt/opal-gateway"
CONC = 16
RUNS = 5
STOP_PCT = 80.0
PILOT_STOP_PCT = 70.0
WINDOW_DAYS = 395


def mem_used_pct():
    d = {}
    for ln in open("/proc/meminfo"):
        k, v = ln.split(":", 1)
        d[k] = int(v.split()[0])
    return 100.0 * (1.0 - d["MemAvailable"] / d["MemTotal"])


def cpu_times():
    f = open("/proc/stat").readline().split()[1:]
    v = [int(x) for x in f]
    idle = v[3] + (v[4] if len(v) > 4 else 0)
    return sum(v), idle


def gw_rss_mb():
    best = 0
    for pid in os.listdir("/proc"):
        if pid.isdigit():
            try:
                cmd = open("/proc/%s/cmdline" % pid, "rb").read().replace(b"\0", b" ").decode("utf-8", "replace")
                if "uvicorn" in cmd:
                    for ln in open("/proc/%s/status" % pid):
                        if ln.startswith("VmRSS:"):
                            best = max(best, int(ln.split()[1]) // 1024)
            except Exception:
                pass
    return best


class Monitor(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.peak = 0.0
        self.stop_flag = threading.Event()
        self.abort = threading.Event()
        self.samples = 0

    def run(self):
        while not self.stop_flag.is_set():
            p = mem_used_pct()
            self.samples += 1
            self.peak = max(self.peak, p)
            if p > STOP_PCT:
                self.abort.set()
            time.sleep(0.25)


def pct(xs, q):
    s = sorted(xs)
    if len(s) == 1:
        return s[0]
    k = (len(s) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def host(table: str) -> dict:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    with open(os.path.join(ROOT, ".env"), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v)
    import datetime as dt
    from concurrent.futures import ThreadPoolExecutor
    from app import client_core as cc
    from app import client_adapter_bd49f as bd
    from app import typed_scope
    out = {"table": table, "concurrency": CONC, "stop_pct": STOP_PCT}
    columns = bd.TXN_COLUMNS if table == "transactions" else bd.FEE_READ_COLUMNS
    ctx = cc._new_ctx()
    bd.bind_firms()
    segment = bd._firm(ctx, "49financial")
    prefix = bd._live_prefix(ctx, segment, table)
    semantics = bd.PARTITION_SEMANTICS[table]
    dated = bd._partitions(ctx, prefix)
    newest = dated[-1]
    end = dt.date.fromisoformat(newest)
    start = end - dt.timedelta(days=WINDOW_DAYS)
    plan = bd._window_plan(ctx, prefix, semantics, start, end, None)
    in_window = list(plan["in_window"])
    out.update({"partitions_listed_in_prefix": len(dated), "partitions": len(in_window), "first": in_window[0], "last": in_window[-1], "semantics": semantics,
                "columns": len(columns)})
    # object sizes of exactly the files the reader picks (same listing the reader makes)
    scope = ctx._scope(prefix)
    real = scope.served_prefixes[0]
    listed = typed_scope.list_keys(scope, real)
    by_part = {}
    for o in listed:
        if o["key"].endswith(".parquet"):
            d = cc._partition_of(cc._tail(o["key"], real))
            if d:
                by_part.setdefault(d, []).append(o)
    size_of = lambda o: int(o.get("size") if o.get("size") is not None else o.get("Size", 0) or 0)   # noqa: E731
    total_bytes = sum(size_of(max(by_part[p], key=lambda o: o["key"])) for p in in_window if p in by_part)
    out["bytes"] = total_bytes
    out["bytes_basis"] = "sum of the S3 object sizes of the files read (compressed parquet as stored), not the bytes after column pruning"
    out["files_with_a_listed_object"] = sum(1 for p in in_window if p in by_part)

    mon = Monitor()
    mon.start()
    out["host_before"] = {"mem_used_pct": round(mem_used_pct(), 1), "gateway_rss_mb": gw_rss_mb(), "cpus": os.cpu_count()}

    def one(part):
        if mon.abort.is_set():
            return None
        try:
            return len(ctx.read_rows(prefix, part, columns=list(columns)))
        except Exception as exc:
            return "ERR:" + type(exc).__name__

    def read_all(parts):
        t0 = time.monotonic()
        c0 = cpu_times()
        with ThreadPoolExecutor(CONC) as ex:
            res = list(ex.map(one, parts))
        wall = time.monotonic() - t0
        c1 = cpu_times()
        errs = sorted({r for r in res if isinstance(r, str)})
        done = [r for r in res if isinstance(r, int)]
        busy = 100.0 * (1.0 - (c1[1] - c0[1]) / max(1, c1[0] - c0[0]))
        return {"wall": wall, "files_read": len(done), "errors": len([r for r in res if isinstance(r, str)]), "error_kinds": errs,
                "empty_reads": sum(1 for r in done if r == 0), "rows": sum(done), "skipped_on_abort": sum(1 for r in res if r is None), "host_cpu_busy_pct": round(busy, 1)}

    # PILOT: 16 partitions at the real concurrency; the measurement does not start if memory goes past the pilot bound
    mon.peak = 0.0
    pilot = read_all(in_window[-CONC:])
    out["pilot"] = {"files": CONC, "wall_seconds": round(pilot["wall"], 2), "peak_mem_used_pct": round(mon.peak, 1), "errors": pilot["errors"]}
    if mon.peak > PILOT_STOP_PCT or mon.abort.is_set() or pilot["errors"]:
        out["verdict"] = "STOPPED-AT-PILOT"
        mon.stop_flag.set()
        return out
    runs = []
    for i in range(RUNS):
        mon.peak = 0.0
        r = read_all(in_window)
        r["peak_mem_used_pct"] = round(mon.peak, 1)
        runs.append(r)
        out["runs_done"] = i + 1
        if mon.abort.is_set() or r["errors"] or r["files_read"] != len(in_window):
            out["verdict"] = "STOPPED-IN-RUN-%d" % (i + 1)
            break
    else:
        out["verdict"] = "COMPLETE"
    mon.stop_flag.set()
    walls = [r["wall"] for r in runs]
    out["runs"] = [{"wall_seconds": round(r["wall"], 3), "files_read": r["files_read"], "errors": r["errors"], "error_kinds": r["error_kinds"], "empty_reads": r["empty_reads"],
                    "rows": r["rows"], "skipped_on_abort": r["skipped_on_abort"], "host_cpu_busy_pct": r["host_cpu_busy_pct"], "peak_mem_used_pct": r["peak_mem_used_pct"]} for r in runs]
    if walls:
        out["p50"] = round(pct(walls, 0.5), 3)
        out["p95"] = round(pct(walls, 0.95), 3)
    out["host_after"] = {"mem_used_pct": round(mem_used_pct(), 1), "gateway_rss_mb": gw_rss_mb()}
    out["peak_mem_used_pct_overall"] = max([r["peak_mem_used_pct"] for r in runs] + [out["pilot"]["peak_mem_used_pct"]])
    return out


def runner(table: str, outp: str) -> None:
    import boto3
    instance = "i-07dccb1615503ac99"
    bucket = "opal-313476888478-lambda-artifacts"
    key = "ec2/opal-gateway/ev3_measure.py"
    boto3.client("s3").put_object(Bucket=bucket, Key=key, Body=io.open(os.path.abspath(__file__), "rb").read())
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/ev3_measure.py && aws s3 cp s3://%s/%s /tmp/ev3_measure.py --region us-east-1 >/dev/null && "
           "/opt/opal-gateway/.venv/bin/python /tmp/ev3_measure.py --host %s" % (bucket, key, table))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=1500)["Command"]["CommandId"]
    inv = None
    for _ in range(320):
        time.sleep(4)
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    io.open(outp + ".raw.txt", "w", encoding="utf-8", newline="\n").write("status=%s\n--- STDOUT ---\n%s\n--- STDERR ---\n%s\n" % (inv["Status"], so, inv.get("StandardErrorContent", "")[-500:]))
    if "EV3_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("EV3_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps({k: v for k, v in doc.items() if k != "runs"}, indent=1))
    for r in doc.get("runs", []):
        print("  run: wall %.2f s, files %d, errors %d, empty %d, cpu %.0f%%, peak mem %.1f%%" % (r["wall_seconds"], r["files_read"], r["errors"], r["empty_reads"], r["host_cpu_busy_pct"], r["peak_mem_used_pct"]))


if __name__ == "__main__":
    if "--host" in sys.argv:
        print("EV3_JSON")
        try:
            print(json.dumps(host(sys.argv[sys.argv.index("--host") + 1]), separators=(",", ":"), default=str))
        except Exception:
            print(json.dumps({"fatal": traceback.format_exc()[-900:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1], sys.argv[2])
