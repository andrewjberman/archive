#!/usr/bin/env bash
# MX-d-8 AC1 (FWD-14, FWD-17): the routing harness carries Alyssa's six phrasings (Q28-Q33) and the three write asks
# (Q34-Q36), each quoted from PRD v0.7 FWD-14/FWD-17, and routes all 9 to their expected entry on the first try; the
# original 27 asks keep the round-7 floor of 24.
. "$(dirname "$0")/_root.sh"
out=$(cd "$GW" && timeout 110 python tests/routing/run_routing.py 2>&1 | tr -d '\r'); rc=$?
hit=0; seen=0
for q in Q28 Q29 Q30 Q31 Q32 Q33 Q34 Q35 Q36; do
  l=$(printf '%s\n' "$out" | grep -E "^$q " | tail -1)
  [ -n "$l" ] && seen=$((seen+1))
  printf '%s' "$l" | grep -qE ' HIT( |$)' && hit=$((hit+1)) || echo "NOT HIT: ${l:-$q absent}"
done
orig=0; for i in $(seq -w 1 27); do printf '%s\n' "$out" | grep -E "^Q$i " | grep -qE ' HIT( |$)' && orig=$((orig+1)); done
echo "her phrasings + write asks: present $seen of 9, routed $hit of 9 on the first try; original asks routed $orig of 27 (floor 24)"
if [ "$hit" = 9 ] && [ "$orig" -ge 24 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
