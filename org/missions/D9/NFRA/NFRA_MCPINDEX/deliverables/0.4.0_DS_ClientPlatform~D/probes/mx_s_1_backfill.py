#!/usr/bin/env python3
"""MX-s-1 step 3 -- backfill TrueShares holdings bronze -> silver fact_holdings.

Runs the REPO converter (the fixed bytes), not the deployed Lambda, which still
predates _convert_trueshares_holdings. Rule 13: DS owns these silver scripts and
their QA deploy.

IDEMPOTENT by construction: convert_trueshares skips a date whose silver partition
already exists (partition_exists) unless --force. Nothing is ever deleted.

Usage:
    python mx_s_1_backfill.py --list                 # read-only inventory
    python mx_s_1_backfill.py --date 2026-08-24      # one date, both funds
    python mx_s_1_backfill.py --all                  # every pending date
"""
import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = _HERE
for _ in range(12):
    if os.path.isdir(os.path.join(_ROOT, "data", "assets", "scripts", "silver")):
        break
    _ROOT = os.path.dirname(_ROOT)
sys.path.insert(0, os.path.join(_ROOT, "data", "assets", "scripts", "silver"))
sys.path.insert(0, os.path.join(_ROOT, "data", "assets", "scripts", "lib"))

import boto3  # noqa: E402

import etf_conversion as ec  # noqa: E402
import mirror_conversion as mc  # noqa: E402

BUCKET = os.environ.get("MONOLITH_BUCKET", "opal-data-assets")
FUNDS = ("DIVZ", "IDVZ")


def bronze_holdings(s3, fund):
    prefix = "trueshares/" + fund + "/bronze/holdings/"
    return sorted(k for k in mc._list_all(s3, prefix, BUCKET) if k.endswith(".csv"))


def silver_holdings(s3, fund):
    prefix = "trueshares/" + fund + "/silver/fact_holdings/"
    return sorted(k for k in mc._list_all(s3, prefix, BUCKET)
                  if k.endswith("/data.parquet"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--date", default="")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    s3 = boto3.client("s3", region_name="us-east-1")

    print("=== INVENTORY (read-only) ===", flush=True)
    pending = []
    for fund in FUNDS:
        b = bronze_holdings(s3, fund)
        sv = silver_holdings(s3, fund)
        have = {k.split("date=")[1].split("/")[0] for k in sv}
        bdates = [ec.classify_key(k).date for k in b]
        miss = [d for d in bdates if d not in have]
        print("  %s  bronze=%d dates(%s..%s)  silver=%d  pending=%d"
              % (fund, len(b), bdates[0] if bdates else "-",
                 bdates[-1] if bdates else "-", len(sv), len(miss)), flush=True)
        for k, d in zip(b, bdates):
            if args.date and d != args.date:
                continue
            if d in have and not args.force:
                continue
            pending.append((fund, d, k))

    if args.list:
        print("\n  pending units: %d" % len(pending), flush=True)
        for fund, d, k in pending:
            print("    %s %s  %s" % (fund, d, k), flush=True)
        print("\nREAD-ONLY: nothing written.", flush=True)
        return 0

    if not (args.all or args.date):
        print("\nRefusing: pass --list, --date <YYYY-MM-DD> or --all.", flush=True)
        return 2

    print("\n=== CONVERT (%d unit(s)) ===" % len(pending), flush=True)
    wrote, skipped, failed = [], [], []
    for fund, d, k in pending:
        try:
            r = ec.convert_trueshares(s3, k, force=args.force, bucket=BUCKET)
        except Exception as exc:
            failed.append((fund, d, repr(exc)))
            print("  FAIL   %s %s  %r" % (fund, d, exc), flush=True)
            continue
        if r.action == "converted":
            wrote.extend(r.silver_keys)
            print("  OK     %s %s  rows_in=%s rows_out=%s -> %s"
                  % (fund, d, r.rows_in, r.rows_out, r.silver_keys[0]), flush=True)
        elif r.action == "skipped-idempotent":
            skipped.append((fund, d))
            print("  SKIP   %s %s  already present" % (fund, d), flush=True)
        else:
            failed.append((fund, d, r.action + " " + str(r.reason)))
            print("  OTHER  %s %s  action=%s reason=%s"
                  % (fund, d, r.action, r.reason), flush=True)

    print("\n=== KEYS WRITTEN (%d) ===" % len(wrote), flush=True)
    for k in wrote:
        print("  " + k, flush=True)
    print("\nconverted=%d skipped_idempotent=%d failed=%d"
          % (len(wrote), len(skipped), len(failed)), flush=True)
    for fund, d, why in failed:
        print("  FAILED %s %s -- %s" % (fund, d, why), flush=True)

    print("\n=== POST-STATE (live re-read) ===", flush=True)
    for fund in FUNDS:
        b = bronze_holdings(s3, fund)
        sv = silver_holdings(s3, fund)
        print("  %s  bronze=%d  silver=%d" % (fund, len(b), len(sv)), flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
