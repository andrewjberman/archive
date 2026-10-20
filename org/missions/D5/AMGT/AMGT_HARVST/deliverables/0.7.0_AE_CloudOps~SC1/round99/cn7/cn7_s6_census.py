"""cn-7 stage 6 independent read (read only): expected-written census from the model-block pool, and
read-back of every written dossier against the gateway's pick rule. ASCII only."""
import datetime as dt
import gzip
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor

import boto3

LOG = sys.argv[1]
BUCKET = "opal-data-harvest"
BLOCK_PREFIX = "derived/model_block/"
DOSSIER_PREFIX = "amgt/harvest/gold/research_dossier/"
BOUNDARY = dt.datetime(2026, 10, 20, 13, 0, 0, tzinfo=dt.timezone.utc)  # 09:00 America/New_York (EDT, UTC-4)
AS_OF_RE = re.compile(r"as_of=(\d{4}-\d{2}-\d{2})\.")

s3 = boto3.client("s3", region_name="us-east-1")

rows = {}
for line in open(LOG, encoding="ascii", errors="replace"):
    m = re.match(r"REFRESH (\S+) status=(\S+) .*?guard=(\S+)", line)
    if m:
        w = re.search(r"wrote (s3://\S+)", line)
        rows[m.group(1)] = {"status": m.group(2), "guard": m.group(3), "wrote": w.group(1) if w else None}
print("names in log:", len(rows))


def safe(k):
    return k.replace("/", "-SLASH-")


def listing(prefix):
    out = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
        out.extend(page.get("Contents", []) or [])
    return out


def newest_block(k):
    base = BLOCK_PREFIX + safe(k) + "/"
    stamps = []
    for o in listing(base):
        if o["Key"].endswith("/model_block.json"):
            stamps.append(o["Key"][len(base):-len("/model_block.json")])
    return max(stamps) if stamps else None


def pick(k):
    objs = [o for o in listing(DOSSIER_PREFIX + "security_key=" + safe(k) + "/") if o["Key"].endswith((".json", ".json.gz"))]
    by = {}
    for o in objs:
        m = AS_OF_RE.search(o["Key"])
        if m:
            by.setdefault(m.group(1), []).append(o)
    if not by:
        return None, None
    stamp = max(by)
    best = max(by[stamp], key=lambda o: (o["LastModified"].isoformat(), o["Key"]))
    return best["Key"], stamp


def check(k):
    r = rows[k]
    stamp = newest_block(k)
    today = bool(stamp) and dt.datetime.strptime(stamp, "%Y%m%dT%H%M%SZ").replace(tzinfo=dt.timezone.utc) > BOUNDARY
    res = {"name": k, "newest_block": stamp, "block_today": today, "status": r["status"]}
    if r["status"] == "WRITTEN":
        key = r["wrote"][len("s3://" + BUCKET + "/"):]
        body = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
        if key.endswith(".gz"):
            body = gzip.decompress(body)
        doc = json.loads(body.decode("utf-8"))
        picked, stamp_as_of = pick(k)
        res.update({"parses": isinstance(doc, dict), "as_of_ok": stamp_as_of == "2026-10-20", "pick_is_new": picked == key,
                    "key": key})
    return res


with ThreadPoolExecutor(8) as ex:
    results = list(ex.map(check, sorted(rows)))

expected = [r for r in results if r["block_today"]]
written = [r for r in results if r["status"] == "WRITTEN"]
guard = [r for r in results if r["status"] == "SKIPPED_GUARD"]
print("names with newest model block later than 2026-10-20T13:00:00Z (09:00 ET): %d of %d" % (len(expected), len(results)))
print("written: %d | skipped_guard: %d" % (len(written), len(guard)))
print("written names whose newest block is NOT today:", [r["name"] for r in written if not r["block_today"]])
print("today-block names not written:", [(r["name"], r["status"]) for r in expected if r["status"] != "WRITTEN"])
print("not-today-block names:", [(r["name"], r["newest_block"]) for r in results if not r["block_today"]])
ok = [r for r in written if r["parses"] and r["as_of_ok"] and r["pick_is_new"]]
print("samples_ok=%d of %d (all written names read back: parses, as_of=2026-10-20, gateway pick == the new object)" % (len(ok), len(written)))
for r in written:
    if not (r["parses"] and r["as_of_ok"] and r["pick_is_new"]):
        print("SAMPLE FAIL", r)
bp = [r for r in results if r["name"] == "BP/_LN_Equity"]
print("BP/_LN_Equity:", bp)
