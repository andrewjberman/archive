#!/usr/bin/env bash
# MX-x-4 AC1 (row Z-W21-S23): the deploy wrapper's manifest rewrite is UTF-8 through a JSON parser -- on a fixture manifest
# carrying non-ASCII escapes it moves exactly the target service's keys and leaves every other entry equal.
. "$(dirname "$0")/_root.sh"
t=.tools/tests/test_safe_ec2_deploy_manifest.py
[ -f "$t" ] || { echo "$t absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 110 python -m pytest "$t" -q -rA -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -6
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
