"""AMGT_CORPUS round 25 -- the expected diff of the aa-2 served act (map rebuild with aa-3's families + ONE re-derive carrying aa-1's
label rule), per FIGURE and per SCOPE: the builder rebuilds a TEMP copy of field_map.json; model_block_pull's own _resolved_unit /
_resolved_sign read that temp map, and its own _figure_currency (with the block's security) reads each figure's currency and basis,
against every figure of the newest served block of each key. Read-only (S3 reads, temp map). BP/NG are EXCLUDED in either form
(Z-S64). The issuer's file; run as a named script with python -u.

  -> 'MAP fields_changed N <names>'
  -> one 'BLOCK <key> unit U sign S currency C basis_only B measured_to_other X ccy_to_none Z' per moving block
  -> 'SCOPE <scope> currency C basis_only B' per scope with a label move
  -> 'MNEM <mnemonic> <from_ccy>/<from_basis_head> -> <to_ccy>/<to_basis_head> n' per label transition
  -> 'm3 keys K move_blocks M unit_changes U sign_changes S currency_changes C basis_only_changes B measured_to_other X
      ccy_to_none Z'
"""
import collections
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
B = "opal-data-harvest"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def measured(u):
    u = str(u or "")
    return bool(u) and not u.startswith("UNRESOLVED") and not u.startswith("SEE field_map")


def head(basis):
    return str(basis).split(":", 1)[0].split(" (", 1)[0]


tmp = Path(tempfile.mkdtemp(prefix="m3_")) / "field_map.json"
shutil.copyfile(FM, tmp)
bum = load("bum_m3", os.path.join(RES, "build_unit_map.py"))
bum.FIELD_MAP_PATH = tmp
with redirect_stdout(io.StringIO()):
    bum.main(["--population", "crosswalk"])
before = {e["mnemonic"]: e for e in json.load(open(FM, encoding="utf-8"))["fields"]}
after = {e["mnemonic"]: e for e in json.load(open(tmp, encoding="utf-8"))["fields"]}
fields = sorted(m for m in set(before) | set(after)
                if json.dumps(before.get(m), sort_keys=True, default=str) != json.dumps(after.get(m), sort_keys=True, default=str))
print("MAP fields_changed %d %s" % (len(fields), " ".join(fields)), flush=True)

mbp = load("mbp_m3", os.path.join(RES, "model_block_pull.py"))
mbp._FIELD_MAP_PATH = tmp
mbp._FIELD_MAP_CACHE = None

s3 = boto3.client("s3")
latest = {}
for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix="derived/model_block/"):
    for o in pg.get("Contents", []):
        rest = o["Key"][len("derived/model_block/"):]
        if rest.endswith("/model_block.json"):
            k = rest.rsplit("/", 2)[0]
            if "/" in k or "-SLASH-" in k:
                continue
            if k not in latest or o["Key"] > latest[k]:
                latest[k] = o["Key"]
T = collections.Counter()
scope_ct = collections.Counter()
trans = collections.Counter()
for k in sorted(latest):
    blk = json.loads(s3.get_object(Bucket=B, Key=latest[k])["Body"].read())
    sec = blk.get("security")
    cur = blk.get("currencies") or {}
    u = s = c = bo = x = z = 0
    for f in blk.get("figures", []):
        m = f.get("mnemonic")
        nu = mbp._resolved_unit(m, sec)
        ns = mbp._resolved_sign(m, sec, f.get("value"))
        nc, nb = mbp._figure_currency(m, cur.get("quote"), cur.get("reporting"), security=sec)
        if nu != f.get("unit"):
            u += 1
            x += int(measured(f.get("unit")))
        s += int(ns != f.get("sign"))
        if nc != f.get("currency"):
            c += 1
            z += int(nc is None)
            scope_ct[(f.get("scope"), "currency")] += 1
            trans["%s %s/%s -> %s/%s" % (m, f.get("currency"), head(f.get("currency_basis")), nc, head(nb))] += 1
        elif nb != f.get("currency_basis"):
            bo += 1
            scope_ct[(f.get("scope"), "basis_only")] += 1
            trans["%s %s/%s -> %s/%s" % (m, f.get("currency"), head(f.get("currency_basis")), nc, head(nb))] += 1
    for kk, vv in (("U", u), ("S", s), ("C", c), ("B", bo), ("X", x), ("Z", z)):
        T[kk] += vv
    if u or s or c or bo:
        T["moving"] += 1
        print("BLOCK %s unit %d sign %d currency %d basis_only %d measured_to_other %d ccy_to_none %d" % (k, u, s, c, bo, x, z),
              flush=True)
for (sc, kind), n in sorted(scope_ct.items(), key=lambda t: (str(t[0][0]), t[0][1])):
    print("SCOPE %s %s %d" % (sc, kind, n))
for t, n in sorted(trans.items()):
    print("MNEM %s %d" % (t, n))
print("m3 keys %d move_blocks %d unit_changes %d sign_changes %d currency_changes %d basis_only_changes %d measured_to_other %d "
      "ccy_to_none %d" % (len(latest), T["moving"], T["U"], T["S"], T["C"], T["B"], T["X"], T["Z"]))
