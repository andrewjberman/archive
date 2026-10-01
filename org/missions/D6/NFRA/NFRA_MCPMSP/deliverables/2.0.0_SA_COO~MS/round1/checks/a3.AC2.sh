#!/usr/bin/env bash
# MS-a-3 AC2 (the boundary, exercised AS the account with its own credential): verify-boundary.ps1 with the real MSP
# config at C:\opal_runtime_msp\runtime.msp.config.json prints "BOUNDARY: DENIED-OK" (the workspace probe read is
# denied to Opal_MSP while its state dir is writable).
. "$(dirname "$0")/_root.sh"
V="opal_ai/opal/runtime/provision/verify-boundary.ps1"; C='C:\opal_runtime_msp\runtime.msp.config.json'
[ -f "$V" ] || { echo "$V absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(native "$V")" -Config "$C" 2>&1 | tr -d '\r' | grep -m1 'BOUNDARY:')
echo "verify-boundary (msp config): ${out:-NONE}"
if [ "$out" = "BOUNDARY: DENIED-OK" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
