#!/usr/bin/env python3
"""OG-pm-2 -- read-only CloudWatch reads (AWS/ApplicationELB, gateway LB + TG) of RequestCount and TargetResponseTime
SampleCount/p95 for whole UTC days. Usage: pm2_cw.py <out.json> <YYYY-MM-DD> [...]"""
import datetime as dt
import json
import sys

import boto3

LB = "app/opal-gateway/89166a68f337e5a4"
TG = "targetgroup/opal-gateway-tg/00997fc81f087cb8"
cw = boto3.client("cloudwatch", region_name="us-east-1")
D = [{"Name": "LoadBalancer", "Value": LB}, {"Name": "TargetGroup", "Value": TG}]
out = {}
for day in sys.argv[2:]:
    a = dt.datetime.fromisoformat(day + "T00:00:00+00:00")
    b = a + dt.timedelta(days=1)
    rq = cw.get_metric_statistics(Namespace="AWS/ApplicationELB", MetricName="RequestCount", Dimensions=D, StartTime=a, EndTime=b, Period=86400, Statistics=["Sum"])["Datapoints"]
    rt = cw.get_metric_statistics(Namespace="AWS/ApplicationELB", MetricName="TargetResponseTime", Dimensions=D, StartTime=a, EndTime=b, Period=86400, Statistics=["SampleCount"], ExtendedStatistics=["p95"])["Datapoints"]
    out[day] = {"request_count": int(sum(x["Sum"] for x in rq)), "rq_datapoints": len(rq), "rt_datapoints": len(rt),
                "sample_count": rt[0]["SampleCount"] if rt else None, "p95_seconds": rt[0]["ExtendedStatistics"]["p95"] if rt else None}
    print(day, out[day])
json.dump(out, open(sys.argv[1], "w", encoding="utf-8", newline="\n"), indent=1)
