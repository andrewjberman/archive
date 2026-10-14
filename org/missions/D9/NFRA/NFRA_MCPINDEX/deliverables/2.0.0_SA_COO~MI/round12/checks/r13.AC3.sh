#!/usr/bin/env bash
# MX-r-13 AC3 (FWD-20 depth on the DEPLOYED catalog bytes, EVERY (a) tool): c10.AC1 (per-tool claims, measured ones
# agreeing with the aws CLI, no absent on a dated artifact) AND c10.AC3 (answer-time depth on every measured row, with
# the CVO's two anchors), run on this tree, whose catalog and discover equal the deployed bytes once the ledger closes.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
a=$(bash "$H/c10.AC1.sh" 2>&1); ar=$?; b=$(bash "$H/c10.AC3.sh" 2>&1); br=$?
printf '%s\n' "$a" | grep -E '^DEPTH'; printf '%s\n' "$b" | grep -E '^ANSWER-TIME'
echo "catalog rc=$ar; answer-time rc=$br"
if [ "$ar" = 0 ] && [ "$br" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
