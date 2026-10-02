#!/usr/bin/env bash
# MX-x-5 AC3 (Z-S75): the aws shim (.tools/aws and .tools/aws.cmd) exports PYTHONUTF8=1 so non-ASCII CLI output decodes;
# its test prints a non-ASCII glyph through the shim's environment without a charmap error.
. "$(dirname "$0")/_root.sh"
t=.tools/tests/test_aws_shim_utf8.sh
[ -f "$t" ] || { echo "$t absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 110 bash "$t" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -4
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
