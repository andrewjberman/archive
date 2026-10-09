"""The issuer's read of the 13:00Z sweep -- ledger etfs-rivalfunds-r27 L2, ledger etfs-rivalfunds-r28-aw1-dell1-20261009 L2, aw-1 J1.

    python sweep_read.py <page day, e.g. 2026-10-09>      (run from the repository root; read-only)

Reads, for the page day: the served manifest (funds_updated, the AI run record, ai_grounding), the newest AI rows object
(research_hypotheses) and the served index.html. Prints, for the AI rows: run id, prompt version, rows per kind, grounding
PASS/FAIL, period codes left in any text field (ai_accounts' own _CODE_RE), items whose text lacks its period's two dates,
corrections and attached figures from input_manifest, and the Direction Verdict opening census (dates read as one token).
A count is printed with its denominator; nothing is graded here -- J1 is the CVO's.
"""
import collections
import io
import json
import os
import re
import sys

import boto3
import pandas as pd

sys.path.insert(0, os.path.join(os.getcwd(), "data", "etfs", "scripts"))
from rivalfunds import ai_accounts as A  # noqa: E402

DAY = sys.argv[1]
B = "opal-data-etfs"
s3 = boto3.client("s3", region_name="us-east-1")
m = json.loads(s3.get_object(Bucket=B, Key=f"rivalfunds/etfs/platinum/page/date={DAY}/manifest.json")["Body"].read())
print(f"manifest: generated_at {m.get('generated_at')} batch {m.get('batch_id')} funds_updated {m.get('funds_updated')} of "
      f"{m.get('funds_total')}")
print("AI run record:", json.dumps((m.get("a1_produced") or {}).get("research_hypotheses_run")))
print("ai_grounding:", json.dumps(m.get("ai_grounding"))[:400])

pre = f"rivalfunds/etfs/gold/research_hypotheses/date={DAY}/"
objs = []
for page in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix=pre):
    objs += page.get("Contents", [])
print(f"AI rows objects under {pre}: {len(objs)}")
if not objs:
    print("NO AI ROWS for the day")
    sys.exit(2)
newest = max(objs, key=lambda o: o["LastModified"])
df = pd.read_parquet(io.BytesIO(s3.get_object(Bucket=B, Key=newest["Key"])["Body"].read()))
print(f"newest: {newest['Key']} ({newest['LastModified']}); rows {len(df)}; run_id {sorted(df['run_id'].unique())}; "
      f"prompt_version {sorted(df['prompt_version'].unique())}")
for kind, g in df.groupby("kind"):
    print(f"  {kind}: {len(g)} rows; grounding {dict(collections.Counter(g['grounding']))}")
codes, nodates, corr, attached = [], [], 0, 0
for _, r in df.iterrows():
    body = " ".join([str(r["text"]), str(r["invalidation"])] + json.loads(r["observed"] or "[]") + json.loads(r["inferred"] or "[]"))
    found = sorted({x.group(1).upper() for x in A._CODE_RE.finditer(body)})
    if found:
        codes.append(f"{r['fund_id']}/{r['kind']}: {found}")
    if len(re.findall(r"\d{4}-\d{2}-\d{2}", str(r["text"]))) < 2:
        nodates.append(f"{r['fund_id']}/{r['kind']}")
    im = json.loads(r["input_manifest"] or "{}")
    corr += int(im.get("corrections") or 0)
    attached += int(im.get("attached_figures") or 0)
print(f"period codes left: {len(codes)} of {len(df)} items {codes}")
print(f"items whose text carries fewer than two ISO dates: {len(nodates)} of {len(df)} {nodates}")
print(f"corrections sent: {corr}; attached figures: {attached} (over {len(df)} items)")
fails = df[df["grounding"] != "PASS"]
for _, r in fails.iterrows():
    print(f"  FAIL {r['fund_id']}/{r['kind']}: {str(r['grounding_reason'])[:200]}")
dv = df[df["kind"] == "direction_verdict"]
ops = [" ".join(re.sub(r"\d{4}-\d{2}-\d{2}", "<date>", str(t)).split()[:4]).lower() for t in dv["text"]]
for f, t in zip(dv["fund_id"], dv["text"]):
    print(f"  {f:6} | {' '.join(str(t).split()[:14])}")
if ops:
    top, n = collections.Counter(ops).most_common(1)[0]
    print(f"Direction Verdict openings: {len(ops)}; most shared '{top}' x{n}; a quarter is {len(ops) / 4:.2f} -> "
          f"{'within' if n <= len(ops) / 4 else 'OVER'}")
