"""AMGT_RESAPP round 54, AMGT-ad-2 -- the compliance act: every stored D-1 document's no-span sentences moved to `held_no_span` by
ad-1's `drafting_build --hold-unspanned`, read on the store and on the DEPLOYED /thesis route (read-only).
  --what save  --dir D   (the executor, BEFORE the act) the 12 stored drafting/v1 objects' bytes -> D/store/<key>.json, and the served
                         /thesis bodies -> D/served/<key>.json.
  --what store --dir D   every stored document graded against its pre-act bytes by ad-1's rule (round54/checks/ad_1_hold.py `grade`):
                         exactly the no-span sentences moved to held_no_span in the pipeline's held shape, every span-carrying sentence
                         byte-equal in place, every other top-level key byte-equal, the deployed validator accepting it; and 0 no-span
                         sentences left in any stored section.
  --what served --dir D  per name, the served /thesis body against the pre-act one: `drafted_sections` sentences byte-equal (the page's
                         text does not move -- the adapter already held these sentences at read), `held_no_span_count` equal,
                         `held_no_span_at_read` 0, `held_no_span_on_object` = the pre-act at-read count, basis READ_GATE_PLUS_OBJECT,
                         every other key equal apart from generated_at / as_of_date and the per-section held_no_span_at_read.
                         AMENDMENT 2: those read-time stamps are dropped at every depth, not only at the top level.
usage: python <this> --what save|store|served --dir D   (from the repo root)"""
import argparse
import importlib.util
import json
import os
import sys

sys.path.insert(0, os.getcwd())
import boto3  # noqa: E402
from lib.research.filings import drafting_build as db  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402

HOLD = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round54/checks/ad_1_hold.py"
CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
VOLATILE = ("generated_at", "as_of_date", "read_at", "served_at", "request_id")
MOVES = ("held_no_span_at_read", "held_no_span_on_object", "held_no_span_basis", "drafted_sections")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def keys_of(s3):
    pages = s3.get_paginator("list_objects_v2").paginate(Bucket=crosswalk.POOL_BUCKET, Prefix="drafting/v1/")
    return [o["Key"] for p in pages for o in p.get("Contents", []) if o["Key"].endswith(".json")]


def unvolatile(o):
    """AMENDMENT 2: the read-time stamps are dropped at EVERY depth (VLO's nested model.generated_at moved 19:37Z -> 19:53Z between
    two reads of an unchanged model block), never a data field."""
    if isinstance(o, dict):
        return {k: unvolatile(v) for k, v in o.items() if k not in VOLATILE}
    if isinstance(o, list):
        return [unvolatile(v) for v in o]
    return o


def sec_sentences(body):
    return json.dumps([[s.get("section_id"), s.get("sentences")] for s in body.get("drafted_sections") or []], sort_keys=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--what", choices=("save", "store", "served"), required=True)
    ap.add_argument("--dir", required=True)
    a = ap.parse_args()
    s3 = boto3.client("s3", region_name="us-east-1")
    keys = keys_of(s3)
    names = [k.rsplit("/", 1)[1][:-5] for k in keys]
    bad = []
    if a.what in ("save", "served"):
        cl = load("capture_lib", CAPTURE_LIB)
        lam = boto3.client("lambda", region_name=cl.REGION)
    if a.what == "save":
        os.makedirs(os.path.join(a.dir, "store"), exist_ok=True)
        os.makedirs(os.path.join(a.dir, "served"), exist_ok=True)
        for k, n in zip(keys, names):
            open(os.path.join(a.dir, "store", n + ".json"), "wb").write(s3.get_object(Bucket=crosswalk.POOL_BUCKET, Key=k)["Body"].read())
            body, _m = cl._invoke(lam, "%s/security/%s/thesis" % (cl.ROUTE_PREFIX, n))
            json.dump(body, open(os.path.join(a.dir, "served", n + ".json"), "w", encoding="utf-8"), sort_keys=True)
            if not body:
                bad.append("%s: empty served body" % n)
        print("saved %d stored documents and %d served bodies to %s" % (len(keys), len(keys), a.dir))
        label = "PRE-ACT CAPTURE SAVED"
    elif a.what == "store":
        hold = load("ad_1_hold", HOLD)
        moved_total = 0
        for k, n in zip(keys, names):
            try:
                pre = json.load(open(os.path.join(a.dir, "store", n + ".json"), encoding="utf-8"))
            except FileNotFoundError:
                bad.append("%s: no pre-act capture" % n)
                continue
            live = db._get_json_object(s3, k)
            moved, why = hold.grade(pre, live)
            left = sum(1 for sec in live.get("sections") or [] for s in sec.get("sentences") or [] if hold.nonverbatim(s))
            moved_total += moved
            print("%s: moved %d, no-span left %d%s" % (n, moved, left, "" if not why else " BAD %s" % why[:2]))
            bad += ["%s: %s" % (n, w) for w in why] + (["%s: %d no-span sentences left" % (n, left)] if left else [])
        print("documents %d; sentences moved %d" % (len(keys), moved_total))
        label = "EVERY STORED D-1 DOCUMENT HOLDS ITS NO-SPAN SENTENCES AND MOVES NOTHING ELSE"
    else:
        for n in names:
            try:
                pre = json.load(open(os.path.join(a.dir, "served", n + ".json"), encoding="utf-8"))
            except FileNotFoundError:
                bad.append("%s: no pre-act capture" % n)
                continue
            post, _m = cl._invoke(lam, "%s/security/%s/thesis" % (cl.ROUTE_PREFIX, n))
            post = post or {}
            want_on_object = pre.get("held_no_span_at_read")
            checks = {
                "sentences byte-equal": sec_sentences(pre) == sec_sentences(post),
                "held_no_span_count equal": pre.get("held_no_span_count") == post.get("held_no_span_count"),
                "at_read 0": post.get("held_no_span_at_read") == 0,
                "on_object = pre at_read (%s)" % want_on_object: post.get("held_no_span_on_object") == want_on_object,
                "basis READ_GATE_PLUS_OBJECT": post.get("held_no_span_basis") == "READ_GATE_PLUS_OBJECT",
            }
            others = [k for k in set(pre) | set(post) if k not in VOLATILE and k not in MOVES
                      and json.dumps(unvolatile(pre.get(k)), sort_keys=True) != json.dumps(unvolatile(post.get(k)), sort_keys=True)]
            if others:
                checks["other keys unmoved (moved: %s)" % others[:4]] = False
            failed = [c for c, ok in checks.items() if not ok]
            print("%s: at_read %s -> %s, on_object %s -> %s, count %s -> %s%s"
                  % (n, pre.get("held_no_span_at_read"), post.get("held_no_span_at_read"), pre.get("held_no_span_on_object"),
                     post.get("held_no_span_on_object"), pre.get("held_no_span_count"), post.get("held_no_span_count"),
                     "" if not failed else " BAD %s" % failed))
            bad += ["%s: %s" % (n, f) for f in failed]
        label = "THE SERVED /THESIS TEXT IS UNMOVED AND READS THE HOLD FROM THE OBJECT"
    for b in bad[:20]:
        print("  BAD", b)
    ok = bool(keys) and not bad
    print("%s: %s" % (label, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
