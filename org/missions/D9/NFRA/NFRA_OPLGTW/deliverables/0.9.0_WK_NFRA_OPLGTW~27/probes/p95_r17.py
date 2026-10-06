#!/usr/bin/env python3
"""OG-pm-1 -- read-only CloudWatch reads for the full day 2026-10-05 and write P95_R17.json. Usage: p95_r17.py <out> <md5_note>"""
import datetime as dt
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
P = HERE.parents[2] / "0.9.0_WK_NFRA_OPLGTW~11" / "probes" / "assemble_capacity.py"
spec = importlib.util.spec_from_file_location("ac", P)
ac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ac)

WS, WE = "2026-10-05T00:00:00Z", "2026-10-06T00:00:00Z"
SEGS = [("4b6b823fae", "2026-10-05T00:00:00Z", "2026-10-05T02:17:58Z"),
        ("e91819e281", "2026-10-05T02:17:58Z", "2026-10-05T14:22:36Z"),
        ("37be3485db", "2026-10-05T14:22:36Z", "2026-10-06T00:00:00Z")]


def secs(a, b):
    def f(x):
        return dt.datetime.fromisoformat(x.replace("Z", "+00:00"))
    return int((f(b) - f(a)).total_seconds())


def floor_min(x):
    f = dt.datetime.fromisoformat(x.replace("Z", "+00:00"))
    return f.replace(second=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def ceil_min(x):
    f = dt.datetime.fromisoformat(x.replace("Z", "+00:00"))
    if f.second:
        f = f.replace(second=0) + dt.timedelta(minutes=1)
    return f.strftime("%Y-%m-%dT%H:%M:%SZ")


def one(a, b):
    """one period spanning [a,b] widened outward to whole minutes (CloudWatch period must be a multiple of 60)"""
    a, b = floor_min(a), ceil_min(b)
    n = secs(a, b)
    rt = ac.stats("TargetResponseTime", a, b, n, ["SampleCount"], ["p95"])
    rq = ac.stats("RequestCount", a, b, n, ["Sum"])
    fx = ac.stats("HTTPCode_Target_5XX_Count", a, b, n, ["Sum"])
    p95 = None
    samples = None
    if rt:
        if len(rt) != 1:
            print("WARN: %d datapoints for %s..%s" % (len(rt), a, b))
        p95 = rt[0]["ExtendedStatistics"]["p95"]
        samples = rt[0]["SampleCount"]
    return {"p95_seconds": p95, "sample_count": samples,
            "request_count": (int(sum(x["Sum"] for x in rq)) if rq else None),
            "5xx_sum": (int(sum(x["Sum"] for x in fx)) if fx else None),
            "query": [a, b], "datapoints": {"rt": len(rt), "req": len(rq), "5xx": len(fx)}}


def main():
    out, md5note = sys.argv[1], sys.argv[2]
    full = one(WS, WE)
    segs = []
    for rel, a, b in SEGS:
        r = one(a, b)
        segs.append({"release": rel, "start": a, "end": b, "p95_seconds": r["p95_seconds"],
                     "request_count": r["request_count"], "5xx_sum": r["5xx_sum"], "sample_count": r["sample_count"], "query_window_widened_to_whole_minutes": r["query"]})
    hourly = []
    s = dt.datetime.fromisoformat(WS.replace("Z", "+00:00"))
    for i in range(24):
        a = (s + dt.timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        b = (s + dt.timedelta(hours=i + 1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        r = one(a, b)
        hourly.append({"hour_start": a, "p95_seconds": r["p95_seconds"], "request_count": r["request_count"],
                       "5xx_sum": r["5xx_sum"], "datapoint_present": r["datapoints"]["rt"] > 0})
    p95 = full["p95_seconds"]
    ok = p95 is not None and p95 <= 0.5535 * 1.2
    d = {"window_start": WS, "window_end": WE, "served_segments": segs, "request_count": full["request_count"],
         "5xx_sum": full["5xx_sum"], "sample_count": full["sample_count"], "p95_seconds": p95,
         "hourly_p95": hourly, "reference_seconds": 0.5535, "cap_fraction": 0.20, "cap_seconds": 0.5535 * 1.2,
         "verdict": "WITHIN_CAP" if ok else "REGRESSION", "host_md5_witness": md5note,
         "full_day_datapoints": full["datapoints"],
         "instrument": "CloudWatch GetMetricStatistics AWS/ApplicationELB LB %s TG %s; p95 ExtendedStatistics, one period per window/segment/hour" % (ac.LB_DIM, ac.TG_DIM)}
    if not ok:
        d["row_id"] = "NFRA_OPLGTW-Z-W27-S3"
    Path(out).write_text(json.dumps(d, indent=1), encoding="utf-8", newline="\n")
    print("p95", p95, "req", full["request_count"], "5xx", full["5xx_sum"], "verdict", d["verdict"])
    for sg in segs:
        print(sg)
    for h in hourly:
        print(h)


main()
