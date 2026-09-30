"""AMGT_CORPUS round 25, CRPS-aa-3 -- the worker's class table of the still-UNRESOLVED served units, checked against a measurement
this checker makes itself: the served count over the newest block of every key EXCEPT the slash-bearing keys (EXCLUDED,
Z-S64), and the count the round's builder PROJECTS (a rebuild into a TEMP copy of the committed map, each figure resolved through
the reader). Read-only on S3; the committed map is never written. The issuer's file.

  -> 'aa3 keys K excluded E measured_before M table_total T classes C dispositions_complete D projected_after P
      table_remaining R consistent True|False'
"""
import importlib.util
import io
import json
import os
import shutil
import subprocess
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

import boto3

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
TABLE = os.path.join(TOP, "org/missions/D5/AMGT/AMGT_CORPUS/deliverables/0.9.0_WK_AMGT_CORPUS~3/UNRESOLVED_CLASSES_ROUND25.json")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


s3 = boto3.client("s3")
B = "opal-data-harvest"
latest = {}
for page in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix="derived/model_block/"):
    for o in page.get("Contents", []):
        rest = o["Key"][len("derived/model_block/"):]
        if rest.count("/") >= 2 and rest.endswith("model_block.json"):
            key, stamp = rest.rsplit("/", 2)[0], rest.rsplit("/", 2)[1]
            if key not in latest or stamp > latest[key][0]:
                latest[key] = (stamp, o["Key"])
excluded = sorted(k for k in latest if "/" in k)
keys = sorted(k for k in latest if "/" not in k)
blocks = [json.loads(s3.get_object(Bucket=B, Key=latest[k][1])["Body"].read()) for k in keys]
measured = sum(1 for b in blocks for f in b.get("figures", []) if str(f.get("unit", "")).startswith("UNRESOLVED"))

d = tempfile.mkdtemp(prefix="z1_")
tmp = Path(d) / "field_map.json"
shutil.copyfile(os.path.join(RES, "field_map.json"), tmp)
bum = load("bum_z1", os.path.join(RES, "build_unit_map.py"))
bum.FIELD_MAP_PATH = tmp
with redirect_stdout(io.StringIO()):
    bum.main(["--population", "crosswalk"])
mbp = load("mbp_z1", os.path.join(RES, "model_block_pull.py"))
mbp._FIELD_MAP_PATH = tmp
mbp._FIELD_MAP_CACHE = None
projected = sum(1 for b in blocks for f in b.get("figures", [])
                if str(mbp._resolved_unit(f.get("mnemonic"), b.get("security"))).startswith(("UNRESOLVED", "SEE field_map")))
shutil.rmtree(d, ignore_errors=True)

if not os.path.exists(TABLE):
    print("MISSING %s" % TABLE)
    print("aa3 keys %d excluded %d measured_before %d table_total 0 classes 0 dispositions_complete False projected_after %d "
          "table_remaining -1 consistent False" % (len(keys), len(excluded), measured, projected))
    raise SystemExit(0)
t = json.load(open(TABLE, encoding="utf-8"))
classes = t.get("classes") or []
total = sum(int(c.get("count") or 0) for c in classes)
complete = all(c.get("mnemonic") and c.get("reason_class") and c.get("disposition") in ("family", "stays_unresolved")
               and str(c.get("reason") or "").strip() for c in classes) and bool(classes)
ex_ok = sorted(e.get("key") for e in (t.get("excluded") or []) if e.get("row") == "Z-S64") == excluded
remaining = int(t.get("remaining_after", -1))
consistent = total == measured and remaining == projected and ex_ok and int(t.get("denominator_keys", -1)) == len(keys)
print("aa3 keys %d excluded %d measured_before %d table_total %d classes %d dispositions_complete %s projected_after %d "
      "table_remaining %d consistent %s" % (len(keys), len(excluded), measured, total, len(classes), complete, projected,
                                            remaining, consistent))
