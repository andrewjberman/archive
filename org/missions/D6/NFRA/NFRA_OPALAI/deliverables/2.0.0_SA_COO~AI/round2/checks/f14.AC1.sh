#!/usr/bin/env bash
# OA-f-14 AC1 (the built behaviour, CTO R25.3 @ NFRA_OPLGTW ledger/ROUND_ANALYSIS.round19.md:100): a SCOPED identity's
# /login consent asks only for the Graph scopes its allowlisted tools need, from a per-tool scope map; an UNSCOPED
# identity's consent is the full GRAPH_SCOPES envelope, unchanged. Six NAMED tests in the NEW
# tests/test_scoped_consent_r253.py must each PASS, with 0 failed or errored tests in that file.
. "$(dirname "$0")/_root.sh"
G=infra/aws/ec2/opal-gateway
T=tests/test_scoped_consent_r253.py
[ -f "$G/$T" ] || { echo "$T absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$G" && timeout 110 python -m pytest "$T" -rA -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r' | grep -v '^[[:space:]]*$')
need="test_r253_map_covers_every_scoped_tool test_r253_map_scopes_are_consented test_r253_concierge_consent_is_narrow test_r253_unscoped_consent_unchanged test_r253_both_legs_same_scopes test_r253_silent_acquire_within_consent"
n=0; p=0; miss=""
for t in $need; do n=$((n+1)); if printf '%s\n' "$out" | grep -qE "^PASSED tests[/\]test_scoped_consent_r253[.]py::$t( |$)"; then p=$((p+1)); else miss="$miss $t"; fi; done
failed=$(printf '%s\n' "$out" | grep -cE '^(FAILED|ERROR) ')
summ=$(printf '%s\n' "$out" | tail -1)
echo "named arms passed $p of $n; failed/errored tests $failed; summary: $summ"
[ -n "$miss" ] && echo "not passed:$miss"
if [ "$p" = "$n" ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
