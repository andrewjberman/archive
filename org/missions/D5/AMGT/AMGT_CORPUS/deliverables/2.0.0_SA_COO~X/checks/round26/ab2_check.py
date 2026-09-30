"""AMGT_CORPUS round 26, CRPS-ab-2 (analysis ruling 2) -- the unit classifier decides from the key's SERIES median, never one
sample. The builder rebuilds a TEMP copy of field_map.json over the crosswalk population; the producer's own `_resolved_unit`
reads it. Printed FROM the rule, never predicted:
  - BP/ LN Equity PE_RATIO and PROF_MARGIN (their served units read UNRESOLVED at the cut);
  - every served UNRESOLVED figure over the newest block of each key (raw-slash keys excluded; the encoded BP/NG keys included),
    before (served) and after (the rebuilt map), with the key count beside every count (ruling 4);
  - the discriminating bands, unchanged (their sha256 against the base recorded at the cut).
Read-only (S3 reads, temp map). The issuer's file.

  -> one 'FIG <key> <mnemonic> <fiscal_year> <before head> -> <after head>' per served UNRESOLVED figure
  -> 'ab2 bp_pe_ratio H bp_prof_margin H keys K unresolved_before B unresolved_after A bands_unchanged True|False'
"""
import hashlib
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
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
B = "opal-data-harvest"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def head(u):
    s = str(u or "")
    return "UNRESOLVED" if s.startswith("UNRESOLVED") else ("POINTER" if s.startswith("SEE field_map") else s.split(" ", 1)[0])


tmp = Path(tempfile.mkdtemp(prefix="ab2_")) / "field_map.json"
shutil.copyfile(os.path.join(RES, "field_map.json"), tmp)
bum = load("bum_ab2", os.path.join(RES, "build_unit_map.py"))
bands = {k: getattr(bum, k) for k in sorted(dir(bum)) if k.startswith("BAND_") or k.endswith("_BANDS")}
bands_sha = hashlib.sha256(json.dumps(bands, sort_keys=True, default=str).encode("utf-8")).hexdigest()
bum.FIELD_MAP_PATH = tmp
with redirect_stdout(io.StringIO()):
    bum.main(["--population", "crosswalk"])
mbp = load("mbp_ab2", os.path.join(RES, "model_block_pull.py"))
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
                continue  # the kept raw-slash copies; the identity is read at its encoded key
            if k not in latest or o["Key"] > latest[k]:
                latest[k] = o["Key"]
before = after = 0
for k in sorted(latest):
    blk = json.loads(s3.get_object(Bucket=B, Key=latest[k])["Body"].read())
    sec = blk.get("security")
    for f in blk.get("figures", []):
        if head(f.get("unit")) != "UNRESOLVED":
            continue
        before += 1
        nu = mbp._resolved_unit(f.get("mnemonic"), sec)
        after += int(head(nu) == "UNRESOLVED")
        print("FIG %s %s %s %s -> %s" % (k, f.get("mnemonic"), f.get("fiscal_year"), head(f.get("unit")), head(nu)))
bp = "BP/ LN Equity"
base_sha = open(os.path.join(HERE, "ab2_bands_base.sha256")).read().strip()
print("ab2 bp_pe_ratio %s bp_prof_margin %s keys %d unresolved_before %d unresolved_after %d bands_unchanged %s" % (
    head(mbp._resolved_unit("PE_RATIO", bp)), head(mbp._resolved_unit("PROF_MARGIN", bp)), len(latest), before, after,
    bands_sha == base_sha))
