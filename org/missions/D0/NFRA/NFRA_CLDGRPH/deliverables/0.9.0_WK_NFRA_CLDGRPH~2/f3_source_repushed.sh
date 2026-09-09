#!/usr/bin/env bash
# F3-AC2 -- THE SOURCE RE-PUSHED FROM HEAD UNDER A NEVER-2 ENTRY (TO-CG-F-3).
#
# THE OBJECT IS THE CLAIM, so every number is read from the object AT THE KEY,
# live, on every run -- not from the local file that was uploaded and not from
# the ledger's own prose. f3_read_s3_zip.py takes them with three RANGED GETs
# (End-Of-Central-Directory -> central directory -> the one small entry whose
# bytes we need), so the read costs a few hundred KiB instead of 173 MiB and
# fits the order's `timeout 120` without ever trusting a producer's self-report.
#
# The ledger's status is read from the FILE'S OWN header line, not asserted here.
# The July zero (0 files under portal/src) is printed beside the new count as the
# control: the same instrument, on the same key, read 0 before this act.
#
# Run from the repository root.
set -u
D="org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2"
LEDGER="org/critical_paths/change_management/20260909T184608Z_stitch-source-repush_deploy_completion.md"

python - "$D" "$LEDGER" <<'PY'
import json
import os
import re
import subprocess
import sys

d, ledger = sys.argv[1], sys.argv[2]
reader = os.path.join(d, "f3_read_s3_zip.py")
r = subprocess.run([sys.executable, reader], capture_output=True, text=True)
if r.returncode != 0:
    print("READER_FAILED rc=%d" % r.returncode)
    print(r.stdout)
    print(r.stderr)
    sys.exit(1)
z = json.loads(r.stdout)

# the ledger entry's OWN status line (the file, not a claim about it)
txt = open(ledger, encoding="utf-8").read()
m = re.search(r"^\*\*Status:\*\*\s*(\w+)", txt, re.M)
status = m.group(1) if m else "UNREADABLE"
closed = re.search(r"^\*\*Closed \(UTC\):\*\*\s*(\S+)", txt, re.M)
opened = re.search(r"^\*\*Opened \(UTC\):\*\*\s*(\S+)", txt, re.M)

# the control: the SAME key, read by the same class of instrument, BEFORE the act
ctl = json.load(open(os.path.join(d, "f3_asis_zip_manifest.json"), encoding="utf-8"))

print("F3-AC2 -- THE SOURCE RE-PUSHED FROM HEAD UNDER A NEVER-2 ENTRY")
print("  read of the SERVED object at: %s (live, this run)" % z["read_at_utc"])
print()
print("SOURCE_ZIP_LASTMODIFIED=%s" % z["last_modified_utc"])
print("SOURCE_ZIP_PORTAL_SRC_FILES=%d" % z["prefix_count"])
print("SOURCE_ZIP_SHA_FILE=%s" % z["read_entry_value"])
print("LEDGER_ENTRY_STATUS=%s" % status)
print()
print("  -- the served object --")
print("     s3://%s/%s" % (z["bucket"], z["key"]))
print("     ContentLength  : %d B" % z["content_length"])
print("     ETag           : %s" % z["etag"])
print("     entries        : %d (central directory), %d names parsed"
      % (z["central_directory_entries"], z["names_parsed"]))
print("     ranged GETs    : %d  (no full download; the object is 173 MiB)"
      % z["ranged_gets"])
print()
print("  -- the control: the SAME key BEFORE this act (July object, 7 Jul 2026) --")
print("     LastModified   : %s" % ctl["last_modified"])
print("     ETag           : %s" % ctl["etag"])
print("     entries        : %d" % ctl["entries"])
print("     portal/src     : %d   <- the zero this criterion is discriminated against"
      % ctl["portal_src_entries"])
print("     sha file       : %s" % ctl["stitch_source_sha_txt"])
print()
print("  -- the NEVER-2 ledger entry --")
print("     %s" % ledger)
print("     opened %s   closed %s"
      % (opened.group(1) if opened else "?", closed.group(1) if closed else "?"))
print("     task families touched: NONE (a CodeBuild source zip; no image, no tag,")
print("     no task definition -- stated in the entry rather than omitted)")
print()
print("  DENOMINATOR: 1 of 1 S3 object written by this seat in this order; "
      "%d of %d zip entries enumerated from the central directory; "
      "1 of 1 ledger entry, read from its own header line."
      % (z["names_parsed"], z["central_directory_entries"]))
PY
