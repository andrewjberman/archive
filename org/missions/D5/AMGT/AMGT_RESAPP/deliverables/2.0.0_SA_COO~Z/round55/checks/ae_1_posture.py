"""AMGT_RESAPP round 55, AMGT-ae-1 -- the first posture batch since ad-2 held 179 no-span D-1 sentences on 12 objects: its diff read
from the batch's OWN output (CTO round-54 analysis item 1; rulings 1 and 5). Read-only (S3 + the deployed /posture route).
TARGETS: every posture subject whose newest `posture/v1/<key>/<as_of>.json` has the subject OR its `comparable` among the names whose
stored D-1 document carries a non-empty `held_no_span` (the 12 ad-2 moved).
  --what pre --dir D     (the executor, BEFORE the batch) per target: the newest object's key, verdict, cites, and each pack's
                         `counts.drafted_sentences`; plus TWO live reads of the served /posture route a few seconds apart -- the
                         paths that differ between them are the route's volatile set (ruling 1: measured, dropped by PATH) -> D/pre.json.
  The batch re-runs each target AT ITS PRIOR OBJECT'S as_of (so M-1 / R-1 / universe are the inputs the prior run read and only D-1
  differs) and so OVERWRITES that key; the bucket is versioned, and `pre` records each key's VersionId (the rollback).
  --what post --dir D    per target, the SAME key carries a NEW VersionId and: each pack's drafted_sentences equals the number of sentences in
                         that name's LIVE D-1 sections (after ad-2: span-carrying only -- the held sentences are not in the pack; a
                         name with no D-1 document packs 0); cites_validated == cites_total; verdict in {better, worse, hold, steer_clear, absent (a classed ABSENT document)};
                         the served /posture route serves the new object (its as_of and verdict), comparing only non-volatile paths.
                         Verdict moves are PRINTED (before -> after, read from the batch's own output), never graded.
usage: python <this> --what pre|post --dir D   (from the repo root)"""
import argparse
import importlib.util
import json
import os
import sys
import time

sys.path.insert(0, os.getcwd())
import boto3  # noqa: E402

BUCKET = "opal-data-harvest"
CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
VERDICTS = {"better", "worse", "hold", "steer_clear", "absent"}  # "absent": the classed ABSENT document (an unresolved side)


def keys(s3, prefix):
    pages = s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix)
    return [o for p in pages for o in p.get("Contents", [])]


def jget(s3, key):
    return json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())


def held_by_name(s3, served=None):
    out = {}
    for o in keys(s3, "drafting/v1/"):
        doc = jget(s3, o["Key"])
        name = o["Key"].rsplit("/", 1)[1][:-5]
        if served is not None:
            served[name] = sum(len(sec.get("sentences") or []) for sec in doc.get("sections") or [])
        n = len(doc.get("held_no_span") or [])
        if n:
            out[name] = n
    return out


def newest_by_subject(s3):
    by = {}
    for o in keys(s3, "posture/v1/"):
        parts = o["Key"].split("/")
        if len(parts) >= 4 and parts[3].endswith(".json"):
            cur = by.get(parts[2])
            if cur is None or parts[3] > cur.split("/")[3]:
                by[parts[2]] = o["Key"]
    return by


def paths(o, p=""):
    if isinstance(o, dict):
        r = {}
        for k, v in o.items():
            r.update(paths(v, "%s/%s" % (p, k)))
        return r
    if isinstance(o, list):
        r = {}
        for i, v in enumerate(o):
            r.update(paths(v, "%s/%d" % (p, i)))
        return r
    return {p: json.dumps(o, sort_keys=True)}


def serve(cl, lam, key):
    body, _m = cl._invoke(lam, "%s/security/%s/posture" % (cl.ROUTE_PREFIX, key))
    return body or {}


def summary(doc):
    return {"verdict": doc.get("verdict"), "as_of": doc.get("as_of"), "comparable": doc.get("comparable"),
            "cites": [doc.get("cites_validated"), doc.get("cites_total")],
            "drafted": {k: (v.get("counts") or {}).get("drafted_sentences") for k, v in (doc.get("packs") or {}).items()}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--what", choices=("pre", "post"), required=True)
    ap.add_argument("--dir", required=True)
    a = ap.parse_args()
    s3 = boto3.client("s3", region_name="us-east-1")
    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    lam = boto3.client("lambda", region_name=cl.REGION)
    in_sections = {}
    held = held_by_name(s3, in_sections)
    newest = newest_by_subject(s3)
    path = os.path.join(a.dir, "pre.json")
    bad = []
    if a.what == "pre":
        targets = {}
        for subj, key in sorted(newest.items()):
            doc = jget(s3, key)
            if subj in held or doc.get("comparable") in held:
                r1 = serve(cl, lam, subj)
                time.sleep(3)
                r2 = serve(cl, lam, subj)
                p1, p2 = paths(r1), paths(r2)
                volatile = sorted(k for k in set(p1) | set(p2) if p1.get(k) != p2.get(k))
                version = s3.head_object(Bucket=BUCKET, Key=key).get("VersionId")
                targets[subj] = {"object": key, "version": version, **summary(doc), "served_volatile": volatile}
        os.makedirs(a.dir, exist_ok=True)
        json.dump({"held": held, "targets": targets}, open(path, "w", encoding="utf-8"), indent=1, sort_keys=True)
        for s, t in targets.items():
            print("%s: %s verdict %s drafted %s volatile %s" % (s, t["object"].rsplit("/", 1)[1], t["verdict"], t["drafted"], t["served_volatile"]))
        print("names holding sentences %d (total %d); targets %d" % (len(held), sum(held.values()), len(targets)))
        ok = bool(targets)
        label = "PRE-BATCH STATE SAVED"
    else:
        try:
            pre = json.load(open(path, encoding="utf-8"))
        except FileNotFoundError:
            print("no pre-batch capture at %s" % path)
            pre = {"targets": {}, "held": {}}
            bad.append("no pre-batch capture")
        moved = 0
        for subj, t in sorted(pre["targets"].items()):
            key = t["object"]
            if s3.head_object(Bucket=BUCKET, Key=key).get("VersionId") == t.get("version"):
                bad.append("%s: %s still at its pre-batch VersionId" % (subj, key))
                continue
            doc = jget(s3, key)
            s = summary(doc)
            why = []
            for name, after in (s["drafted"] or {}).items():
                want = in_sections.get(name, 0)
                if after != want:
                    why.append("%s pack drafted %s, want %s (its live D-1 sections)" % (name, after, want))
            if s["cites"][0] != s["cites"][1]:
                why.append("cites %s of %s validated" % tuple(s["cites"]))
            if s["verdict"] not in VERDICTS:
                why.append("verdict %r off the enum" % s["verdict"])
            served = serve(cl, lam, subj)
            vol = set(t.get("served_volatile") or [])
            ps, pd = paths(served), paths(doc)
            for field in ("/as_of", "/verdict"):
                if field not in vol and ps.get(field) != pd.get(field):
                    why.append("served %s %s != stored %s" % (field, ps.get(field), pd.get(field)))
            moved += s["verdict"] != t["verdict"]
            print("%s: %s v%s -> new | verdict %s -> %s | drafted %s -> %s | cites %s%s"
                  % (subj, t["object"].rsplit("/", 1)[1], str(t.get("version"))[:8], t["verdict"], s["verdict"], t["drafted"],
                     s["drafted"], s["cites"], "" if not why else " BAD %s" % why))
            bad += ["%s: %s" % (subj, w) for w in why]
        print("targets %d; verdicts moved %d (read from the batch's output, not graded)" % (len(pre["targets"]), moved))
        ok = bool(pre["targets"]) and not bad
        label = "THE POSTURE BATCH READS THE HELD PACKS AND SERVES ITS OWN OUTPUT"
    for b in bad[:20]:
        print("  BAD", b)
    print("%s: %s" % (label, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
