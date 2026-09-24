#!/usr/bin/env bash
# OA-w-3 AC1 (FWD-13, built): a STANDALONE clone of the nested opal_ai at its HEAD -- no workspace on the path -- runs
# opal/checks/run_checks.sh to exit 0 and prints "CHECKS: PASS" with its denominators.
. "$(dirname "$0")/_root.sh"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/oa_w3_ac1_$$"; rm -rf "$T"
timeout 60 git clone -q "$(pwd)/opal_ai" "$T/c" 2>&1 | tail -2
[ -f "$T/c/opal/checks/run_checks.sh" ] || { echo "run_checks.sh absent in the clone"; rm -rf "$T"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$T/c" && timeout 100 env -u PYTHONPATH bash opal/checks/run_checks.sh 2>&1 | tr -d '\r'); rc=$?
rm -rf "$T"
printf '%s\n' "$out" | tail -6
if [ "$rc" = 0 ] && printf '%s\n' "$out" | grep -qx 'CHECKS: PASS'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
