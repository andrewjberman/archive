"""AMGT_CORPUS round 23 CRPS-y-4 -- the before-state and expected diff for the served act (map commit + ONE re-derive pass under
--no-sa-fallback), read from the builder and the served blocks. Read-only: the builder writes a TEMP copy of field_map.json;
S3 reads only. The issuer's file.

  -> 'MAP entries_changed E fields_touched F shared_changed S securities_added A top_level_changed T'
  -> one 'BLOCK <key> same_raw <bool> filled_by_sa <n> unit_flips <n> to_measured <n> still_unresolved <n>' per block
  -> 'y4 blocks K flip_blocks B unit_flips U to_measured M stale_raw R sa_filled_blocks S sa_filled_figures SF'
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
FM = os.path.join(RES, "field_map.json")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def measured(u):
    u = str(u or "")
    return bool(u) and not u.startswith("UNRESOLVED") and not u.startswith("SEE field_map")


d = tempfile.mkdtemp(prefix="y4_")
tmp = Path(d) / "field_map.json"
shutil.copyfile(FM, tmp)
bum = load("bum_y4", os.path.join(RES, "build_unit_map.py"))
bum.FIELD_MAP_PATH = tmp
with redirect_stdout(io.StringIO()):
    bum.main(["--population", "crosswalk"])
before = json.load(open(FM, encoding="utf-8"))
after = json.load(open(tmp, encoding="utf-8"))
top = int({k: v for k, v in before.items() if k not in ("fields", "securities")} != {k: v for k, v in after.items() if k not in ("fields", "securities")})
added = len(set(after.get("securities") or []) - set(before.get("securities") or []))
bf = {e["mnemonic"]: e for e in before["fields"]}
af = {e["mnemonic"]: e for e in after["fields"]}
entries = fields = shared = 0
for m in set(bf) | set(af):
    b, a = bf.get(m) or {}, af.get(m) or {}
    if json.dumps(b, sort_keys=True, default=str) == json.dumps(a, sort_keys=True, default=str):
        continue
    fields += 1
    per = {"per_security_detail", "measured_on"} | {k for k in ("unit", "sign") if isinstance(b.get(k), dict) or isinstance(a.get(k), dict)}
    if {k: v for k, v in b.items() if k not in per} != {k: v for k, v in a.items() if k not in per}:
        shared += 1
    secs = set(b.get("per_security_detail") or {}) | set(a.get("per_security_detail") or {})
    for s in secs:
        if json.dumps((b.get("per_security_detail") or {}).get(s), sort_keys=True, default=str) != json.dumps(
                (a.get("per_security_detail") or {}).get(s), sort_keys=True, default=str):
            entries += 1
print("MAP entries_changed %d fields_touched %d shared_changed %d securities_added %d top_level_changed %d" % (
    entries, fields, shared, added, top))

mbp = load("mbp_y4", os.path.join(RES, "model_block_pull.py"))
mbp._FIELD_MAP_PATH = tmp
mbp._FIELD_MAP_CACHE = None
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
tot = flip_blocks = to_meas = stale = sa_blocks = sa_figs = 0
for key, (stamp, k) in sorted(latest.items()):
    blk = json.loads(s3.get_object(Bucket=B, Key=k)["Body"].read())
    sec = blk.get("security")
    raws = sorted(o["Key"] for o in s3.list_objects_v2(Bucket=B, Prefix="bloomberg/harvest/bronze/refdata/security_key=%s/" % key).get("Contents", []))
    newest = raws[-1].rsplit("/", 1)[-1].replace(".json", "") if raws else None
    same = blk.get("raw_stamp_used") == newest
    ff = (blk.get("forecast_fallback") or {}).get("filled_by_sa") or 0
    flips = tm = still = 0
    for f in blk.get("figures", []):
        new = mbp._resolved_unit(f.get("mnemonic"), sec)
        if new != f.get("unit"):
            flips += 1
            tm += int(measured(new) and not measured(f.get("unit")))
        still += int(not measured(new))
    sa_f = sum(1 for f in blk.get("figures", []) if f.get("source") == "SA_FALLBACK")
    tot += flips
    flip_blocks += int(flips > 0)
    to_meas += tm
    stale += int(not same)
    sa_blocks += int(sa_f > 0 or ff > 0)
    sa_figs += sa_f
    print("BLOCK %s same_raw %s filled_by_sa %s sa_figures %d unit_flips %d to_measured %d still_unmeasured %d" % (
        key, same, ff, sa_f, flips, tm, still))
shutil.rmtree(d, ignore_errors=True)
print("y4 blocks %d flip_blocks %d unit_flips %d to_measured %d stale_raw %d sa_filled_blocks %d sa_filled_figures %d" % (
    len(latest), flip_blocks, tot, to_meas, stale, sa_blocks, sa_figs))
