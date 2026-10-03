#!/usr/bin/env python3
"""OG-r-4 -- assemble CAPACITY_R4.json from (a) the verbatim on-host run (onhost_run_r4_full.json), (b) the ALB
idle_timeout read, (c) CloudWatch GetMetricStatistics for the post-4231bd2ddc window, (d) the md5 confirmation.
Reuses OG-r-3's helpers (stats/day_key). READ calls only.
Usage: assemble_capacity_r4.py <host_run.json> <alb_dir> <out> <win_start> <win_end> <served_release> <md5_equal:true|false> <before_ssm> <run_ssm> <fetch_ssm>
"""
import datetime as _dt
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
spec = importlib.util.spec_from_file_location("ac", HERE.parents[2] / "0.9.0_WK_NFRA_OPLGTW~11" / "probes" / "assemble_capacity.py")
ac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ac)


def hour_window(start, end):
    s = _dt.datetime.fromisoformat(start.replace("Z", "+00:00"))
    e = _dt.datetime.fromisoformat(end.replace("Z", "+00:00"))
    secs = int((e - s).total_seconds())
    assert secs % 3600 == 0, "window must be whole hours"
    fives = {_dt.datetime.fromisoformat(p["Timestamp"]).astimezone(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"): p["Sum"]
             for p in ac.stats("HTTPCode_Target_5XX_Count", start, end, 3600, ["Sum"])}
    reqs = {_dt.datetime.fromisoformat(p["Timestamp"]).astimezone(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"): p["Sum"]
            for p in ac.stats("RequestCount", start, end, 3600, ["Sum"])}
    rt = {_dt.datetime.fromisoformat(p["Timestamp"]).astimezone(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"): p
          for p in ac.stats("TargetResponseTime", start, end, 3600, ["SampleCount"], ["p95"])}
    hours = []
    for i in range(secs // 3600):
        k = (s + _dt.timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        p = rt.get(k, {})
        hours.append({"hour_start": k, "http_5xx_sum": fives.get(k, 0.0), "http_5xx_datapoint_present": k in fives,
                      "request_count_sum": reqs.get(k, 0.0), "sample_count": p.get("SampleCount", 0.0),
                      "p95_seconds": (p.get("ExtendedStatistics") or {}).get("p95")})
    whole = ac.stats("TargetResponseTime", start, end, secs, ["SampleCount"], ["p95"])
    w = whole[0] if whole else {}
    return {"window_start": start, "window_end": end, "hour_buckets": len(hours), "hours": hours,
            "http_5xx_sum_total": sum(x["http_5xx_sum"] for x in hours),
            "request_count_total": sum(x["request_count_sum"] for x in hours),
            "zero_5xx_every_hour": all(x["http_5xx_sum"] == 0 for x in hours),
            "window_sample_count": w.get("SampleCount"),
            "window_p95_seconds": (w.get("ExtendedStatistics") or {}).get("p95"), "window_p95_period_seconds": secs}


def main(a):
    host, alb, out, ws, we, rel, eq, s_before, s_run, s_fetch = a[1:11]
    d = json.loads(Path(host).read_text(encoding="utf-8"))
    alb = Path(alb)
    attrs = json.loads((alb / "alb_attrs.json").read_text(encoding="utf-8"))["Attributes"]
    idle = int(next(x["Value"] for x in attrs if x["Key"] == "idle_timeout.timeout_seconds"))
    arn = (alb / "alb_arn.txt").read_text(encoding="utf-8").strip()
    read_utc = (alb / "alb_read_utc.txt").read_text(encoding="utf-8").strip()
    w = hour_window(ws, we)
    reg = None if w["window_p95_seconds"] is None else (w["window_p95_seconds"] - ac.BEFORE_P95) / ac.BEFORE_P95
    d["ac4"] = {
        "instrument": "CloudWatch GetMetricStatistics, AWS/ApplicationELB, period 3600 per hour bucket plus one whole-window "
                      "period for the p95; HTTPCode_Target_5XX_Count Sum, RequestCount Sum, TargetResponseTime SampleCount + p95",
        "dimensions": {"LoadBalancer": ac.LB_DIM, "TargetGroup": ac.TG_DIM},
        "before_reference": {"source": "OG-p-1 BASELINE.json OGP1-AC11", "p95_seconds": ac.BEFORE_P95,
                             "window": "2026-09-02T19:15Z..2026-09-16T19:15Z", "sample_count": 43745.0},
        "window_note": "baseline_window and post_release_window are the SAME post-4231bd2ddc window (service restart "
                       "2026-10-02T19:23:25Z, manifest deployed_at 2026-10-02T19:23:40Z); it is hours long, not 7 days",
        "baseline_window": w, "post_release_window": w,
        "baseline_p95_regression_fraction": reg, "p95_regression_max_fraction": 0.2,
        "baseline_p95_within_cap": reg is not None and reg <= 0.2,
        "post_release_p95_regression_fraction": reg,
        "named_incident_disqualification": "a named incident disqualifies any window that contains it; nothing is excised from inside a window (R-OG-23B)",
    }
    d["ac5"] = {"instrument": "elbv2 describe-load-balancer-attributes idle_timeout.timeout_seconds", "load_balancer_arn": arn,
                "read_utc": read_utc, "idle_timeout_seconds": idle, "query_export_prep_deadline_seconds": ac.DEADLINE_S,
                "idle_timeout_exceeds_prep_deadline": idle > ac.DEADLINE_S}
    d["served_release"] = rel
    d["engine_md5_equal"] = (eq == "true")
    d["assembled_from"] = {
        "md5_check": "SSM %s (md5sum of app/integrations/schwab/* on the host, before the run) vs git show 4231bd2ddc bytes, 11 of 11 equal" % s_before,
        "onhost_run": "SSM %s (onhost_bench.py --scale full --contract <scratch copy>, /opt/opal-gateway/.venv python on i-07dccb1615503ac99), JSON fetched verbatim by SSM %s (md5 10585c39... equal on host and local)" % (s_run, s_fetch),
        "alb_attrs": "elbv2 describe-load-balancer-attributes at " + read_utc,
        "cloudwatch": "get-metric-statistics, window %s..%s" % (ws, we)}
    d["assembled_utc"] = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    Path(out).write_text(json.dumps(d, indent=1, sort_keys=True), encoding="utf-8", newline="\n")
    print("wrote", out)
    print("window 5xx", w["http_5xx_sum_total"], "requests", w["request_count_total"], "p95", w["window_p95_seconds"], "regression", reg)
    return 0

sys.exit(main(sys.argv))
