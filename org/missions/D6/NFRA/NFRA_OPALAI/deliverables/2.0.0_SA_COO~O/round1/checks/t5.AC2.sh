#!/usr/bin/env bash
# OA-t-5 AC2 (seam, REAL neighbour = the live policy store, read-only): asker_scope.probe_store() against the gateway's
# configured store returns NO-PROFILE for a random never-profiled principal, and STORE-UNAVAILABLE for the same principal
# against a table that does not exist -- the two failure shapes are distinguishable, so a dead store can never read as
# "this asker has no policy".
. "$(dirname "$0")/_root.sh"
cd infra/aws/ec2/opal-gateway || { echo "gateway dir absent"; echo "RESULT: FAIL"; exit 1; }
[ -f app/asker_scope.py ] || { echo "app/asker_scope.py absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 90 python -c "
from app import asker_scope as a
tid='00000000-0000-4000-8000-0000000000a1'; oid='00000000-0000-4000-8000-0000000000b2'
print('live=' + a.probe_store(tid, oid))
print('bogus=' + a.probe_store(tid, oid, table='opal-nonexistent-table-oa-t5-probe'))
" 2>&1 | tr -d '\r')
live=$(printf '%s\n' "$out" | grep -m1 '^live=' | sed 's/^live=//')
bogus=$(printf '%s\n' "$out" | grep -m1 '^bogus=' | sed 's/^bogus=//')
echo "live store: ${live:-(none)}; bogus table: ${bogus:-(none)}"
[ -z "$live" ] && printf '%s\n' "$out" | tail -3
if [ "$live" = NO-PROFILE ] && [ "$bogus" = STORE-UNAVAILABLE ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
