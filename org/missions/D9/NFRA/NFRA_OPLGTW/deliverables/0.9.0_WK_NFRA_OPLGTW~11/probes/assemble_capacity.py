#!/usr/bin/env python3
"""OG-r-3 -- assemble CAPACITY.json from (a) the on-host run of onhost_bench.py (fetched verbatim over SSM), (b) the
ALB idle_timeout read taken immediately before that run, and (c) CloudWatch GetMetricStatistics reads for the two
ruled AC4 windows. Every source is cited in `assembled_from`. This script makes AWS READ calls (elbv2/cloudwatch
through .tools/aws.cmd); the probe og_r3.py makes none.

Usage: assemble_capacity.py <host_run.json> <alb_dir> <out CAPACITY.json>
"""
from __future__ import annotations

import datetime as _dt
import json
import subprocess
import sys
from pathlib import Path

AWS = str(Path(__file__).resolve().parents[8] / ".tools" / "aws.cmd")
REGION = "us-east-1"
LB_DIM = "app/opal-gateway/89166a68f337e5a4"
TG_DIM = "targetgroup/opal-gateway-tg/00997fc81f087cb8"
BEFORE_P95 = 0.5535024102704742      # OGP1-AC11, 2026-09-02T19:15Z..2026-09-16T19:15Z, sample_count 43745
BASELINE = ("2026-09-11T00:00:00Z", "2026-09-18T00:00:00Z")
POST = ("2026-09-21T00:00:00Z", "2026-09-28T00:00:00Z")
DEADLINE_S = 30.0


def aws(*args: str) -> dict:
    out = subprocess.run([AWS, *args, "--region", REGION, "--output", "json"], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError("aws %s failed: %s" % (" ".join(args[:3]), out.stderr[:300]))
    return json.loads(out.stdout)


def stats(metric: str, start: str, end: str, period: int, statistic=None, extended=None) -> list:
    args = ["cloudwatch", "get-metric-statistics", "--namespace", "AWS/ApplicationELB", "--metric-name", metric,
            "--dimensions", "Name=LoadBalancer,Value=" + LB_DIM, "Name=TargetGroup,Value=" + TG_DIM,
            "--start-time", start, "--end-time", end, "--period", str(period)]
    if statistic:
        args += ["--statistics", *statistic]
    if extended:
        args += ["--extended-statistics", *extended]
    return aws(*args)["Datapoints"]


def day_key(ts: str) -> str:
    """The UTC calendar day of a CloudWatch datapoint timestamp. The CLI renders timestamps in LOCAL time
    (e.g. 2026-09-10T20:00:00-04:00 is the 2026-09-11T00:00Z bucket), so slicing the string would shift every
    bucket a day; convert to UTC first."""
    return _dt.datetime.fromisoformat(ts).astimezone(_dt.timezone.utc).date().isoformat()


def window(start: str, end: str) -> dict:
    fives = {day_key(p["Timestamp"]): p["Sum"] for p in stats("HTTPCode_Target_5XX_Count", start, end, 86400, ["Sum"])}
    reqs = {day_key(p["Timestamp"]): p["Sum"] for p in stats("RequestCount", start, end, 86400, ["Sum"])}
    rt = {day_key(p["Timestamp"]): p for p in stats("TargetResponseTime", start, end, 86400, ["SampleCount"],
                                                     ["p95"])}
    d0 = _dt.date.fromisoformat(start[:10])
    days = []
    for i in range(7):
        d = (d0 + _dt.timedelta(days=i)).isoformat()
        p = rt.get(d, {})
        days.append({"day": d, "http_5xx_sum": fives.get(d, 0.0), "http_5xx_datapoint_present": d in fives,
                     "request_count_sum": reqs.get(d, 0.0), "sample_count": p.get("SampleCount", 0.0),
                     "p95_seconds": (p.get("ExtendedStatistics") or {}).get("p95")})
    whole = stats("TargetResponseTime", start, end, 7 * 86400, ["SampleCount"], ["p95"])
    w = whole[0] if whole else {}
    return {
        "window_start": start, "window_end": end, "day_buckets": len(days), "days": days,
        "http_5xx_sum_total": sum(x["http_5xx_sum"] for x in days),
        "request_count_total": sum(x["request_count_sum"] for x in days),
        "zero_5xx_every_day": all(x["http_5xx_sum"] == 0 for x in days),
        "requests_nonzero_every_day": all(x["request_count_sum"] > 0 for x in days),
        "window_sample_count": w.get("SampleCount"),
        "window_p95_seconds": (w.get("ExtendedStatistics") or {}).get("p95"),
        "window_p95_period_seconds": 7 * 86400,
    }


def main(argv: list) -> int:
    host_path, alb_dir, out_path = Path(argv[1]), Path(argv[2]), Path(argv[3])
    d = json.loads(host_path.read_text(encoding="utf-8"))
    attrs = json.loads((alb_dir / "alb_attrs.json").read_text(encoding="utf-8"))["Attributes"]
    idle = int(next(a["Value"] for a in attrs if a["Key"] == "idle_timeout.timeout_seconds"))
    arn = (alb_dir / "alb_arn.txt").read_text(encoding="utf-8").strip()
    read_utc = (alb_dir / "alb_read_utc.txt").read_text(encoding="utf-8").strip()

    base = window(*BASELINE)
    post = window(*POST)
    reg = None
    if base["window_p95_seconds"] is not None:
        reg = (base["window_p95_seconds"] - BEFORE_P95) / BEFORE_P95
    post_reg = None
    if post["window_p95_seconds"] is not None:
        post_reg = (post["window_p95_seconds"] - BEFORE_P95) / BEFORE_P95
    d["ac4"] = {
        "instrument": "CloudWatch GetMetricStatistics, namespace AWS/ApplicationELB, period 86400 per day bucket "
                      "(plus one 7-day period for the window p95); metrics HTTPCode_Target_5XX_Count Sum, "
                      "RequestCount Sum, TargetResponseTime SampleCount + p95",
        "dimensions": {"LoadBalancer": LB_DIM, "TargetGroup": TG_DIM},
        "before_reference": {"source": "OG-p-1 BASELINE.json OGP1-AC11", "p95_seconds": BEFORE_P95,
                             "window": "2026-09-02T19:15Z..2026-09-16T19:15Z", "sample_count": 43745.0},
        "baseline_window": base, "post_release_window": post,
        "baseline_p95_regression_fraction": reg, "p95_regression_max_fraction": 0.2,
        "baseline_p95_within_cap": (reg is not None and reg <= 0.2),
        "post_release_p95_regression_fraction": post_reg,
        "named_incident_disqualification": "a named incident disqualifies any window that contains it; nothing is "
                                           "excised from inside a window (R-OG-23B)",
    }
    d["ac5"] = {"instrument": "elbv2 describe-load-balancer-attributes idle_timeout.timeout_seconds",
                "load_balancer_arn": arn, "read_utc": read_utc, "idle_timeout_seconds": idle,
                "query_export_prep_deadline_seconds": DEADLINE_S, "idle_timeout_exceeds_prep_deadline": idle > DEADLINE_S}
    d["assembled_from"] = {
        "onhost_run": "SSM command e32bd390-4b24-4e5f-9e4d-49824f691a05 (full scale, /opt/opal-gateway/.venv python on "
                      "i-07dccb1615503ac99), JSON fetched verbatim by SSM 509be35b-21ea-4c63-a24f-bb1388933e58",
        "alb_attrs": "elbv2 describe-load-balancer-attributes at " + read_utc,
        "cloudwatch": "get-metric-statistics, windows %s..%s and %s..%s" % (BASELINE + POST),
    }
    d["assembled_utc"] = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out_path.write_text(json.dumps(d, indent=1, sort_keys=True), encoding="utf-8", newline="\n")
    print("wrote", out_path)
    print("baseline: 5xx total", base["http_5xx_sum_total"], "requests", base["request_count_total"],
          "p95", base["window_p95_seconds"], "regression", reg)
    print("post:     5xx total", post["http_5xx_sum_total"], "requests", post["request_count_total"],
          "p95", post["window_p95_seconds"], "regression", post_reg)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
