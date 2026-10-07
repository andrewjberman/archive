"""AMGT_RESAPP round 78, issuer act 1 -- the read-back of the pool mint that carries the legal names.

  python r78_pool_mint_readback.py --before <VersionId> [--after <VersionId>]

Compares the served pool object (the latest version, or --after) with the version it replaced: the keys, every existing field
of every record, the count of records carrying a legal name, three resolve() controls, and one read of the deployed name
search. Read-only. Exit 0 when branch A of the signed halves holds, 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

BUCKET, KEY = "opal-data-harvest", "crosswalk/v1/2026-10-07.json"
FN = "opal-amgt-scoped-api"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", default=None)
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    sys.path.insert(0, root)
    import boto3

    s3 = boto3.client("s3", region_name="us-east-1")
    head = s3.head_object(Bucket=BUCKET, Key=KEY)
    after_id = a.after or head.get("VersionId")
    old = json.loads(s3.get_object(Bucket=BUCKET, Key=KEY, VersionId=a.before)["Body"].read())
    new = json.loads(s3.get_object(Bucket=BUCKET, Key=KEY, VersionId=after_id)["Body"].read())
    results = []

    def clause(name, cond, detail=""):
        results.append(bool(cond))
        print("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))

    print("before %s; after %s (latest %s)" % (a.before, after_id, head.get("VersionId")))
    o = {r["security_key"]: r for r in old["records"]}
    n = {r["security_key"]: r for r in new["records"]}
    clause("R1 the same keys", set(o) == set(n) and len(n) == 243,
           "%d before, %d after, only before %s, only after %s" % (len(o), len(n), sorted(set(o) - set(n))[:3], sorted(set(n) - set(o))[:3]))
    moved = {}
    for key in set(o) & set(n):
        for field, value in o[key].items():
            if n[key].get(field) != value:
                moved.setdefault(field, []).append(key)
    clause("R2 no existing field of any record moved", not moved, "%s" % {f: len(v) for f, v in moved.items()})
    added = sorted(set(f for key in n for f in n[key] if f not in o.get(key, {})))
    clause("R3 the only added record field is legal_name", added == ["legal_name"], "%s" % added)
    named = sum(1 for r in new["records"] if (r.get("legal_name") or {}).get("value"))
    carry = sum(1 for r in new["records"] if "legal_name" in r)
    clause("R4 every record carries the field and 211 hold a name", carry == 243 and named == 211,
           "carry %d of 243, named %d; denominators.with_legal_name %s" % (carry, named, (new.get("denominators") or {}).get("with_legal_name")))
    top = sorted(k for k in set(old) | set(new) if k != "records" and old.get(k) != new.get(k))
    print("   top-level fields that differ: %s" % top)

    from lib.research.identity import crosswalk

    crosswalk.load_crosswalk(refresh=True)
    res = {form: crosswalk.resolve(form) for form in ("AMD_US_Equity", "ABNB_US_Equity", "CSCO_US_Equity")}
    clause("R5 resolve() controls read as before: AMD and ABNB measured, CSCO not in the pool",
           res["AMD_US_Equity"].get("resolution") == "MEASURED" and res["ABNB_US_Equity"].get("resolution") == "MEASURED"
           and res["CSCO_US_Equity"].get("resolution") == "UNRESOLVED",
           "%s" % {k: v.get("resolution") for k, v in res.items()})

    lam = boto3.client("lambda", region_name="us-east-1")
    event = {"rawPath": "/api/scoped/amgt/resolve", "rawQueryString": "q=Lenovo", "queryStringParameters": {"q": "Lenovo"},
             "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    raw = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    body = raw.get("body") or ""
    clause("R6 the deployed name search still lists Lenovo's record", raw.get("statusCode") == 200 and "992_HK_Equity" in body,
           "status %s; body bytes %d" % (raw.get("statusCode"), len(body)))
    ok = all(results)
    print("R78 POOL MINT READ-BACK: %s" % ("BRANCH A HOLDS" if ok else "NOT BRANCH A"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
