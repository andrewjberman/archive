"""Shared reads for HVST-o-5's issuer checks (2.0.0_SA_COO~H). Read-only: S3 LIST and local file reads."""
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from lib.opal_data_harvest.harvest_grammar import SOURCE_FOR_PUBLISHER  # noqa: E402
from lib.research.harvest import store  # noqa: E402

LIVE = ("barrons", "bbg", "ft", "wsj")
CONTROL = ("sa",)
# AMENDMENT 1: attempt 1 ran one job (config jobs_per_run: 1) and barrons was challenged (Branch B, not retried).
# The re-cut runs jobs on bbg, ft and wsj only; barrons joins sa as a root that must gain NO object.
JOB_PUBLISHERS = ("bbg", "ft", "wsj")
NO_NEW = ("sa", "barrons")
# AMENDMENT 2: ft was request_rejected in attempt 2 (Branch B), so it joins the no-write roots; the S3 writer is
# `upload-harvest` over the local outbox, run once after both collection runs.
NO_NEW = ("sa", "barrons", "ft")
WRITE_PUBLISHERS = ("bbg", "wsj")
RUNTIME = "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest"
SECURITY_KEY = "992_HK_Equity"
WK = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~65")
SIGNING_BEFORE = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round25/o5_signing_before.json")


def harvest_root(publisher):
    """'{source}/harvest/' for a publisher, cut from the store's own builder, never typed."""
    tp = store.table_prefix(SOURCE_FOR_PUBLISHER[publisher], "bronze", "x")
    return tp.split("/harvest/", 1)[0] + "/harvest/"


def snapshot(client=None):
    """{publisher: {key: [etag, size]}} for every object under each publisher's harvest root."""
    client = client or store._default_client()
    out = {}
    for publisher in LIVE + CONTROL:
        objs = {}
        paginator = client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=store.HARVEST_BUCKET, Prefix=harvest_root(publisher)):
            for obj in page.get("Contents", []) or []:
                objs[obj["Key"]] = [obj["ETag"].strip('"'), obj["Size"]]
        out[publisher] = objs
    return out


def table_of(key):
    """'<tier>/<table>' from '{source}/harvest/{tier}/{table}/...'."""
    rest = key.split("/harvest/", 1)[1].split("/")
    return "/".join(rest[:2])


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)


def diff(before, after):
    """(moved, removed, new) per publisher: moved = same key, different ETag or size."""
    res = {}
    for publisher in LIVE + CONTROL:
        b, a = before.get(publisher, {}), after.get(publisher, {})
        moved = sorted(k for k in b if k in a and a[k] != b[k])
        removed = sorted(k for k in b if k not in a)
        new = sorted(k for k in a if k not in b)
        res[publisher] = (moved, removed, new)
    return res


def counts(snap):
    return {p: len(snap.get(p, {})) for p in LIVE + CONTROL}
