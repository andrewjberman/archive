#!/usr/bin/env python
"""OG-ap-34 Phase B, CTO CT1 Amendment 1: read the SERVICE back, one SSM probe per interval. READ-ONLY.
  python ap34_monitor.py --once                       -> one probe, printed (the baseline taken just before the switch)
  python ap34_monitor.py <out.jsonl> <baseline_mb> [minutes=30] [interval_s=60]  -> the 30-minute read-back
Each probe: UTC time, the service MainPID, its VmRSS (MB), NRestarts, host memory used (percent), the /health status (a probe is its own short call; it never overlaps a page
because no page is run in the service). A line TRIGGER is written to <out.jsonl>.trigger the moment the service grows more than 300 MB above the baseline or the host passes
80 percent (CT1) or 85 percent (the written rollback trigger), or health is not 200 twice in a row. Counts, MB, percentages and UTC times only."""
from __future__ import annotations

import json
import sys
import time

import boto3

INSTANCE = "i-07dccb1615503ac99"
CMD = ("pid=$(systemctl show opal-gateway -p MainPID --value); "
       "rss=$(awk '/^VmRSS:/{print $2}' /proc/$pid/status 2>/dev/null); "
       "host=$(awk '/^MemTotal:/{t=$2}/^MemAvailable:/{a=$2}END{printf \"%.1f\", 100*(1-a/t)}' /proc/meminfo); "
       "code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 http://127.0.0.1:8080/health); "
       "nr=$(systemctl show opal-gateway -p NRestarts --value); "
       "echo \"P|$(date -u +%Y-%m-%dT%H:%M:%SZ)|$pid|$rss|$host|$code|$nr\"")
ssm = boto3.client("ssm")


def probe():
    cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [CMD]})["Command"]["CommandId"]
    for _ in range(40):
        time.sleep(1.5)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    line = next((ln for ln in inv.get("StandardOutputContent", "").splitlines() if ln.startswith("P|")), None)
    if not line:
        return {"t": None, "error": inv.get("Status")}
    _p, t, pid, rss, host, code, nr = line.split("|")
    return {"t": t, "pid": int(pid) if pid.isdigit() else None, "service_rss_mb": round(int(rss) / 1024.0, 1) if rss.isdigit() else None,
            "host_pct": float(host), "health": int(code) if code.isdigit() else None, "n_restarts": nr}


def main():
    if "--once" in sys.argv:
        print(json.dumps(probe()))
        return
    out, base = sys.argv[1], float(sys.argv[2])
    minutes = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    interval = int(sys.argv[4]) if len(sys.argv) > 4 else 60
    t_end = time.monotonic() + minutes * 60
    bad_health = 0
    n = 0
    while True:
        t0 = time.monotonic()
        rec = probe()
        rec["n"] = n
        rec["growth_vs_baseline_mb"] = None if rec.get("service_rss_mb") is None else round(rec["service_rss_mb"] - base, 1)
        with open(out, "a", encoding="utf-8", newline=chr(10)) as fh:
            fh.write(json.dumps(rec) + chr(10))
        why = []
        if rec.get("growth_vs_baseline_mb") is not None and rec["growth_vs_baseline_mb"] > 300:
            why.append("service grew %.1f MB above the baseline" % rec["growth_vs_baseline_mb"])
        if rec.get("host_pct") is not None and rec["host_pct"] > 80:
            why.append("host %.1f percent above 80" % rec["host_pct"])
        bad_health = bad_health + 1 if rec.get("health") != 200 else 0
        if bad_health >= 2:
            why.append("health not 200 on two probes in a row")
        if why:
            with open(out + ".trigger", "a", encoding="utf-8", newline=chr(10)) as fh:
                fh.write("%s %s" % (rec.get("t"), "; ".join(why)) + chr(10))
        n += 1
        if time.monotonic() >= t_end:
            break
        time.sleep(max(1.0, interval - (time.monotonic() - t0)))
    with open(out + ".done", "w", encoding="utf-8") as fh:
        fh.write("done %d probes" % n)


if __name__ == "__main__":
    main()
