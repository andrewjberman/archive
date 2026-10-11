"""AMGT_RESAPP round-89 PREP -- D1-S16: a peer member that the identity pool holds under `<TICKER> US` serves that identity.

  python r89_peer_identity.py [--where local|deployed]        (repo root, PYTHONPATH=<repo root>)

The live `/security/ASML_NA_Equity/peers` (b7Lj1J, measured 2026-10-11): 12 of 12 members read identity UNRESOLVED. The
producer resolves the bare scanner ticker ("INTC"), which the crosswalk does not hold; the crosswalk holds the Bloomberg form
("INTC US" -> INTC_US_Equity, MEASURED). 7 of the 10 United States members resolve under that form. The route serves the stored
object with decorators and never rewrites it, so the fix is a serve-time decorator, as `_with_numeric_tickers` is.

The expectation is computed here, independently, from the REAL crosswalk -- never a hard-coded name list:
    I1 every United States member whose `<ticker> US` crosswalk read is MEASURED serves `identity.resolution` MEASURED, the same
       `security_key` as that read, and a top-level `security_key` equal to it. The denominator (members, US-ticker members,
       resolvable) is printed and the resolvable count must be at least 1 (an empty expectation proves nothing).
    I2 a member the pool does not hold, and every non-US member, serves NO key it was not given: identity is not MEASURED.
    I3 nothing is removed or reordered, and `ticker`, `name`, `price` and `country` of every member are byte-equal to the stored
       object's.
Verdict: R89 PEER IDENTITY: YES|NO (exit 0|1). At the base (2026-10-11) I1 FAILs, I2 and I3 PASS.
"""
from __future__ import annotations

import argparse
import json
import sys

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
SUBJECT = "ASML_NA_Equity"


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def call(where, path):
    event = {
        "rawPath": "%s%s" % (PREFIX, path),
        "queryStringParameters": None,
        "requestContext": {"http": {"method": "GET"}},
        "headers": {"x-firm-id": "opal"},
    }
    if where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")
        r = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        from lib.research.api import scoped_amgt

        r = scoped_amgt.handler(event)
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


def is_us_alpha(member):
    ticker = member.get("ticker")
    return (member.get("country") == "United States" and isinstance(ticker, str)
            and ticker.isascii() and ticker.isalpha())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", default="local", choices=["local", "deployed"])
    where = ap.parse_args().where

    from lib.research.api import scoped_amgt
    from lib.research.identity import crosswalk

    stored, rec = scoped_amgt.read_pool_object(scoped_amgt.PEERS_PREFIX, SUBJECT)
    code, served = call(where, "/security/%s/peers" % SUBJECT)
    members = served.get("members") or []
    stored_members = (stored or {}).get("members") or []
    print("   where=%s status=%s stored=%s served members=%d stored members=%d" % (
        where, code, rec.get("object_key"), len(members), len(stored_members)))

    expected = {}
    for m in members:
        if is_us_alpha(m):
            hit = crosswalk.resolve(m["ticker"] + " US")
            if hit.get("resolution") == crosswalk.RESOLUTION_MEASURED and hit.get("security_key"):
                expected[m["ticker"]] = hit["security_key"]
    us = [m for m in members if is_us_alpha(m)]
    print("   denominators: members %d | US-ticker members %d | resolvable under '<T> US' %d" % (
        len(members), len(us), len(expected)))

    bad = []
    for m in members:
        if m.get("ticker") in expected:
            ident = m.get("identity") or {}
            if not (ident.get("resolution") == "MEASURED" and ident.get("security_key") == expected[m["ticker"]]
                    and m.get("security_key") == expected[m["ticker"]]):
                bad.append((m.get("ticker"), ident.get("resolution"), ident.get("security_key"), m.get("security_key")))
    for t, res, key, top in bad:
        print("   NOT SERVED: %s identity.resolution=%r identity.security_key=%r security_key=%r" % (t, res, key, top))
    i1 = say(code == 200 and len(expected) >= 1 and not bad,
             "I1 every member the pool holds under '<ticker> US' serves that identity (%d of %d)" % (
                 len(expected) - len(bad), len(expected)))

    leaked = [m.get("ticker") for m in members
              if m.get("ticker") not in expected and (m.get("identity") or {}).get("resolution") == "MEASURED"
              and not str(m.get("ticker", "")).isdigit()]
    i2 = say(not leaked, "I2 no member outside the pool's holdings serves a MEASURED identity (leaked: %s)" % leaked)

    keep = ("ticker", "name", "price", "country")
    same = (len(members) == len(stored_members)
            and all(all(a.get(k) == b.get(k) for k in keep) for a, b in zip(members, stored_members)))
    i3 = say(same, "I3 members neither removed nor reordered; ticker, name, price, country equal to the stored object's")

    ok = i1 and i2 and i3
    print("R89 PEER IDENTITY: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
