"""AMGT_CORPUS round 28 CRPS-ad-2 -- THE ZERO-VALUE SIGN OVER-REFUSAL (PRD v0.7 FWD-20; round-27 analysis s.3 item 2).

A zero SAMPLE makes today's map write the whole series' sign as UNRESOLVED ("sampled value is exactly zero -- sign is ambiguous,
not claimed"), and the producer keeps a map-UNRESOLVED sign on every figure, so BA's DPS of 4.69 is refused with its zeros.
Measured at base (r28_census.py): 364 refused fiscal figures over 100 keys, 354 of them on that reason (IS_DIV_PER_SHR, EQY_DPS).

Method (read-only, the round-27 serializing dry run): the working tree's builder rebuilds a TEMP map over the crosswalk
population; then the working tree's `stage_derive` runs against it for EVERY key (newest block; raw-slash copies excluded) with a
client that passes reads through and CAPTURES writes. On the captured blocks:
  - the check face's own bucket (`lib.research.checkface.run_checks.unit_status_for`) over every fiscal-year figure: refused, and
    refused on the zero-sample reason
  - BA's IS_DIV_PER_SHR: how many of its fiscal figures pass the check face (the positive control)
  - against the SERVED newest block: value moves, unit moves, and sign moves on a figure whose served sign was NOT the zero-sample
    reason (each must be 0); every (from, to) sign transition is printed
  -> 'TRANS sign <mnemonic> <from> -> <to> n' per transition
  -> 'ad2 keys K refuse R refuse_zero_sample Z ba_dps_shown S of N value_moves V unit_moves U other_sign_moves O errors E'
"""
import collections
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

import boto3

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
sys.path[:0] = [TOP, RES]
from lib.research.checkface.run_checks import unit_status_for  # noqa: E402

B = "opal-data-harvest"
WRITES = {"put_object", "copy_object", "delete_object", "delete_objects", "upload_file", "upload_fileobj"}
ZERO_REASON = "sampled value is exactly zero"


class Capture:
    def __init__(self, real):
        self._real = real
        self.captured = []

    def __getattr__(self, name):
        if name in WRITES:
            def cap(*a, **kw):
                body = kw.get("Body")
                self.captured.append((name, kw.get("Key"), body.read() if hasattr(body, "read") else body))
                return {"ETag": '"dry-run"'}
            return cap
        return getattr(self._real, name)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def head(u):
    s = str(u)
    if s == "None":
        return "None"
    if ZERO_REASON in s:
        return "UNRESOLVED(zero-sample)"
    return "UNRESOLVED" if s.startswith("UNRESOLVED") else s.split(":", 1)[0].split(" (", 1)[0]


def fkey(f):
    return (f.get("mnemonic"), f.get("scope"), f.get("fiscal_period"), f.get("fiscal_year"), f.get("period_end_date"),
            f.get("override"))


fm = os.path.join(RES, "field_map.json")
tmp = Path(tempfile.mkdtemp(prefix="ad2_")) / "field_map.json"
shutil.copyfile(fm, tmp)
bum = load("bum_ad2", os.path.join(RES, "build_unit_map.py"))
bum.FIELD_MAP_PATH = tmp
with redirect_stdout(io.StringIO()):
    bum.main(["--population", "crosswalk"])
mbp = load("mbp_ad2", os.path.join(RES, "model_block_pull.py"))
mbp._FIELD_MAP_PATH = tmp
mbp._FIELD_MAP_CACHE = None

real = boto3.client("s3")
latest = {}
for pg in real.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix="derived/model_block/"):
    for o in pg.get("Contents", []):
        rest = o["Key"][len("derived/model_block/"):]
        if rest.endswith("/model_block.json"):
            k = rest.rsplit("/", 2)[0]
            if "/" in k:
                continue
            if k not in latest or o["Key"] > latest[k]:
                latest[k] = o["Key"]
T = collections.Counter()
trans = collections.Counter()
ba_shown = ba_n = 0
for k in sorted(latest):
    old = json.loads(real.get_object(Bucket=B, Key=latest[k])["Body"].read())
    cap = Capture(real)
    try:
        mbp.stage_derive(cap, old.get("security"), raw_stamp=None, sa_fallback=False)
    except Exception as e:  # a refusal is printed, never swallowed
        print("ERROR %s %s: %s" % (k, type(e).__name__, str(e)[:200]), flush=True)
        T["errors"] += 1
        continue
    blocks = [b for op, key, b in cap.captured if op == "put_object" and str(key).endswith("/model_block.json")]
    if len(blocks) != 1:
        print("ERROR %s %d block writes captured" % (k, len(blocks)), flush=True)
        T["errors"] += 1
        continue
    new = json.loads(blocks[0])
    of = {fkey(f): f for f in old.get("figures", [])}
    for f in new.get("figures", []):
        if f.get("scope") == "fiscal_year_line_item":
            st = unit_status_for(f)
            if st not in ("MEASURED", "PENDING"):
                T["refuse"] += 1
                T["refuse_zero"] += int(ZERO_REASON in str(f.get("sign")))
            if k == "BA_US_Equity" and f.get("mnemonic") == "IS_DIV_PER_SHR":
                ba_n += 1
                ba_shown += int(st in ("MEASURED", "PENDING"))
        a = of.get(fkey(f))
        if a is None:
            continue
        T["value"] += int(json.dumps(a.get("value")) != json.dumps(f.get("value")))
        T["unit"] += int(a.get("unit") != f.get("unit"))
        if a.get("sign") != f.get("sign"):
            trans["sign %s %s -> %s" % (f.get("mnemonic"), head(a.get("sign")), head(f.get("sign")))] += 1
            T["other_sign"] += int(ZERO_REASON not in str(a.get("sign")))
for t, n in sorted(trans.items()):
    print("TRANS %s %d" % (t, n))
print("ad2 keys %d refuse %d refuse_zero_sample %d ba_dps_shown %d of %d value_moves %d unit_moves %d other_sign_moves %d "
      "errors %d" % (len(latest), T["refuse"], T["refuse_zero"], ba_shown, ba_n, T["value"], T["unit"], T["other_sign"],
                     T["errors"]))
