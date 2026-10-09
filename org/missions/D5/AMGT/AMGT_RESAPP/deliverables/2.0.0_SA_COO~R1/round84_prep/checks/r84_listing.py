"""AMGT_RESAPP round-84 PREP -- one company, several LISTINGS (CTO~DELL1 ruling, DSGN_AMGTV1 CTO_RULING_ROUND57_R1A_R6 ADDENDUM 2).

  python r84_listing.py --crit AC1 [--where deployed|local] [--write-base]

Candidates sharing ONE issuer identity in the name list's own data, with exactly ONE covered listing, resolve to the covered
listing and the body says which listing and that others exist; anything else answers as before.
    R1 the typed "ASML" thesis route answers 200 for ASML_NA_Equity, and the body names the other listing (ASML_US_Equity);
       /resolve?q=ASML answers security_key ASML_NA_Equity.
    R2 the negative arm: "Micro" (AMD, MU, MSFT: different issuers) still answers the 404 candidate list on the thesis route.
    R3 the other arms are byte-equal to the base: /resolve for a one-candidate query ("Nu") and a no-match query ("zzqx"),
       and the thesis route's 404 for "zzqx". The base bytes are r84_listing_base.json beside this file (--write-base, at
       the base only).
Verdict: R84 LISTING AC1: YES|NO (exit 0|1). At the base (2026-10-09) R1 FAILs, R2 and R3 PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
BASE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "r84_listing_base.json")
R3_CALLS = (("resolve", "Nu"), ("resolve", "zzqx"), ("thesis", "zzqx"))


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def call(where, kind, text):
    if kind == "resolve":
        event = {"rawPath": "%s/resolve" % PREFIX, "queryStringParameters": {"q": text}}
    else:
        event = {"rawPath": "%s/security/%s/thesis" % (PREFIX, text), "queryStringParameters": None}
    event.update({"requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}})
    if where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")
        r = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        from lib.research.api import scoped_amgt

        r = scoped_amgt.handler(event)
    return r.get("statusCode"), r.get("body") or ""


def fingerprint(code, body):
    return "%s:%s" % (code, hashlib.sha256(body.encode("utf-8")).hexdigest()[:16])


def ac1(where, write_base):
    if write_base:
        base = {"%s|%s" % (k, t): fingerprint(*call(where, k, t)) for k, t in R3_CALLS}
        with open(BASE_FILE, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(base, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print("   base written: %s %s" % (BASE_FILE, base))
    code, body = call(where, "thesis", "ASML")
    doc = json.loads(body or "{}")
    served_key = (doc.get("identity") or {}).get("security_key") or doc.get("security_key")
    print("   thesis 'ASML': status %s, served key %r, names ASML_US_Equity: %s" % (
        code, served_key, "ASML_US_Equity" in body))
    rcode, rbody = call(where, "resolve", "ASML")
    rdoc = json.loads(rbody or "{}")
    print("   resolve 'ASML': status %s, status field %r, security_key %r" % (rcode, rdoc.get("status"), rdoc.get("security_key")))
    r1 = say(code == 200 and served_key == "ASML_NA_Equity" and "ASML_US_Equity" in body
             and rdoc.get("security_key") == "ASML_NA_Equity",
             "R1 'ASML' resolves to the covered listing ASML_NA_Equity and names the other listing")
    mcode, mbody = call(where, "thesis", "Micro")
    mdoc = json.loads(mbody or "{}")
    keys = sorted(c.get("security_key") for c in (mdoc.get("candidates") or []))
    print("   thesis 'Micro': status %s, candidates %s" % (mcode, keys))
    r2 = say(mcode == 404 and len(keys) >= 2, "R2 different issuers with similar names still answer the candidate list")
    try:
        with open(BASE_FILE, encoding="utf-8") as fh:
            base = json.load(fh)
    except OSError:
        base = {}
    same = 0
    for kind, text in R3_CALLS:
        now = fingerprint(*call(where, kind, text))
        was = base.get("%s|%s" % (kind, text))
        ok = was is not None and now == was
        print("   %-8s %-6s now %s base %s" % (kind, text, now, was))
        same += ok
    r3 = say(same == len(R3_CALLS), "R3 the one-candidate and no-match arms are byte-equal to the base: %d of %d" % (same, len(R3_CALLS)))
    return r1 and r2 and r3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1"])
    ap.add_argument("--where", choices=("deployed", "local"), default="deployed")
    ap.add_argument("--write-base", action="store_true", help="record the R3 base fingerprints (at the base only)")
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    if root and root not in sys.path:
        sys.path.insert(0, root)
    ok = ac1(a.where, a.write_base)
    print("R84 LISTING AC1: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
