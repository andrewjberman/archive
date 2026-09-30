"""AMGT_CORPUS round 23 -- the expected diff of the SIGN re-derive (VERDICT B), read from the merged reader: each figure of the newest
served block of the 97 y-4 names, resolved through model_block_pull's own _resolved_sign / _resolved_unit with the committed map,
against the served labels. Read-only (S3 reads). The issuer's file.

  python y6_measure.py <pass_keys_file>
  -> one 'BLOCK <key> sign_changes S unit_changes U new_sign_contradicts_value C' per block with S>0 or U>0
  -> 'y6 blocks N move_blocks M sign_changes S unit_changes U new_sign_contradicts_value C served_plain_disagree P'
"""
import importlib.util
import json
import os
import subprocess
import sys

import boto3

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
spec = importlib.util.spec_from_file_location("mbp_y6", os.path.join(TOP, "integrations", "bloomberg", "research", "model_block_pull.py"))
mbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mbp)


def own(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    return "POSITIVE" if v > 0 else ("NEGATIVE" if v < 0 else "ZERO")


def contradicts(label, value):
    o = own(value)
    head = str(label).split(" ", 1)[0]
    return o is not None and head in ("POSITIVE", "NEGATIVE", "ZERO") and head != o


keys = open(sys.argv[1]).read().split()
s3 = boto3.client("s3")
B = "opal-data-harvest"
S = U = C = P = moving = 0
for k in keys:
    st = sorted(o["Key"] for o in s3.list_objects_v2(Bucket=B, Prefix="derived/model_block/%s/" % k).get("Contents", [])
                if o["Key"].endswith("model_block.json"))
    blk = json.loads(s3.get_object(Bucket=B, Key=st[-1])["Body"].read())
    sec = blk.get("security")
    s = u = c = 0
    for f in blk.get("figures", []):
        ns = mbp._resolved_sign(f.get("mnemonic"), sec, f.get("value"))
        nu = mbp._resolved_unit(f.get("mnemonic"), sec)
        s += int(ns != f.get("sign"))
        u += int(nu != f.get("unit"))
        c += int(contradicts(ns, f.get("value")))
        P += int(contradicts(f.get("sign"), f.get("value")))
    S += s
    U += u
    C += c
    moving += int(s > 0 or u > 0)
    if s or u:
        print("BLOCK %s sign_changes %d unit_changes %d new_sign_contradicts_value %d" % (k, s, u, c))
print("y6 blocks %d move_blocks %d sign_changes %d unit_changes %d new_sign_contradicts_value %d served_plain_disagree %d" % (
    len(keys), moving, S, U, C, P))
