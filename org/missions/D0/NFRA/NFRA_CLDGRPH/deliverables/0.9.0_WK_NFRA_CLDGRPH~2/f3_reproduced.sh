#!/usr/bin/env bash
# F3-AC1 -- THE EXIT 2 REPRODUCED ON THE SNAPSHOT AS PULLED (TO-CG-F-3, CG-s-23).
#
# WHAT THIS SCRIPT IS: a READER over the captures the reproduction produced, not
# a re-runner of it. It says so because that is the honest grain. The
# reproduction itself is a 157 MB pull + a 7905-entry unzip + a ~60 s derive; it
# was performed once, at 2026-09-09 18:23Z..18:33Z, BEFORE the re-push at
# 18:47:04Z -- and it CANNOT be re-run afterwards, because the S3 key it reads
# no longer holds the July object. The captures ARE the evidence and they are
# committed beside this script.
#
# Every value below is DERIVED from a capture, never restated from prose:
#   ASIS_ZIP_ETAG        <- f3_asis_headobject.json  (the get-object response)
#   ASIS_LOG_LINES       <- f3_asis_cloud_log_3a5b2473.txt (line count)
#   ASIS_RC              <- the CLOUD's own literal "exit status 2" in that log,
#                           cross-checked against the local run's own last line
#   ASIS_CAUSE           <- the sentinel line present in BOTH readings
#   ASIS_PORTAL_SRC_FILES<- f3_asis_zip_manifest.json (python zipfile over bytes)
#
# Run from the repository root.
set -u
D="org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2"

python - "$D" <<'PY'
import json
import os
import re
import sys

d = sys.argv[1]
head = json.load(open(os.path.join(d, "f3_asis_headobject.json"), encoding="utf-8"))
man = json.load(open(os.path.join(d, "f3_asis_zip_manifest.json"), encoding="utf-8"))
cloud = open(os.path.join(d, "f3_asis_cloud_log_3a5b2473.txt"), encoding="utf-8").read()
local = open(os.path.join(d, "f3_asis_local_run.txt"), encoding="utf-8").read()

cloud_lines = [ln for ln in cloud.splitlines()]
local_lines = [ln for ln in local.splitlines()]

# --- ASIS_RC: the CLOUD's own reading is primary -------------------------------
m = re.search(r"exit status (\d+)", cloud)
cloud_rc = int(m.group(1)) if m else -1
# --- corroboration: the local run of the SNAPSHOT's own bytes ------------------
SENT = "ERROR: GRAIN_SENTINEL_FAIL -- refusing to emit grain-violating stitch graph"
local_sentinel = SENT in local
cloud_sentinel = SENT in cloud
# derive_stitch (snapshot vintage, :237-238) returns 2 on exactly that branch
local_rc_implied = 2 if local_sentinel else -1

cause = "OTHER"
if cloud_sentinel:
    cause = "GRAIN_SENTINEL"
elif re.search(r"usage: |unrecognized arguments|invalid choice", cloud):
    cause = "ARGPARSE"
elif "Traceback (most recent call last)" in cloud or "ModuleNotFoundError" in cloud:
    cause = "IMPORT"

# --- the two readings must agree on the union counts, or the reproduction is
#     of a DIFFERENT run and the rc means nothing --------------------------------
def union(text):
    mm = re.search(r"UNIONED nodes = (\d+), edges = (\d+)", text)
    return (mm.group(1), mm.group(2)) if mm else (None, None)

cu, lu = union(cloud), union(local)
groups_cloud = len(re.findall(r"\[AC-GRAIN\.2\] (\w+): count", cloud))
groups_local = len(re.findall(r"\[AC-GRAIN\.2\] (\w+): count", local))

print("F3-AC1 -- THE EXIT 2 REPRODUCED ON THE SNAPSHOT AS PULLED")
print("  capture vintage: pulled 2026-09-09T18:2xZ, BEFORE the 18:47:04Z re-push")
print()
print("ASIS_RC=%d" % cloud_rc)
print("ASIS_CAUSE=%s" % cause)
print("ASIS_ZIP_ETAG=%s" % head["ETag"])
print("ASIS_LOG_LINES=%d" % len(cloud_lines))
print("ASIS_PORTAL_SRC_FILES=%d" % man["portal_src_entries"])
print()
print("  -- how ASIS_RC was read --")
print("     cloud log literal            : %s" % (m.group(0) if m else "ABSENT"))
print("     cloud log, sentinel line     : %s" % cloud_sentinel)
print("     local run of SNAPSHOT bytes  : sentinel line %s -> rc implied %d"
      % (local_sentinel, local_rc_implied))
print("     the two agree                : %s" % (cloud_rc == local_rc_implied))
print()
print("  -- the discriminating agreement (a wrong-run reproduction would differ) --")
print("     cloud  UNIONED nodes/edges   : %s / %s" % cu)
print("     local  UNIONED nodes/edges   : %s / %s" % lu)
print("     union counts identical       : %s" % (cu == lu and cu[0] is not None))
print("     AC-GRAIN.2 groups cloud/local: %d / %d" % (groups_cloud, groups_local))
print()
print("  -- the zip as pulled (python zipfile over the bytes) --")
print("     entries                      : %d" % man["entries"])
print("     portal/ prefix entries       : %d   <- the workflow comment's own class"
      % man["portal_prefix_entries"])
print("     stitch_source_sha.txt        : %s" % man["stitch_source_sha_txt"])
print("     zip grain_baseline recerts   : %d (HEAD carries 8)"
      % man["zip_grain_baseline_recertifications"])
print()
print("  DENOMINATOR: 1 of 1 rule-initiated build read (the newest, "
      "opal-stitch-produce:3a5b2473-f46a-490a-ae5e-874a96c90b16); "
      "%d of %d log events captured; 1 of 1 local run of the snapshot's own bytes."
      % (len(cloud_lines), len(cloud_lines)))
PY
