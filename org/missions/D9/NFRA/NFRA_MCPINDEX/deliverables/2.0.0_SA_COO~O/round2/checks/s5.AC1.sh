#!/usr/bin/env bash
# MX-s-5 AC1: infra/aws/lambda/ci/lambda-source-map.json at HEAD holds 0 non-ASCII characters (CLAUDE.md "No non-ASCII":
# ALL non-ASCII out, so every reader -- including record-terraform-deploy.sh's default-codepage read -- decodes it) and
# still parses as JSON. Character count, never a byte delta.
. "$(dirname "$0")/_root.sh"
out=$(git show HEAD:infra/aws/lambda/ci/lambda-source-map.json | python -c "
import json,sys
t=sys.stdin.buffer.read().decode('utf-8')
json.loads(t)
print('nonascii_chars=%d json=ok' % sum(1 for ch in t if ord(ch)>127))" 2>&1 | tr -d '\r')
echo "$out"
if printf '%s' "$out" | grep -q '^nonascii_chars=0 json=ok$'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
