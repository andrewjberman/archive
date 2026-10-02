"""AMGT_CORPUS round 32 CRPS-ah-3 leg v -- the served census over the newest block of every key, plus the negative arms.
Read-only. The issuer's file; run as a named script with python -u.

  python -u v32.py snapshot <file>   BEFORE the act: the newest stamp of every key
  python -u v32.py census <file>     AFTER: DECIMAL counts by mnemonic, value equality against the snapshot's blocks for every
                                     moved key, the keys whose newest stamp moved, and the negative arms
  -> 'DECIMAL <mnemonic> <n>' per mnemonic; 'MOVED <key> <old stamp> -> <new stamp>'; 'ARM ...'
  -> 'v32 keys K figures F best_div_yld_decimal B eqy_dvd_yld_ind_decimal E moved_keys M value_moves V'
"""
import collections
import json
import sys

import boto3

B = "opal-data-harvest"
P = "derived/model_block/"


def newest_all(s3):
    stamps = collections.defaultdict(list)
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix=P):
        for o in pg.get("Contents", []):
            rest = o["Key"][len(P):]
            if rest.endswith("/model_block.json"):
                k = rest.rsplit("/", 2)[0]
                if "/" not in k:
                    stamps[k].append(o["Key"])
    return {k: max(v) for k, v in stamps.items()}


def fkey(f):
    return (f.get("mnemonic"), f.get("scope"), f.get("fiscal_period"), f.get("fiscal_year"), f.get("period_end_date"),
            f.get("override"))


mode, path = sys.argv[1], sys.argv[2]
s3 = boto3.client("s3")
now = newest_all(s3)
if mode == "snapshot":
    json.dump(now, open(path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print("SNAPSHOT keys %d -> %s" % (len(now), path))
    sys.exit(0)
before = json.load(open(path, encoding="utf-8"))
dec = collections.Counter()
figs = vmoves = 0
blocks = {}
for k in sorted(now):
    blk = json.loads(s3.get_object(Bucket=B, Key=now[k])["Body"].read())
    blocks[k] = blk
    for f in blk.get("figures", []):
        figs += 1
        if str(f.get("unit") or "").startswith("DECIMAL"):
            dec[f.get("mnemonic")] += 1
for m, n in sorted(dec.items()):
    print("DECIMAL %s %d" % (m, n))
moved = [k for k in sorted(now) if now[k] != before.get(k)]
for k in moved:
    print("MOVED %s %s -> %s" % (k, str(before.get(k)).split("/")[-2], now[k].split("/")[-2]))
    if before.get(k):
        old = json.loads(s3.get_object(Bucket=B, Key=before[k])["Body"].read())
        of = {fkey(f): f for f in old.get("figures", [])}
        vmoves += sum(1 for f in blocks[k]["figures"]
                      if fkey(f) in of and json.dumps(of[fkey(f)].get("value")) != json.dumps(f.get("value")))
hei = sorted({str(f.get("unit"))[:7] for f in blocks["HEI_US_Equity"]["figures"] if f.get("mnemonic") == "EQY_DVD_YLD_IND"})
jd = sorted({str(f.get("unit")) for f in blocks["JD_US_Equity"]["figures"] if f.get("mnemonic") == "OPER_MARGIN"})
print("ARM HEI EQY_DVD_YLD_IND units %s" % hei)
print("ARM JD OPER_MARGIN units %s stamp_moved %s" % ([u[:40] for u in jd], "JD_US_Equity" in moved))
print("v32 keys %d figures %d best_div_yld_decimal %d eqy_dvd_yld_ind_decimal %d moved_keys %d value_moves %d" % (
    len(now), figs, dec["BEST_DIV_YLD"], dec["EQY_DVD_YLD_IND"], len(moved), vmoves))
