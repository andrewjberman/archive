#!/usr/bin/env bash
# AMGT_RESAPP round 51, AMGT-zz-4 AC3 -- the scoped-API build PRINTS the packaged-file CONTENT DIFF against the DEPLOYED artifact
# (CTO round-50 ruling 4; row Z-S307: a never-widen half read packaging from code comments). A `--build-only` run of
# infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh prints, for every packaged file, one line
#   CONTENT-DIFF <IDENTICAL|CHANGED|ADDED|REMOVED> <archive path>
# against the manifest of the artifact the live function runs (its VersionId read from Terraform state / the function), then ONE summary
#   CONTENT-DIFF SUMMARY: files N, IDENTICAL i, CHANGED c, ADDED a, REMOVED r, against <VersionId>
# PASS when the summary prints with i + c + a == N, and lib/opal_naming.py is listed (it IS packaged -- Z-S307).
# usage: bash <this>   (from the repo root; builds locally, uploads NOTHING)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
timeout 900 bash infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh --build-only "$T/scoped.zip" > "$T/log" 2>&1
rc=$?
python - "$T/log" "$rc" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8", errors="replace").read()
lines = re.findall(r"^CONTENT-DIFF (IDENTICAL|CHANGED|ADDED|REMOVED) (\S+)", text, re.M)
s = re.search(r"^CONTENT-DIFF SUMMARY: files (\d+), IDENTICAL (\d+), CHANGED (\d+), ADDED (\d+), REMOVED (\d+), against (\S+)", text, re.M)
print("build rc=%s; CONTENT-DIFF lines %d" % (sys.argv[2], len(lines)))
print(s.group(0) if s else "no 'CONTENT-DIFF SUMMARY:' line")
naming = [p for st, p in lines if p.replace("\\", "/").endswith("lib/opal_naming.py")]
print("lib/opal_naming.py listed: %s" % (naming or "no"))
ok = bool(s) and sys.argv[2] == "0" and int(s.group(2)) + int(s.group(3)) + int(s.group(4)) == int(s.group(1)) and bool(naming)
print("THE BUILD PRINTS ITS CONTENT DIFF AGAINST THE DEPLOYED ARTIFACT: %s" % ("YES" if ok else "NO"))
sys.exit(0 if ok else 1)
PY
