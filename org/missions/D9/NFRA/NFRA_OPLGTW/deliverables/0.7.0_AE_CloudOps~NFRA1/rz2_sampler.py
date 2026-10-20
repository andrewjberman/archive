#!/usr/bin/env python
"""OG-rz-2 Phase B: the DOWNTIME sampler. Runs until the stop file exists. Every 2 seconds one unauthenticated POST to the public MCP endpoint (a healthy gateway answers 401 itself; a stopped or hung one answers 5xx or nothing);
every 5th sample also reads the target group's state. READ ONLY; writes one JSON line per sample: UTC time, the HTTP status word (or the error class), and the target state. No address is written.
usage: python rz2_sampler.py <out.jsonl> <stopfile>"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request

import boto3

OUT, STOP = sys.argv[1:3]
URL = "https://mcp.opalinvest.dev/mcp"
INSTANCE = "i-07dccb1615503ac99"
elb = boto3.client("elbv2", region_name="us-east-1")
TGARNS = [t["TargetGroupArn"] for t in elb.describe_target_groups()["TargetGroups"] if "gateway" in t["TargetGroupName"]]


def probe():
    try:
        req = urllib.request.Request(URL, data=b"{}", method="POST", headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except Exception as exc:  # noqa: BLE001
        return type(exc).__name__


def target_state():
    try:
        return [d["TargetHealth"]["State"] for a in TGARNS for d in elb.describe_target_health(TargetGroupArn=a)["TargetHealthDescriptions"] if d["Target"]["Id"] == INSTANCE]
    except Exception as exc:  # noqa: BLE001
        return type(exc).__name__


def main():
    n = 0
    with open(OUT, "a", encoding="utf-8", newline="\n") as fh:
        while not os.path.exists(STOP):
            rec = {"t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "code": probe()}
            if n % 5 == 0:
                rec["target"] = target_state()
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            n += 1
            time.sleep(2)
    print("sampler stopped after %d samples" % n)


if __name__ == "__main__":
    main()
