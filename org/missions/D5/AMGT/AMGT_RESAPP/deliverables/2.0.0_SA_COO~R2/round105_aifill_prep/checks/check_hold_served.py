"""check_hold_served.py -- acceptance for AMGT-ar-7 (the AI-fill HOLD: the scoped API serves `ai_fill` ABSENT for every name and moves nothing else).

  PYTHONPATH=<repo root> AIFILL_SERVED_FUNCTION=<fn> python check_hold_served.py capture --names A,B,C --out FILE     (BEFORE the apply: the live /thesis bodies)
  PYTHONPATH=<repo root> AIFILL_SERVED_FUNCTION=<fn> python check_hold_served.py verify  --pre FILE                    (AFTER the apply)
`capture` invokes the live function (GET) for each name and writes {name: body} locally (client research content: keep it uncommitted).
`verify` re-reads the same names and prints `AIFILL HOLD SERVED: YES|NO (k of n)`; per name it requires:
  - the route answers 200 and still carries the key `ai_fill`;
  - ai_fill.status is ABSENT, read_completed is true, source is none, blocks is {} (the document is held back, the read itself completed);
  - every key other than `ai_fill` equals the captured body, ignoring read clocks and float last-digit noise.
At the base (the AI fill still served) the first two requirements fail: the check reads NO.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import sys

FUNCTION_ENV = "AIFILL_SERVED_FUNCTION"
CLOCK = re.compile(r"(read_at|fetched_at|generated_at|served_at|_clock|elapsed|duration|request_id|latency|as_of_read)", re.I)


def invoke(key, function_name):
    import boto3

    event = {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "queryStringParameters": None,
             "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    lam = boto3.client("lambda", region_name="us-east-1")
    r = json.loads(lam.invoke(FunctionName=function_name, Payload=json.dumps(event).encode("utf-8"))["Payload"].read())
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


def differs(a, b, path=""):
    """The paths at which a and b differ, ignoring read clocks and 1e-9 relative float noise."""
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if CLOCK.search(str(k)):
                continue
            if k not in a or k not in b:
                out.append("%s.%s" % (path, k))
            else:
                out.extend(differs(a[k], b[k], "%s.%s" % (path, k)))
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append("%s[len %d vs %d]" % (path, len(a), len(b)))
        else:
            for i, (x, y) in enumerate(zip(a, b)):
                out.extend(differs(x, y, "%s[%d]" % (path, i)))
    else:
        if a != b:
            try:
                fa, fb = float(a), float(b)
                if abs(fa - fb) <= 1e-9 * max(1.0, abs(fa), abs(fb)):
                    return out
            except (TypeError, ValueError):
                pass
            out.append(path)
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)
    c = sub.add_parser("capture")
    c.add_argument("--names", required=True)
    c.add_argument("--out", required=True)
    v = sub.add_parser("verify")
    v.add_argument("--pre", required=True)
    args = ap.parse_args()
    function_name = os.environ.get(FUNCTION_ENV)
    if not function_name:
        print("BLOCKED: set %s to the served function's name" % FUNCTION_ENV)
        return 2
    if args.mode == "capture":
        names = [n for n in args.names.split(",") if n]
        with concurrent.futures.ThreadPoolExecutor(4) as ex:
            got = list(ex.map(lambda n: (n,) + invoke(n, function_name), names))
        bad = [(n, s) for n, s, _ in got if s != 200]
        json.dump({n: b for n, _, b in got}, open(args.out, "w", encoding="utf-8"))
        print("CAPTURED %d name(s) to %s; non-200: %s" % (len(got), args.out, bad or "none"))
        return 1 if bad else 0

    pre = json.load(open(args.pre, encoding="utf-8"))
    rows = []

    def arm(name, ok, detail=""):
        rows.append(ok)
        print("ARM %-84s %s %s" % (name, "PASS" if ok else "FAIL", str(detail)[:160]))

    for name, before in sorted(pre.items()):
        status, after = invoke(name, function_name)
        fill = after.get("ai_fill")
        arm("%s: 200 and the key ai_fill is still present" % name, status == 200 and "ai_fill" in after, status)
        fill = fill if isinstance(fill, dict) else {}
        arm("%s: ai_fill ABSENT, read completed, source none, blocks {}" % name,
            fill.get("status") == "ABSENT" and fill.get("read_completed") is True and fill.get("blocks") == {} and fill.get("source") in (None, "none"),
            "%s/%s/%s" % (fill.get("status"), fill.get("read_completed"), fill.get("source")))
        moved = differs({k: v for k, v in before.items() if k != "ai_fill"}, {k: v for k, v in after.items() if k != "ai_fill"})
        arm("%s: no key other than ai_fill moved" % name, not moved, moved[:3])
    ok = bool(rows) and all(rows)
    print("AIFILL HOLD SERVED: %s (%d of %d)" % ("YES" if ok else "NO", sum(rows), len(rows)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
