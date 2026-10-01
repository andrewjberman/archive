#!/usr/bin/env bash
# OPLGTW TRNSPT-DEPS OG-tx-1 AC2: the three transcript tools are read class (in BOTH SAFE_TOOLS and NATIVE_TOOLS), no
# Graph scope is added (C7), and the gateway's hard tool count (test_ogz2_ac08) matches the registry after the add.
. "$(dirname "$0")/_root.sh"
H="$(pwd)/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/trnspt/checks"
reg=$(cd "$GW" && timeout 60 python "$(native "$H/_reg.py")" find_online_meeting list_meeting_transcripts read_meeting_transcript 2>&1 | tr -d '\r')
printf '%s\n' "$reg"
AUDIT_PATH="$(mktemp)"; export AUDIT_PATH
pytest_named tests/test_entitlement_admin.py test_ogz2_ac08; c=$?; restore_audit; rm -f "$AUDIT_PATH"
if printf '%s\n' "$reg" | grep -q "^REG 3 of 3; SCOPES same$" && [ "$c" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
