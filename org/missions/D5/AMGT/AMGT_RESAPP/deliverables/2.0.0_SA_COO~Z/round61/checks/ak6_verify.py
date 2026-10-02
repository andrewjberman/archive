"""AMGT_RESAPP round 61 -- ak-6's read-back after the stored-field rewrite (CTO half @af95b2f1c0 conditions 1-3).

  python ak6_verify.py --plan <json> [--plan ...] --base <AK6_BASE_VERSIONS.json> [--expect-sha <sha256> ...]

  C1 (condition 1) each plan file's sha256 is one of the --expect-sha values (the halves' table), in the given order;
  C2 (condition 2) for EVERY key and EVERY planned field: the CURRENT object's field equals the plan's `after` (n of n);
  C3 (condition 3) for EVERY key: the current object with its planned fields masked equals the BASE VersionId's object (from
     the appendix) with the same fields masked -- the whole-object PUT changed nothing else (n of n);
  C4 every key's current VersionId differs from its base VersionId (the write happened).
Verdict: AK6 READ-BACK CLEAN: YES|NO. Read-only (GetObject, incl. by VersionId); writes nothing.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from collections import defaultdict

import boto3

BUCKET = "opal-data-harvest"
_TOK = re.compile(r"([A-Za-z0-9_]+)|\[(\d+)\]")
MASK = "<<PLANNED-FIELD>>"


def _parts(path):
    return [(k, int(i) if i else None) for k, i in _TOK.findall(path)]


def _get(doc, path):
    node = doc
    for key, idx in _parts(path):
        node = node[key] if idx is None else node[idx]
    return node


def _set(doc, path, value):
    parts = _parts(path)
    node = doc
    for key, idx in parts[:-1]:
        node = node[key] if idx is None else node[idx]
    key, idx = parts[-1]
    node[key if idx is None else idx] = value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="append", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--expect-sha", action="append", default=[])
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    shas = [hashlib.sha256(open(p, "rb").read()).hexdigest() for p in a.plan]
    if a.expect_sha:
        clause("C1 the plans are the frozen bytes", shas == a.expect_sha, f"{shas}")
    by_key = defaultdict(list)
    for p in a.plan:
        for e in json.load(open(p, encoding="utf-8")).get("entries") or []:
            by_key[e["store_key"]].append(e)
    base = {r["store_key"]: r["version_id"] for r in json.load(open(a.base, encoding="utf-8"))["rows"]}
    s3 = boto3.client("s3", region_name="us-east-1")
    fields_ok = fields_n = keys_same = keys_moved = 0
    bad_fields, bad_rest, unmoved, missing_base = [], [], [], []
    for key in sorted(by_key):
        cur_obj = s3.get_object(Bucket=BUCKET, Key=key)
        cur = json.loads(cur_obj["Body"].read().decode("utf-8"))
        if key not in base:
            missing_base.append(key)
            continue
        old = json.loads(s3.get_object(Bucket=BUCKET, Key=key, VersionId=base[key])["Body"].read().decode("utf-8"))
        if cur_obj.get("VersionId") != base[key]:
            keys_moved += 1
        else:
            unmoved.append(key)
        cur_m, old_m = copy.deepcopy(cur), copy.deepcopy(old)
        for e in by_key[key]:
            fields_n += 1
            try:
                if _get(cur, e["store_field"]) == e.get("after"):
                    fields_ok += 1
                else:
                    bad_fields.append((key, e["store_field"]))
                _set(cur_m, e["store_field"], MASK)
                _set(old_m, e["store_field"], MASK)
            except (KeyError, IndexError, TypeError) as err:
                bad_fields.append((key, f"{e['store_field']} unlocatable: {err}"))
        if cur_m == old_m:
            keys_same += 1
        else:
            bad_rest.append(key)
    n = len(by_key)
    clause("C2 every planned field reads the plan's after", fields_n and fields_ok == fields_n and not bad_fields,
           f"{fields_ok} of {fields_n} fields; bad {bad_fields[:5]}")
    clause("C3 every object minus its planned fields equals its base version", keys_same == n and not missing_base,
           f"{keys_same} of {n} keys; differing {bad_rest[:5]}; missing base {missing_base[:5]}")
    clause("C4 every key moved off its base VersionId", keys_moved == n, f"{keys_moved} of {n}; unmoved {unmoved[:5]}")
    print(f"AK6 READ-BACK CLEAN: {'YES' if all(ok) else 'NO'}")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
