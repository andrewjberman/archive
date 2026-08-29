"""INC3-A -- measure the Tax SMA account population and its DECLARED discriminator. READ-ONLY.

TO: D1_CATVIEWS.TO-A3-DS.taxsma-account-population-and-discriminator @c024f32e9f
Author: 0.4.0_DS_ClientPlatform~Z, 2026-08-29.

WHAT THIS ESTABLISHES, AND WHY IT IS NOT THE DOCSTRING
------------------------------------------------------
Three seats located the membership rule in `build_fact_taxsma_report.py:47`'s
"Scope: Chiles-only for now" docstring. That is a SCOPE NOTE dated 2026-07-17 and it is
STALE. The same docstring's next sentence is the operative one -- "this module processes
EVERY ACCOUNT PRESENT IN THE BRONZE PARTITION" -- i.e. the producer applies NO membership
filter at all. The real discriminator is one plane up and is code, not prose:

    taxsma_registry.py:144-149   list_active() -> [a for a in accounts if a["status"] == "active"]
    lambda_function.py:252-273   discover_accounts(): the roster is "the SINGLE source of truth"
    lambda_function.py:315       accounts = event.get("accounts") or discover_accounts()
    ARTIFACT  s3://opal-data-assets/blackdiamond/49f/_ops/taxsma_roster.json  (S3-versioned)

⛔ THE INSTRUMENT TRAP THIS HARNESS EXISTS TO SHOW: measuring progress as "which of the 5
resolve through dim_account_xref" UNDER-REPORTS. The xref is the TIER-1 surface; tier-3
(account-api) resolutions land in the ROSTER and never enter the xref. Two ACTIVE accounts
with resolved BD ids read as unresolved there. Both numbers are printed side by side so the
disagreement is visible rather than inferred.

NO S3 WRITES. NO VENDOR API CALL (the account-api sweep that would resolve Bump/Macy needs
Andrew's per-use egress word and is NOT invoked here). Reads only.

Usage: python inc3a_taxsma_population_measure.py [--xref-date 2026-08-27]
"""
from __future__ import annotations

import argparse
import io
import json
import sys

import boto3
import pandas as pd

BUCKET = "opal-data-assets"
ROSTER_KEY = "blackdiamond/49f/_ops/taxsma_roster.json"
XREF_PREFIX = "blackdiamond/49f/silver/dim_account_xref/"
GOLD_PREFIX = "blackdiamond/49f/gold/dim_taxsma_report/"
BAR = "=" * 88


def normalize_schwab(acct) -> str:
    """taxsma_registry.normalize_schwab, re-implemented locally so this harness has no
    import dependency on the Lambda tree. Digits only, zero-padded to 10, FAIL LOUD."""
    s = str(acct).strip().replace("-", "")
    if not s.isdigit():
        raise ValueError(f"schwab account {acct!r} is not all-digits -- exact-number only")
    if len(s) > 10:
        raise ValueError(f"schwab account {acct!r} has >10 digits")
    return s.zfill(10)


def _latest_xref_key(s3, pinned=None) -> str:
    keys = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=XREF_PREFIX):
        keys += [o["Key"] for o in page.get("Contents", []) if o["Key"].endswith("data.parquet")]
    if not keys:
        raise FileNotFoundError("no dim_account_xref data.parquet -- OUT OF CORPUS, not absence")
    if pinned:
        hit = [k for k in keys if f"date={pinned}/" in k]
        if not hit:
            raise FileNotFoundError(f"no xref partition date={pinned} (have {len(keys)})")
        return hit[0]
    return max(keys)


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--xref-date", default=None, help="pin an xref partition (default: newest)")
    args = ap.parse_args(argv)
    s3 = boto3.client("s3")

    # ---- AC1: the set, with the denominator it was drawn from --------------------------
    head = s3.head_object(Bucket=BUCKET, Key=ROSTER_KEY)
    roster = json.loads(s3.get_object(Bucket=BUCKET, Key=ROSTER_KEY)["Body"].read())
    accts = roster["accounts"]

    print(BAR)
    print("AC1 -- THE TAX SMA ACCOUNT SET, ENUMERATED, WITH ITS DENOMINATOR")
    print(BAR)
    print(f"SOURCE OF TRUTH s3://{BUCKET}/{ROSTER_KEY}")
    print(f"  VersionId {head.get('VersionId')}  LastModified {head['LastModified']}  "
          f"bytes {head['ContentLength']}  schema_version {roster.get('schema_version')}")
    print(f"DENOMINATOR: {len(accts)} enrolled entries = accounts CONSIDERED, not accounts matched")
    print()
    print(f"{'SCHWAB':<12} {'CLIENT':<24} {'STATUS':<19} {'BD_INTERNAL':<12} {'TIER':<8}")
    print("-" * 78)
    for a in accts:
        print(f"{a['schwab_account']:<12} {str(a['client_name'])[:24]:<24} {a['status']:<19} "
              f"{str(a['bd_internal_id'] or '-'):<12} {str(a['resolution_tier'] or '-'):<8}")

    active = [a for a in accts if a["status"] == "active"]
    pending = [a for a in accts if a["status"] == "pending_resolution"]
    print()
    print(f"  ACTIVE  (what discover_accounts() pulls): {len(active)} of {len(accts)}  "
          f"{[a['schwab_account'] for a in active]}")
    print(f"  PENDING (deliberately excluded)        : {len(pending)} of {len(accts)}  "
          f"{[a['schwab_account'] for a in pending]}")
    print(f"  Andrew-direct population = 5; roster carries {len(accts)}. "
          f"INDEPENDENT INSTRUMENTS AGREE: {len(accts) == 5}")

    # ---- the instrument test ------------------------------------------------------------
    xkey = _latest_xref_key(s3, args.xref_date)
    x = pd.read_parquet(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=xkey)["Body"].read()))
    xs = {str(v).strip() for v in x["schwab_account_id"].dropna()}
    xs = {v.zfill(10) if v.isdigit() else v for v in xs}

    print()
    print(BAR)
    print("INSTRUMENT TEST -- 'which of the 5 resolve through dim_account_xref' UNDER-REPORTS")
    print(BAR)
    print(f"xref {xkey}  rows={len(x)}  distinct non-null schwab_account_id={len(xs)}")
    print()
    print(f"{'SCHWAB':<12} {'CLIENT':<24} {'IN_XREF?':<10} {'ROSTER_STATUS':<19} {'TIER':<8}")
    print("-" * 78)
    in_xref = 0
    for a in accts:
        k = normalize_schwab(a["schwab_account"])
        hit = k in xs
        in_xref += int(hit)
        print(f"{k:<12} {str(a['client_name'])[:24]:<24} {('YES' if hit else 'no'):<10} "
              f"{a['status']:<19} {str(a['resolution_tier'] or '-'):<8}")
    print()
    print(f"  xref-resolved : {in_xref} of {len(accts)}")
    print(f"  roster-active : {len(active)} of {len(accts)}")
    print(f"  DISAGREEMENT  : {in_xref != len(active)}   "
          "<- tier-3 resolutions land in the ROSTER, never in the tier-1 xref")

    # ---- AC3: negative controls ---------------------------------------------------------
    print()
    print(BAR)
    print("AC3 -- NEGATIVE CONTROL ON THE DISCRIMINATOR (three independent arms)")
    print(BAR)
    roster_keys = {normalize_schwab(a["schwab_account"]) for a in accts}
    outside = sorted(xs - roster_keys)
    print(f"ARM 1 -- NOT ENROLLED: {len(outside)} of {len(xs)} xref accounts are absent from the "
          "roster and are never pulled.")
    if outside:
        print(f"  named exemplar EXCLUDED: {outside[0]} (in the 49F xref, absent from the roster)")
    print()
    print("ARM 2 -- ENROLLED BUT STATUS-GATED (an OBSERVED refusal of named accounts):")
    for a in pending:
        print(f"  {a['schwab_account']} ({a['client_name']}): status={a['status']}, "
              f"bd_internal_id={a['bd_internal_id']} -> list_active() EXCLUDES it")
    print(f"  list_active() admits {len(active)} of {len(accts)} enrolled accounts.")
    print()
    print("ARM 3 -- KEY-SHAPE GATE refuses a fuzzy/last-4 input (never silently coerces):")
    for bad in ("27265115x", "last4-5115", "00272651159999"):
        try:
            normalize_schwab(bad)
            print(f"  {bad!r:<18} -> ACCEPTED   <-- CONTROL FAILED")
        except ValueError:
            print(f"  {bad!r:<18} -> RAISES ValueError (fail-loud)")

    # ---- AC4: reconcile against the one known-good number -------------------------------
    print()
    print(BAR)
    print("AC4 -- RECONCILE AGAINST THE ONE KNOWN-GOOD NUMBER")
    print(BAR)
    gold = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=GOLD_PREFIX):
        gold += [o["Key"] for o in page.get("Contents", [])]
    print(f"gold objects under {GOLD_PREFIX}: {len(gold)}")
    for k in sorted(gold):
        print(f"  {k}")
    known = "0027265115"
    hit = [a for a in accts if normalize_schwab(a["schwab_account"]) == known]
    print()
    print(f"  {known} present in the derived set: {bool(hit)}")
    if hit:
        h = hit[0]
        print(f"    client={h['client_name']} status={h['status']} tier={h['resolution_tier']} "
              f"bd_internal_id={h['bd_internal_id']}")
        print("    -> RECONCILES. The derivation does not drop the only account ever produced.")
    print()
    print("  ⛔ The gold PARTITION COUNT is NOT the coverage denominator (3.0.0_SA_CVO~Z 15875:")
    print("     three bare groupby calls drop NULL keys). The denominator is the ROSTER.")
    print()
    print(BAR)
    print(f"COVERAGE TODAY: gold holds {len(gold)} of {len(accts)} enrolled accounts. "
          f"A bronze pull would reach {len(active)} of {len(accts)}.")
    print(f"5 of {len(accts)} additionally requires the tier-3 account-api sweep on "
          f"{[a['schwab_account'] for a in pending]} -- Andrew's per-use egress word. NOT invoked here.")
    print(BAR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
