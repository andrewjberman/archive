"""AMGT_CORPUS round 35, CRPS-ak-4 leg v (CTO half conditions 3 and 4) -- read-only. The issuer's file.

  Usage: python v35.py <CUTOFF stamp prefix, e.g. 20261004T133>
  For every REGISTERED name, its newest derived block is the act's block when its stamp >= CUTOFF; it is compared with the
  name's PREVIOUS block (the one it replaced).
    v1 names re-derived (newest >= CUTOFF) / not re-derived (listed: Branch B's failures)
    v2 base-field VALUES moved between the previous and the newest block, over the re-derived names (expected 0: the same raw
       is re-derived), keyed (scope, fiscal_year, period, mnemonic); moved samples printed
    v3 the 52's figures carrying the pointer unit "SEE field_map.json" in the newest blocks of the re-derived names
       (expected 0); the 52's figures and unresolved entries counted beside it
  A positive control: with CUTOFF at a fresh PULL's stamp, v2 must read non-zero (fresh market data moves values).
"""
import collections
import importlib.util
import json
import os
import subprocess
import sys

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
for p in (TOP, RES):
    if p not in sys.path:
        sys.path.insert(0, p)
spec = importlib.util.spec_from_file_location("mbp_v35", os.path.join(RES, "model_block_pull.py"))
mbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mbp)
from lib.research.identity import crosswalk  # noqa: E402

CUTOFF = sys.argv[1]
NEW = set(mbp.HEADER_FIELDS[18:]) | set(mbp.HIST_FIELDS[39:]) | set(mbp.FORECAST_FIELDS[11:])
BASE = set(mbp.HEADER_FIELDS[:18]) | set(mbp.HIST_FIELDS[:39]) | set(mbp.FORECAST_FIELDS[:11])
assert len(NEW) == 52


def _stamps_by_segment(client):
    prefix = "derived/%s/" % mbp.ENGINE
    found = collections.defaultdict(list)
    token = None
    while True:
        kwargs = {"Bucket": mbp.BUCKET, "Prefix": prefix}
        if token:
            kwargs["ContinuationToken"] = token
        page = client.list_objects_v2(**kwargs)
        for item in page.get("Contents", []):
            key = item["Key"]
            if key.endswith("/model_block.json"):
                seg, stamp, _ = key[len(prefix):].rsplit("/", 2)
                found[seg].append((stamp, key))
        if not page.get("IsTruncated"):
            return found
        token = page.get("NextContinuationToken")


def _block(client, key):
    body = json.loads(client.get_object(Bucket=mbp.BUCKET, Key=key)["Body"].read())
    return body.get("model_block", body)


def _base_values(block):
    out = {}
    for f in block.get("figures", []):
        if f.get("mnemonic") in BASE:
            out[(f.get("scope"), str(f.get("fiscal_year")), str(f.get("period")), f.get("mnemonic"))] = f.get("value")
    return out


s3 = mbp._s3()
stamps = _stamps_by_segment(s3)
registered = mbp._registered_security_keys()
redone, not_redone = [], []
moved = []
pointer = new_figs = new_unres = 0
for sk in registered:
    entries = sorted(stamps.get(crosswalk.slash_safe_key(sk)) or stamps.get(sk) or [])
    if not entries or entries[-1][0] < CUTOFF:
        not_redone.append((sk, entries[-1][0] if entries else "NO BLOCK"))
        continue
    redone.append(sk)
    newest = _block(s3, entries[-1][1])
    if len(entries) >= 2:
        prev = _block(s3, entries[-2][1])
        a, b = _base_values(prev), _base_values(newest)
        for k in set(a) | set(b):
            if a.get(k) != b.get(k):
                moved.append((sk, k, a.get(k), b.get(k)))
    for f in newest.get("figures", []):
        if f.get("mnemonic") in NEW:
            new_figs += 1
            if str(f.get("unit", "")).startswith("SEE field_map.json"):
                pointer += 1
    new_unres += sum(1 for u in newest.get("unresolved", []) if u.get("mnemonic") in NEW)

print("v1 registered %d redone %d not_redone %d" % (len(registered), len(redone), len(not_redone)))
for sk, why in not_redone:
    print("   NOT-REDONE %s newest %s" % (sk, why))
print("v2 base_values_moved %d over %d names %s" % (len(moved), len(redone), [(m[0], m[1][3], m[2], m[3]) for m in moved[:4]]))
print("v3 new52 figures %d unresolved %d pointer_unit_figures %d" % (new_figs, new_unres, pointer))
