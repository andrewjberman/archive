"""AMGT_RESAPP round-91 PREP -- AMGT-pp-1 as DEPLOYED: a non-digit non-US peer a held company names exactly serves that identity.

  PYTHONPATH=<repo root> python r91_name_match_deployed.py [--where deployed|local] [--limit N]

For each keyed crosswalk subject (243), the peers route of the live function (Lambda invoke, GET only; `--where local` calls the repo's
own handler on the same live pool) is read, and for every member the rule would own -- a ticker that is NOT all digits and NOT a United
States alphabetic ticker -- the expectation is computed independently from the member's own name and the held-name index:
    D1 a member whose name token names exactly one held company serves that key, identity MEASURED, matched_as company_name.
    D2 a member whose name names no held company, or two, serves no key from this rule (it is byte-equal to the stored member).
    D3 denominators: members examined, candidates (D1's population), served correctly; the candidate count must be at least 1.
SHARED DEPENDENCY, stated: the expectation and the route both read `scoped_amgt._held_name_index()`; the index is not graded here.
Verdict: R91 NAME MATCH DEPLOYED: YES|NO (exit 0|1). At the base (2026-10-11, KlosR/ap8O.. successor l8egBo/rf..) D1 FAILs.
"""
import argparse
import json
import sys

import boto3

from lib.research.api import scoped_amgt
from lib.research.identity import crosswalk
from lib.research.peers import numeric_tickers as nt

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
_LAM = boto3.client("lambda", region_name="us-east-1")


def peers(where, key):
    path = "%s/security/%s/peers" % (PREFIX, key)
    event = {"rawPath": path, "queryStringParameters": None,
             "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    if where == "deployed":
        r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        r = scoped_amgt.handler(event)
    return json.loads(r.get("body") or "{}")


def owned(member):
    t = member.get("ticker")
    if not isinstance(t, str) or not t.strip() or nt.is_numeric_ticker(member):
        return False
    return not (member.get("country") == "United States" and t.isascii() and t.isalpha())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", default="deployed", choices=["deployed", "local"])
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    doc, _i, _a = crosswalk.load_crosswalk()
    keys = [r["security_key"] for r in doc["records"] if r.get("resolution") == "MEASURED" and r.get("security_key")]
    if args.limit:
        keys = keys[: args.limit]
    index = scoped_amgt._held_name_index()
    examined = candidates = served_ok = missing = leaked = 0
    examples = []
    for key in keys:
        for m in peers(args.where, key).get("members") or []:
            if not isinstance(m, dict) or not owned(m):
                continue
            examined += 1
            tok = nt.name_token(scoped_amgt._clean_display_name(m.get("name")))
            held = sorted(set(index.get(tok) or [])) if tok else []
            ident = m.get("identity") if isinstance(m.get("identity"), dict) else {}
            served = ident.get("security_key") if ident.get("resolution") == "MEASURED" else None
            if len(held) == 1:
                candidates += 1
                if served == held[0] and ident.get("matched_as") == nt.MATCHED_AS_NAME:
                    served_ok += 1
                elif len(examples) < 4:
                    missing += 1
                    examples.append((key, m.get("ticker"), m.get("name"), held[0], served))
                else:
                    missing += 1
            elif served and ident.get("matched_as") == nt.MATCHED_AS_NAME:
                leaked += 1
    print("   where=%s subjects=%d | members examined %d | candidates (name names exactly one held company) %d | served correctly %d"
          " | missing %d | leaked %d" % (args.where, len(keys), examined, candidates, served_ok, missing, leaked))
    for e in examples:
        print("   missing e.g. %s %r %r expected %s served %s" % e)
    d1 = candidates >= 1 and missing == 0 and served_ok == candidates
    d2 = leaked == 0
    print("%s D1 every candidate serves its held key as company_name" % ("PASS" if d1 else "FAIL"))
    print("%s D2 no member serves a company_name match the rule does not predict" % ("PASS" if d2 else "FAIL"))
    ok = d1 and d2
    print("R91 NAME MATCH DEPLOYED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
