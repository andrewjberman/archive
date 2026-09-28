#!/usr/bin/env bash
# OA-f-4 AC2 (the ERROR arm, CTO ruling msg 26260: "an arm that cannot START is ERROR, never DENIED-OK"): run the
# script at opal_ai ${OA_NESTED_REF:-HEAD} with -CredPath pointing at a credential for a user that DOES NOT EXIST
# (NoSuchUser_OAf4, a throwaway password), against a scratch config. Neither arm can start, so the one BOUNDARY line must
# read ERROR with exit 3 -- never DENIED-OK (exit 0) and never BREACH (exit 1). This needs the account Opal_Agent to
# exist (it does, since G-ACCT step 2) only to pass the NOT-PROVISIONED gate; the arms never log on as it.
. "$(dirname "$0")/_root.sh"
REF="${OA_NESTED_REF:-HEAD}"
F="opal/runtime/provision/verify-boundary.ps1"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f4ac2_$$")"; mkdir -p "$T/st"
git -C opal_ai show "$REF:$F" > "$T/v.ps1" 2>/dev/null
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"
python -c "import json,sys;json.dump({'checkout_dir':sys.argv[2]+'\\\\co','state_dir':sys.argv[2]+'\\\\st','workspace_probe_file':sys.argv[2]+'\\\\probe.txt','prod_ref':'PROD'},open(sys.argv[1],'w'))" "$T/cfg.json" "$WT"
timeout 30 powershell -NoProfile -Command "\$p = ConvertTo-SecureString 'Zz9-not-a-real-pw-OAf4' -AsPlainText -Force; New-Object System.Management.Automation.PSCredential('NoSuchUser_OAf4', \$p) | Export-Clixml -LiteralPath '$WT\\bogus.xml'" >/dev/null 2>&1
out=$(timeout 90 powershell -NoProfile -ExecutionPolicy Bypass -File "$WT\\v.ps1" -Config "$WT\\cfg.json" -CredPath "$WT\\bogus.xml" 2>&1 | tr -d '\r'); rc=$?
line=$(printf '%s\n' "$out" | grep -m1 '^BOUNDARY:')
rm -rf "$T"
echo "opal_ai $REF: rc=$rc line='${line:-none}'"
if [ "$rc" = 3 ] && printf '%s' "$line" | grep -q '^BOUNDARY: ERROR'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
