"""AMGT_CORPUS round 33 CRPS-ai-2 leg v -- the served census over the newest block of every key, beside the negative arms and the
CTO half's per-family served figures (msg 28595). Read-only. The issuer's file; run as a named script with python -u.

  python -u v33.py snapshot <file>   BEFORE the act: the newest stamp of every key and the UNRESOLVED-unit count
  python -u v33.py census <file>     AFTER: DECIMAL / UNRESOLVED unit counts, the keys whose newest stamp moved, value moves on them,
                                     the negative arms and one served figure per series-median family
  -> 'v33 keys K figures F decimal D unresolved_before UB unresolved_after UA moved_keys M value_moves V'
"""
import collections
import json
import sys

import boto3

B = "opal-data-harvest"
P = "derived/model_block/"
SECS = {"HEI_US_Equity", "MELI_US_Equity", "PWR_US_Equity", "JD_US_Equity", "ORA_FP_Equity", "RWE_GR_Equity",
        "BP-SLASH-_LN_Equity", "AZN_LN_Equity", "RKT_LN_Equity", "TTE_FP_Equity", "ULVR_LN_Equity"}


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


def unresolved(u):
    return str(u or "").startswith(("UNRESOLVED", "ZERO-DOMINATED", "SEE field_map"))


def census(s3, stamps):
    dec = collections.Counter()
    unres = 0
    figs = 0
    blocks = {}
    for k in sorted(stamps):
        blk = json.loads(s3.get_object(Bucket=B, Key=stamps[k])["Body"].read())
        blocks[k] = blk
        for f in blk.get("figures", []):
            figs += 1
            if str(f.get("unit") or "").startswith("DECIMAL"):
                dec[f.get("mnemonic")] += 1
            if unresolved(f.get("unit")):
                unres += 1
    return dec, unres, figs, blocks


mode, path = sys.argv[1], sys.argv[2]
s3 = boto3.client("s3")
now = newest_all(s3)
if mode == "snapshot":
    dec, unres, figs, _ = census(s3, now)
    json.dump({"stamps": now, "unresolved": unres, "decimal": sum(dec.values()), "figures": figs},
              open(path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print("SNAPSHOT keys %d figures %d decimal %d unresolved %d -> %s" % (len(now), figs, sum(dec.values()), unres, path))
    sys.exit(0)
pre = json.load(open(path, encoding="utf-8"))
before = pre["stamps"]
dec, unres, figs, blocks = census(s3, now)
for m, n in sorted(dec.items()):
    print("DECIMAL %s %d" % (m, n))
moved = [k for k in sorted(now) if now[k] != before.get(k)]
vmoves = 0
for k in moved:
    print("MOVED %s %s -> %s" % (k, str(before.get(k)).split("/")[-2], now[k].split("/")[-2]))
    old = json.loads(s3.get_object(Bucket=B, Key=before[k])["Body"].read())
    of = {fkey(f): f for f in old.get("figures", [])}
    vmoves += sum(1 for f in blocks[k]["figures"]
                  if fkey(f) in of and json.dumps(of[fkey(f)].get("value")) != json.dumps(f.get("value")))
ba = sorted({str(f.get("unit")) for f in blocks["BA_US_Equity"]["figures"] if f.get("mnemonic") == "BEST_DIV_YLD"})
print("ARM BA BEST_DIV_YLD units %s stamp_moved %s" % (ba, "BA_US_Equity" in moved))
print("ARM outside-the-11 stamps moved: %d of %d" % (len([k for k in moved if k not in SECS]), len(now) - len(SECS & set(now))))
print("ARM DECIMAL-confirmed (a ground confirms DECIMAL): count %d (named empty in both halves)" % sum(dec.values()))
for k, m in (("ORA_FP_Equity", "RETURN_ON_INV_CAPITAL"), ("BP-SLASH-_LN_Equity", "RETURN_COM_EQY"), ("JD_US_Equity", "OPER_MARGIN")):
    fs = sorted((f for f in blocks[k]["figures"] if f.get("mnemonic") == m), key=lambda f: str(f.get("fiscal_year")))
    f = fs[-1] if fs else {}
    print("FAMILY %s %s FY%s value %s unit %s" % (k, m, f.get("fiscal_year"), f.get("value"), f.get("unit")))
print("v33 keys %d figures %d decimal %d unresolved_before %d unresolved_after %d moved_keys %d value_moves %d" % (
    len(now), figs, sum(dec.values()), pre["unresolved"], unres, len(moved), vmoves))
