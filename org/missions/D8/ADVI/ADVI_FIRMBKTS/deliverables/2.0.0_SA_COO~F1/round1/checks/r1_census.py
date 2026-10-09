"""ADVI_FIRMBKTS round 1 check for cell FB-t-1 (the key census), issuer 2.0.0_SA_COO~F1.

--static grades census.json alone (4 arms). --live grades it against a fresh listing of the three legacy
buckets (2 arms). --root points at another tree (the issuer's positive control). Never edit this file.
"""
import argparse
import datetime
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

BUCKETS = ("opal-data-bd", "opal-data-inf", "opal-data-cot")
REL = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables/census.json"
MAX_CLASSES = 500


def _root(arg):
    if arg:
        return arg
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return out.stdout.strip()


def _ts(s):
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)


def _load(root):
    path = os.path.join(root, REL)
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def static_arms(doc):
    res = []
    ok = isinstance(doc, dict) and set(doc.get("buckets", {})) == set(BUCKETS)
    try:
        _ts(doc.get("listed_at", ""))
    except Exception:
        ok = False
    ok = ok and "arn:aws:" in str(doc.get("instrument", ""))
    res.append(("S1 shape: listed_at, instrument with an ARN, exactly the three legacy buckets", ok))
    if not ok:
        return res + [("S2 denominators", False), ("S3 disjoint prefixes", False), ("S4 prefix form", False), ("S5 grain", False)]
    s2 = s3 = s4 = True
    for b in BUCKETS:
        bd = doc["buckets"][b]
        classes = bd.get("classes") or []
        total = sum(int(c.get("objects", 0)) for c in classes)
        good = isinstance(bd.get("objects"), int) and bd["objects"] > 0 and total == bd["objects"]
        for c in classes:
            good = good and int(c.get("objects", 0)) > 0 and str(c.get("sample_key", "")).startswith(str(c.get("prefix", "\0")))
            good = good and bool(c.get("last_modified_max"))
        print("  %s: objects=%s sum(classes)=%d classes=%d" % (b, bd.get("objects"), total, len(classes)))
        s2 = s2 and good
        prefixes = [c.get("prefix", "") for c in classes]
        if len(set(prefixes)) != len(prefixes):
            s3 = False
        dirs = sorted(p for p in prefixes if p.endswith("/"))
        for i in range(len(dirs) - 1):
            if dirs[i + 1].startswith(dirs[i]):
                print("  OVERLAP %s: %r contains %r" % (b, dirs[i], dirs[i + 1]))
                s3 = False
        for c in classes:
            if not (c["prefix"].endswith("/") or c["prefix"] == c.get("sample_key")):
                print("  FORM %s: %r neither ends in / nor equals its sample_key" % (b, c["prefix"]))
                s4 = False
    res.append(("S2 every bucket's class counts sum to its denominator, each class non-empty with a sample in it", s2))
    res.append(("S3 class prefixes are unique and directory classes are disjoint (a single-key class may sit "
                "under one and takes its key from it)", s3))
    res.append(("S4 every class prefix ends in / or is a single key", s4))
    s5 = all(len(doc["buckets"][b].get("classes") or []) <= MAX_CLASSES for b in BUCKETS)
    res.append(("S5 the table grain: no bucket carries more than %d classes (an entity-id or partition segment "
                "left in a prefix multiplies them)" % MAX_CLASSES, s5))
    return res


def _list(bucket):
    import boto3
    pag = boto3.client("s3").get_paginator("list_objects_v2")
    out = []
    for page in pag.paginate(Bucket=bucket):
        for o in page.get("Contents", []):
            out.append((o["Key"], o["LastModified"]))
    return out


def _owner(key, prefixes):
    if key in prefixes:
        return key
    i = key.find("/")
    while i != -1:
        if key[: i + 1] in prefixes:
            return key[: i + 1]
        i = key.find("/", i + 1)
    return None


def live_arms(doc):
    listed_at = _ts(doc["listed_at"])
    with ThreadPoolExecutor(max_workers=3) as ex:
        listings = dict(zip(BUCKETS, ex.map(_list, BUCKETS)))
    l1 = l2 = True
    for b in BUCKETS:
        prefixes = {c["prefix"] for c in doc["buckets"][b]["classes"]}
        hits = dict.fromkeys(prefixes, 0)
        old_unc, new_unc = [], 0
        for key, lm in listings[b]:
            p = _owner(key, prefixes)
            if p is None:
                if lm <= listed_at:
                    old_unc.append(key)
                else:
                    new_unc += 1
            else:
                hits[p] += 1
        empty = [p for p, n in hits.items() if n == 0]
        print("  %s: live=%d uncovered(before listed_at)=%d new-after-snapshot uncovered=%d empty classes=%d of %d"
              % (b, len(listings[b]), len(old_unc), new_unc, len(empty), len(prefixes)))
        for k in old_unc[:5]:
            print("    UNCOVERED %s" % k)
        for p in empty[:5]:
            print("    EMPTY %s" % p)
        l1 = l1 and not old_unc
        l2 = l2 and not empty
    return [("L1 every live key that existed at listed_at falls in exactly one class", l1),
            ("L2 every class holds at least one live key", l2)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--static", action="store_true")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--root")
    a = ap.parse_args()
    root = _root(a.root)
    try:
        doc = _load(root)
    except Exception as e:
        print("ABSENT or unreadable: %s (%s)" % (REL, type(e).__name__))
        doc = None
    label = "LIVE" if a.live else "STATIC"
    if doc is None:
        arms = [("census.json present", False)]
    elif a.live:
        arms = live_arms(doc) if all(ok for _, ok in static_arms(doc)) else [("static arms must pass first", False)]
    else:
        arms = static_arms(doc)
    for name, ok in arms:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in arms if ok)
    total = 2 if a.live else 5
    print("ROUND 1 CENSUS %s: %d of %d arms" % (label, n, total))
    sys.exit(0 if n == total else 1)


if __name__ == "__main__":
    main()
