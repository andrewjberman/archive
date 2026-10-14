"""check_ar3_aifill_served.py -- acceptance for AMGT-ar-3 (the redeployed adapter serves `ai_fill` and moves nothing else).

  PYTHONPATH=<repo root> python check_ar3_aifill_served.py capture --names A,B,C --out FILE      (BEFORE the apply: the live /thesis bodies)
  PYTHONPATH=<repo root> python check_ar3_aifill_served.py verify  --pre FILE --stored-name AMD_US_Equity   (AFTER the apply)
`capture` invokes the live function (GET) for each name and writes {name: body} locally (client research content: keep it uncommitted).
`verify` re-reads the same names and checks, printing `AIFILL AR-3 SERVED: YES|NO (k of n)`:
  - the stored name serves ai_fill.status SERVED with five blocks EQUAL to the stored document (read from S3 by the producer's own reader);
  - for every captured name every key of the /thesis body other than `ai_fill` is equal before and after, ignoring read clocks and float last-digit noise;
  - a name with no stored document serves ai_fill.status ABSENT with read_completed true (the captured names that have no stored document).
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
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
    import os

    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)
    c = sub.add_parser("capture")
    c.add_argument("--names", required=True)
    c.add_argument("--out", required=True)
    v = sub.add_parser("verify")
    v.add_argument("--pre", required=True)
    v.add_argument("--stored-name", required=True)
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

    from lib.research.aifill import store

    pre = json.load(open(args.pre, encoding="utf-8"))
    rows = []

    def arm(name, ok, detail=""):
        rows.append(ok)
        print("ARM %-72s %s %s" % (name, "PASS" if ok else "FAIL", str(detail)[:160]))

    stored = store.read_document(args.stored_name)
    arm("the stored document for %s exists" % args.stored_name, stored is not None)
    status, body = invoke(args.stored_name, function_name)
    fill = body.get("ai_fill") or {}
    arm("%s: the /thesis route answers 200 and carries ai_fill" % args.stored_name, status == 200 and "ai_fill" in body, status)
    arm("%s: ai_fill.status is SERVED, source pool, read completed" % args.stored_name, fill.get("status") == "SERVED" and fill.get("source") == "pool" and fill.get("read_completed") is True, fill.get("reason") or fill.get("status"))
    if stored is not None:
        arm("%s: the five served blocks EQUAL the stored document's blocks" % args.stored_name, fill.get("blocks") == stored.get("blocks"))
        arm("%s: as_of and generated_at EQUAL the stored document's" % args.stored_name, fill.get("as_of") == stored.get("as_of") and fill.get("generated_at") == stored.get("generated_at"))
    for name, before in sorted(pre.items()):
        st, after = invoke(name, function_name)
        extra = sorted(k for k in after if k not in before)
        moved = differs({k: v for k, v in before.items() if k != "ai_fill"}, {k: v for k, v in after.items() if k != "ai_fill"})
        arm("%s: 200, the only key added is ai_fill, and no other key moved" % name, st == 200 and extra == ["ai_fill"] and not moved, "extra=%s moved=%s" % (extra, moved[:3]))
        if name != args.stored_name and store.read_document(name) is None:
            f = after.get("ai_fill") or {}
            arm("%s: no stored document -> ABSENT with the read completed" % name, f.get("status") == "ABSENT" and f.get("read_completed") is True, f.get("status"))
    ok = bool(rows) and all(rows)
    print("AIFILL AR-3 SERVED: %s (%d of %d)" % ("YES" if ok else "NO", sum(rows), len(rows)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
