"""AMGT_RESAPP round 78 -- the issuer's hand reads after the bb-18 apply (CTO half C4 and C5; COO half, issuer's calls).

  python r78_bb18_issuer_hand_reads.py

GET-shaped direct invokes of the deployed function, read-only. It prints what each returned and gives no verdict of its own
beyond the status codes; the issuer writes the reading in the act's record.
  1. C4: the lead-panel rankings route with an as-of date in 2009, on the default window and on the 90-day window (the 90-day
     branch is the one that reaches the unguarded staleness call site);
  2. C5 / bb-4: /thesis for a slash name, BP/_LN_Equity -- the officers served;
  3. C5 / bb-7: /resolve?q=apple and ?q=microsoft -- the legal-name search;
  4. the live CodeSha256, read before and after.
"""
from __future__ import annotations

import json
import sys
import urllib.parse

import boto3

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"


def main():
    lam = boto3.client("lambda", region_name="us-east-1")

    def sha():
        return lam.get_function_configuration(FunctionName=FN)["CodeSha256"]

    def get(path, query=None):
        event = {"rawPath": PREFIX + path, "rawQueryString": urllib.parse.urlencode(query or {}),
                 "queryStringParameters": query or None, "requestContext": {"http": {"method": "GET"}},
                 "headers": {"x-firm-id": "opal"}}
        resp = lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())
        raw = json.loads(resp["Payload"].read())
        err = resp.get("FunctionError")
        try:
            body = json.loads(raw.get("body") or "{}") if isinstance(raw, dict) else {}
        except (ValueError, TypeError):
            body = {"_unparsed": str(raw.get("body"))[:200]}
        return (raw.get("statusCode") if isinstance(raw, dict) else None), body, err, raw

    print("live CodeSha256 before: %s" % sha())

    print("\n== 1. C4: an as-of date in 2009 on the rankings route ==")
    for label, query in (("default window", {"as_of": "2009-06-01"}), ("90-day window", {"days": "90", "as_of": "2009-06-01"}),
                         ("90-day window, no as_of (control)", {"days": "90"})):
        code, body, err, raw = get("/lead-panel/rankings/trending/price", query)
        keys = sorted(body.keys())[:12] if isinstance(body, dict) else []
        print("  %-34s status %s  FunctionError %s  as_of_date %r  requested_as_of %r  stale_trading_days %r  rows %s" % (
            label, code, err, body.get("as_of_date"), body.get("requested_as_of"), body.get("stale_trading_days"),
            len(body.get("rows") or []) if isinstance(body.get("rows"), list) else body.get("rows")))
        if code != 200 or err:
            print("     body/raw: %s" % (json.dumps(body)[:300] if body else str(raw)[:300]))
        else:
            print("     keys %s; reason %r" % (keys, (body.get("reason") or body.get("ranking_reason") or "")[:160]))

    print("\n== 2. bb-4: /thesis officers for a slash name ==")
    for key in ("BP/_LN_Equity", "NG/_LN_Equity"):
        code, body, err, _raw = get("/security/%s/thesis" % urllib.parse.quote(key, safe=""))
        mgmt = body.get("management") or {}
        officers = mgmt.get("officers") or []
        print("  %-16s status %s  FunctionError %s  officers %d  source %r" % (key, code, err, len(officers),
                                                                           mgmt.get("source") or mgmt.get("officers_source")))
        for o in officers[:3]:
            print("     %s -- %s" % (o.get("name"), o.get("role")))
        if not officers:
            print("     management keys %s reason %r" % (sorted(mgmt.keys())[:10], str(mgmt.get("reason") or mgmt.get("absent_reason"))[:160]))

    print("\n== 3. bb-7: name search by legal name ==")
    for q in ("apple", "microsoft", "Lenovo"):
        code, body, err, _raw = get("/resolve", {"q": q})
        cands = body.get("candidates") or []
        print("  q=%-10s status %s  FunctionError %s  answer %r  candidates %d %s" % (
            q, code, err, body.get("status") or body.get("resolution") or body.get("answer"), len(cands),
            [(c.get("security_key"), c.get("name")) for c in cands[:3]]))
        if not cands:
            print("     body %s" % json.dumps(body)[:260])

    print("\nlive CodeSha256 after: %s" % sha())
    return 0


if __name__ == "__main__":
    sys.exit(main())
