#!/usr/bin/env bash
# MS-sg-1 AC2 (the control -- Opal-staff serving and round 1's firm path are unmoved with MSP_CALLING_IDENTITIES empty):
# the asker, adapter and round-1 suites pass with nothing failed and at least 48 passed.
. "$(dirname "$0")/_root.sh"
out=$(cd "$G" && AUDIT_PATH="$(mktemp "${TMPDIR:-/tmp}/ms_e2g_audit.XXXXXX")" timeout 110 python -m pytest tests/test_asker_scope.py tests/test_asker_binding.py tests/test_asker_nochannels.py tests/test_access_state.py tests/test_email_deny.py tests/test_mcpmsp_asker_firm.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
tail=$(printf '%s\n' "$out" | tail -1)
failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
passed=$(printf '%s' "$tail" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); passed=${passed:-0}
echo "asker + adapter + round-1 suites: $tail"
if [ "$failed" = 0 ] && [ "$passed" -ge 48 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
