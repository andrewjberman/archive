"""AMGT_RESAPP round-92 PREP -- the census the CTO's round-91 analysis names (`amgt_minor_unit_census`): no minor-unit currency label beside a
major-unit price anywhere on the live peers routes, no served currency beside a stale reason, and the correct major-unit codes kept.

  PYTHONPATH=<repo root> python r92_minor_unit_census.py [--where deployed|local] [--limit N]

Every member of every keyed subject's peers route (243 subjects, about 2,230 members) is read (Lambda invoke, GET only; `--where local`
calls the repo's own handler on the same live pool):
    M1 member rows serving a currency whose code is a minor-unit code (a lower-case last letter, or GBX, ILA): must be 0.
    M2 member rows serving BOTH a `price_currency` and a `price_currency_reason`: must be 0.
    M3 control: member rows serving a major-unit currency: reported, and must be at least the base's 149 (USD 125, CHF 9, EUR 8,
       JPY 6, HKD 1) less any that a legitimate refusal removes; this floor guards a guard that serves nothing.
Verdict: R92 MINOR-UNIT CENSUS: YES|NO (exit 0|1). At the base (2026-10-11, live l8egBo/rf..) M1 reads 12 and M2 reads 156: NO.
"""
import argparse
import json
import sys

import boto3

from lib.research.api import scoped_amgt
from lib.research.identity import crosswalk

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
MAJOR_FLOOR = 149
_LAM = boto3.client("lambda", region_name="us-east-1")


def peers(where, key):
    event = {"rawPath": "%s/security/%s/peers" % (PREFIX, key), "queryStringParameters": None,
             "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    if where == "deployed":
        r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        r = scoped_amgt.handler(event)
    return json.loads(r.get("body") or "{}")


def is_minor(code):
    return isinstance(code, str) and (code in ("GBX", "ILA") or (len(code) == 3 and code[-1].islower()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", default="deployed", choices=["deployed", "local"])
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    doc, _i, _a = crosswalk.load_crosswalk()
    keys = [r["security_key"] for r in doc["records"] if r.get("resolution") == "MEASURED" and r.get("security_key")]
    if args.limit:
        keys = keys[: args.limit]
    rows = minor = both = major = 0
    examples = []
    for key in keys:
        for m in peers(args.where, key).get("members") or []:
            if not isinstance(m, dict):
                continue
            rows += 1
            cur, reason = m.get("price_currency"), m.get("price_currency_reason")
            if cur and is_minor(cur):
                minor += 1
                if len(examples) < 4:
                    examples.append((key, m.get("ticker"), m.get("price"), cur))
            elif cur:
                major += 1
            if cur and reason:
                both += 1
    print("   where=%s subjects=%d | member rows %d | major-unit currencies served %d | minor-unit labels %d | currency AND reason %d" % (
        args.where, len(keys), rows, major, minor, both))
    for e in examples:
        print("   minor-unit e.g. %s %s price=%s currency=%s" % e)
    m1, m2 = minor == 0, both == 0
    m3 = major >= MAJOR_FLOOR or args.limit is not None
    for ok, label in ((m1, "M1 no minor-unit label beside a scanner price"), (m2, "M2 no served currency beside a stale reason"),
                      (m3, "M3 control: the major-unit codes are kept (floor %d)" % MAJOR_FLOOR)):
        print("%s %s" % ("PASS" if ok else "FAIL", label))
    ok = m1 and m2 and m3
    print("R92 MINOR-UNIT CENSUS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
