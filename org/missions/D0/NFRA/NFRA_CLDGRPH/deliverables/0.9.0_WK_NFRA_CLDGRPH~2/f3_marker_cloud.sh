#!/usr/bin/env bash
# F3-AC4 -- THE MARKER WAS WRITTEN BY THE CLOUD (TO-CG-F-3, CG-s-23).
#
# THIS READ IS PERISHABLE AND THE SCRIPT SAYS SO ON EVERY RUN.
# .tools/git-hooks/stitch-refresh-post-commit.sh is installed in .git/hooks/
# post-commit on this laptop AND at site Z. Within ~60 s of ANY commit at either
# clone touching portal/, data/*/scripts/, org/modules/graph/ or the two derive
# scripts, it republishes stitch/stitch_graph.json + stitch_marker.json with
# producer=stitch-local (issuer ruling on row NFRA_CLDGRPH-S71, 3.0.0_SA_CVO
# 18:44Z). So the S3 marker has TWO writers and the cloud's is not the last one
# by construction. THE HOOK IS NOT TOUCHED BY THIS ORDER -- it carries an
# Andrew-direct of 2026-07-07 and its reconciliation is 1.0.0_SA_CTO's.
#
# Therefore this script ALWAYS prints two readings and names which one the four
# criterion values are taken from:
#   * THE PINNED READ -- f3_marker_capture.json, taken at 2026-09-09T18:52:13Z..
#     18:52:20Z, 3 minutes after the ad-hoc build wrote the marker at 18:49:37Z.
#     This is the reading the criterion is met by (issuer ruling, same message).
#   * THE LIVE READ -- taken now, on every run. If it still shows the cloud's
#     marker, the two agree and the pinned read is merely corroborated. If it
#     shows stitch-local, the overwrite instant and the overwriting clone's
#     git_sha are printed, and the values stay on the pinned read.
#
# Run from the repository root.
set -u
D="org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2"

python - "$D" <<'PY'
import datetime
import hashlib
import json
import os
import subprocess
import sys

import boto3

d = sys.argv[1]
B = "opal-313476888478-globgrph"
MK, AK = "stitch/stitch_marker.json", "stitch/stitch_graph.json"

pinned = json.load(open(os.path.join(d, "f3_marker_capture.json"), encoding="utf-8"))

s3 = boto3.client("s3", region_name="us-east-1")
t0 = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
mh = s3.head_object(Bucket=B, Key=MK)
live = json.loads(s3.get_object(Bucket=B, Key=MK)["Body"].read())
live_lm = mh["LastModified"].astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

live_is_cloud = (live.get("producer") == "stitch-codebuild"
                 and live.get("git_sha") == pinned["marker"]["git_sha"]
                 and live.get("built_at") == pinned["marker"]["built_at"])

if live_is_cloud:
    src, m = "LIVE (and identical to the pinned read)", live
    ah = s3.head_object(Bucket=B, Key=AK)
    body = s3.get_object(Bucket=B, Key=AK)["Body"].read()
    sha = hashlib.sha256(body).hexdigest()
    art_bytes, art_lm = ah["ContentLength"], ah["LastModified"].astimezone(
        datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sha_src = "measured NOW over the served artifact (%d B)" % art_bytes
else:
    src, m = "PINNED 2026-09-09T18:52:13Z..18:52:20Z (the live marker has been overwritten)", pinned["marker"]
    sha = pinned["artifact_sha256_measured"]
    art_bytes, art_lm = pinned["artifact_bytes"], pinned["artifact_last_modified_utc"]
    sha_src = "measured at the pinned instant over the served artifact (%d B)" % art_bytes

sha_in_repo = subprocess.run(["git", "cat-file", "-e", m.get("git_sha", "") + "^{commit}"],
                             capture_output=True).returncode == 0
laptop_sha = "9b99b4934217c54aea516591a65e1009a5f9bdf6"
laptop_in_repo = subprocess.run(["git", "cat-file", "-e", laptop_sha + "^{commit}"],
                                capture_output=True).returncode == 0
laptop_desc = subprocess.run(
    ["git", "log", "-1", "--format=%an %ad %s", "--date=iso", laptop_sha],
    capture_output=True, text=True)
laptop_desc = laptop_desc.stdout.strip()[:110] if laptop_desc.returncode == 0 else "ABSENT"
absent_sha = "0" * 40
absent_in_repo = subprocess.run(["git", "cat-file", "-e", absent_sha + "^{commit}"],
                                capture_output=True).returncode == 0
head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
head_in_repo = subprocess.run(["git", "cat-file", "-e", head + "^{commit}"],
                              capture_output=True).returncode == 0

print("F3-AC4 -- THE MARKER WAS WRITTEN BY THE CLOUD")
print("  values taken from: %s" % src)
print("  live read at     : %s" % t0)
print()
print("MARKER_PRODUCER=%s" % m.get("producer"))
print("MARKER_GIT_SHA=%s" % m.get("git_sha"))
print("MARKER_SHA_IN_THIS_REPO=%s" % ("true" if sha_in_repo else "false"))
print("ARTIFACT_SHA256_MATCH=%s"
      % ("true" if sha == m.get("artifact_sha256") else "false"))
print()
print("  -- the marker, in full --")
for k in ("built_at", "aws_snapshot", "git_sha", "producer",
          "total_nodes", "total_edges", "artifact_sha256"):
    print("     %-16s: %s" % (k, m.get(k)))
print()
print("  -- the artifact --")
print("     key             : s3://%s/%s" % (B, AK))
print("     bytes           : %s" % art_bytes)
print("     LastModified    : %s" % art_lm)
print("     sha256          : %s" % sha)
print("     marker claims   : %s" % m.get("artifact_sha256"))
print("     %s" % sha_src)
print()
print("  -- the LIVE marker right now (printed whether or not it is the cloud's) --")
print("     producer        : %s" % live.get("producer"))
print("     built_at        : %s" % live.get("built_at"))
print("     git_sha         : %s" % live.get("git_sha"))
print("     LastModified    : %s" % live_lm)
print("     is the cloud's  : %s" % live_is_cloud)
if not live_is_cloud:
    print("     !! OVERWRITTEN at %s by the post-commit hook's local publish;" % live_lm)
    print("        the overwriting clone's git_sha is above. The criterion's values")
    print("        stay on the pinned post-build read, per the issuer ruling on S71.")
print()
print("  -- the CONTROLS this criterion must be able to FAIL against --")
print("     PRODUCER is the discriminator, and it is the ONLY one that works.")
print("     producer=stitch-local FAILS this read whatever its date (issuer ruling,")
print("     TO-CG-F-3 'MEASURED BY THE ISSUER AT THE CUT'); the PRD's token")
print("     producer=stitch-cloud is read as the buildspec's literal stitch-codebuild.")
print()
print("     git_sha MEMBERSHIP DOES NOT DISCRIMINATE -- measured, not assumed:")
print("       the 17:53:55Z laptop marker's git_sha %s" % laptop_sha)
print("       git cat-file -e -> in THIS repository: %s" % laptop_in_repo)
print("       git log -1 -> %s" % laptop_desc)
print("       The task order (and row NFRA_CLDGRPH-S70) assert that sha is NOT an")
print("       object in this repository. At this worktree's vintage it IS: a commit")
print("       of 1.0.0_SA_CTO~Z's, contained in CLOUD, made ~57 s before that marker")
print("       was written. The laptop publisher is the post-commit hook on THIS")
print("       estate, not a foreign clone. Filed as NFRA_CLDGRPH-W2-S42.")
print("       So MARKER_SHA_IN_THIS_REPO would read true for the laptop marker too,")
print("       and it is reported here as a PROVENANCE fact, never as the cloud test.")
print()
print("     THE ORACLE IS STILL LIVE, both directions, same instrument, same call:")
print("       POSITIVE: HEAD %s -> %s" % (head, head_in_repo))
print("       NEGATIVE: %s -> %s" % (absent_sha, absent_in_repo))
print("       so 'false' is reachable and a 'true' above is not a constant.")
print()
print("  DENOMINATOR: 2 of 2 S3 keys the CodeBuild role may write (stitch/"
      "stitch_graph.json, stitch/stitch_marker.json), both read; 1 of 1 marker; "
      "2 of 2 readings printed (pinned + live).")
PY
