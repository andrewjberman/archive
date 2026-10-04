"""AMGT-ap-4 CTO half condition 3 -- the RANGE route's cold read on the DEPLOYED function.

Mirrors r64_served.py's c15 instrument EXACTLY (same invoke, same LogType=Tail, same
`Init Duration` cold test, same `\tDuration:` ms read, same AMGT_SEGMENT tail) and differs
only in the path and query, so the two numbers are comparable:

  c15        /security/BA_US_Equity/timeline/day/2026-09-08   (the DAY route, graded, <5 s)
  this read  /security/BA_US_Equity/timeline?from=...&to=...  (the RANGE route, reported)

Over 5 s is NOT a rollback trigger here (no graded check covers the range route); it is
reported, and the issuer files a row plus a round-67 cell.

3 CONCURRENT invokes, because a sequential second invoke reuses the first's environment and
would read cold=False -- the same trap r64 c15 solves with a ThreadPoolExecutor.

Usage: python ap4_range_cold.py [--to YYYY-MM-DD] [--runs 3]
"""
from __future__ import annotations

import argparse
import base64
import datetime as _dt
import importlib.util
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor

CAPTURE_LIB = ("org/missions/D5/AMGT/AMGT_RESAPP/deliverables/"
               "0.9.0_WK_AMGT_RESAPP~158/capture_lib.py")
PREFIX = "/api/scoped/amgt"
FROM = "2026-09-01"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", default=_dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d"),
                    help="window end; default is today UTC")
    ap.add_argument("--runs", type=int, default=3)
    a = ap.parse_args()

    import boto3

    cl = _load("capture_lib", CAPTURE_LIB)
    lam = boto3.client("lambda", region_name=cl.REGION)
    path = PREFIX + "/security/BA_US_Equity/timeline"
    query = {"from": FROM, "to": a.to}
    print(f"   RANGE route cold read: {path}?from={FROM}&to={a.to} on {cl.FUNCTION}")
    print(f"   {a.runs} CONCURRENT invoke(s); cold is proven by Init Duration in the REPORT line")

    def one(_):
        ev = {"rawPath": path, "headers": {"x-firm-id": "opal"},
              "requestContext": {"http": {"method": "GET"}}, "queryStringParameters": query}
        r = lam.invoke(FunctionName=cl.FUNCTION, Payload=json.dumps(ev).encode("utf-8"),
                       LogType="Tail")
        raw = json.loads(r["Payload"].read())
        log = base64.b64decode(r.get("LogResult") or b"").decode("utf-8", "replace")
        rep = next((ln for ln in log.splitlines() if ln.startswith("REPORT")), "")
        dur = re.search(r"\tDuration: ([\d.]+) ms", rep)
        init = re.search(r"Init Duration: ([\d.]+) ms", rep)
        body = json.loads(raw.get("body") or "{}") if isinstance(raw, dict) else {}
        arts = body.get("articles") or []
        wc = body.get("word_cloud") or {}
        # Print the body's top-level keys. `articles` read 0 on the warm sample while the DAY
        # route serves 6, and a probe that names a key the route does not use would report an
        # emptiness that is the PATTERN's, not the world's (READ_HERE s.5's own lesson).
        return {"status": raw.get("statusCode"),
                "duration_ms": float(dur.group(1)) if dur else None,
                "cold": init is not None,
                "init_ms": float(init.group(1)) if init else None,
                "articles": len(arts),
                "word_cloud_terms": len(wc.get("terms") or []),
                "body_keys": sorted(body.keys()) if isinstance(body, dict) else None,
                "list_valued_keys": {k: len(v) for k, v in body.items()
                                     if isinstance(v, list)} if isinstance(body, dict) else None,
                "segments": [ln.strip() for ln in log.splitlines() if "AMGT_SEGMENT" in ln][:8]}

    with ThreadPoolExecutor(max_workers=a.runs) as pool:
        runs = list(pool.map(one, range(a.runs)))

    for i, r in enumerate(runs):
        print(f"   run {i + 1}: status={r['status']} duration_ms={r['duration_ms']} "
              f"cold={r['cold']} init_ms={r['init_ms']} articles={r['articles']} "
              f"word_cloud_terms={r['word_cloud_terms']}")
        print(f"       body keys: {r['body_keys']}")
        print(f"       list-valued keys and their lengths: {r['list_valued_keys']}")
        for s in r["segments"]:
            print(f"       {s}")

    cold = [r for r in runs if r["cold"]]
    ok200 = [r for r in runs if r["status"] == 200]
    durs = [r["duration_ms"] for r in cold if r["duration_ms"] is not None]
    print(f"   COLD {len(cold)} of {len(runs)}; status 200 {len(ok200)} of {len(runs)}; "
          f"AMGT_SEGMENT present {sum(1 for r in runs if r['segments'])} of {len(runs)}")
    if durs:
        print(f"   cold duration_ms: min {min(durs)} max {max(durs)}; "
              f"over 5000 ms: {sum(1 for d in durs if d >= 5000)} of {len(durs)}")
    else:
        print("   cold duration_ms: NO COLD RUN IN THIS SAMPLE -- the number below is not a cold read")
    print("   NOTE: this read is REPORTED, not graded. Over 5 s is not a rollback trigger "
          "(CTO half condition 3); it files a row and a round-67 cell.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
