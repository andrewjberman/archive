#!/usr/bin/env bash
# F3-AC3 -- ONE AD-HOC BUILD SUCCEEDED ON THE RE-PUSHED SOURCE (TO-CG-F-3).
#
# The build id is PINNED below because the claim is about ONE build -- the one
# this order started at 2026-09-09T18:48:15Z, after the re-push closed. Its
# status, initiator and phase list are re-read LIVE from CodeBuild on every run,
# so this is a reader of the world and not a restatement of a capture.
#
# THE CONTROL IS PRINTED BESIDE IT: the project's preceding builds, read from the
# same API in the same call. They are FAILED and rule-initiated. A project that
# cannot fail would make SUCCEEDED meaningless; this one failed 67 times.
#
# Run from the repository root.
set -u
BID="opal-stitch-produce:daaedf78-3ea7-4dd4-828b-be1c843f5d4c"

python - "$BID" <<'PY'
import collections
import datetime
import sys

import boto3

bid = sys.argv[1]
cb = boto3.client("codebuild", region_name="us-east-1")
read_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

b = cb.batch_get_builds(ids=[bid])["builds"][0]


def ts(x):
    return x.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if x else "-"


print("F3-AC3 -- ONE AD-HOC BUILD SUCCEEDED ON THE RE-PUSHED SOURCE")
print("  live read at: %s" % read_at)
print()
print("ADHOC_BUILD_ID=%s" % b["id"])
print("ADHOC_BUILD_STATUS=%s" % b["buildStatus"])
print("ADHOC_BUILD_INITIATOR=%s" % b["initiator"])
print()
print("  started  : %s" % ts(b.get("startTime")))
print("  ended    : %s" % ts(b.get("endTime")))
print("  project  : %s" % b["projectName"])
print("  log      : %s : %s" % (b["logs"]["groupName"], b["logs"].get("streamName")))
print("  phases   : %s" % ", ".join(
    "%s=%s" % (p["phaseType"], p.get("phaseStatus", "-")) for p in b.get("phases", [])))
print()
print("  -- the CONTROL: this project's other builds, same API, same call --")
ids = cb.list_builds_for_project(projectName="opal-stitch-produce")["ids"]
others = [i for i in ids if i != bid][:10]
det = cb.batch_get_builds(ids=others)["builds"] if others else []
tally = collections.Counter(x["buildStatus"] for x in det)
for x in det[:5]:
    print("     %s  %-10s initiator=%s  started=%s"
          % (x["id"].split(":")[1][:8], x["buildStatus"], x["initiator"], ts(x.get("startTime"))))
print("     ... tally over the %d most recent OTHER builds: %s"
      % (len(det), dict(tally)))
print("     the project CAN fail, and did, 67 of 67 times before this act")
print("     (3.0.0_SA_CVO's census C-S34) -- so SUCCEEDED discriminates.")
print()
rule_initiated = [x for x in det if x["initiator"].startswith("rule/")]
print("  -- the initiator is NOT the rule --")
print("     this build's initiator       : %s" % b["initiator"])
print("     starts with 'rule/'          : %s" % b["initiator"].startswith("rule/"))
print("     rule-initiated among controls: %d of %d" % (len(rule_initiated), len(det)))
print("     the NIGHTLY at 03:00Z stays the acceptance (F3-AC6, graded by 3.0.0_SA_CVO);")
print("     this ad-hoc build is the TEST, which is why a non-rule initiator is required.")
print()
print("  DENOMINATOR: 1 of 1 ad-hoc build started by this order; "
      "%d of %d most recent other builds read as the control (page 1 of "
      "list-builds-for-project, %d ids)." % (len(det), len(others), len(ids)))
PY
