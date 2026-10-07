#!/usr/bin/env bash
# OPLGTW OG-al-2 AC2 (ONE row, nothing else): against the r25 release sha, identity_tool_allowlist.txt gains exactly ONE
# non-comment line and loses none; that line names opal_data_refresh_status, carries no client= qualifier, and its
# identity is one the overlay already names; the lines above it carry the authorization (the record's path). And
# test_scoped_consent_r253.py and test_data_entitlement_guard.py still pass whole.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
A="$GW/identity_tool_allowlist.txt"
line=$(python "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r26/checks/al2_row_ok.py" 240ac2fe5abde944f15358ab563cb4b2ab63f09f "$A" | tr -d '\r'); rc=$?
export AUDIT_PATH="${TMP:-/tmp}/og_r26_al2b_audit_$$.jsonl"
ok=0; n=0
for f in tests/test_scoped_consent_r253.py tests/test_data_entitlement_guard.py; do
  n=$((n+1)); (cd "$GW" && timeout 300 python -m pytest "$f" -q -p no:cacheprovider --color=no >/dev/null 2>&1) && ok=$((ok+1))
done
restore_audit; rm -f "$AUDIT_PATH"
echo "$line; guard test files green $ok of $n"
[ "$rc" = 0 ] && [ "$ok" = "$n" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
