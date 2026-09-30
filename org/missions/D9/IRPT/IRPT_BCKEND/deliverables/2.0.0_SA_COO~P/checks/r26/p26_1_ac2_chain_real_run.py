"""Round 26 AC (IB-pr-261, rows W86-S1 / S216) -- ONE REAL RUN of the INF gold chain, after the ship, reaches the raw
writers: INF_API_SILVER_REPS ok (the step that has failed daily since 2026-09-28) and INF_API_PULL_POSITIONS_DAILY ok,
and the run date's raw positions file exists.

Usage: python p26_1_ac2_chain_real_run.py
Reads (read-only, four S3 calls):
  s3://opal-data-inf/telemetry/inf-gold-layer-runner/status.json   -- the runner's own status
  s3://opal-data-inf/bronze/positions/<run date>.jsonl.gz            -- HeadObject
Requires: run_id newer than chain_full_20260930_113346 (the 11:33Z scheduled run that failed at step 3, read at the
cut); steps_done carries INF_API_SILVER_REPS status ok AND INF_API_PULL_POSITIONS_DAILY status ok; the raw positions
jsonl.gz for the run date has LastModified after 2026-09-30T12:00:00Z.
Pass line: P26-1-AC2 PASS. Base (at the cut): FAIL -- status.json reads run chain_full_20260930_113346 status failed,
steps_done = PULL_UNIFIED ok, PULL_REPS ok, SILVER_REPS fail.
"""
import datetime as dt
import json
import sys

import boto3

BUCKET = "opal-data-inf"
BASE_RUN = "chain_full_20260930_113346"
CUT = dt.datetime(2026, 9, 30, 12, 0, tzinfo=dt.timezone.utc)


def fail(msg):
    print("P26-1-AC2 FAIL: " + msg)
    sys.exit(1)


s3 = boto3.client("s3", region_name="us-east-1")
try:
    st = json.loads(s3.get_object(Bucket=BUCKET, Key="telemetry/inf-gold-layer-runner/status.json")["Body"].read())
except Exception as exc:  # noqa: BLE001
    fail("status.json unreadable: %s" % str(exc)[:160])

run_id = st.get("run_id", "")
print("  status.json run_id=%s status=%s updated_at=%s" % (run_id, st.get("status"), st.get("updated_at")))
if not run_id or run_id <= BASE_RUN:
    fail("run_id %r is not newer than the base run %s" % (run_id, BASE_RUN))

done = {s.get("name"): s.get("status") for s in st.get("progress", {}).get("steps_done", [])}
for step in ("INF_API_SILVER_REPS", "INF_API_PULL_POSITIONS_DAILY"):
    if done.get(step) != "ok":
        fail("%s status=%r (steps_done: %d)" % (step, done.get(step), len(done)))
    print("  %s ok" % step)

# The run date: the chain's own started_at day (UTC), the day its raw files are keyed by.
try:
    started = dt.datetime.fromisoformat(st["started_at"].replace("Z", "+00:00"))
except Exception:  # noqa: BLE001
    fail("started_at unreadable: %r" % st.get("started_at"))
key = "bronze/positions/%s.jsonl.gz" % started.date().isoformat()
try:
    h = s3.head_object(Bucket=BUCKET, Key=key)
except Exception as exc:  # noqa: BLE001
    fail("raw positions absent: %s (%s)" % (key, str(exc)[:120]))
if h["LastModified"] < CUT:
    fail("%s LastModified %s is before the cut" % (key, h["LastModified"].isoformat()))
print("  raw OK: s3://%s/%s %s bytes at %s" % (BUCKET, key, h["ContentLength"], h["LastModified"].isoformat()))
print("P26-1-AC2 PASS (run %s)" % run_id)
