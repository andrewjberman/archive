#!/usr/bin/env bash
# OA-w-3 AC2 (difference control against AC1): the same standalone clone with ONE planted file -- a .py that does not
# compile and carries a non-ASCII byte -- makes run_checks.sh exit non-zero and print "CHECKS: FAIL" naming both
# py_compile and ascii. Same harness, one file flipped.
. "$(dirname "$0")/_root.sh"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/oa_w3_ac2_$$"; rm -rf "$T"
timeout 60 git clone -q "$(pwd)/opal_ai" "$T/c" 2>&1 | tail -2
[ -f "$T/c/opal/checks/run_checks.sh" ] || { echo "run_checks.sh absent in the clone"; rm -rf "$T"; echo "RESULT: FAIL"; exit 1; }
printf 'def broken(:\n    return "caf\xc3\xa9"\n' > "$T/c/opal/_oa_w3_plant.py"
out=$(cd "$T/c" && timeout 100 env -u PYTHONPATH bash opal/checks/run_checks.sh 2>&1 | tr -d '\r'); rc=$?
rm -rf "$T"
v=$(printf '%s\n' "$out" | grep -m1 -E '^CHECKS: ' || echo "(no CHECKS line)")
pc=$(printf '%s\n' "$out" | grep -ci 'py_compile'); as=$(printf '%s\n' "$out" | grep -ci 'ascii')
echo "rc=$rc; $v; py_compile named=$pc; ascii named=$as"
if [ "$rc" != 0 ] && [ "$v" = "CHECKS: FAIL" ] && [ "$pc" -ge 1 ] && [ "$as" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
