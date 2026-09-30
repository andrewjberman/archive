"""AMGT_CORPUS round 23, CRPS-y-1 -- the UNRESOLVED-unit census BEFORE (the newest served block of every key, as served) and
AFTER (the same figures resolved through the round's unit builder, run over the crosswalk population into a TEMP copy of the
committed field_map.json; the committed map is never written). Read-only on S3. The issuer's file.

  -> 'y1 blocks K before unresolved B pointer_before PB no_family_before NB after unresolved A pointer_after PA no_family_after NA
      crncy_after C per_share_after P'
  (POINTER = the reader's 'SEE field_map.json ... not yet built' unit: no map entry at all for that field and name)
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
PER_SHARE = {"IS_DIV_PER_SHR", "REVENUE_PER_SH", "BOOK_VAL_PER_SH"}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def unresolved(u):
    return str(u or "").startswith("UNRESOLVED")


def pointer(u):
    return str(u or "").startswith("SEE field_map")


def no_family(u):
    return "not in any known field" in str(u or "")


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
blocks = [json.loads(s3.get_object(Bucket=B, Key=k)["Body"].read()) for _, (_, k) in sorted(latest.items())]

before = sum(1 for b in blocks for f in b.get("figures", []) if unresolved(f.get("unit")))
nb = sum(1 for b in blocks for f in b.get("figures", []) if no_family(f.get("unit")))
pb = sum(1 for b in blocks for f in b.get("figures", []) if pointer(f.get("unit")))

d = tempfile.mkdtemp(prefix="y1_census_")
tmp = Path(d) / "field_map.json"
shutil.copyfile(os.path.join(RES, "field_map.json"), tmp)
bum = load("bum_y1", os.path.join(RES, "build_unit_map.py"))
bum.FIELD_MAP_PATH = tmp
with redirect_stdout(io.StringIO()):
    bum.main(["--population", "crosswalk"])
mbp = load("mbp_y1", os.path.join(RES, "model_block_pull.py"))
mbp._FIELD_MAP_PATH = tmp
mbp._FIELD_MAP_CACHE = None

after = na = crncy = per_share = pa = 0
for b in blocks:
    sec = b.get("security")
    for f in b.get("figures", []):
        u = mbp._resolved_unit(f.get("mnemonic"), sec)
        pa += int(pointer(u))
        if unresolved(u):
            after += 1
            na += int(no_family(u))
            crncy += int(f.get("mnemonic") == "EQY_FUND_CRNCY")
            per_share += int(f.get("mnemonic") in PER_SHARE)
shutil.rmtree(d, ignore_errors=True)
print("y1 blocks %d before unresolved %d pointer_before %d no_family_before %d after unresolved %d pointer_after %d no_family_after %d "
      "crncy_after %d per_share_after %d" % (len(blocks), before, pb, nb, after, pa, na, crncy, per_share))
