#!/usr/bin/env bash
# MX-c-6 AC3 (C2, C3): every tool named by a `needs:` entry is registered by some gateway integration; unknown 0, and
# at least one need names a tool.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
out=$(timeout 60 python "$(native "$H/c6_tools.py")" "$(native "$(pwd)/$GW")" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -5
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
