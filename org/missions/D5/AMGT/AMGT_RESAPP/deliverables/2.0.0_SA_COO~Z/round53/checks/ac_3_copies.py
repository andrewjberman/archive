"""AMGT_RESAPP round 53, AMGT-ac-3 -- the raw-slash objects (40: CTO msg 27160, AMENDMENT 1) are copied to their encoded keys, byte-equal, and the raw objects are KEPT
(CTO round-52 ruling 4; CORPUS round-23 ruling 2's single window).
Reads the object list `round53/SLASH_OBJECTS.json` (written by 2.0.0_SA_COO~Z from 2.0.0_SA_COO~X's supplied list and before-state, before
the GO): {"bucket": "opal-data-harvest", "objects": [{"raw_key": ..., "encoded_key": ..., "raw_sha256": ...}, ...]}. For EVERY object:
the raw key still exists with its listed sha256 (kept, unchanged), and the encoded key exists with the SAME sha256. PASS when every listed object holds and the list has 40 (AMENDMENT 1).
usage: python <this>   (from the repo root; S3 GET/HEAD only)"""
import hashlib
import json
import sys

import boto3

LIST = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round53/SLASH_OBJECTS.json"


def sha(cl, b, k):
    try:
        return hashlib.sha256(cl.get_object(Bucket=b, Key=k)["Body"].read()).hexdigest()
    except cl.exceptions.NoSuchKey:
        return None


def main():
    try:
        doc = json.load(open(LIST, encoding="utf-8"))
    except FileNotFoundError:
        print("no %s (the issuer writes it from COO~X's supplied list before the GO)" % LIST)
        print("THE RAW-SLASH OBJECTS READ AT THEIR ENCODED KEYS, BYTE-EQUAL, RAW KEPT: NO")
        return 1
    cl = boto3.client("s3", region_name="us-east-1")
    objs, bad = doc.get("objects") or [], []
    for o in objs:
        raw, enc = sha(cl, doc["bucket"], o["raw_key"]), sha(cl, doc["bucket"], o["encoded_key"])
        if raw != o["raw_sha256"]:
            bad.append("raw moved or gone: %s" % o["raw_key"])
        if enc != o["raw_sha256"]:
            bad.append("encoded %s: %s" % ("absent" if enc is None else "differs", o["encoded_key"]))
    for b in bad[:8]:
        print("  BAD", b)
    print("objects %d; raw kept and encoded byte-equal: %d" % (len(objs), len(objs) - len({b.split(': ', 1)[1] for b in bad})))
    ok = len(objs) == 40 and not bad
    print("THE RAW-SLASH OBJECTS READ AT THEIR ENCODED KEYS, BYTE-EQUAL, RAW KEPT: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
