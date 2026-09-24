#!/usr/bin/env bash
# MP-t-4 AC2 (seam, REAL neighbour = the live grant store, read-only): the handler module's read path, called for a random
# never-profiled principal against the gateway's configured store, answers NO-PROFILE -- a read the box can make -- and
# against a table that does not exist answers STORE-UNAVAILABLE (the two shapes stay distinguishable).
. "$(dirname "$0")/_root.sh"
cd infra/aws/ec2/opal-gateway || { echo "gateway dir absent"; echo "RESULT: FAIL"; exit 1; }
[ -f app/admin_grants.py ] || { echo "app/admin_grants.py absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 90 python -c "
from app import admin_grants as g
tid='00000000-0000-4000-8000-0000000000c3'; oid='00000000-0000-4000-8000-0000000000d4'
print('live=' + g.read_grant_state(tid, oid))
print('bogus=' + g.read_grant_state(tid, oid, table='opal-nonexistent-table-mp-t4-probe'))
" 2>&1 | tr -d '\r')
live=$(printf '%s\n' "$out" | grep -m1 '^live=' | sed 's/^live=//'); bogus=$(printf '%s\n' "$out" | grep -m1 '^bogus=' | sed 's/^bogus=//')
echo "live store: ${live:-(none)}; bogus table: ${bogus:-(none)}"
[ -z "$live" ] && printf '%s\n' "$out" | tail -3
if [ "$live" = NO-PROFILE ] && [ "$bogus" = STORE-UNAVAILABLE ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
