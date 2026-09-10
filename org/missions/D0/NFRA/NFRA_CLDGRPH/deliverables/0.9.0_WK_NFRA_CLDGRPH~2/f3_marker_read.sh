#!/usr/bin/env bash
# F3-AC5 -- A NIGHT THAT DID NOT RUN READS DIFFERENTLY FROM ONE THAT DID.
#
# ONE reader (f3_marker_verdict.py, whose age bar is IMPORTED from the estate's
# own infra/aws/globgrph/_provenance.py:41 DEFAULT_AGE_WARN_HOURS = 26.0, never
# re-typed), applied to THREE inputs, returning THREE distinct verdicts:
#
#   LIVE     the marker at s3://opal-313476888478-globgrph/stitch/stitch_marker.json,
#            read live on every run                                      -> FRESH
#   PLANTED  a marker that is a COMPLETE, WELL-FORMED, ENTIRELY PLAUSIBLE object
#            -- every field the cloud's marker carries, a real snapshot key, a
#            real sha256 -- whose ONLY defect is that built_at is 80 h old
#                                                                        -> STALE
#   MISSING  a key that does not exist (a 404 from the same bucket)      -> NO-RUN
#
# That is the whole point of the criterion: the PLANTED case is what a night
# that did not run actually looks like -- last night's object, still sitting
# there, parsing perfectly. A reader that checks shape returns the same answer
# for it as for tonight's; this one does not, because it reads VINTAGE.
#
# NO S3 OBJECT IS WRITTEN AND NO FILE IS PLANTED ON DISK. The planted marker is
# built IN MEMORY at run time (built_at = now - 80 h, so it can never age out of
# its own band), and the missing key is probed with a read that 404s.
#
# Run from the repository root.
set -u
D="org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2"

python - "$D" <<'PY'
import datetime
import importlib.util
import json
import os
import sys

import boto3
import botocore

d = sys.argv[1]
spec = importlib.util.spec_from_file_location(
    "f3_marker_verdict", os.path.join(d, "f3_marker_verdict.py"))
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)

B = "opal-313476888478-globgrph"
LIVE_KEY = "stitch/stitch_marker.json"
MISSING_KEY = "stitch/stitch_marker.json.f3-no-such-key-probe"
now = datetime.datetime.now(datetime.timezone.utc)
s3 = boto3.client("s3", region_name="us-east-1")


def fetch(key):
    try:
        return json.loads(s3.get_object(Bucket=B, Key=key)["Body"].read()), True, "200"
    except botocore.exceptions.ClientError as e:
        return None, False, e.response["Error"]["Code"]


live, live_present, live_code = fetch(LIVE_KEY)
missing, missing_present, missing_code = fetch(MISSING_KEY)

planted = dict(live) if live else {}
planted.update({
    "built_at": (now - datetime.timedelta(hours=80)).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "producer": "stitch-codebuild",
})

print("F3-AC5 -- A NIGHT THAT DID NOT RUN READS DIFFERENTLY FROM ONE THAT DID")
print("  reader   : %s" % os.path.join(d, "f3_marker_verdict.py"))
print("  age bar  : %s h  <- %s" % (V.AGE_BAR, V.BAR_SOURCE))
print("  read at  : %s" % now.strftime("%Y-%m-%dT%H:%M:%SZ"))
print()
print(V.render("LIVE_VERDICT", live, present=live_present, now=now))
print(V.render("PLANTED_STALE_VERDICT", planted, present=True, now=now))
print(V.render("MISSING_VERDICT", missing, present=missing_present, now=now))
print()
print("  -- the three inputs, so the verdicts can be checked against them --")
print("     LIVE     s3://%s/%s" % (B, LIVE_KEY))
print("              GET -> %s   built_at=%s  producer=%s"
      % (live_code, (live or {}).get("built_at"), (live or {}).get("producer")))
print("     PLANTED  generated at run time, in memory, NOT written to S3")
print("              built_at=%s  (now - 80 h)  producer=%s"
      % (planted.get("built_at"), planted.get("producer")))
print("              every OTHER field copied from the live marker, so the object is")
print("              indistinguishable from a good one except by its vintage:")
for k in ("aws_snapshot", "git_sha", "total_nodes", "total_edges", "artifact_sha256"):
    print("                %-16s %s" % (k, planted.get(k)))
print("     MISSING  s3://%s/%s" % (B, MISSING_KEY))
print("              GET -> %s   (a real 404 from the same bucket and the same"
      % missing_code)
print("              client as the LIVE read -- not a simulated absence)")
print()
verdicts = [V.verdict(live, present=live_present, now=now)[0],
            V.verdict(planted, present=True, now=now)[0],
            V.verdict(missing, present=missing_present, now=now)[0]]
print("  -- the discrimination --")
print("     three inputs -> %s" % ", ".join(verdicts))
print("     distinct verdicts: %d of 3" % len(set(verdicts)))
print("     NEVER A PLAUSIBLE OBJECT: the PLANTED input parses, validates and")
print("     carries a real artifact_sha256; it is refused on VINTAGE alone.")
print()
print("  -- what this does NOT claim --")
print("     No rule is disabled by this order (an infra act, out of the grant), so")
print("     the MISSING case is exercised on a key that does not exist rather than")
print("     by suppressing a night. The consumer repoint (comp_debt.py:128-160,")
print("     which reads a LOCAL manifest today) is CG-s-25 / TO-CG-F-5, not this")
print("     order; what is proven here is that the marker CAN be read three ways.")
print()
print("  DENOMINATOR: 3 of 3 cases the criterion names (live, planted-stale,")
print("  missing), one reader, one age bar, imported not re-typed.")
PY
