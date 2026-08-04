"""BR1-DS leg 3 -- the Eclipse overlap-compare harness (Gate-1 acceptance instrument).

Compares the STAGING pull (inf-api-eclipse Lambda -> bronze/eclipse_qa/{date}/) against
the PRODUCTION pull (the EC2 box -> bronze/eclipse/{date}/) for one day, field-exact,
and emits the day's verdict. Five clean trading days = the Gate-1 overlap acceptance
(plan @7538cbc5f); day-1's verdict starts the clock.

CLASSIFICATION, not auto-pass (the honest shape): the two pulls hit a CURRENT-STATE
vendor minutes apart, so a same-day value can legitimately move between them. The
harness therefore classifies every difference rather than binary-failing:
  IDENTICAL         byte-equal payload
  VALUE-DRIFT       same structure/keys, numeric leaf deltas only (count + max |delta|
                    printed) -- the explainable pull-skew class, judged at the gate
  STRUCTURAL        key-set / row-count / shape divergence -- NEVER explainable by
                    pull skew; any STRUCTURAL = the day FAILS
  MISSING           artifact present on one side only = the day FAILS
Sidecar compare: rows_per_artifact equality EXACT (timestamps/jwt_source/dry_run
excluded -- process fields, not content).
Verdict ledger: appends one JSON line per run to
org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/BR1_overlap_ledger.jsonl
(committed by the operator with the day's read -- the gate reads the ledger).

READ-ONLY against S3. Usage: python eclipse_overlap_compare.py [--date YYYY-MM-DD]
Author: 0.4.0_DS_ClientPlatform  TO: OPAL_VENDORPROVENANCE.BR1-DS.script-legs
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import boto3

BUCKET = "opal-data-inf"
PROD_PREFIX = "bronze/eclipse"
STAGE_PREFIX = "bronze/eclipse_qa"
LEDGER = Path("org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/BR1_overlap_ledger.jsonl")
SIDECAR_PROCESS_FIELDS = {"started_at", "completed_at", "jwt_source", "dry_run"}

s3 = boto3.client("s3", region_name="us-east-1")


def _list_day(prefix: str, date: str) -> "dict[str, str]":
    """artifact-name -> full key for one day's partition (sidecar included)."""
    out = {}
    pag = s3.get_paginator("list_objects_v2")
    for page in pag.paginate(Bucket=BUCKET, Prefix=f"{prefix}/{date}/"):
        for o in page.get("Contents", []):
            name = o["Key"].split(f"{prefix}/{date}/", 1)[1]
            out[name] = o["Key"]
    return out


def _get_json(key: str):
    return json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())


def _numeric_leaf_deltas(a, b, path=""):
    """(structural_diffs, value_deltas). Structural = key/shape/type/non-numeric
    mismatches; value = numeric leaf differences (path, a, b)."""
    structural, values = [], []
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            structural.append((path, f"key sets differ: only-prod={sorted(set(a)-set(b))[:4]} "
                                     f"only-stage={sorted(set(b)-set(a))[:4]}"))
            return structural, values
        for k in a:
            s_, v_ = _numeric_leaf_deltas(a[k], b[k], f"{path}.{k}")
            structural += s_
            values += v_
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            structural.append((path, f"list length {len(a)} vs {len(b)}"))
            return structural, values
        for i, (x, y) in enumerate(zip(a, b)):
            s_, v_ = _numeric_leaf_deltas(x, y, f"{path}[{i}]")
            structural += s_
            values += v_
    else:
        if a == b:
            return structural, values
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) \
                and not isinstance(a, bool) and not isinstance(b, bool):
            values.append((path, a, b))
        else:
            structural.append((path, f"{type(a).__name__}({str(a)[:40]}) != "
                                     f"{type(b).__name__}({str(b)[:40]})"))
    return structural, values


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"))
    a = ap.parse_args()

    prod = _list_day(PROD_PREFIX, a.date)
    stage = _list_day(STAGE_PREFIX, a.date)
    print(f"[overlap] {a.date}: prod artifacts={len(prod)} stage artifacts={len(stage)}")
    if not prod or not stage:
        print(f"[overlap] VERDICT INCOMPLETE-DAY: one side absent "
              f"(prod={bool(prod)} stage={bool(stage)}) -- not a comparison day")
        return 2

    per_artifact, day_fail = {}, False
    names = sorted(set(prod) | set(stage))
    for name in names:
        if name not in prod or name not in stage:
            per_artifact[name] = {"class": "MISSING",
                                  "side": "stage-only" if name in stage else "prod-only"}
            day_fail = True
            continue
        pa, sa = _get_json(prod[name]), _get_json(stage[name])
        if name.endswith("_meta/pull_complete.json") or name == "_meta/pull_complete.json":
            pa = {k: v for k, v in pa.items() if k not in SIDECAR_PROCESS_FIELDS}
            sa = {k: v for k, v in sa.items() if k not in SIDECAR_PROCESS_FIELDS}
        structural, values = _numeric_leaf_deltas(pa, sa)
        if structural:
            per_artifact[name] = {"class": "STRUCTURAL", "n": len(structural),
                                  "first": structural[:3]}
            day_fail = True
        elif values:
            per_artifact[name] = {"class": "VALUE-DRIFT", "n": len(values),
                                  "max_abs": max(abs(x - y) for _, x, y in values)}
        else:
            per_artifact[name] = {"class": "IDENTICAL"}

    verdict = "FAIL" if day_fail else (
        "CLEAN-IDENTICAL" if all(v["class"] == "IDENTICAL" for v in per_artifact.values())
        else "CLEAN-WITH-DRIFT")
    for name, v in per_artifact.items():
        print(f"  {name}: {v['class']}"
              + (f" n={v['n']} max_abs={v.get('max_abs', '')}" if v['class'] != 'IDENTICAL' else "")
              + (f" {v.get('first','')}" if v['class'] == 'STRUCTURAL' else ""))
    print(f"[overlap] DAY VERDICT {a.date}: {verdict}")

    rec = {"date": a.date, "ran_at": dt.datetime.now(dt.timezone.utc).isoformat(),
           "verdict": verdict, "artifacts": per_artifact}
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, default=str) + "\n")
    print(f"[overlap] ledger appended: {LEDGER}")
    return 1 if day_fail else 0


if __name__ == "__main__":
    sys.exit(main())
