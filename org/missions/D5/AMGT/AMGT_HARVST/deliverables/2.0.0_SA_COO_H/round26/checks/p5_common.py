"""Shared reads for HVST-p-5's issuer checks (2.0.0_SA_COO~H). Read-only: S3 LIST/GET and the local outbox."""
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1_common as c  # noqa: E402

from lib.opal_data_harvest.harvest_grammar import SOURCE_FOR_PUBLISHER  # noqa: E402
from lib.research.harvest import store  # noqa: E402

WRITE = ("bbg", "wsj")
NO_NEW = ("barrons", "ft", "sa")
LENOVO = "992_HK_Equity"
RUNTIME = "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest"
WK = os.path.join(c.ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~70")
SIGNING = os.path.join(c.ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round26/p5_signing_before.json")


def roots():
    """{label: prefix} -- the five publisher harvest roots, the run-record table, and chatter_daily; all builder output."""
    out = {}
    for p in WRITE + NO_NEW:
        tp = store.table_prefix(SOURCE_FOR_PUBLISHER[p], "bronze", "x")
        out[p] = tp.split("/harvest/", 1)[0] + "/harvest/"
    out["run_record"] = store.table_prefix("amgt", "bronze", "run_record")
    out["chatter_daily"] = store.table_prefix("amgt", "gold", "chatter_daily")
    return out


def snapshot(cl=None):
    cl = cl or store._default_client()
    snap = {}
    for label, prefix in roots().items():
        objs = {}
        for page in cl.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
            for obj in page.get("Contents", []) or []:
                objs[obj["Key"]] = [obj["ETag"].strip('"'), obj["Size"]]
        snap[label] = objs
    return snap


def diff(before, after):
    res = {}
    for label in before:
        b, a = before[label], after.get(label, {})
        res[label] = (sorted(k for k in b if k in a and a[k] != b[k]), sorted(k for k in b if k not in a),
                      sorted(k for k in a if k not in b))
    return res


def outbox_pending():
    db = sqlite3.connect(os.path.join(RUNTIME, "progress.sqlite3"))
    out = {}
    for t in ("harvest_raw_outbox", "harvest_listing_outbox"):
        out[t] = db.execute("SELECT publisher, count(*) FROM %s WHERE status='pending' GROUP BY publisher" % t).fetchall()
    return out
