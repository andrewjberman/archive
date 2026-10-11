"""AMGT_RESAPP round-93 PREP -- rr-6: after the peers rebuild, no subject lists its own company and nothing else left a set.

  PYTHONPATH=<repo root> python r93_self_peer_census.py --write-baseline <out.json>      (read the live routes now, write the baseline)
  PYTHONPATH=<repo root> python r93_self_peer_census.py --baseline <baseline.json>       (grade the live routes against it)

Instrument: for each of the 243 MEASURED crosswalk subjects, the deployed function's `/security/<key>/peers` (Lambda invoke, GET only): the members
(ticker, served `security_key`) and `member_count`. The baseline is the same read BEFORE the rebuild.
    S1 no subject has a member whose served `security_key` equals the subject's own key (the baseline lists the subjects that did).
    S2 every member removed from a subject's set, against the baseline, is one of that subject's own-company members (nothing else left a set).
    S3 every subject that lost a self member and has further candidates still has at least its baseline member count (the set was backfilled).
    S4 control: every subject whose baseline set had no self member is member-for-member equal to its baseline.
Verdict: R93 SELF PEER CENSUS: YES|NO (exit 0|1). At the base (2026-10-11, the baseline against itself) S1 FAILs (10 subjects list themselves).
"""
import argparse
import json
import sys

import boto3

from lib.research.identity import crosswalk

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
_LAM = boto3.client("lambda", region_name="us-east-1")


def peers(key):
    event = {"rawPath": "%s/security/%s/peers" % (PREFIX, key), "queryStringParameters": None,
             "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    return json.loads(r.get("body") or "{}")


def read_all():
    doc, _i, _a = crosswalk.load_crosswalk()
    keys = [r["security_key"] for r in doc["records"] if r.get("resolution") == "MEASURED" and r.get("security_key")]
    out = {}
    for key in keys:
        body = peers(key)
        members = []
        for m in body.get("members") or []:
            k = m.get("security_key") or (m.get("identity") or {}).get("security_key")
            members.append([m.get("ticker"), k])
        out[key] = {"member_count": len(members), "members": members, "as_of": body.get("as_of")}
    return out


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-baseline")
    ap.add_argument("--baseline")
    args = ap.parse_args()
    now = read_all()
    if args.write_baseline:
        json.dump(now, open(args.write_baseline, "w"), sort_keys=True)
        selfs = {k: [t for t, mk in v["members"] if mk == k] for k, v in now.items()}
        selfs = {k: v for k, v in selfs.items() if v}
        print("   baseline written: %d subjects, %d members, %d subjects list their own company: %s" % (
            len(now), sum(v["member_count"] for v in now.values()), len(selfs), sorted(selfs)))
        return 0
    base = json.load(open(args.baseline))
    own_now = {k: [t for t, mk in v["members"] if mk == k] for k, v in now.items()}
    own_now = {k: v for k, v in own_now.items() if v}
    own_base = {k: {t for t, mk in v["members"] if mk == k} for k, v in base.items()}
    s2_bad, s3_bad, s4_bad = [], [], []
    for key, b in base.items():
        n = now.get(key)
        if n is None:
            s4_bad.append(key)
            continue
        before = {t for t, _k in b["members"]}
        after = {t for t, _k in n["members"]}
        removed = before - after
        if not removed <= own_base[key]:
            s2_bad.append((key, sorted(removed - own_base[key])))
        if own_base[key]:
            if n["member_count"] < b["member_count"] and len(after) < 12 and removed <= own_base[key]:
                s3_bad.append((key, b["member_count"], n["member_count"]))
        elif before != after:
            s4_bad.append(key)
    print("   subjects %d | baseline subjects with a self member %d | now %d" % (
        len(base), sum(1 for v in own_base.values() if v), len(own_now)))
    results = [
        say(not own_now, "S1 no subject lists its own company", "still: %s" % sorted(own_now)[:6]),
        say(not s2_bad, "S2 every removed member was an own-company member", "other removals: %s" % s2_bad[:4]),
        say(not s3_bad, "S3 a set that lost its self member is backfilled to its baseline count", "short: %s" % s3_bad[:4]),
        say(not s4_bad, "S4 control: a subject without a self member is member-for-member equal", "moved: %s" % s4_bad[:4]),
    ]
    print("   arms passed %d of %d" % (sum(1 for r in results if r), len(results)))
    ok = all(results)
    print("R93 SELF PEER CENSUS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
