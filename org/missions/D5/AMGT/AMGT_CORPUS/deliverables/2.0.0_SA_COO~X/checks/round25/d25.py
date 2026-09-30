"""AMGT_CORPUS round 25 aa-2 served act, leg d -- the dossier refresh of the 21 moving names that have a dossier, and its verify read
from S3 (never from the writer's log). The issuer's file; run as a named script with python -u (round-24 ruling 2).

  python -u d25.py write            -> 'DOSSIER <key> wrote <bool> uri <uri>' per name; 'LEG-D names N wrote W unchanged U errors E'
  python -u d25.py structure <T>    -> exactly one new object per name since T (UTC ISO), changed document keys, other names written
  python -u d25.py inputs           -> inputs_equal_now per name, 8 threads
"""
import collections
import concurrent.futures
import datetime
import json
import os
import sys

import boto3

from lib.research.corpus import dossier

KEYS = ("1299_HK_Equity 939_HK_Equity 992_HK_Equity AZN_LN_Equity BABA_US_Equity BA_US_Equity BZLFY_US_Equity HSBA_LN_Equity "
        "ICT_PM_Equity JD_US_Equity NOVN_SW_Equity PBR_US_Equity RIO_LN_Equity SHOP_CN_Equity SPOT_US_Equity TSM_US_Equity "
        "TTE_FP_Equity UBSG_SW_Equity ULVR_LN_Equity UNVGY_US_Equity ZURN_SW_Equity").split()  # the 22 minus 6861_JP (no dossier)
# CRPS-aa-4: D25_KEYS (comma list of IDENTITY keys, e.g. BP/_LN_Equity) replaces the list.
if os.environ.get("D25_KEYS"):
    KEYS = os.environ["D25_KEYS"].split(",")
B = "opal-data-harvest"
P = "amgt/harvest/gold/research_dossier/"


def listing(s3):
    objs = collections.defaultdict(list)
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix=P):
        for o in pg.get("Contents", []):
            # the gold partition is slash-safe; decode it to the identity the KEYS carry
            objs[o["Key"][len(P):].split("/")[0].split("=", 1)[1].replace("-SLASH-", "/")].append(o)
    return objs


def write():
    c = boto3.client("s3")
    wrote = unchanged = errors = 0
    for k in KEYS:
        try:
            r = dossier.write_one(k, client=c)
            wrote += int(bool(r.get("wrote")))
            unchanged += int(not r.get("wrote"))
            print("DOSSIER %s wrote %s uri %s" % (k, r.get("wrote"), r.get("uri")), flush=True)
        except Exception as e:  # one name's failure is reported, never swallowed
            errors += 1
            print("ERROR: %s %s: %s" % (k, type(e).__name__, e), flush=True)
    print("LEG-D names %d wrote %d unchanged %d errors %d" % (len(KEYS), wrote, unchanged, errors))


def structure(t_iso):
    s3 = boto3.client("s3")
    T = datetime.datetime.strptime(t_iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    objs = listing(s3)
    others = sorted(k for k, lst in objs.items() if k not in KEYS and any(o["LastModified"] > T for o in lst))
    one_new = 0
    changed = collections.Counter()
    for k in KEYS:
        lst = sorted(objs[k], key=lambda o: o["LastModified"])
        new = [o for o in lst if o["LastModified"] > T]
        old = [o for o in lst if o["LastModified"] <= T]
        one_new += int(len(new) == 1)
        if len(new) != 1 or not old:
            print("BAD %s new_objects %d predecessors %d" % (k, len(new), len(old)), flush=True)
            continue
        dc = json.loads(s3.get_object(Bucket=B, Key=new[0]["Key"])["Body"].read())
        dp = json.loads(s3.get_object(Bucket=B, Key=old[-1]["Key"])["Body"].read())
        dc, dp = dc.get("document", dc), dp.get("document", dp)
        for q in set(dc) | set(dp):
            if json.dumps(dc.get(q), sort_keys=True, default=str) != json.dumps(dp.get(q), sort_keys=True, default=str):
                if q == "fields" and isinstance(dc.get(q), dict) and isinstance(dp.get(q), dict):
                    for r in set(dc[q]) | set(dp[q]):
                        if json.dumps(dc[q].get(r), sort_keys=True, default=str) != json.dumps(dp[q].get(r), sort_keys=True,
                                                                                               default=str):
                            changed["fields." + r] += 1
                else:
                    changed[q] += 1
    print("DOSSIER-CHANGED-KEYS %s" % dict(changed))
    print("LEG-D-STRUCTURE names %d exactly_one_new %d other_names_written %d %s" % (len(KEYS), one_new, len(others), others))


def inputs():
    objs = listing(boto3.client("s3"))

    def one(k):
        newest = sorted(objs[k], key=lambda o: o["LastModified"])[-1]
        doc = json.loads(boto3.client("s3").get_object(Bucket=B, Key=newest["Key"])["Body"].read())
        doc = doc.get("document", doc)
        return k, dossier.current_inputs(k, client=boto3.client("s3")) == doc.get("inputs")

    eq = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for k, e in ex.map(one, KEYS):
            eq += int(e)
            print("INPUTS %s equal_now %s" % (k, e), flush=True)
    print("LEG-D-INPUTS names %d inputs_equal_now %d" % (len(KEYS), eq))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "write":
        write()
    elif mode == "structure":
        structure(sys.argv[2])
    else:
        inputs()
