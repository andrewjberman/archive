#!/usr/bin/env bash
# MX-x-4 AC2 (row Z-W21-S21): the halt gate resolves the serial for THIS session and tree -- a worktree that shares the
# issuer's session id but declares its own serial resolves to its own, and the issuer's tree still resolves to the issuer.
. "$(dirname "$0")/_root.sh"
t=.tools/tests/test_halt_gate_session_serial.sh
[ -f "$t" ] || { echo "$t absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 110 bash "$t" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -6
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
