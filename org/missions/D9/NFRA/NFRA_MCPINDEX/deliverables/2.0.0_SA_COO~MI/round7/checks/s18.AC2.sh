#!/usr/bin/env bash
# MX-s-18 AC2 (control, CTO 3a negative control ii): data/cot/ is byte-unchanged since the round-7 issuance base
# (cot is a separate firm from bd; the fix lives in the BD runner only).
. "$(dirname "$0")/_root.sh"
B=$(cat "$(dirname "$0")/ISSUANCE_BASE" 2>/dev/null | tr -d "\r\n ")
[ -n "$B" ] || { echo "ISSUANCE_BASE absent"; echo "RESULT: FAIL"; exit 1; }
git diff --quiet "$B" HEAD -- data/cot/; rc=$?
n=$(git diff --name-only "$B" HEAD -- data/cot/ | wc -l)
echo "data/cot/ files changed since $B: $n"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
