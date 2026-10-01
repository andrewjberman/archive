"""AMGT_CORPUS round 27, CRPS-ac-1 (round-26 analysis ruling 3) -- a ZERO-DOMINATED unit class: a key whose fiscal-year series is
mostly exact zeros has no magnitude to classify by, so it reads its own class ("no magnitude: n of m years are zero"), never a
guessed unit. The builder rebuilds a TEMP map over the crosswalk population; the producer's own `_resolved_unit` reads it against
EVERY figure of the newest served block of 100 keys (raw-slash copies excluded, encoded keys included). Read-only. The issuer's file.

  -> one 'TRANS <mnemonic> <from head> -> <to head> n' per (from, to) unit pair that moves
  -> 'ac1 bbse3_unit H bbse3_count <n> of <m> keys K other_unit_changes N bands_unchanged True|False'
"""
import collections
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

import boto3

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
B = "opal-data-harvest"
TARGET = ("BBSE3_BZ_Equity", "CAPITAL_EXPEND")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def head(u):
    s = str(u or "")
    if s.startswith("UNRESOLVED"):
        return "UNRESOLVED"
    if s.startswith("SEE field_map"):
        return "POINTER"
    return re.split(r"[:( ]", s, 1)[0]


tmp = Path(tempfile.mkdtemp(prefix="ac1_")) / "field_map.json"
shutil.copyfile(os.path.join(RES, "field_map.json"), tmp)
bum = load("bum_ac1", os.path.join(RES, "build_unit_map.py"))
bands = {k: getattr(bum, k) for k in sorted(dir(bum)) if k.startswith("BAND_") or k.endswith("_BANDS")}
bands_sha = hashlib.sha256(json.dumps(bands, sort_keys=True, default=str).encode("utf-8")).hexdigest()
bum.FIELD_MAP_PATH = tmp
with redirect_stdout(io.StringIO()):
    bum.main(["--population", "crosswalk"])
mbp = load("mbp_ac1", os.path.join(RES, "model_block_pull.py"))
mbp._FIELD_MAP_PATH = tmp
mbp._FIELD_MAP_CACHE = None

s3 = boto3.client("s3")
latest = {}
for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix="derived/model_block/"):
    for o in pg.get("Contents", []):
        rest = o["Key"][len("derived/model_block/"):]
        if rest.endswith("/model_block.json"):
            k = rest.rsplit("/", 2)[0]
            if "/" in k:
                continue
            if k not in latest or o["Key"] > latest[k]:
                latest[k] = o["Key"]
trans = collections.Counter()
other = 0
target_unit = None
for k in sorted(latest):
    blk = json.loads(s3.get_object(Bucket=B, Key=latest[k])["Body"].read())
    sec = blk.get("security")
    for f in blk.get("figures", []):
        nu = mbp._resolved_unit(f.get("mnemonic"), sec)
        if (k, f.get("mnemonic")) == TARGET:
            target_unit = nu
            continue
        if nu != f.get("unit"):
            other += 1
            trans["%s %s -> %s" % (f.get("mnemonic"), head(f.get("unit")), head(nu))] += 1
for t, n in sorted(trans.items()):
    print("TRANS %s %d" % (t, n))
m = re.search(r"(\d+) of (\d+)", str(target_unit or ""))
base_sha = open(os.path.join(HERE, "ac1_bands_base.sha256")).read().strip()
print("ac1 bbse3_unit %s bbse3_count %s keys %d other_unit_changes %d bands_unchanged %s" % (
    head(target_unit), "%s of %s" % m.groups() if m else "none", len(latest), other, bands_sha == base_sha))
