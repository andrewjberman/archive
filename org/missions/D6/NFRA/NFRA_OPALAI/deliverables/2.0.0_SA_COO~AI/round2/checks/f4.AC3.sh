#!/usr/bin/env bash
# OA-f-4 AC3 (AMENDMENT 1, CTO ruling msg 26294: "a test that runs each arm and asserts that a verdict FILE exists").
# The script at opal_ai ${OA_NESTED_REF:-HEAD} is run with -SelfTestAsCurrentUser: each arm goes through the SAME
# Start-Process -EncodedCommand plumbing but WITHOUT -Credential, so no Opal_Agent logon is needed. The scratch config's
# probe file is READABLE by the current user, so a correctly RUNNING probe arm answers ALLOWED and the control arm OK:
# the one line must be `BOUNDARY: BREACH probe=ALLOWED control=OK` with exit 1. An arm that did not run (the quoting
# defect: no verdict file) reads ERROR and fails this check. The check ALSO asserts both verdict files exist in the
# scratch state_dir afterwards, and that the script names -EncodedCommand and no `-Command`.
. "$(dirname "$0")/_root.sh"
REF="${OA_NESTED_REF:-HEAD}"
F="opal/runtime/provision/verify-boundary.ps1"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f4ac3_$$")"; mkdir -p "$T/st"
git -C opal_ai show "$REF:$F" > "$T/v.ps1" 2>/dev/null
printf 'probe\n' > "$T/probe.txt"
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"
enc=$(grep -c -- '-EncodedCommand' "$T/v.ps1"); cmdq=$(grep -cE -- "'-Command'|-Command " "$T/v.ps1")
python -c "import json,sys;json.dump({'checkout_dir':sys.argv[2]+'\\\\co','state_dir':sys.argv[2]+'\\\\st','workspace_probe_file':sys.argv[2]+'\\\\probe.txt','prod_ref':'PROD'},open(sys.argv[1],'w'))" "$T/cfg.json" "$WT"
out=$(timeout 90 powershell -NoProfile -ExecutionPolicy Bypass -File "$WT\\v.ps1" -Config "$WT\\cfg.json" -SelfTestAsCurrentUser 2>&1 | tr -d '\r'); rc=$?
line=$(printf '%s\n' "$out" | grep -m1 '^BOUNDARY:')
vf=$(ls "$T/st" 2>/dev/null | grep -c '\.verdict$')
rm -rf "$T"
echo "opal_ai $REF: -EncodedCommand refs=$enc -Command refs=$cmdq; rc=$rc line='${line:-none}'; verdict files=$vf"
if [ "$enc" -ge 1 ] && [ "$cmdq" = 0 ] && [ "$rc" = 1 ] && [ "$line" = "BOUNDARY: BREACH probe=ALLOWED control=OK" ] && [ "$vf" -ge 2 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
