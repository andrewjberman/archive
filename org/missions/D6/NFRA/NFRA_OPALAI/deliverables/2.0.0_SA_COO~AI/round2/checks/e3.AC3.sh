#!/usr/bin/env bash
# OA-e-3 AC3 (the built behaviour, AT THE RELEASE BRANCH): tests/test_identity_scope.py as it stands on the release branch
# passes, and its named test test_concierge_seed_admits_asker_query PASSED (the concierge is admitted opal_asker_query and
# the seed differs from the live base by exactly that one tool).
. "$(dirname "$0")/_root.sh"
B="rel-nfra-opalai-r2-asker-switch-on-gateway"
git rev-parse -q --verify "$B" >/dev/null || { echo "release branch $B absent"; echo "RESULT: FAIL"; exit 1; }
tmp=$(mktemp -d)
git archive "$B" infra/aws/ec2/opal-gateway | tar -x -C "$tmp" || { echo "archive failed"; rm -rf "$tmp"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$tmp/infra/aws/ec2/opal-gateway" && timeout 110 python -m pytest tests/test_identity_scope.py -rA -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r' | grep -v '^[[:space:]]*$')
rm -rf "$tmp"
named=$(printf '%s\n' "$out" | grep -cE "^PASSED tests/test_identity_scope.py::test_concierge_seed_admits_asker_query( |$)")
failed=$(printf '%s\n' "$out" | grep -cE '^(FAILED|ERROR) ')
echo "named test passed=$named; failed/errored=$failed; summary: $(printf '%s\n' "$out" | tail -1)"
if [ "$named" = 1 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
