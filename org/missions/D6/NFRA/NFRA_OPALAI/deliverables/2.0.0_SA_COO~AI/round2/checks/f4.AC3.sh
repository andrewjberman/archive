#!/usr/bin/env bash
# OA-f-4 AC3 (AMENDMENT 2, CTO ruling msg 26297). The two arms ship as FILES beside the script,
# opal/runtime/provision/boundary-arm-probe.ps1 and boundary-arm-control.ps1 (checkout ACL RX for Opal_Agent; never
# written into state_dir). verify-boundary.ps1 runs each with `-File <arm.ps1> ...`, so the logon command line stays
# under CreateProcessWithLogonW's 1024-character limit (measured by 0.0.0_AB_MSTR~Z at 00:04Z: the -EncodedCommand line
# was ~1150 and no child started). This check:
#  - reads the file: -EncodedCommand refs=0, `-Command` refs=0, `-File` refs>=2, and both arm files present at REF;
#  - runs -SelfTestAsCurrentUser on the provision folder exported from REF (the arms are resolved beside the script)
#    against a scratch config whose probe is READABLE, so the correct line is `BOUNDARY: BREACH probe=ALLOWED control=OK`
#    (exit 1) with 2 verdict files, which proves both arm FILES run and write verdicts;
#  - reads the script's own `ARGLEN: probe=<n> control=<m>` line (the length of the argument string it hands
#    Start-Process for each arm, built exactly as on the credential path) and requires both under 1024.
# The seam drops -Credential, so it is NOT a control for the logon path itself: that acceptance is MSTR~Z's real step 3.
. "$(dirname "$0")/_root.sh"
REF="${OA_NESTED_REF:-HEAD}"
D="opal/runtime/provision"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f4ac3_$$")"; mkdir -p "$T/st"
git -C opal_ai archive "$REF" "$D" 2>/dev/null | tar -x -C "$T" 2>/dev/null
V="$T/$D/verify-boundary.ps1"
[ -f "$V" ] || { echo "verify-boundary.ps1 absent at $REF"; rm -rf "$T"; echo "RESULT: FAIL"; exit 1; }
arms=0; for a in boundary-arm-probe.ps1 boundary-arm-control.ps1; do [ -f "$T/$D/$a" ] && arms=$((arms+1)); done
enc=$(grep -c -- '-EncodedCommand' "$V"); cmdq=$(grep -cE -- "'-Command'|-Command " "$V"); fil=$(grep -cE -- "'-File'|-File " "$V")
printf 'probe\n' > "$T/probe.txt"
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"; WD="$(cygpath -w "$T/$D" 2>/dev/null || echo "$T/$D")"
python -c "import json,sys;json.dump({'checkout_dir':sys.argv[2]+'\\\\co','state_dir':sys.argv[2]+'\\\\st','workspace_probe_file':sys.argv[2]+'\\\\probe.txt','prod_ref':'PROD'},open(sys.argv[1],'w'))" "$T/cfg.json" "$WT"
out=$(timeout 90 powershell -NoProfile -ExecutionPolicy Bypass -File "$WD\\verify-boundary.ps1" -Config "$WT\\cfg.json" -SelfTestAsCurrentUser 2>&1 | tr -d '\r'); rc=$?
line=$(printf '%s\n' "$out" | grep -m1 '^BOUNDARY:')
arg=$(printf '%s\n' "$out" | grep -m1 '^ARGLEN:')
pl=$(printf '%s' "$arg" | sed -n 's/.*probe=\([0-9][0-9]*\).*/\1/p'); cl=$(printf '%s' "$arg" | sed -n 's/.*control=\([0-9][0-9]*\).*/\1/p')
vf=$(ls "$T/st" 2>/dev/null | grep -c '\.verdict$')
rm -rf "$T"
echo "opal_ai $REF: arm files=$arms; -EncodedCommand refs=$enc -Command refs=$cmdq -File refs=$fil; rc=$rc line='${line:-none}'; verdict files=$vf; ${arg:-ARGLEN: none}"
if [ "$arms" = 2 ] && [ "$enc" = 0 ] && [ "$cmdq" = 0 ] && [ "$fil" -ge 2 ] && [ "$rc" = 1 ] \
   && [ "$line" = "BOUNDARY: BREACH probe=ALLOWED control=OK" ] && [ "$vf" -ge 2 ] \
   && [ -n "$pl" ] && [ -n "$cl" ] && [ "$pl" -lt 1024 ] && [ "$cl" -lt 1024 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
