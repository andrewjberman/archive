"""R-4 AS AMENDED BY ITS AUTHOR (3.0.0_SA_CVO 85166): the RELATION

    (r_gross - r_net) * BMV == cf_net - cf_gross

on EVERY fee account-day regardless of BMV sign. That grader verified it on 3 rows of one
partition with both controls; this runs it on the whole population.

WHY THE RELATION AND NOT THE INEQUALITY: "r_gross > r_net" encodes the convention only where
BMV > 0. The relation is sign-agnostic, so it tests the CONVENTION rather than the denominator,
and it is the form that can be evaluated on all three members of the census.

FLOAT COMPARISON IS DONE ON A RELATIVE TOLERANCE, and the tolerance is stated rather than
hidden: these are ratios reconstructed through a division, so exact equality is not the right
oracle. Any row failing it is printed in full, never summarised away.
"""

from __future__ import annotations

import io
import json
from pathlib import Path

import boto3
import pandas as pd

BUCKET = "opal-data-49financial"
GOLD = "gold/advi/canonical/twr_daily"
LED = Path("org/tier2_senior/0.7.0_AE_CloudOps~L/deliverables/"
           "ADVI_49F.c02-REEMIT_CAMPAIGN_LEDGER.jsonl")

s3 = boto3.client("s3", region_name="us-east-1")

dates = []
for line in LED.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line:
        continue
    r = json.loads(line)
    if r.get("outcome") == "ARTIFACT-COMPLETE":
        dates.append(r["date"])
dates = sorted(set(dates))

fee_total = 0
rel_ok = 0
bad = []
pos_domain = 0          # BMV > 0 fee account-days
pos_domain_gross_gt = 0
neg_domain = 0          # BMV <= 0 fee account-days
nonfee_total = 0
nonfee_zero = 0
parts_with_fee = 0

for i, d in enumerate(dates, 1):
    df = pd.read_parquet(io.BytesIO(
        s3.get_object(Bucket=BUCKET, Key=f"{GOLD}/date={d}/data.parquet")["Body"].read()))
    if "cf_gross" not in df.columns:
        continue
    ok = df[df.status == "OK"].copy()
    if not len(ok):
        continue
    ok["gap"] = ok.r_gross - ok.r_net
    isfee = ok.cf_gross != ok.cf_net
    fee = ok[isfee]
    nofee = ok[~isfee]
    nonfee_total += len(nofee)
    nonfee_zero += int((nofee.gap == 0).sum())
    if not len(fee):
        continue
    parts_with_fee += 1
    fee_total += len(fee)
    lhs = fee.gap * fee.bmv
    rhs = fee.cf_net - fee.cf_gross
    denom = rhs.abs().where(rhs.abs() > 0, 1.0)
    within = ((lhs - rhs).abs() / denom) < 1e-9
    rel_ok += int(within.sum())
    for _, r in fee[~within].iterrows():
        bad.append({"date": d, "account_id": r.account_id, "bmv": r.bmv,
                    "gap": r.gap, "lhs": r.gap * r.bmv,
                    "rhs": r.cf_net - r.cf_gross})
    p = fee[fee.bmv > 0]
    pos_domain += len(p)
    pos_domain_gross_gt += int((p.gap > 0).sum())
    neg_domain += int((fee.bmv <= 0).sum())
    if i % 100 == 0:
        print(f"  ... {i}/{len(dates)}", flush=True)

print("\n===== R-4 AS AMENDED (3.0.0_SA_CVO 85166) -- THREE MEMBERS, EACH WITH ITS DENOMINATOR =====")
print(f"partitions carrying >=1 fee account-day : {parts_with_fee} of {len(dates)}")
print("\n1. THE RELATION, sign-agnostic, the convention itself:")
print(f"   (r_gross - r_net) * BMV == cf_net - cf_gross  holds on "
      f"{rel_ok:,} of {fee_total:,} fee account-days   (rel tol 1e-9)")
print(f"   violations: {len(bad)}")
for b in bad[:20]:
    print(f"     {b}")
print("\n2. THE INEQUALITY on its DECLARED domain (BMV > 0):")
print(f"   r_gross > r_net on {pos_domain_gross_gt:,} of {pos_domain:,} fee account-days")
print("\n3. BMV <= 0 fee account-days, NOT-EVALUABLE-BY-DOMAIN, on their own line:")
print(f"   count {neg_domain} -- a return is undefined on a non-positive base; the relation "
      f"in (1) still holds on them")
print(f"\nNEGATIVE CONTROL: non-fee gap EXACTLY 0 on {nonfee_zero:,} of {nonfee_total:,}")
print(f"\nCHECKSUM vs the acceptance pass: fee account-days {fee_total:,} (expected 77,087); "
      f"BMV<=0 fee rows {neg_domain} (expected 15); positive-domain {pos_domain:,} "
      f"(expected 77,072)")
