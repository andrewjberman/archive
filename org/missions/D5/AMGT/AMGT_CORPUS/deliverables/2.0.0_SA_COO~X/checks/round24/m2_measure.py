"""AMGT_CORPUS round 24 -- the expected diff of the z-1 served act (map commit + ONE re-derive of the moving blocks), per FIGURE:
the builder rebuilds a TEMP copy of field_map.json (crosswalk population, as the act's leg a will), then model_block_pull's own
_resolved_unit / _resolved_sign read that temp map against every figure of the newest served block of each key. Read-only
(S3 reads, temp map). BP/_LN and NG/_LN are excluded (Z-S64). The issuer's file.

  python m2_measure.py
  -> 'MAP entries_changed E fields F' then one 'BLOCK <key> unit_changes U to_measured M sign_changes S new_sign_contradicts_value C' per moving block
  -> 'm2 keys K move_blocks B unit_changes U to_measured M measured_to_other X sign_changes S new_sign_contradicts_value C'
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
EXCLUDED = {"BP/_LN_Equity", "NG/_LN_Equity"}
B = "opal-data-harvest"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def measured(u):
    u = str(u or "")
    return bool(u) and not u.startswith("UNRESOLVED") and not u.startswith("SEE field_map")


def own(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    return "POSITIVE" if v > 0 else ("NEGATIVE" if v < 0 else "ZERO")


def contradicts(label, value):
    o = own(value)
    head = str(label).split(" ", 1)[0]
    return o is not None and head in ("POSITIVE", "NEGATIVE", "ZERO") and head != o


tmp = Path(tempfile.mkdtemp(prefix="m2_")) / "field_map.json"
shutil.copyfile(FM, tmp)
bum = load("bum_m2", os.path.join(RES, "build_unit_map.py"))
bum.FIELD_MAP_PATH = tmp
with redirect_stdout(io.StringIO()):
    bum.main(["--population", "crosswalk"])
before = {e["mnemonic"]: e for e in json.load(open(FM, encoding="utf-8"))["fields"]}
after = {e["mnemonic"]: e for e in json.load(open(tmp, encoding="utf-8"))["fields"]}
fields = sorted(m for m in set(before) | set(after)
                if json.dumps(before.get(m), sort_keys=True, default=str) != json.dumps(after.get(m), sort_keys=True, default=str))
print("MAP fields_changed %d %s" % (len(fields), " ".join(fields)))

mbp = load("mbp_m2", os.path.join(RES, "model_block_pull.py"))
mbp._FIELD_MAP_PATH = tmp
mbp._FIELD_MAP_CACHE = None

s3 = boto3.client("s3")
keys = set()
for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix="derived/model_block/"):
    for o in pg.get("Contents", []):
        if o["Key"].endswith("/model_block.json"):
            keys.add(o["Key"][len("derived/model_block/"):].rsplit("/", 2)[0])
keys = sorted(k for k in keys if k not in EXCLUDED)
if os.environ.get("M2_KEYS"):
    keys = [k for k in keys if k in os.environ["M2_KEYS"].split(",")]
TRANS = {}
T = dict(U=0, M=0, X=0, S=0, C=0, moving=0)
for k in keys:
    st = []
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix="derived/model_block/%s/" % k):
        st += [o["Key"] for o in pg.get("Contents", []) if o["Key"].endswith("/model_block.json")]
    blk = json.loads(s3.get_object(Bucket=B, Key=sorted(st)[-1])["Body"].read())
    sec = blk.get("security")
    u = m = x = s = c = 0
    for f in blk.get("figures", []):
        nu = mbp._resolved_unit(f.get("mnemonic"), sec)
        ns = mbp._resolved_sign(f.get("mnemonic"), sec, f.get("value"))
        if nu != f.get("unit"):
            u += 1
            m += int(measured(nu) and not measured(f.get("unit")))
            x += int(measured(f.get("unit")))
        if ns != f.get("sign"):
            tk = "sign %s -> %s" % (str(f.get("sign")).split(":", 1)[0].split("-ON-")[0], str(ns).split(":", 1)[0].split("-ON-")[0])
            TRANS[tk] = TRANS.get(tk, 0) + 1
        s += int(ns != f.get("sign"))
        c += int(contradicts(ns, f.get("value")))
    for kk, vv in (("U", u), ("M", m), ("X", x), ("S", s), ("C", c)):
        T[kk] += vv
    T["moving"] += int(u > 0 or s > 0)
    if u or s:
        print("BLOCK %s unit_changes %d to_measured %d measured_to_other %d sign_changes %d new_sign_contradicts_value %d"
              % (k, u, m, x, s, c))
for tk in sorted(TRANS):
    print("TRANSITION %s %d" % (tk, TRANS[tk]))
print("m2 keys %d move_blocks %d unit_changes %d to_measured %d measured_to_other %d sign_changes %d new_sign_contradicts_value %d"
      % (len(keys), T["moving"], T["U"], T["M"], T["X"], T["S"], T["C"]))
