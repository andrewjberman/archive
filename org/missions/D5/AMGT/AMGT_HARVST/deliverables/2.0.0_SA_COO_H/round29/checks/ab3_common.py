"""Shared reads for HVST-ab-3's issuer checks (2.0.0_SA_COO~H): backfill batch 1 -- 10 names x {bbg, wsj, sa} and
Lenovo x {barrons, ft} (AMENDMENTS 1-3). Read-only: S3 LIST/GET, the local outbox, the collector's own `plan`.
"""
import json
import os
import sqlite3
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from lib.opal_data_harvest.harvest_grammar import SOURCE_FOR_PUBLISHER  # noqa: E402
from lib.research.harvest import store  # noqa: E402

HARVST = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST")
UNIVERSE = os.path.join(HARVST, "deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json")
LENOVO_FILE = os.path.join(HARVST, "deliverables/0.9.0_WK_AMGT_HARVST~65/o5_lenovo.security.json")
SEC_DIR = os.path.join(HARVST, "deliverables/2.0.0_SA_COO_H/round29/ab3_securities")
WK = os.path.join(HARVST, "deliverables/0.9.0_WK_AMGT_HARVST~83")
SIGNING = os.path.join(HARVST, "deliverables/2.0.0_SA_COO_H/round29/ab3_signing_before.json")
PLAN_SIGNED = os.path.join(HARVST, "deliverables/2.0.0_SA_COO_H/round29/ab3_plan_signed.json")
RUNTIME = "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest"

# The first 10 rows of aa-5's aa5_plan_190.json, in file order (ab-3 section 1).
NAMES = ["2317_TT_Equity", "2602335D_US_Equity", "9433_JP_Equity", "AAPL_US_Equity", "ABBV_US_Equity", "ABT_US_Equity",
         "ADM_US_Equity", "AEP_US_Equity", "AIG_US_Equity", "AIZ_US_Equity"]
LENOVO = "992_HK_Equity"
NAME_PUBS = ("bbg", "wsj", "sa")
LENOVO_PUBS = ("barrons", "ft")
PUBLISHERS = ("bbg", "wsj", "sa", "barrons", "ft")
FLOOR = "2026-01-01"


def expected_jobs(sa_in=True):
    """{(security_key, publisher)} batch 1 owes; without sa (a persisting 402) only the probe's one sa job remains."""
    pubs = NAME_PUBS if sa_in else ("bbg", "wsj")
    jobs = {(n, p) for n in NAMES for p in pubs}
    if not sa_in:
        jobs.add((NAMES[0], "sa"))
    return jobs | {(LENOVO, p) for p in LENOVO_PUBS}


def security_file(key):
    return LENOVO_FILE if key == LENOVO else os.path.join(SEC_DIR, "%s.security.json" % key)


def write_security_files():
    """One collector security file per batch-1 name, copied VERBATIM from the gold universe row (the o5_lenovo shape)."""
    with open(UNIVERSE, encoding="utf-8") as fh:
        by_key = {s["key"]: s for s in json.load(fh)}
    os.makedirs(SEC_DIR, exist_ok=True)
    for key in NAMES:
        with open(security_file(key), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(by_key[key], fh, indent=2, sort_keys=True)
            fh.write("\n")


def plan(key, publishers):
    """The collector's OWN pre-run print (`plan`, no publisher request): {publisher: planned listing pages}."""
    out = subprocess.run([sys.executable, "-m", "lib.opal_data_harvest", "plan", "--security-json", security_file(key),
                          "--publishers", *publishers, "--floor", FLOOR, "--with-watermark"],
                         capture_output=True, text=True, cwd=ROOT, check=True).stdout
    lines = [json.loads(x) for x in out.splitlines() if x.strip().startswith("{")]
    return {x["publisher"]: {"pages": x["planned_listing_pages"], "bound": x["bound"], "basis": "DEFAULT",
                             "watermark_source": x.get("watermark_source")} for x in lines if "publisher" in x}


def full_plan():
    rows = {}
    for key in NAMES:
        for pub, v in plan(key, NAME_PUBS).items():
            rows["%s|%s" % (key, pub)] = v
    for pub, v in plan(LENOVO, LENOVO_PUBS).items():
        rows["%s|%s" % (LENOVO, pub)] = v
    return rows


def roots():
    out = {}
    for p in PUBLISHERS:
        tp = store.table_prefix(SOURCE_FOR_PUBLISHER[p], "bronze", "x")
        out[p] = tp.split("/harvest/", 1)[0] + "/harvest/"
    out["run_record"] = store.table_prefix("amgt", "bronze", "run_record")
    out["chatter_daily"] = store.table_prefix("amgt", "gold", "chatter_daily")
    out["article_security_mention"] = store.table_prefix("amgt", "gold", "article_security_mention")
    return out


NO_NEW = ("chatter_daily", "article_security_mention")


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
    db = sqlite3.connect("file:%s/progress.sqlite3?mode=ro" % RUNTIME, uri=True)
    out = {}
    for t in ("harvest_raw_outbox", "harvest_listing_outbox"):
        out[t] = db.execute("SELECT publisher, count(*) FROM %s WHERE status='pending' GROUP BY publisher" % t).fetchall()
    return out


def run_records(keys, cl=None):
    cl = cl or store._default_client()
    return [json.loads(cl.get_object(Bucket=store.HARVEST_BUCKET, Key=k)["Body"].read()) for k in keys]


def jobs_by_pair(records):
    """(security_key, publisher) -> the LAST job for that pair across the records (a probe retry supersedes)."""
    out = {}
    for rec in sorted(records, key=lambda r: r.get("started_at") or ""):
        for j in rec.get("jobs") or []:
            out[(j.get("security_key"), j.get("publisher"))] = dict(j, run_id=rec.get("run_id"))
    return out


def listing_pages(records):
    """(security_key, publisher) -> listing requests that returned OK, from the run records' attempt rows (ab-1 A2)."""
    out = {}
    for rec in records:
        for a in rec.get("request_attempts") or []:
            if a.get("request_kind") == "listing" and a.get("class") == "ok":
                k = (a.get("security_key"), a.get("publisher"))
                out[k] = out.get(k, 0) + 1
    return out


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True, default=str)
