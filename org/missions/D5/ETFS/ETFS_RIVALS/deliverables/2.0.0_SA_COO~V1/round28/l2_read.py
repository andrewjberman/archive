"""The issuer's L2 read of both deploys (WS2/WS3 @b48273e3d0, live 14:49Z; the lookup @b86feccfeb, live 15:22Z) on a page day.

    python l2_read.py <page day, e.g. 2026-10-10> [<coverage snapshot dir, default C:/tmp/rv-ws23-covsnap>]

Read-only. Runs, in order, and prints each section's own result line:
  1. report_lines.py over the 11:00Z chain (10:55-11:40) and the 13:00Z sweep (12:55-13:45) of the day;
  2. sweep_read.py <day> (the AI rows: grounding, codes, dates, $0.0 million, openings);
  3. coverage_snapshot.py compare <snapshot dir> (CTO condition 8: each of the 20 keys unchanged / changed, STOP lines);
  4. corporate_actions: every object under gold/corporate_actions/ written on the day (inferred and void), with each row's
     security_id, event_type, ratio, ex_date and source_url;
  5. the dramatic-move report the daily Lambda logged in the sweep window (the `dramatic_move:` line: cap, candidates,
     searched, calls, written, failed, capped);
  6. Tokio Marine on the served page: every fund chart holding TKOMY_US_Equity, its `adjustment` and gap reasons.
Nothing here grades; the grades are the issuer's (L2, AC2) and the CVO's.
"""
import datetime as dt
import json
import pathlib
import subprocess
import sys

import boto3

DAY = sys.argv[1]
SNAP = sys.argv[2] if len(sys.argv) > 2 else "C:/tmp/rv-ws23-covsnap"
HERE = pathlib.Path(__file__).resolve().parent
B = "opal-data-etfs"
s3 = boto3.client("s3", region_name="us-east-1")
FUNDS = ["BASG", "BIDD", "CGIC", "ETFT", "GQGU", "IDVZ", "INEQ", "PCLG", "PFOE", "SCHY", "TSEL", "TXUE", "WCMG"]


def run(label, args):
    print(f"\n===== {label}: {' '.join(args)}")
    r = subprocess.run([sys.executable] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout + r.stderr).strip().splitlines()
    print("\n".join(out[-40:]))
    print(f"[rc {r.returncode}]")


run("1a REPORT lines, 11:00Z chain", [str(HERE / "report_lines.py"), f"{DAY}T10:55", f"{DAY}T11:40"])
run("1b REPORT lines, 13:00Z sweep", [str(HERE / "report_lines.py"), f"{DAY}T12:55", f"{DAY}T13:45"])
run("2 sweep_read", [str(HERE / "sweep_read.py"), DAY])
run("3 coverage compare", [str(HERE / "coverage_snapshot.py"), "compare", SNAP])

print("\n===== 4 corporate_actions written on the day")
import io  # noqa: E402

import pandas as pd  # noqa: E402

day0 = dt.datetime.fromisoformat(DAY).replace(tzinfo=dt.timezone.utc)
objs = []
for page in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix="rivalfunds/etfs/gold/corporate_actions/"):
    objs += [o for o in page.get("Contents", []) if o["LastModified"] >= day0]
print(f"objects written on or after {DAY}: {len(objs)}")
for o in objs:
    df = pd.read_parquet(io.BytesIO(s3.get_object(Bucket=B, Key=o["Key"])["Body"].read()))
    print(f"  {o['Key'].split('corporate_actions/')[1]} ({o['LastModified']:%H:%M:%SZ}): {len(df)} row(s)")
    if "event_type" in df.columns:
        print(f"    event types: {df['event_type'].astype(str).value_counts().to_dict()}")
    keep = df[df.get("event_type", pd.Series(dtype=str)).astype(str).isin(["split", "merger"])] if "event_type" in df.columns else df
    if "TKOMY" in df.get("security_id", pd.Series(dtype=str)).astype(str).str.cat(sep=" "):
        keep = pd.concat([keep, df[df["security_id"].astype(str).str.contains("TKOMY")]]).drop_duplicates()
    cols = [c for c in ("security_id", "event_type", "ratio", "ex_date", "source_url", "void_revision", "reason") if c in df.columns]
    for rec in keep[cols].head(30).to_dict("records"):  # splits, mergers, voids and TKOMY rows only
        print(f"    {rec}")

print("\n===== 5 the dramatic-move report in the daily Lambda's log")
logs = boto3.client("logs", region_name="us-east-1")
t0 = int(dt.datetime.fromisoformat(f"{DAY}T12:55").replace(tzinfo=dt.timezone.utc).timestamp() * 1000)
t1 = int(dt.datetime.fromisoformat(f"{DAY}T13:45").replace(tzinfo=dt.timezone.utc).timestamp() * 1000)
kw = {"logGroupName": "/aws/lambda/etfs-rivalfunds-daily-lambda", "startTime": t0, "endTime": t1,
      "filterPattern": '"dramatic_move"'}


def _all_events(params):
    """Every matching message of the log group in the window, paginated."""
    out = []
    while True:
        page = logs.filter_log_events(**params)
        out += [e["message"].strip() for e in page.get("events", [])]
        if not page.get("nextToken"):
            return out
        params = dict(params, nextToken=page["nextToken"])


lines = _all_events(kw)
print(f"log lines naming dramatic_move: {len(lines)}")
for ln in lines[:20]:
    print("  " + ln[:300])

print("\n===== 6 Tokio Marine (TKOMY_US_Equity) on the served page")
held = 0
for f in FUNDS:
    try:
        j = json.loads(s3.get_object(Bucket=B, Key=f"rivalfunds/etfs/platinum/page/date={DAY}/charts/{f}.json")["Body"].read())
    except s3.exceptions.NoSuchKey:
        print(f"  {f}: no chart object for {DAY}")
        continue
    v = (j.get("securities") or {}).get("TKOMY_US_Equity")
    if v is None:
        continue
    held += 1
    gaps = [g.get("reason") if isinstance(g, dict) else g for g in (v.get("gaps") or [])]
    print(f"  {f}: adjustment {json.dumps(v.get('adjustment'))[:300]} | gap reasons {gaps[:6]}")
print(f"funds whose chart holds TKOMY_US_Equity: {held} of {len(FUNDS)}")
