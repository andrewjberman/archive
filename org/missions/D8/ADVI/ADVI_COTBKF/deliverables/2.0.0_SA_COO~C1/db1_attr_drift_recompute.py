"""ADVI_COTBKF TO-CB-db-1 (issuer's recompute): how far the stale Cottonwood account_attributes silver partition has drifted from the newest bronze pull.

Reads, read-only, with the vendored .tools/aws.cmd shim: silver/account_attributes/2026-08-19.parquet (the only silver partition) and the bronze workbook
forwardfill_v2/account_attributes/ACCOUNT_ATTRIBUTES_DAILY_<date>.xlsx (default 2026-10-15), both in bucket opal-data-cot. Prints counts only; no account id.
  python db1_attr_drift_recompute.py [bronze_date]
    ATTR-DRIFT old_rows=<n> new_rows=<n> old_accounts=<n> new_accounts=<n> added=<n> removed=<n> both=<n> multibook_old=<n> multibook_new=<n>
               changed_supervised=<n> changed_billable=<n> changed_position_only=<n> changed_portfolio_group=<n> changed_any=<n> multibook_flag_disagree_new=<n>
Rules: an account is a distinct AccountID; a flag changes when an account present in both has a different set of values for that column across its rows (a multi-book
account has two rows, so its set of books is compared as a set); added = in the bronze and not in the silver partition; removed = the reverse; multibook = accounts
with more than one row; multibook_flag_disagree_new = multi-row accounts in the bronze whose supervised, billable or position_only values are not all equal
(the case gold A_00 refuses with SystemExit). Values are compared as stripped strings, a blank or missing value as the empty string.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

BUCKET = "opal-data-cot"
DATE = sys.argv[1] if len(sys.argv) > 1 else "2026-10-15"
REPO = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or ".")
AWS = str(REPO / ".tools" / "aws.cmd")


def fetch(key, dest):
    r = subprocess.run([AWS, "s3", "cp", "s3://%s/%s" % (BUCKET, key), str(dest), "--only-show-errors"], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("fetch failed for %s rc=%d" % (key, r.returncode))


tmp = Path(tempfile.mkdtemp(prefix="db1_attr_"))
fetch("silver/account_attributes/2026-08-19.parquet", tmp / "old.parquet")
fetch("forwardfill_v2/account_attributes/ACCOUNT_ATTRIBUTES_DAILY_%s.xlsx" % DATE, tmp / "new.xlsx")
old = pd.read_parquet(tmp / "old.parquet")
new = pd.read_excel(tmp / "new.xlsx", sheet_name="Sheet1", dtype=str)
old = old.rename(columns={"account_supervised": "supervised", "account_billable": "billable"})
new = new.rename(columns={"AccountID": "account_id", "Portfolio Group": "portfolio_group", "Position Only": "position_only",
                          "Account Supervised": "supervised", "Account Billable": "billable"})
cols = ["supervised", "billable", "position_only", "portfolio_group"]
for df in (old, new):
    df["account_id"] = df["account_id"].astype(str).str.strip()
    for c in cols:
        df[c] = df[c].fillna("").astype(str).str.strip()
old_ids, new_ids = set(old["account_id"]), set(new["account_id"])
both = old_ids & new_ids


def sets(df, c):
    return df[df["account_id"].isin(both)].groupby("account_id")[c].agg(lambda s: frozenset(s))


changed = {}
any_changed = set()
for c in cols:
    a, b = sets(old, c), sets(new, c)
    diff = {k for k in both if a[k] != b[k]}
    changed[c] = len(diff)
    any_changed |= diff
mb = lambda df: int((df.groupby("account_id").size() > 1).sum())  # noqa: E731
dup = new[new.duplicated(subset=["account_id"], keep=False)]
disagree = int((dup.groupby("account_id")[["supervised", "billable", "position_only"]].nunique() > 1).any(axis=1).sum()) if len(dup) else 0
print("ATTR-DRIFT old_rows=%d new_rows=%d old_accounts=%d new_accounts=%d added=%d removed=%d both=%d multibook_old=%d multibook_new=%d "
      "changed_supervised=%d changed_billable=%d changed_position_only=%d changed_portfolio_group=%d changed_any=%d multibook_flag_disagree_new=%d"
      % (len(old), len(new), len(old_ids), len(new_ids), len(new_ids - old_ids), len(old_ids - new_ids), len(both), mb(old), mb(new),
         changed["supervised"], changed["billable"], changed["position_only"], changed["portfolio_group"], len(any_changed), disagree))
