"""AMGT_CORPUS round 26 CRPS-ab-4 leg c -- capture, then compare (the aa-4 method, over the 18 moving keys). The issuer's file; run as a
named script with python -u.

  python -u c26.py capture <dir> <store_key>...   BEFORE the act: the producer's own stage_derive with a write-capturing client
                                                  saves each expected block and the served predecessor's key
  python -u c26.py compare <dir> <store_key>...   AFTER the act: the newest served block of each key must EQUAL its captured
                                                  expected block with every `vintage` stripped
  -> 'c26 keys K new_stamps S equal_dry_run E value_moves V case_value_moves C'
"""
import importlib.util
import json
import os
import subprocess
import sys

import boto3

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
B = "opal-data-harvest"
WRITES = {"put_object", "copy_object", "delete_object", "delete_objects", "upload_file", "upload_fileobj"}


class Capture:
    def __init__(self, real):
        self._real = real
        self.captured = []

    def __getattr__(self, name):
        if name in WRITES:
            def cap(*a, **kw):
                body = kw.get("Body")
                self.captured.append((name, kw.get("Key"), body.read() if hasattr(body, "read") else body))
                return {"ETag": '"dry-run"'}
            return cap
        return getattr(self._real, name)


def strip_vintage(x):
    if isinstance(x, dict):
        return {q: strip_vintage(w) for q, w in x.items() if q != "vintage"}
    if isinstance(x, list):
        return [strip_vintage(w) for w in x]
    return x


def fkey(f):
    return (f.get("mnemonic"), f.get("scope"), f.get("fiscal_period"), f.get("fiscal_year"), f.get("period_end_date"),
            f.get("override"))


def newest(s3, k):
    st = []
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix="derived/model_block/%s/" % k):
        st += [o["Key"] for o in pg.get("Contents", []) if o["Key"].endswith("/model_block.json")]
    return sorted(st)[-1]


mode, d, keys = sys.argv[1], sys.argv[2], sys.argv[3:]
s3 = boto3.client("s3")
if mode == "capture":
    spec = importlib.util.spec_from_file_location("mbp_c26", os.path.join(RES, "model_block_pull.py"))
    mbp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mbp)
    os.makedirs(d, exist_ok=True)
    for k in keys:
        pred = newest(s3, k)
        sec = json.loads(s3.get_object(Bucket=B, Key=pred)["Body"].read()).get("security")
        cap = Capture(s3)
        mbp.stage_derive(cap, sec, raw_stamp=None, sa_fallback=False)
        blocks = [b for op, key, b in cap.captured if op == "put_object" and str(key).endswith("/model_block.json")]
        assert len(cap.captured) == 1 and len(blocks) == 1, (k, [c[:2] for c in cap.captured])
        open(os.path.join(d, k + ".expected.json"), "wb").write(blocks[0] if isinstance(blocks[0], bytes) else blocks[0].encode())
        open(os.path.join(d, k + ".pred.txt"), "w").write(pred + "\n" + sec + "\n")
        print("CAPTURED %s %s predecessor %s" % (k, sec, pred.split("/")[-2]), flush=True)
else:
    new_stamps = equal = vmoves = cmoves = 0
    for k in keys:
        pred, _sec = open(os.path.join(d, k + ".pred.txt")).read().split("\n")[:2]
        exp = json.load(open(os.path.join(d, k + ".expected.json"), encoding="utf-8"))
        cur_key = newest(s3, k)
        if cur_key <= pred:
            print("MISMATCH %s no new stamp" % k)
            continue
        new_stamps += 1
        cur = json.loads(s3.get_object(Bucket=B, Key=cur_key)["Body"].read())
        old = json.loads(s3.get_object(Bucket=B, Key=pred)["Body"].read())
        eq = json.dumps(strip_vintage(cur), sort_keys=True, default=str) == json.dumps(strip_vintage(exp), sort_keys=True, default=str)
        equal += int(eq)
        of = {fkey(f): f for f in old["figures"]}
        v = sum(1 for f in cur["figures"] if fkey(f) in of and json.dumps(of[fkey(f)].get("value")) != json.dumps(f.get("value")))
        vmoves += v
        ov = ((old.get("cases") or {}).get("base") or {}).get("value")
        nv = ((cur.get("cases") or {}).get("base") or {}).get("value")
        cmoves += int(ov != nv)
        if not eq or v:
            print("MISMATCH %s equal_dry_run %s value_moves %d" % (k, eq, v))
    print("c26 keys %d new_stamps %d equal_dry_run %d value_moves %d case_value_moves %d" % (len(keys), new_stamps, equal, vmoves,
                                                                                            cmoves))
