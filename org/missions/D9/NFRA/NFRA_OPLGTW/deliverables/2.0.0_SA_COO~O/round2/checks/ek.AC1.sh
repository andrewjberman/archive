#!/usr/bin/env bash
# OPLGTW OG-e-1 AC1: the new email-deny suite passes, 11 tests (A1), without moto. AUDIT_PATH points at a temp file so the
# run never writes the tracked infra/aws/ec2/opal-gateway/audit.jsonl.
R="$(git rev-parse --show-toplevel)"; cd "$R/infra/aws/ec2/opal-gateway" || exit 9
export AUDIT_PATH="$(mktemp)"
out=$(timeout 300 python -m pytest tests/test_email_deny.py -q -p no:cacheprovider --color=no 2>&1 | tail -1)
rm -f "$AUDIT_PATH"
echo "$out"
if printf '%s' "$out" | grep -Eq '^11 passed' && ! printf '%s' "$out" | grep -Eq 'failed|error'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
