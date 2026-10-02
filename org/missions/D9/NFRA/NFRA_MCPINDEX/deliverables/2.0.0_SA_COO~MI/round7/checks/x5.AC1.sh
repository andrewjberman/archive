#!/usr/bin/env bash
# MX-x-5 AC1 (Z-W23-S2): the halt-gate recipient-scoping test passes on the session-resolved serial (no .agent_context).
. "$(dirname "$0")/_root.sh"
out=$(timeout 110 bash .tools/test-haltgt-recipient-scoping.sh 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -4
c=$(grep -c "agent_context" .tools/test-haltgt-recipient-scoping.sh); echo ".agent_context references in the fixture: $c"; [ "$c" = 0 ] || rc=1
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
