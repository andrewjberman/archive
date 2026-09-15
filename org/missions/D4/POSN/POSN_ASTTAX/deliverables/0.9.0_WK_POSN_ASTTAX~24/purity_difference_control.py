#!/usr/bin/env python3
"""W1-AC3 -- PURITY: every EXISTING field of characteristics.json is unchanged.

POSN_ASTTAX.TO-W1-1, cell AT6-s-1, `0.9.0_WK_POSN_ASTTAX~24`.

THE QUESTION THIS ANSWERS, AND THE ONE IT DOES NOT
    It answers: over the SAME three inputs, does the working producer emit exactly what
    HEAD's producer emits, except for the two keys this cell adds (`tickers` and
    `method.tickers_block`)? It does NOT answer whether the new block is correct -- that is
    W1-AC4's dry run, read against the served artifact in W1-AC12.

WHY IT IS A DIFFERENCE CONTROL AND NOT A RE-READ OF MY OWN OUTPUT
    The two arms differ in EXACTLY ONE THING: the module bytes. The three input objects are
    read ONCE, read-only, from the live keys and the SAME python objects are handed to both
    arms, so nothing in the inputs, the clock or the environment can differ between them.
    HEAD's module is extracted with `git show HEAD:<path>` into a REPO-MIRRORING temp tree,
    because that module computes `parents[4]` to find the repo root -- dropped flat into a
    temp directory it would IndexError at import, which is the same trap build_package.py's
    layout exists to avoid.

THE POSITIVE CONTROL IS NOT OPTIONAL
    A comparator that cannot fail proves nothing. After the real compare, ONE leaf of the
    working arm is perturbed and the same comparator is run again: it must print False. Both
    results are printed; either one missing makes this criterion unread.

NOTHING IS WRITTEN. Three GetObjects, no PutObject, no local artifact.
ASCII only.
"""
from __future__ import annotations

import argparse
import copy
import gzip
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

import boto3

HOLDINGS = ("opal-data-cot", "platinum/satellites/holdings.json")
POSITIONING = ("opal-data-portal-v2", "json/positioning/positioning_data.json")
BBG_BUCKET = "opal-data-etfs"
PRODUCER_PATH = "data/assets/scripts/gold/build_satellites_characteristics.py"
CALENDAR_PATH = "lib/trading_calendar.py"
ADDED_KEYS = ("tickers", "method.tickers_block")
AS_OF = "2026-09-15"  # fixed and shared by both arms -- a clock difference is not a code difference


def load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def extract_head_tree(root: str) -> str:
    """HEAD's producer in a repo-MIRRORING tree, so its parents[4] resolves."""
    gold = os.path.join(root, "data", "assets", "scripts", "gold")
    os.makedirs(gold, exist_ok=True)
    os.makedirs(os.path.join(root, "lib"), exist_ok=True)
    blob = subprocess.check_output(["git", "show", "HEAD:" + PRODUCER_PATH])
    if not blob:
        raise SystemExit("REFUSED: HEAD:%s is EMPTY (a mangled ref reads clean-empty)." % PRODUCER_PATH)
    target = os.path.join(gold, "build_satellites_characteristics.py")
    with open(target, "wb") as fh:
        fh.write(blob)
    shutil.copyfile(CALENDAR_PATH, os.path.join(root, "lib", "trading_calendar.py"))
    print("HEAD module extracted: %d bytes -> %s" % (len(blob), target))
    return target


def count_leaves(obj) -> int:
    if isinstance(obj, dict):
        return sum(count_leaves(v) for v in obj.values())
    if isinstance(obj, list):
        return sum(count_leaves(v) for v in obj)
    return 1


def strip_added(doc: dict) -> dict:
    out = copy.deepcopy(doc)
    removed = []
    if "tickers" in out:
        del out["tickers"]
        removed.append("tickers")
    if "tickers_block" in (out.get("method") or {}):
        del out["method"]["tickers_block"]
        removed.append("method.tickers_block")
    print("STRIPPED from the working arm: %s" % (", ".join(removed) or "NOTHING"))
    if sorted(removed) != sorted(ADDED_KEYS):
        raise SystemExit("REFUSED: expected to strip %s, stripped %s" % (list(ADDED_KEYS), removed))
    return out


def first_difference(a, b, path="$"):
    if type(a) is not type(b):
        return "%s: type %s != %s" % (path, type(a).__name__, type(b).__name__)
    if isinstance(a, dict):
        for k in a:
            if k not in b:
                return "%s.%s: present in HEAD arm, absent in working arm" % (path, k)
        for k in b:
            if k not in a:
                return "%s.%s: present in working arm, absent in HEAD arm" % (path, k)
        for k in a:
            d = first_difference(a[k], b[k], "%s.%s" % (path, k))
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return "%s: len %d != %d" % (path, len(a), len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_difference(x, y, "%s[%d]" % (path, i))
            if d:
                return d
        return None
    if a != b:
        return "%s: %r != %r" % (path, a, b)
    return None


def perturb_one_leaf(doc: dict):
    """Move exactly ONE existing leaf -- the positive control's only change."""
    out = copy.deepcopy(doc)
    for code in out.get("satellites") or {}:
        sat = out["satellites"][code]
        sat["total_weight"] = round(float(sat["total_weight"]) + 0.0001, 6)
        return out, "satellites.%s.total_weight %s -> %s" % (
            code, doc["satellites"][code]["total_weight"], sat["total_weight"])
    raise SystemExit("REFUSED: no leaf to perturb -- the positive control cannot run.")


def main() -> int:
    ap = argparse.ArgumentParser(description="W1-AC3 purity difference control")
    ap.add_argument("--bbg-as-of", required=True)
    args = ap.parse_args()

    s3 = boto3.client("s3")

    # --- the three inputs, read ONCE, read-only ----------------------------
    holdings = json.loads(s3.get_object(Bucket=HOLDINGS[0], Key=HOLDINGS[1])["Body"].read().decode("utf-8"))
    raw = s3.get_object(Bucket=POSITIONING[0], Key=POSITIONING[1])["Body"].read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    positioning = json.loads(raw.decode("utf-8"))
    import pandas as pd
    pq_key = "bbg/%s/characteristics.parquet" % args.bbg_as_of
    mf_key = "bbg/%s/run_manifest.json" % args.bbg_as_of
    frame = pd.read_parquet(io.BytesIO(s3.get_object(Bucket=BBG_BUCKET, Key=pq_key)["Body"].read()))
    manifest = json.loads(s3.get_object(Bucket=BBG_BUCKET, Key=mf_key)["Body"].read().decode("utf-8"))
    print("INPUTS (read once, read-only, handed to BOTH arms):")
    print("  s3://%s/%s  holdings as_of=%s satellites=%d"
          % (HOLDINGS[0], HOLDINGS[1], holdings.get("as_of"), len(holdings.get("satellites") or {})))
    print("  s3://%s/%s  data_as_of=%s" % (POSITIONING[0], POSITIONING[1], positioning.get("data_as_of")))
    print("  s3://%s/%s  rows=%d cols=%d" % (BBG_BUCKET, pq_key, len(frame), len(frame.columns)))
    print("  s3://%s/%s  run_class=%s" % (BBG_BUCKET, mf_key, manifest.get("run_class")))
    print("  as_of (both arms, fixed): %s | bbg_as_of: %s" % (AS_OF, args.bbg_as_of))

    tmp = tempfile.mkdtemp(prefix="w1ac3_head_")
    try:
        head_path = extract_head_tree(tmp)
        head = load_module(head_path, "producer_head")
        work = load_module(PRODUCER_PATH, "producer_work")

        # Each arm indexes the SAME frame with its OWN bbg_index -- so the index is inside the
        # difference, not outside it. The working arm's third return value is the new per-ticker
        # extra map; the first two are compared below as a control on edit (b).
        head_rows, head_coll = head.bbg_index(frame)
        work_rows, work_coll, work_extra = work.bbg_index(frame)
        rows_same = first_difference(head_rows, work_rows) is None
        print("bbg_index row map (the aggregate's input) DEEP-EQUAL across arms: %s  [%d ticker(s)]"
              % (rows_same, len(head_rows)))
        print("bbg_index collisions equal: %s | working arm's SEPARATE extra map: %d ticker(s)"
              % (list(head_coll) == list(work_coll), len(work_extra)))

        head_doc = head.build(holdings, positioning, head_rows, manifest, AS_OF, args.bbg_as_of,
                              bbg_collisions=head_coll)
        # history_loader is NOT passed: the two stripped keys are the only thing it feeds, and
        # a network read inside a purity control would be a second difference between the arms.
        work_doc = work.build(holdings, positioning, work_rows, manifest, AS_OF, args.bbg_as_of,
                              bbg_collisions=work_coll, bbg_extra=work_extra, history_loader=None)

        print("working arm top-level keys: %s" % sorted(work_doc))
        print("HEAD    arm top-level keys: %s" % sorted(head_doc))
        work_stripped = strip_added(work_doc)

        leaves_head = count_leaves(head_doc)
        leaves_work = count_leaves(work_stripped)
        diff = first_difference(head_doc, work_stripped)
        print("LEAF COUNT compared: HEAD %d vs working-stripped %d" % (leaves_head, leaves_work))
        print("DEEP-EQUAL %s" % (diff is None))
        if diff is not None:
            print("FIRST DIFFERENCE: %s" % diff)

        perturbed, what = perturb_one_leaf(work_stripped)
        pdiff = first_difference(head_doc, perturbed)
        print("POSITIVE CONTROL perturbed: %s" % what)
        print("POSITIVE CONTROL DEEP-EQUAL %s" % (pdiff is None))
        print("POSITIVE CONTROL first difference: %s" % pdiff)

        ok = (diff is None) and (pdiff is not None) and rows_same and leaves_head > 200
        print("W1-AC3 %s -- added keys stripped: %s; leaves %d > 200: %s"
              % ("PASS" if ok else "FAIL", list(ADDED_KEYS), leaves_head, leaves_head > 200))
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
