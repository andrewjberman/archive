"""AMGT_RESAPP round 71 -- c38, the Lead Panel load time (ANDREW-DIRECT 2026-10-05 ~15:0xZ, via 2.0.0_SA_COO~D msg 29618:
"the chatter/price views take almost a minute to load").

  --where deployed|local [--bar-ms 2000]

Times each Lead Panel read the page makes, warm (one priming call first, then 3 timed calls) on the deployed function:
  /lead-panel/timeseries/collected/chatter ?days=30, 90, 365
  /lead-panel/rankings/trending/price       default, ?days=90, ?days=365
  /lead-panel/rankings/breakout/price       default, ?days=90, ?days=365
C1: every read's WORST warm time is under the bar (2,000 ms default) with status 200. Each read prints min/max ms.
Verdict: R71 C38 SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import time

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PREFIX = "/api/scoped/amgt"
READS = [("/lead-panel/timeseries/collected/chatter", {"days": d}) for d in ("30", "90", "365")]
READS += [(f"/lead-panel/rankings/{mv}/price", q) for mv in ("trending", "breakout") for q in (None, {"days": "90"}, {"days": "365"})]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    ap.add_argument("--bar-ms", type=float, default=2000.0)
    a = ap.parse_args()
    if a.where == "deployed":
        import boto3

        cl = _load("capture_lib", CAPTURE_LIB)
        lam = boto3.client("lambda", region_name=cl.REGION)

        def call(path, query=None):
            body, meta = cl._invoke(lam, path, query)
            return 200 if body is not None else meta.get("status")
    else:
        from lib.research.api import scoped_amgt

        def call(path, query=None):
            r = scoped_amgt.handler({"rawPath": path, "requestContext": {"http": {"method": "GET"}},
                                     "headers": {"x-firm-id": "opal"}, "queryStringParameters": query})
            return r.get("statusCode")

    bad = []
    for path, q in READS:
        call(PREFIX + path, q)
        times, codes = [], []
        for _ in range(3):
            t0 = time.time()
            codes.append(call(PREFIX + path, q))
            times.append((time.time() - t0) * 1000.0)
        worst = max(times)
        label = f"{path}{'?' + json.dumps(q) if q else ''}"
        print(f"   {label}: min {min(times):.0f} ms max {worst:.0f} ms status {sorted(set(codes))}")
        if worst >= a.bar_ms or any(c != 200 for c in codes):
            bad.append(f"{label}:{worst:.0f}ms")
    ok = not bad
    print(f"{'PASS' if ok else 'FAIL'} C1 every Lead Panel read is under {a.bar_ms:.0f} ms warm reads {len(READS)} over-bar {len(bad)} e.g. {bad[:4]}")
    print(f"R71 C38 SERVED: {'YES' if ok else 'NO'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
