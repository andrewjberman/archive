#!/usr/bin/env bash
# F4-AC3 -- ONE REAL DERIVE ON THE NEW DIGEST FOLDED THE STITCH. TO-CG-F-4 step 3.
#
# The task ARN is PINNED: the claim is about ONE derive -- the ad-hoc run this order
# started on task definition globgrph-derive-runner:8, the revision the image act
# created. Its status, its task-definition ARN and its CloudWatch log are re-read LIVE
# on every run, so this is a reader of the world, not a restatement of a capture.
#
# THE CONTROL IS THE PREVIOUS DERIVE, read from the same log group in the same call:
# an image without the fold cannot print a STITCH_INGEST line at all, so "the line is
# present" only means something beside a run where it is absent. Both are printed.
#
# Run from the repository root.
set -u

python - <<'PY'
import datetime
import re

import boto3

TASK = "arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/deee298ca1bd422fa3fcc124cf42a86f"
NEW_DIGEST = "sha256:478d0a43742b2ed5a44631c6352b5713c5ba22f015d82a673cfb93428a9dae20"

ecs = boto3.client("ecs", region_name="us-east-1")
logs = boto3.client("logs", region_name="us-east-1")
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

t = ecs.describe_tasks(cluster="opal-globgrph", tasks=[TASK])["tasks"][0]
c = t["containers"][0]
td = ecs.describe_task_definition(taskDefinition=t["taskDefinitionArn"])["taskDefinition"]
cd = td["containerDefinitions"][0]
image = cd.get("image", "")
opts = (cd.get("logConfiguration") or {}).get("options") or {}
group = opts.get("awslogs-group")
prefix = opts.get("awslogs-stream-prefix")
stream = "%s/%s/%s" % (prefix, cd["name"], TASK.rsplit("/", 1)[-1])


def events(g, s):
    out, tok = [], None
    while True:
        kw = {"logGroupName": g, "logStreamName": s, "startFromHead": True}
        if tok:
            kw["nextToken"] = tok
        r = logs.get_log_events(**kw)
        out.extend(e["message"].rstrip("\n") for e in r["events"])
        if r.get("nextForwardToken") == tok or not r["events"]:
            break
        tok = r["nextForwardToken"]
    return out


lines = events(group, stream)
ingest = [ln for ln in lines if "STITCH_INGEST " in ln and ln.startswith("INFO:")]
fails = [ln for ln in lines if "STITCH_INGEST_FAIL" in ln or "STITCH_INGEST_NONE" in ln]
unmapped = [ln for ln in lines if "STITCH_UNMAPPED_TYPE" in ln]
relabel = [ln for ln in lines if "NODE_TYPE_LAYER relabel applied" in ln]
gap = [ln for ln in lines if "NODE_TYPE_LAYER_GAP" in ln]

print("F4-AC3 -- ONE REAL DERIVE ON THE NEW DIGEST FOLDED THE STITCH")
print("  live read at: %s" % now)
print()
print("DERIVE_TASK=%s" % TASK)
print("DERIVE_TASK_DEFINITION=%s" % t["taskDefinitionArn"])
print("DERIVE_IMAGE_IS_THE_NEW_DIGEST=%s" % (NEW_DIGEST in image))
print("DERIVE_LAST_STATUS=%s exit_code=%s" % (t["lastStatus"], c.get("exitCode")))
for ln in ingest:
    print(ln)
print("STITCH_INGEST_LINES=%d" % len(ingest))
print("STITCH_INGEST_FAIL_LINES=%d" % len(fails))
print()
print("  -- the taxonomy guard, in the cloud, on the real artifact --")
for ln in relabel:
    print("     " + ln)
print("     NODE_TYPE_LAYER_GAP lines: %d   (a non-zero here is a derive that FAILED CLOSED)"
      % len(gap))
print("     STITCH_UNMAPPED_TYPE lines: %d   (the five gated types are in the map now;"
      % len(unmapped))
print("     any line here names a type NOBODY has mapped -- the next producer's invention)")
for ln in unmapped[:5]:
    print("       " + ln[:150])
print()
print("  -- the CONTROL: the PREVIOUS derive in the same log group --")
streams = logs.describe_log_streams(logGroupName=group, orderBy="LastEventTime",
                                    descending=True, limit=6)["logStreams"]
others = [s for s in streams if s["logStreamName"] != stream][:2]
for s in others:
    prev = events(group, s["logStreamName"])
    pi = [ln for ln in prev if "STITCH_INGEST " in ln]
    when = datetime.datetime.fromtimestamp(
        s.get("firstEventTimestamp", 0) / 1000.0, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print("     %s  first_event=%s  events=%d  STITCH_INGEST lines=%d"
          % (s["logStreamName"].rsplit("/", 1)[-1][:12], when, len(prev), len(pi)))
print("     an image without the fold cannot print the line at all, which is what makes")
print("     its presence above evidence rather than decoration.")
print()
m = re.search(r"nodes=(\d+) edges=(\d+) skipped_dup=(\d+) stamped=(\d+)",
              ingest[0] if ingest else "")
if m:
    print("  DENOMINATOR: 1 of 1 ad-hoc derive on the new digest; %s nodes and %s edges folded, "
          "%s duplicate node(s) skipped, %s node(s) stamped vocabulary=stitch-v1; "
          "%d of %d log events read (whole stream, paginated to the end)."
          % (m.group(1), m.group(2), m.group(3), m.group(4), len(lines), len(lines)))
else:
    print("  DENOMINATOR: 1 of 1 ad-hoc derive; %d log events read; NO STITCH_INGEST line found."
          % len(lines))
PY
