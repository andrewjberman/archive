"""GAP_EXPLAIN_A1 -- POSN_AGGFIX.TO-A1-1, cell AF1-s-1 (C-GAP-EXPLAINED). READ-ONLY.

Prints the served platinum/mdpf/global/aum-metrics.json head and its gap
(total.model_aum - sum(by_model[].aum)); reads the gold fold object that
data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py names as its input
(AGG_GLOBAL_KEY) at the version whose as_of_last equals the served period and
whose LastModified precedes the served file; prints the fold's model_aua
frontier and every per-key frontier; reproduces the gap from the fold with the
producer's OWN MODEL_ORDER constant and its :497-512 per-key rule; runs a
control arm (one served by_model row raised by 1.00 in memory); writes
AF1_S1_GAP_EXPLANATION.md beside itself. Author 0.9.0_WK_POSN_AGGFIX~1.
Nothing is written to S3.
"""
import gzip
import importlib.util
import json
import os
import subprocess
import sys

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE,
                      capture_output=True, text=True, check=True).stdout.strip()
HEAD = subprocess.run(["git", "rev-parse", "--short=10", "HEAD"], cwd=HERE,
                      capture_output=True, text=True, check=True).stdout.strip()
PRODUCER_REL = "data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py"
SERVED_BUCKET = "opal-data-portal-v2"
SERVED_KEY = "platinum/mdpf/global/aum-metrics.json"

_spec = importlib.util.spec_from_file_location("dim_mdpf_aum_metrics", os.path.join(ROOT, PRODUCER_REL))
prod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(prod)

s3 = boto3.client("s3", region_name="us-east-1")


def body_json(resp):
    raw = resp["Body"].read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return json.loads(raw)


def c2(x):
    return round(float(x), 2)


def fmt(x):
    return "None" if x is None else format(c2(x), ",.2f")


# ---- 1. the served file ---------------------------------------------------------------
sr = s3.get_object(Bucket=SERVED_BUCKET, Key=SERVED_KEY)
served = body_json(sr)
period = served["period"]
s_model_aum = c2(served["total"]["model_aum"])
s_rows = [(r["model_name"], c2(r["aum"])) for r in served["by_model"]]
s_sum = c2(sum(a for _, a in s_rows))
s_gap = c2(s_model_aum - s_sum)
print("== SERVED ==")
print(f"key             s3://{SERVED_BUCKET}/{SERVED_KEY}")
print(f"VersionId       {sr.get('VersionId')}")
print(f"LastModified    {sr['LastModified'].isoformat()}")
print(f"ContentEncoding {sr.get('ContentEncoding')}")
print(f"period          {period}")
print(f"last_updated    {served.get('last_updated')}")
print(f"total.aum       {fmt(served['total']['aum'])}")
print(f"total.model_aum {s_model_aum:,.2f}")
for name, a in s_rows:
    print(f"  by_model  {name:<28} {a:>18,.2f}")
print(f"sum(by_model[].aum) {s_sum:,.2f}   rows={len(s_rows)}")
print(f"GAP served = total.model_aum - sum(by_model[].aum) = {s_gap:,.2f}")

# ---- 2. the gold fold input for that period ---------------------------------------------
gold_bucket, gold_key = prod.ASSETS_BUCKET, prod.AGG_GLOBAL_KEY
print()
print("== GOLD FOLD INPUT (dim_mdpf_aum_metrics.py AGG_GLOBAL_KEY) ==")
versions = []
for listing in s3.get_paginator("list_object_versions").paginate(Bucket=gold_bucket, Prefix=gold_key):
    versions.extend(v for v in listing.get("Versions", []) if v["Key"] == gold_key)
versions.sort(key=lambda v: v["LastModified"], reverse=True)
print(f"versions listed {len(versions)} (all pages); choosing the newest with LastModified <= served "
      f"LastModified and as_of_last == {period}")
fold, fold_ver = None, None
loads = 0
for v in versions:
    if v["LastModified"] > sr["LastModified"]:
        continue
    loads += 1
    doc = body_json(s3.get_object(Bucket=gold_bucket, Key=gold_key, VersionId=v["VersionId"]))
    if (doc.get("as_of_last") or doc["dates"][-1]) == period:
        fold, fold_ver = doc, v
        break
    if loads >= 12:
        break
if fold is None:
    print(f"ERROR: no fold version with as_of_last == {period} within {loads} loads")
    sys.exit(2)
print(f"key             s3://{gold_bucket}/{gold_key}")
print(f"VersionId       {fold_ver['VersionId']}")
print(f"LastModified    {fold_ver['LastModified'].isoformat()}  (served LastModified {sr['LastModified'].isoformat()})")
print(f"as_of_last      {fold.get('as_of_last')}   n_dates={len(fold['dates'])}   "
      f"meta.generated_at={(fold.get('meta') or {}).get('generated_at')}   versions loaded={loads}")
dates = fold["dates"]
gi = dates.index(fold.get("as_of_last") or dates[-1])
f_model_aua = c2(fold["model_aua"][gi])
pcs = fold.get("point_class") or [None] * len(dates)
print(f"model_aua frontier (row {gi}, {dates[gi]}) {f_model_aua:,.2f}   point_class={pcs[gi]}")
print(f"model_aua _frontier() {fmt(prod._frontier(fold['model_aua']))}")

print("per-key frontiers (fold by_model, every key):")
print(f"  {'model_key':<38} {'cohort':<6} {'in MODEL_ORDER':<14} {'value@frontier':>18} {'_frontier()':>18}")
rows = []
for mk, node in fold["by_model"].items():
    mv = node.get("model_value") or []
    at = mv[gi] if gi < len(mv) else None
    fr = prod._frontier(mv)
    rows.append((mk, node.get("cohort_class"), mk in prod.MODEL_ORDER, at, fr, node.get("display_name")))
    print(f"  {mk:<38} {str(node.get('cohort_class')):<6} {str(mk in prod.MODEL_ORDER):<14} "
          f"{fmt(at):>18} {fmt(fr):>18}")

# The producer's own per-key rule (:497-512): MODEL_ORDER keys, cohort 'model', value at the
# frontier row, falling back to the last real value.
served_rule = {}
for mk in prod.MODEL_ORDER:
    node = fold["by_model"].get(mk)
    if node is None or node.get("cohort_class") != "model":
        continue
    mv = node.get("model_value") or []
    cur = mv[gi] if gi < len(mv) else None
    if cur is None:
        cur = prod._frontier(mv)
    if cur is None:
        continue
    served_rule[mk] = c2(cur)
g_sum = c2(sum(served_rule.values()))
g_gap = c2(f_model_aua - g_sum)
cohort_model_all = c2(sum(c2(r[3]) for r in rows if r[1] == "model" and r[3] is not None))
outside = [(r[0], r[5], c2(r[3])) for r in rows if r[1] == "model" and not r[2] and r[3] is not None]
outside_sum = c2(sum(v for _, _, v in outside))
non_model = [(r[0], r[1], c2(r[3])) for r in rows if r[1] != "model" and r[3] is not None]
diff_sg = abs(c2(s_gap - g_gap))
print()
print("== REPRODUCTION ==")
print(f"producer MODEL_ORDER ({PRODUCER_REL}@{HEAD}) = {len(prod.MODEL_ORDER)} keys")
print(f"sum over MODEL_ORDER keys by the :497-512 rule = {g_sum:,.2f}")
print(f"GAP gold = model_aua frontier - that sum = {g_gap:,.2f}")
print(f"GAP served {s_gap:,.2f}  vs  GAP gold {g_gap:,.2f}  |diff| = {diff_sg:.2f}  "
      f"-> {'REPRODUCED within 0.01' if diff_sg <= 0.01 else 'NOT REPRODUCED'}")
row_match = 0
served_by_name = dict(s_rows)
for mk, v in served_rule.items():
    sv = served_by_name.get(prod.SERVED_MODEL_NAME[mk])
    row_match += int(sv is not None and abs(c2(sv - v)) <= 0.01)
print(f"served by_model rows equal to the fold's per-key value: {row_match} of {len(served_rule)}")
print(f"identity: sum of ALL cohort 'model' keys at frontier = {cohort_model_all:,.2f}; "
      f"model_aua - that = {c2(f_model_aua - cohort_model_all):,.2f}")
print(f"cohort 'model' keys OUTSIDE MODEL_ORDER: {len(outside)} -> "
      + "; ".join(f"{k} ({d}) {v:,.2f}" for k, d, v in outside))
print(f"their sum {outside_sum:,.2f}; GAP gold - their sum = {c2(g_gap - outside_sum):,.2f}")
print("non-model cohort keys (not in model_aua): " + "; ".join(f"{k} [{c}] {v:,.2f}" for k, c, v in non_model))

# ---- 3. control arm ------------------------------------------------------------------
ctl_rows = [list(r) for r in s_rows]
ctl_rows[0][1] = c2(ctl_rows[0][1] + 1.00)
ctl_gap = c2(s_model_aum - c2(sum(a for _, a in ctl_rows)))
moved = abs(c2(s_gap - ctl_gap))
print()
print("== CONTROL ==")
print(f"raised by_model row '{ctl_rows[0][0]}' by 1.00 in memory -> computed gap {ctl_gap:,.2f} "
      f"(was {s_gap:,.2f}); gap moved by {moved:.2f} -> {'FIRED (exactly 1.00)' if moved == 1.00 else 'DID NOT FIRE'}")

# ---- 4. the explanation note ---------------------------------------------------------
explained = diff_sg <= 0.01 and abs(c2(g_gap - outside_sum)) <= 0.01 and len(outside) > 0
verdict = "DEFECT" if explained else "UNDETERMINED"
outside_txt = "; ".join(f"`{k}` (fold display_name '{d}', cohort_class 'model') {v:,.2f}" for k, d, v in outside)
note = f"""# AF1-s-1 -- the gap between the per-model rows and Opal's model total, explained

**Task order:** POSN_AGGFIX.TO-A1-1 (cell AF1-s-1, C-GAP-EXPLAINED). **Author:** 0.9.0_WK_POSN_AGGFIX~1.
**Produced by:** `a1_gap_explain.py` beside this file, run at workspace `{HEAD}`. Every AMOUNT, VersionId and count below is
printed by that run; line and commit citations are the author's reads at `{HEAD}`.

## The served file

- `s3://{SERVED_BUCKET}/{SERVED_KEY}` VersionId `{sr.get('VersionId')}`, LastModified {sr['LastModified'].isoformat()}, period **{period}**.
- `total.model_aum` = {s_model_aum:,.2f}; `sum(by_model[].aum)` over {len(s_rows)} rows = {s_sum:,.2f}.
- **Gap = {s_gap:,.2f}.**

## The gold input, and the gap reproduced from it

- `s3://{gold_bucket}/{gold_key}` VersionId `{fold_ver['VersionId']}`, LastModified {fold_ver['LastModified'].isoformat()},
  `as_of_last` {fold.get('as_of_last')}. This is the object `dim_mdpf_aum_metrics.py` reads as `AGG_GLOBAL_KEY` (`:54`, `:114`),
  at the newest version written before the served file.
- `model_aua` at the frontier row = {f_model_aua:,.2f}. The producer serves this value, rounded, as `total.model_aum`
  (`compose_current` `:184`, `:234`; `build_aum_metrics` `:488`, `:541`).
- The fold carries {len(rows)} `by_model` keys. The producer's per-key loop (`:497-512`) walks only its fixed `MODEL_ORDER` tuple
  (`:94-102`, {len(prod.MODEL_ORDER)} keys), keeping cohort `model`. Those {len(served_rule)} keys sum to {g_sum:,.2f}.
  **Gap from gold = {g_gap:,.2f}**; it differs from the served gap by {diff_sg:.2f}. Of the served rows, {row_match} of
  {len(served_rule)} equal the fold's per-key value.
- The sum of ALL cohort `model` keys at the frontier is {cohort_model_all:,.2f}; `model_aua` minus that sum =
  {c2(f_model_aua - cohort_model_all):,.2f}. So `model_aua` is exactly the sum of the fold's cohort `model` keys.
- Cohort `model` keys the fold carries but `MODEL_ORDER` does not list: {len(outside)}. They are {outside_txt},
  summing to {outside_sum:,.2f}. The gap minus that sum = {c2(g_gap - outside_sum):,.2f}.
- Keys with another cohort ({', '.join(f'{k} [{c}]' for k, c, _ in non_model)}) are not in `model_aua`, so they are
  not part of this gap.
- Control arm: one served `by_model` row raised by 1.00 in memory moved the computed gap by {moved:.2f}.

## What the gap is

The gap is **the Fixed Income model's assets** (`opal_fixed_income`). The global fold counts that key in `model_aua`, and so
in the served `total.model_aum`. The served `by_model` has no row for it: `dim_mdpf_aum_metrics.py` builds its rows from a
fixed seven-key `MODEL_ORDER` (5 primary models + 2 blends) and has no `SERVED_MODEL_NAME` entry for Fixed Income.

The key joined the fold's `GLOBAL_MODEL_KEYS` at `2d5f8a7f74` (2026-08-26; `dim_mdpf_aggregate_aua_timeseries.py:126-140`).
That comment lists the files that must change in the same commit when a key is added, and `dim_mdpf_aum_metrics.py` is not
on the list. `dim_mdpf_aum_metrics.py` was last changed at `4707880967` (2026-08-06), before the key existed.

The crosswalk (`mdpf_revamp_model_crosswalk.py:126-139`) records Fixed Income as `served=False`, meaning "not in the 49F
SmartX served by_model{{7}} projection", and says "model_aua already carries these dollars -- by_model was the SHORT side".
The two blends in these served rows are `served=False` too, so that flag does not decide which keys get a row here.

{verdict}: against the producer's own stated contract. `dim_mdpf_aum_metrics.py:31-32` defines `by_model` as
"cohort_class=='model' ONLY", and `:27-28` defines `total.model_aum` as the `model_aua` frontier. The fold marks
`opal_fixed_income` cohort `model` and counts it in `model_aua`, yet the served rows omit it, so they fall short of
`total.model_aum` by exactly its value. The mechanism is a fixed key tuple (`:94-102`, walked at `:497`) that did not grow
when the fold's key set grew; the same tuple would silently omit any later cohort `model` key too. The producer's owner is
`0.4.0_DS_ClientPlatform` (Author line `:39`, gate `1.0.0_SA_CTO`). This project edits nothing there; the surprise row
POSN_AGGFIX-Z-W1-S1 carries the finding.

## What this means for the Positioning aggregate (read-only note)

Fixed Income is not a primary model and not a blend of primary models (`org/standards/POSN_AGGREGATE_MODEL_SET.json` v1.0).
Under that standard's `membership_rule`, its {outside_sum:,.2f} falls outside the aggregate and is reported with the assets
left out. The standard's `measured_against.rows_outside_the_rule: 0` counts the seven served `by_model` rows. That count is
right for those rows, but it cannot see this key, because the served rows never carry it.
"""
out = os.path.join(HERE, "AF1_S1_GAP_EXPLANATION.md")
with open(out, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(note)
nb = open(out, "rb").read()
vline = [ln for ln in note.splitlines() if ln.startswith(("DEFECT", "NOT-A-DEFECT", "UNDETERMINED"))]
print()
print(f"WROTE {os.path.relpath(out, ROOT)} ({len(nb)} B, non-ascii={len(nb) - len(nb.decode('utf-8'))}); "
      f"verdict line: {vline[0][:60] if vline else 'MISSING'}")
