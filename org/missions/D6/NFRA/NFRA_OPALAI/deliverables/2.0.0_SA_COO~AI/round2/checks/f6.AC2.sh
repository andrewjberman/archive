#!/usr/bin/env bash
# OA-f-6 AC2 (built, CTO ruling msg 26306): verify-boundary.ps1 at opal_ai ${OA_F6_REF:-HEAD} has FOUR arm files beside it
# (probe, control, checkout, config). The two NEW negative arms try an Opal_Agent WRITE into checkout_dir and a
# write-open of runtime.config.json, and each must be DENIED on the real account. The self-test seam
# (-SelfTestAsCurrentUser, no -Credential) runs every arm FILE against a scratch config where all four targets are
# WRITABLE by the current user, so the correct line is
#   BOUNDARY: BREACH probe=ALLOWED control=OK checkout=ALLOWED config=ALLOWED   (exit 1)
# with 4 verdict files, which proves each arm RUNS and writes its verdict. The config file's bytes are UNCHANGED after the
# run (the arm opens it for write and writes nothing), and `ARGLEN:` names all four arms under 1024. The logon path's own
# acceptance stays 0.0.0_AB_MSTR~Z's real run.
. "$(dirname "$0")/_root.sh"
REF="${OA_F6_REF:-HEAD}"
D="opal/runtime/provision"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f6ac2_$$")"; mkdir -p "$T/root/state" "$T/root/opal_ai"
git -C opal_ai archive "$REF" "$D" 2>/dev/null | tar -x -C "$T" 2>/dev/null
arms=0; for a in probe control checkout config; do [ -f "$T/$D/boundary-arm-$a.ps1" ] && arms=$((arms+1)); done
printf 'probe\n' > "$T/probe.txt"
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"; WD="$(cygpath -w "$T/$D" 2>/dev/null || echo "$T/$D")"
python -c "import json,sys;json.dump({'checkout_dir':sys.argv[2]+'\\\\root\\\\opal_ai','state_dir':sys.argv[2]+'\\\\root\\\\state','workspace_probe_file':sys.argv[2]+'\\\\probe.txt','prod_ref':'PROD'},open(sys.argv[1],'w'))" "$T/root/runtime.config.json" "$WT"
before=$(md5sum "$T/root/runtime.config.json" | awk '{print $1}')
out=$(timeout 100 powershell -NoProfile -ExecutionPolicy Bypass -File "$WD\\verify-boundary.ps1" -Config "$WT\\root\\runtime.config.json" -SelfTestAsCurrentUser 2>&1 | tr -d '\r'); rc=$?
after=$(md5sum "$T/root/runtime.config.json" | awk '{print $1}')
line=$(printf '%s\n' "$out" | grep -m1 '^BOUNDARY:')
arg=$(printf '%s\n' "$out" | grep -m1 '^ARGLEN:')
over=$(printf '%s' "$arg" | grep -oE '=[0-9]+' | tr -d '=' | awk '$1>=1024' | grep -c .); cnt=$(printf '%s' "$arg" | grep -oE '=[0-9]+' | grep -c .)
vf=$(ls "$T/root/state" 2>/dev/null | grep -c '\.verdict$')
rm -rf "$T"
echo "opal_ai $REF: arm files=$arms; rc=$rc line='${line:-none}'; verdict files=$vf; config unchanged=$([ "$before" = "$after" ] && echo yes || echo no); ${arg:-ARGLEN: none} (values=$cnt, >=1024: $over)"
if [ "$arms" = 4 ] && [ "$rc" = 1 ] && [ "$line" = "BOUNDARY: BREACH probe=ALLOWED control=OK checkout=ALLOWED config=ALLOWED" ] \
   && [ "$vf" -ge 4 ] && [ "$before" = "$after" ] && [ "$cnt" -ge 4 ] && [ "$over" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
