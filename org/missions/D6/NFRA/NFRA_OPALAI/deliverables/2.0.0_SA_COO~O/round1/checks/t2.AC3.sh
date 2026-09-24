#!/usr/bin/env bash
# OA-t-2 AC3 (the verifier on the real box): verify-boundary.ps1 against this box, where Opal_Agent does not exist yet,
# prints "BOUNDARY: NOT-PROVISIONED" and exits 4 -- a verdict distinct from DENIED-OK (0) and BREACH (1), so an absent
# account can never read as a held boundary.
. "$(dirname "$0")/_root.sh"
P="opal_ai/opal/runtime/provision"
[ -f "$P/verify-boundary.ps1" ] || { echo "$P/verify-boundary.ps1 absent"; echo "RESULT: FAIL"; exit 1; }
W=$(cygpath -w "$P/verify-boundary.ps1"); C=$(cygpath -w "$P/runtime.config.example.json")
out=$(timeout 100 powershell -NoProfile -ExecutionPolicy Bypass -File "$W" -Config "$C" 2>&1 | tr -d '\r'); rc=$?
v=$(printf '%s\n' "$out" | grep -m1 -E '^BOUNDARY: ' || echo "(no BOUNDARY line)")
echo "rc=$rc; $v"
if [ "$rc" = 4 ] && [ "$v" = "BOUNDARY: NOT-PROVISIONED" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
