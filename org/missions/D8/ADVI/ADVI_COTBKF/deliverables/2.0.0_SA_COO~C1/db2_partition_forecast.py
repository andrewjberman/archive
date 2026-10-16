"""ADVI_COTBKF round 106 (issuer's forecast): which silver/account_attributes partitions will the first incremental run write, and what will gold find in the newest?

Read-only. Downloads every forwardfill_v2/account_attributes workbook from opal-data-cot (aws.cmd shim) and applies cot_silver_merge.py's own date rule (the 'End Date'
row of the Timestamps sheet, else the date in the file name) and its own dedup (account_id + portfolio_group, keep first). Prints counts only; no account id.
  python db2_partition_forecast.py
    PARTITION-FORECAST bronze_files=<n> manifest_processed=<n> to_process=<n> distinct_partition_dates=<n> same_date_collisions=<n>
        overwrites_existing_partition=<bool> newest_partition=<date> newest_rows=<n> newest_accounts=<n> newest_multibook=<n> newest_flag_disagree=<n>
Rules: manifest_processed = the bronze file names in the manifest's processed_etags (an unchanged etag is skipped; a changed etag is a re-land and is processed again);
to_process = bronze files not skipped; same_date_collisions = to_process files that map to a partition date another to_process file also maps to (the later file wins);
overwrites_existing_partition = a to_process file maps to a date for which silver/account_attributes/<date>.parquet exists today; the newest_* counts are for the file
the run writes LAST for the newest date, which is the partition gold's sorted-last read takes; newest_flag_disagree = multi-row accounts there whose supervised, billable or
position_only values are not all equal (the case A_00 refuses the build on).
"""
import json
import re
import subprocess
import tempfile
from pathlib import Path

import pandas as pd

BUCKET = "opal-data-cot"
REPO = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or ".")
AWS = str(REPO / ".tools" / "aws.cmd")


def aws(*a):
    return subprocess.run([AWS, *a], capture_output=True, text=True)


tmp = Path(tempfile.mkdtemp(prefix="db2_fc_"))
ls = aws("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", "forwardfill_v2/account_attributes/ACCOUNT_ATTRIBUTES_DAILY_", "--output", "json")
objs = json.loads(ls.stdout).get("Contents", []) if ls.returncode == 0 and ls.stdout.strip() else []
if not objs:
    raise SystemExit("listing failed or empty")
aws("s3", "cp", "s3://%s/silver/cot_incremental_manifest_account_attributes.json" % BUCKET, str(tmp / "m.json"), "--only-show-errors")
manifest = json.load(open(tmp / "m.json"))
etags = manifest.get("processed_etags") or {}
sil = aws("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", "silver/account_attributes/", "--output", "json")
existing = {o["Key"].rsplit("/", 1)[-1][:-8] for o in (json.loads(sil.stdout).get("Contents", []) if sil.stdout.strip() else [])}

todo = []
for o in objs:
    name = o["Key"].rsplit("/", 1)[-1]
    if etags.get(name) is not None and etags[name].strip('"') == o["ETag"].strip('"'):
        continue
    todo.append((name, o["Key"]))


def part_date(path, name):
    try:
        ts = pd.read_excel(path, sheet_name="Timestamps", header=None)
        for _, row in ts.iterrows():
            if str(row.iloc[0]).strip() == "End Date":
                dt = pd.to_datetime(row.iloc[1], errors="coerce")
                if pd.notna(dt):
                    return dt.strftime("%Y-%m-%d")
    except Exception:
        pass
    m = re.search(r"(\d{4}-\d{2}-\d{2})", name)
    return m.group(1) if m else "unknown"


dates = {}
for name, key in sorted(todo):
    p = tmp / name
    aws("s3", "cp", "s3://%s/%s" % (BUCKET, key), str(p), "--only-show-errors")
    dates[name] = part_date(p, name)
vals = list(dates.values())
collide = sum(1 for v in vals if vals.count(v) > 1)
newest = max(vals) if vals else ""
last_file = sorted(n for n, d in dates.items() if d == newest)[-1] if vals else ""
rows = accts = mb = dis = 0
if last_file:
    df = pd.read_excel(tmp / last_file, sheet_name="Sheet1", dtype=str).rename(columns={
        "AccountID": "account_id", "Portfolio Group": "portfolio_group", "Position Only": "position_only",
        "Account Supervised": "supervised", "Account Billable": "billable"})
    for c in ("account_id", "portfolio_group", "position_only", "supervised", "billable"):
        df[c] = df[c].fillna("").astype(str).str.strip()
    df = df.drop_duplicates(subset=["account_id", "portfolio_group"], keep="first")
    rows, accts = len(df), df["account_id"].nunique()
    dup = df[df.duplicated(subset=["account_id"], keep=False)]
    mb = dup["account_id"].nunique()
    dis = int((dup.groupby("account_id")[["supervised", "billable", "position_only"]].nunique() > 1).any(axis=1).sum()) if len(dup) else 0
print("PARTITION-FORECAST bronze_files=%d manifest_processed=%d to_process=%d distinct_partition_dates=%d same_date_collisions=%d "
      "overwrites_existing_partition=%s newest_partition=%s newest_rows=%d newest_accounts=%d newest_multibook=%d newest_flag_disagree=%d"
      % (len(objs), len(etags), len(todo), len(set(vals)), collide, bool(set(vals) & existing), newest, rows, accts, mb, dis))
