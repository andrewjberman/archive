#!/usr/bin/env bash
# OPLGTW round-38 named-test check: the named tests of one gateway test file all pass (runs in the gateway directory; the helper prints
# "pytest rc=<n>; named tests passed <p> of <n>; failed/error lines <f>").
# Usage: _named.sh <test file under infra/aws/ec2/opal-gateway/> <test name>...
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
f="$1"; shift
[ -n "$f" ] && [ "$#" -ge 1 ] || { echo "usage: _named.sh <file> <test>..."; echo "RESULT: FAIL"; exit 2; }
pytest_named "$f" "$@"; rc=$?
restore_audit
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
