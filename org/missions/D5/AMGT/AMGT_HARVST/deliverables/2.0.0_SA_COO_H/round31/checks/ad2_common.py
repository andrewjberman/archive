"""Shared reads for HVST-ad-2's issuer checks (2.0.0_SA_COO~H): sa batch 1 on 10 names from the collector's RESOLVED
universe, one `run --no-sign-in` per name, stop at the first challenge. Read-only: S3 LIST/GET, the local outbox, the
collector's own `plan`."""
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
SEC_DIR = os.path.join(HARVST, "deliverables/2.0.0_SA_COO_H/round31/ad2_securities")
WK = os.path.join(HARVST, "deliverables/0.9.0_WK_AMGT_HARVST~88")
SIGNING = os.path.join(HARVST, "deliverables/2.0.0_SA_COO_H/round31/ad2_signing_before.json")
PLAN_SIGNED = os.path.join(HARVST, "deliverables/2.0.0_SA_COO_H/round31/ad2_plan_signed.json")
RUNTIME = "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest"
FLOOR = "2026-01-01"
N = 10
STOP_STATUSES = ("bot_check", "unclassified", "account_or_harvester_unavailable", "sign_in_refused", "throttled")
OTHER_PUBLISHERS = ("bbg", "wsj", "barrons", "ft")


def names():
    """The first N rows of the collector's resolved universe, in order (each carries a sa_symbol)."""
    from lib.opal_data_harvest.__main__ import universe
    with open(os.path.join(ROOT, "lib/opal_data_harvest/config.json"), encoding="utf-8") as fh:
        cfg = json.load(fh)
    rows = [r for r in universe(cfg) if r.get("sa_symbol")][:N]
    return rows


def security_file(key):
    return os.path.join(SEC_DIR, "%s.security.json" % key)


def write_security_files():
    os.makedirs(SEC_DIR, exist_ok=True)
    for r in names():
        with open(security_file(r["key"]), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(r, fh, indent=2, sort_keys=True)
            fh.write("\n")


def plan():
    out = {}
    for r in names():
        text = subprocess.run([sys.executable, "-m", "lib.opal_data_harvest", "plan", "--security-json",
                               security_file(r["key"]), "--publishers", "sa", "--floor", FLOOR, "--with-watermark"],
                              capture_output=True, text=True, cwd=ROOT, check=True).stdout
        for line in text.splitlines():
            if line.strip().startswith("{"):
                x = json.loads(line)
                if x.get("publisher") == "sa":
                    out[r["key"]] = {"sa_symbol": r["sa_symbol"], "pages": x["planned_listing_pages"],
                                     "bound": x["bound"], "basis": "DEFAULT"}
    return out


def roots():
    out = {}
    for p in ("sa",) + OTHER_PUBLISHERS:
        out[p] = store.table_prefix(SOURCE_FOR_PUBLISHER[p], "bronze", "x").split("/harvest/", 1)[0] + "/harvest/"
    out["run_record"] = store.table_prefix("amgt", "bronze", "run_record")
    out["chatter_daily"] = store.table_prefix("amgt", "gold", "chatter_daily")
    out["article_security_mention"] = store.table_prefix("amgt", "gold", "article_security_mention")
    return out


NO_NEW = OTHER_PUBLISHERS + ("chatter_daily", "article_security_mention")


def snapshot(cl=None):
    cl = cl or store._default_client()
    snap = {}
    for label, prefix in roots().items():
        objs = {}
        for page in cl.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
            for o in page.get("Contents", []) or []:
                objs[o["Key"]] = [o["ETag"].strip('"'), o["Size"]]
        snap[label] = objs
    return snap


def diff(before, after):
    return {label: (sorted(k for k in b if k in after.get(label, {}) and after[label][k] != b[k]),
                    sorted(k for k in b if k not in after.get(label, {})),
                    sorted(k for k in after.get(label, {}) if k not in b)) for label, b in before.items()}


def outbox_pending():
    db = sqlite3.connect("file:%s/progress.sqlite3?mode=ro" % RUNTIME, uri=True)
    return {t: db.execute("SELECT publisher, count(*) FROM %s WHERE status='pending' GROUP BY publisher" % t).fetchall()
            for t in ("harvest_raw_outbox", "harvest_listing_outbox")}


def run_records(keys, cl=None):
    cl = cl or store._default_client()
    return [json.loads(cl.get_object(Bucket=store.HARVEST_BUCKET, Key=k)["Body"].read()) for k in keys]


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True, default=str)
