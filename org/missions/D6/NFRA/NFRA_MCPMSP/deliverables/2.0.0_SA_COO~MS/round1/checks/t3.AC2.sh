#!/usr/bin/env bash
# MS-t-3 AC2 (the behaviour, with its difference control): provision-account.ps1 -Plan changes nothing and prints
# "PLAN: CREATE-USER Opal_Agent" for the UNCHANGED example config (no account_name key: Opal_Agent unmoved) and
# "PLAN: CREATE-USER Opal_MSP" for provision/runtime.msp.config.example.json.
. "$(dirname "$0")/_root.sh"
P="opal_ai/opal/runtime/provision/provision-account.ps1"
A="opal_ai/opal/runtime/provision/runtime.config.example.json"
B="opal_ai/opal/runtime-msp/provision/runtime.msp.config.example.json"
for f in "$P" "$A" "$B"; do [ -f "$f" ] || { echo "$f absent"; echo "RESULT: FAIL"; exit 1; }; done
run() { timeout 60 powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(native "$P")" -Config "$(native "$1")" -Plan 2>&1 | tr -d '\r' | grep -m1 'PLAN: CREATE-USER'; }
a=$(run "$A"); b=$(run "$B")
echo "default config -> ${a:-NONE}; msp config -> ${b:-NONE}"
if [ "$a" = "PLAN: CREATE-USER Opal_Agent" ] && [ "$b" = "PLAN: CREATE-USER Opal_MSP" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
