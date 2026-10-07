#!/usr/bin/env bash
# OPLGTW OG-mf-1 AC1 (row Z-W15-S65, CTO R26): infra/aws/ec2/EC2_MANIFEST.json's opal-gateway row carries
# file_checksums == {} (the estate's convention) and a _checksums_note saying the map is not maintained and that
# deployed_commit plus the release's host md5 read are the record; deployed_commit is unchanged by the edit.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
python - <<'PY'
import json, subprocess
d = json.load(open("infra/aws/ec2/EC2_MANIFEST.json", encoding="utf-8"))["services"]["opal-gateway"]
note = str(d.get("_checksums_note", ""))
fc = d.get("file_checksums")
ok_note = "not maintained" in note.lower() and "deployed_commit" in note
print("file_checksums empty map: %s; note names 'not maintained' and deployed_commit: %s; deployed_commit %s"
      % (fc == {}, ok_note, str(d.get("deployed_commit", ""))[:10]))
ok = fc == {} and ok_note and str(d.get("deployed_commit", "")).startswith("2c27f3a795")
print("RESULT: PASS" if ok else "RESULT: FAIL"); raise SystemExit(0 if ok else 1)
PY
