"""AMGT_CORPUS round 27 CRPS-ac-2 leg v -- the served census over the newest block of every key, plus the CTO's negative arm.
Read-only. The issuer's file; run as a named script with python -u.

  -> 'UNIT <class> <n>' per unit-head class over every figure of the newest block of each key
  -> 'ARM TSM CURR_ENTP_VAL <heads>' and 'ARM BA EQY_DPS unit_equal_predecessor <bool>'
  -> 'v27 keys K figures F unresolved U zero_dominated Z'
"""
import collections
import json

import boto3

B = "opal-data-harvest"
P = "derived/model_block/"


def head(u):
    s = str(u)
    if s == "None":
        return "None"
    if s.startswith("UNRESOLVED"):
        return "UNRESOLVED"
    if s.startswith("ZERO-DOMINATED"):
        return "ZERO-DOMINATED"
    return s.split(":", 1)[0].split(" (", 1)[0]


s3 = boto3.client("s3")
stamps = collections.defaultdict(list)
for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix=P):
    for o in pg.get("Contents", []):
        rest = o["Key"][len(P):]
        if rest.endswith("/model_block.json"):
            k = rest.rsplit("/", 2)[0]
            if "/" not in k:
                stamps[k].append(o["Key"])
units = collections.Counter()
figs = 0
for k in sorted(stamps):
    blk = json.loads(s3.get_object(Bucket=B, Key=max(stamps[k]))["Body"].read())
    for f in blk.get("figures", []):
        figs += 1
        units[head(f.get("unit"))] += 1
for u, n in sorted(units.items()):
    if u in ("UNRESOLVED", "ZERO-DOMINATED"):
        print("UNIT %s %d" % (u, n))


def figs_of(key, idx):
    ks = sorted(stamps[key])
    blk = json.loads(s3.get_object(Bucket=B, Key=ks[idx])["Body"].read())
    return blk, ks[idx]


tsm, _ = figs_of("TSM_US_Equity", -1)
print("ARM TSM CURR_ENTP_VAL %s" % sorted({head(f.get("unit")) for f in tsm["figures"] if f.get("mnemonic") == "CURR_ENTP_VAL"}))
ba, ba_key = figs_of("BA_US_Equity", -1)
ba_units = sorted((str(f.get("fiscal_year")), str(f.get("unit"))) for f in ba["figures"] if f.get("mnemonic") == "EQY_DPS")
bb3, _ = figs_of("BBSE3_BZ_Equity", -2)
bb3n, _ = figs_of("BBSE3_BZ_Equity", -1)
# BA was not re-derived in round 27: its newest stamp must predate the act; the dividend unit is read from the served block
print("ARM BA EQY_DPS newest_stamp %s units %s" % (ba_key.split("/")[-2], sorted({u for _, u in ba_units})))
print("ARM BBSE3 CAPITAL_EXPEND units %s -> %s" % (
    sorted({head(f.get("unit")) for f in bb3["figures"] if f.get("mnemonic") == "CAPITAL_EXPEND"}),
    sorted({head(f.get("unit")) for f in bb3n["figures"] if f.get("mnemonic") == "CAPITAL_EXPEND"})))
print("v27 keys %d figures %d unresolved %d zero_dominated %d" % (len(stamps), figs, units["UNRESOLVED"], units["ZERO-DOMINATED"]))
