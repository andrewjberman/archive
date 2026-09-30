"""Round 26 AC (IB-pr-261, row W86-S1) -- lib/silver_ids.py is SHIPPED to where the gold runner resolves it, and the
two readings the CTO required (ROUND_ANALYSIS.round25P_sweep3_4.md section 1) are on the record BEFORE the copy.

Usage: python p26_1_ac1_silver_ids_shipped.py <worktree root>

Reads <root>/org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~97/RESOLUTION_READINGS.json, which the
worker writes from its own reading, with these keys (every one required, none may be empty):
  sync_layout        -- how orion-gold-dispatch.sh sync_scripts() lays the synced prefixes out on the box (cite lines)
  deployed_dispatch  -- s3 key + sha256 of the deployed dispatch script and whether it equals the repo copy
  sys_path_reading   -- what sys.path a chain step builds, and where the name `lib` therefore resolves (cite lines)
  resolved_targets   -- list of {"s3_key": ..., "repo_path": ..., "sha256": ...}: every object the ship wrote
  collision_census   -- list of {"s3_key": ..., "http": 404|200}: the same basename probed in every OTHER synced prefix
Then, for every resolved target, GetObject on opal-data-inf and compares sha256 to the worktree file at repo_path.
Every target must match; every collision probe must read 404 (a 200 with different bytes fails the flat sync loud).
Pass line: P26-1-AC1 PASS. Base (before the cell): FAIL -- the deliverable does not exist.
"""
import hashlib
import json
import sys
from pathlib import Path

import boto3

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
rec = root / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~97/RESOLUTION_READINGS.json"
BUCKET = "opal-data-inf"


def fail(msg):
    print("P26-1-AC1 FAIL: " + msg)
    sys.exit(1)


if not rec.exists():
    fail("readings deliverable absent: %s" % rec)
try:
    d = json.loads(rec.read_text(encoding="utf-8"))
except Exception as exc:  # noqa: BLE001
    fail("readings deliverable unreadable: %s" % exc)

for k in ("sync_layout", "deployed_dispatch", "sys_path_reading", "resolved_targets", "collision_census"):
    if not d.get(k):
        fail("reading '%s' missing or empty" % k)
if not isinstance(d["resolved_targets"], list) or not d["resolved_targets"]:
    fail("resolved_targets is not a non-empty list")

s3 = boto3.client("s3", region_name="us-east-1")
checked = 0
for t in d["resolved_targets"]:
    key, rp = t.get("s3_key"), t.get("repo_path")
    if not key or not rp:
        fail("target without s3_key/repo_path: %r" % t)
    local = root / rp
    if not local.exists():
        fail("repo_path missing in worktree: %s" % rp)
    want = hashlib.sha256(local.read_bytes()).hexdigest()
    try:
        body = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    except Exception as exc:  # noqa: BLE001
        fail("GetObject %s: %s" % (key, str(exc)[:160]))
    got = hashlib.sha256(body).hexdigest()
    if got != want:
        fail("sha mismatch at %s: s3 %s != worktree %s" % (key, got[:12], want[:12]))
    print("  target OK: s3://%s/%s sha256 %s == %s" % (BUCKET, key, got[:12], rp))
    checked += 1

probes = 0
for c in d["collision_census"]:
    key = c.get("s3_key")
    if not key:
        fail("collision probe without s3_key: %r" % c)
    try:
        s3.head_object(Bucket=BUCKET, Key=key)
        fail("collision: %s EXISTS in another synced prefix (the flat sync would refuse or clobber)" % key)
    except s3.exceptions.ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code not in ("404", "NoSuchKey", "NotFound"):
            fail("collision probe %s: unexpected %s" % (key, code))
    probes += 1

if probes == 0:
    fail("collision_census probed 0 keys")
print("P26-1-AC1 PASS (targets verified %d, collision probes 404 %d)" % (checked, probes))
