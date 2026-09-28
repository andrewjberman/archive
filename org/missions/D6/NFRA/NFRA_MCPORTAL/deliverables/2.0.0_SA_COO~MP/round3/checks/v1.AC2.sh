#!/usr/bin/env bash
# MP-v-1 AC2 (A2, the /sprint arm): inside the worker's recorded window, the gateway's own access log holds a 200 for
# GET /sprint -- the one page served to a signed-in account that is not the owner (C2's /sprint exception).
. "$(dirname "$0")/_root.sh"
. "$(dirname "$0")/_journal.sh"
n200=$(printf '%s\n' "$J" | grep -cE '"GET /sprint HTTP/1.1" 200')
nall=$(printf '%s\n' "$J" | grep -cE '"GET /sprint HTTP/1.1" [0-9]{3}')
echo "GET /sprint in window: 200=$n200 of $nall"
if [ "$n200" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
