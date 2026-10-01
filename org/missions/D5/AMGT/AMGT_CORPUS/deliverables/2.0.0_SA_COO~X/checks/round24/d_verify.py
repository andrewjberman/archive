"""AMGT_CORPUS round 24 z-1 served act, leg d verify -- the dossier refresh, read from S3 (never from the writers' logs).
Read-only. The issuer's file.

  python d_verify.py structure   -> per-name new-object count + the document keys that changed vs the predecessor dossier
  python d_verify.py inputs      -> inputs_equal_now per name (dossier.current_inputs vs the newest stored inputs), 8 threads
"""
import collections
import concurrent.futures
import datetime
import json
import sys

import boto3

from lib.research.corpus import dossier

KEYS = ("2317_TT_Equity 8035_JP_Equity 8306_JP_Equity 8316_JP_Equity 8766_JP_Equity 939_HK_Equity 9433_JP_Equity "
        "ICICIBC_IN_Equity TSM_US_Equity ADBE_US_Equity AMD_US_Equity BA_US_Equity CDNS_US_Equity CELH_US_Equity "
        "IDXX_US_Equity ISRG_US_Equity MELI_US_Equity MNST_US_Equity NFLX_US_Equity NOW_US_Equity NU_US_Equity "
        "QXO_US_Equity SHOP_CN_Equity SNPS_US_Equity SPOT_US_Equity UBER_US_Equity WDAY_US_Equity").split()
B = "opal-data-harvest"
P = "amgt/harvest/gold/research_dossier/"
T = datetime.datetime(2026, 9, 30, 12, 44, tzinfo=datetime.timezone.utc)
s3 = boto3.client("s3")


def listing():
    objs = collections.defaultdict(list)
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix=P):
        for o in pg.get("Contents", []):
            objs[o["Key"][len(P):].split("/")[0].split("=", 1)[1]].append(o)
    return objs


def structure():
    objs = listing()
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
                changed[q] += 1
    print("DOSSIER-CHANGED-KEYS %s" % dict(changed))
    print("LEG-D-STRUCTURE names %d exactly_one_new %d other_names_written %d %s" % (len(KEYS), one_new, len(others), others))


def inputs():
    objs = listing()

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


{"structure": structure, "inputs": inputs}[sys.argv[1]]()
