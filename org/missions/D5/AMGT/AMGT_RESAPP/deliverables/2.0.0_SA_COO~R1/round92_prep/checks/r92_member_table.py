"""AMGT_RESAPP round-92 PREP -- the member-by-member expected-outcome table for the redeploy pair (`AMGT-qq-5`).

  PYTHONPATH=<repo root> python r92_member_table.py <out.json> [--limit N]

BEFORE is the LIVE function's peers response for each keyed subject (Lambda invoke, GET only). AFTER is the checkout's own handler
(`scoped_amgt.handler`) on the same live pool: the code the redeploy would carry, over the same objects. Every member of every subject
(about 2,230 members, 243 subjects) is compared on the fields a redeploy of this code may move; every difference is listed, each with its
cause class. A difference outside {identity, security_key, price_currency, price_currency_reason} is reported as OTHER (a STOP).
Read-only; writes only <out.json>.
"""
import collections
import json
import sys

import boto3

from lib.research.api import scoped_amgt
from lib.research.identity import crosswalk

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
FIELDS = ("identity", "security_key", "price_currency", "price_currency_reason")
_LAM = boto3.client("lambda", region_name="us-east-1")


def event(key):
    return {"rawPath": "%s/security/%s/peers" % (PREFIX, key), "queryStringParameters": None,
            "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}


def live(key):
    r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event(key)).encode())["Payload"].read())
    return json.loads(r.get("body") or "{}")


def local(key):
    r = scoped_amgt.handler(event(key))
    return json.loads(r.get("body") or "{}")


def cause(before, after):
    bk = (before.get("identity") or {}).get("security_key")
    ak = (after.get("identity") or {}).get("security_key")
    if bk != ak:
        return "identity_gained" if not bk else "identity_changed"
    return "currency_only"


def main():
    out_path = sys.argv[1]
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    doc, _i, _a = crosswalk.load_crosswalk()
    keys = [r["security_key"] for r in doc["records"] if r.get("resolution") == "MEASURED" and r.get("security_key")]
    if limit:
        keys = keys[:limit]
    members_total = 0
    changed = []
    other = []
    subject_level = []
    for key in keys:
        b, a = live(key), local(key)
        bm, am = b.get("members") or [], a.get("members") or []
        if len(bm) != len(am):
            subject_level.append((key, "member count %d -> %d" % (len(bm), len(am))))
            continue
        # subject-level fields outside members
        for k in set(b) | set(a):
            if k == "members" or k in ("peer_read",):
                continue
            if b.get(k) != a.get(k):
                subject_level.append((key, "subject field %s" % k))
        for i, (x, y) in enumerate(zip(bm, am)):
            members_total += 1
            if not isinstance(x, dict) or not isinstance(y, dict):
                continue
            moved = [f for f in FIELDS if x.get(f) != y.get(f)]
            outside = [f for f in set(x) | set(y) if f not in FIELDS and x.get(f) != y.get(f)]
            if outside:
                other.append({"subject": key, "ticker": x.get("ticker"), "fields": sorted(outside)})
            if moved:
                changed.append({
                    "subject": key, "i": i, "ticker": x.get("ticker"), "name": x.get("name"), "country": x.get("country"),
                    "price": x.get("price"), "cause": cause(x, y), "fields": moved,
                    "before": {"key": (x.get("identity") or {}).get("security_key"), "currency": x.get("price_currency"),
                               "reason": (x.get("price_currency_reason") or "")[:70] or None},
                    "after": {"key": (y.get("identity") or {}).get("security_key"), "matched_as": (y.get("identity") or {}).get("matched_as"),
                              "currency": y.get("price_currency"), "reason": (y.get("price_currency_reason") or "")[:70] or None},
                })
    by_cause = collections.Counter(c["cause"] for c in changed)
    shape = collections.Counter((c["before"]["currency"], c["after"]["currency"], bool(c["before"]["reason"]), bool(c["after"]["reason"]))
                                for c in changed)
    json.dump({"subjects": len(keys), "members": members_total, "changed": changed, "other": other, "subject_level": subject_level},
              open(out_path, "w"))
    print("subjects %d | members %d | changed %d | OTHER-field changes %d | subject-level differences %d" % (
        len(keys), members_total, len(changed), len(other), len(subject_level)))
    print("by cause:", dict(by_cause))
    for (bc, ac, br, ar), n in sorted(shape.items(), key=lambda kv: -kv[1]):
        print("  currency %-5s -> %-5s | reason %-5s -> %-5s : %d member(s)" % (bc, ac, br, ar, n))
    return 0 if not other and not subject_level else 1


if __name__ == "__main__":
    sys.exit(main())
