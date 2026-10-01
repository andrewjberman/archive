"""AMGT_CORPUS round 26 CRPS-ab-4 -- the expected diff of the served act, by SERIALIZING DRY RUN over EVERY key (standing ruling 3;
round-25 analysis: a transition census reads every (from, to) pair, never the pair expected).

1. The builder rebuilds a TEMP copy of field_map.json over the crosswalk population (ab-2's series-median rule; Z-W2-S18 re-reads
   exception entries): every changed per-security entry is printed.
2. For the newest block of each key (raw-slash copies excluded, encoded keys included; the key count is printed beside every count),
   the producer's own `stage_derive` runs against that temp map with a client that passes reads through and CAPTURES writes (nothing
   is written). The captured block is diffed against the served one on everything.
Read-only. The issuer's file; run as a named script with python -u.

  -> 'MAPENTRY <mnemonic> <security> <old unit/sign head> -> <new>' per changed per-security entry
  -> 'BLOCK <key> unit U sign G currency C value V case K top T other O' per moving block
  -> 'TRANS <kind> <mnemonic> <from> -> <to> n' for every (from, to) pair
  -> 'm4 keys K move_blocks M map_entries E unit U sign G currency C value V case_blocks K top T other O writes_per_block W'
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
B = "opal-data-harvest"
WRITES = {"put_object", "copy_object", "delete_object", "delete_objects", "upload_file", "upload_fileobj"}


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
    return "UNRESOLVED" if s.startswith("UNRESOLVED") else ("POINTER" if s.startswith("SEE field_map") else s.split(":", 1)[0].split(" (", 1)[0])


def fkey(f):
    return (f.get("mnemonic"), f.get("scope"), f.get("fiscal_period"), f.get("fiscal_year"), f.get("period_end_date"),
            f.get("override"))


def strip_vintage(x):
    if isinstance(x, dict):
        return {q: strip_vintage(w) for q, w in x.items() if q != "vintage"}
    if isinstance(x, list):
        return [strip_vintage(w) for w in x]
    return x


fm = os.path.join(RES, "field_map.json")
tmp = Path(tempfile.mkdtemp(prefix="m4_")) / "field_map.json"
shutil.copyfile(fm, tmp)
bum = load("bum_m4", os.path.join(RES, "build_unit_map.py"))
bum.FIELD_MAP_PATH = tmp
with redirect_stdout(io.StringIO()):
    bum.main(["--population", "crosswalk"])
before = {e["mnemonic"]: e for e in json.load(open(fm, encoding="utf-8"))["fields"]}
after = {e["mnemonic"]: e for e in json.load(open(tmp, encoding="utf-8"))["fields"]}
entries = 0
for m in sorted(set(before) | set(after)):
    bd = (before.get(m) or {}).get("per_security_detail") or {}
    ad = (after.get(m) or {}).get("per_security_detail") or {}
    for s in sorted(set(bd) | set(ad)):
        if json.dumps(bd.get(s), sort_keys=True, default=str) != json.dumps(ad.get(s), sort_keys=True, default=str):
            entries += 1
            o, n = bd.get(s) or {}, ad.get(s) or {}
            print("MAPENTRY %s %s %s/%s -> %s/%s" % (m, s, head(o.get("unit")), head(o.get("sign")), head(n.get("unit")),
                                                     head(n.get("sign"))), flush=True)

mbp = load("mbp_m4", os.path.join(RES, "model_block_pull.py"))
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
only = [k for k in sys.argv[1:]] or sorted(latest)
T = collections.Counter()
trans = collections.Counter()
writes = collections.Counter()
for k in only:
    old = json.loads(real.get_object(Bucket=B, Key=latest[k])["Body"].read())
    sec = old.get("security")
    cap = Capture(real)
    try:
        mbp.stage_derive(cap, sec, raw_stamp=None, sa_fallback=False)
    except Exception as e:  # a refusal is printed, never swallowed
        print("ERROR %s %s: %s" % (k, type(e).__name__, str(e)[:200]), flush=True)
        T["errors"] += 1
        continue
    writes[len(cap.captured)] += 1
    blocks = [b for op, key, b in cap.captured if op == "put_object" and str(key).endswith("/model_block.json")]
    new = json.loads(blocks[0])
    of = {fkey(f): f for f in old.get("figures", [])}
    c = collections.Counter()
    for f in new.get("figures", []):
        a = of.get(fkey(f))
        if a is None:
            c["O"] += 1
            trans["figure added %s" % f.get("mnemonic")] += 1
            continue
        for kind, field in (("unit", "unit"), ("sign", "sign"), ("currency", "currency")):
            if a.get(field) != f.get(field):
                c[kind] += 1
                trans["%s %s %s -> %s" % (kind, f.get("mnemonic"), head(a.get(field)), head(f.get(field)))] += 1
        c["V"] += int(json.dumps(a.get("value")) != json.dumps(f.get("value")))
        skip = ("unit", "sign", "value", "vintage", "currency", "currency_basis")
        if json.dumps({q: w for q, w in a.items() if q not in skip}, sort_keys=True, default=str) != json.dumps(
                {q: w for q, w in f.items() if q not in skip}, sort_keys=True, default=str):
            c["O"] += 1
    c["O"] += len(set(of) - {fkey(f) for f in new.get("figures", [])})
    kc = int(json.dumps(strip_vintage(old.get("cases")), sort_keys=True, default=str)
             != json.dumps(strip_vintage(new.get("cases")), sort_keys=True, default=str))
    if kc:
        ob, nb = (old.get("cases") or {}).get("base") or {}, (new.get("cases") or {}).get("base") or {}
        trans["case %s %s/%s -> %s/%s" % (k, ob.get("status"), ob.get("value"), nb.get("status"), nb.get("value"))] += 1
    tops = [q for q in (set(old) | set(new)) - {"figures", "cases", "raw_stamp_used"}
            if json.dumps(strip_vintage(old.get(q)), sort_keys=True, default=str)
            != json.dumps(strip_vintage(new.get(q)), sort_keys=True, default=str)]
    for kk, vv in (("U", c["unit"]), ("G", c["sign"]), ("C", c["currency"]), ("V", c["V"]), ("K", kc), ("T", len(tops)),
                   ("O", c["O"])):
        T[kk] += vv
    if c["unit"] or c["sign"] or c["currency"] or c["V"] or kc or tops or c["O"]:
        T["moving"] += 1
        print("BLOCK %s unit %d sign %d currency %d value %d case %d top %d %s other %d" % (
            k, c["unit"], c["sign"], c["currency"], c["V"], kc, len(tops), ",".join(sorted(tops)) or "-", c["O"]), flush=True)
for t, n in sorted(trans.items()):
    print("TRANS %s %d" % (t, n))
print("m4 keys %d move_blocks %d map_entries %d unit %d sign %d currency %d value %d case_blocks %d top %d other %d errors %d "
      "writes_per_block %s" % (len(only), T["moving"], entries, T["U"], T["G"], T["C"], T["V"], T["K"], T["T"], T["O"],
                               T["errors"], dict(writes)))
