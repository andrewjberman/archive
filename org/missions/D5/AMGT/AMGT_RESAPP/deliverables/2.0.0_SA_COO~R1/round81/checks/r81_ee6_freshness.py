"""AMGT_RESAPP round 81 -- AMGT-ee-6's deployed arm for AMGT-ee-2: the served /freshness words carry one date form.

  python r81_ee6_freshness.py [--where deployed|local]

GET /freshness?view=page (the page's own request) and walk the WHOLE body: every string under a key named `sentence`, and the
top-level `lists.out_of_date`, is served wording the page prints as served.
F1 the route answered 200 with rows (denominator printed);
F2 0 of those served sentences carries a YYYY-MM-DD day;
F3 at least one served sentence carries the house long form ("<Month> <d><st|nd|rd|th>, <YYYY>") -- the positive control.
Deployed, the route reads a STORED SNAPSHOT that only the scheduled event re-writes: run it AFTER ee-6's snapshot leg.
Verdict: R81 EE6 FRESHNESS: YES|NO (exit 0|1). On the live base (OUOsYXa, snapshot of round 80) it reads NO.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
ISO_DAY = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
LONG = re.compile(r"\b(January|February|March|April|May|June|July|August|September|October|November|December) "
                  r"\d{1,2}(st|nd|rd|th), \d{4}\b")


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def walk(node, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "sentence" and isinstance(v, str):
                out.append(v)
            else:
                walk(v, out)
    elif isinstance(node, list):
        for v in node:
            walk(v, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", choices=("deployed", "local"), default="deployed")
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    if root not in sys.path:
        sys.path.insert(0, root)
    event = {"rawPath": PREFIX + "/freshness", "requestContext": {"http": {"method": "GET"}},
             "headers": {"x-firm-id": "opal"}, "queryStringParameters": {"view": "page"}}
    try:
        if a.where == "deployed":
            import boto3
            lam = boto3.client("lambda", region_name="us-east-1")
            r = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
        else:
            from lib.research.api import scoped_amgt
            r = scoped_amgt.handler(event)
        code, body = r.get("statusCode"), json.loads(r.get("body") or "{}")
    except Exception as err:  # noqa: BLE001 -- a failed read is a FAIL line, never a crash
        code, body = "%s: %s" % (type(err).__name__, str(err)[:120]), {}
    sentences = []
    walk(body, sentences)
    ood = (body.get("lists") or {}).get("out_of_date") if isinstance(body, dict) else None
    if isinstance(ood, str):
        sentences.append(ood)
    rows = body.get("rows") if isinstance(body, dict) else None
    iso = [s for s in sentences if ISO_DAY.search(s)]
    longs = [s for s in sentences if LONG.search(s)]
    r1 = say(code == 200 and isinstance(rows, list) and len(rows) > 0,
             "F1 /freshness?view=page answered %s with %s rows; served sentences %d" % (code, len(rows) if isinstance(rows, list) else "no", len(sentences)))
    r2 = say(bool(sentences) and not iso, "F2 served sentences with a YYYY-MM-DD day: %d of %d %s" % (len(iso), len(sentences), iso[:3]))
    r3 = say(bool(longs), "F3 positive control: served sentences in the house long form: %d" % len(longs))
    ok = r1 and r2 and r3
    print("R81 EE6 FRESHNESS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
