"""AMGT_RESAPP round 71 -- the Lead Panel load, COLD and WARM, on the DEPLOYED function (CTO au-7 half condition 3).

  python leadpanel_cold_warm.py --label before|after [--burst 6]

For each Lead Panel read, fires --burst invokes AT ONCE, so the function must start new containers, then 3 sequential invokes.
Each invoke's REPORT line (LogType Tail) gives Duration and, on a container's first request, Init Duration. A COLD sample is one
whose REPORT carries Init Duration; its total is Init + Duration. A WARM sample has none. Prints per read: cold n / min / max
(total ms), warm n / min / max (Duration ms), and the CodeSha256 read before the run. Writes nothing to AWS.
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor

import boto3

FN = "opal-amgt-scoped-api"
P = "/api/scoped/amgt"
READS = [("/lead-panel/timeseries/collected/chatter", {"days": d}) for d in ("30", "90", "365")]
READS += [(f"/lead-panel/rankings/{mv}/price", q) for mv in ("trending", "breakout") for q in (None, {"days": "90"}, {"days": "365"})]


def invoke(lam, path, q):
    ev = {"rawPath": P + path, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
          "queryStringParameters": q}
    r = lam.invoke(FunctionName=FN, Payload=json.dumps(ev).encode(), LogType="Tail")
    out = json.loads(r["Payload"].read())
    log = base64.b64decode(r["LogResult"]).decode(errors="replace")
    d = re.search(r"\tDuration: ([0-9.]+) ms", log)
    i = re.search(r"Init Duration: ([0-9.]+) ms", log)
    return out.get("statusCode"), float(d.group(1)) if d else None, float(i.group(1)) if i else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--burst", type=int, default=6)
    a = ap.parse_args()
    lam = boto3.client("lambda", region_name="us-east-1")
    sha = lam.get_function_configuration(FunctionName=FN)["CodeSha256"]
    print(f"LEADPANEL {a.label}: CodeSha256 {sha} at {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    for path, q in READS:
        with ThreadPoolExecutor(a.burst) as ex:
            burst = list(ex.map(lambda _: invoke(lam, path, q), range(a.burst)))
        seq = [invoke(lam, path, q) for _ in range(3)]
        samples = burst + seq
        cold = [d + i for s, d, i in samples if i is not None and d is not None]
        warm = [d for s, d, i in samples if i is None and d is not None]
        codes = sorted({s for s, _, _ in samples})
        label = path + ("?days=" + q["days"] if q else "")

        def fmt(xs):
            return f"n {len(xs)} min {min(xs):.0f} max {max(xs):.0f}" if xs else "n 0"

        print(f"   {label}: cold(init+duration) {fmt(cold)} | warm(duration) {fmt(warm)} | status {codes}")


if __name__ == "__main__":
    main()
