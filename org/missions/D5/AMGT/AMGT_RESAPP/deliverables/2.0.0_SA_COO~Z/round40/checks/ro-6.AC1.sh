#!/usr/bin/env bash
# AMGT_RESAPP round 40, AMGT-ro-6 AC1 -- the Deere key-form trace exists with its four required sections.
set -u
ROOT="$(git rev-parse --show-toplevel)"; F="$ROOT/org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~157/KEYFORM_TRACE.md"
[ -s "$F" ] || { echo "absent: KEYFORM_TRACE.md"; exit 1; }
n=0; for h in '^## 1\. PEERS' '^## 2\. POSTURE' '^## 3\. CROSSWALK' '^## 4\. THE RULE PROPOSED'; do c=$(grep -c -E "$h" "$F"); echo "$c  $h"; [ "$c" -ge 1 ] && n=$((n+1)); done
echo "sections present: $n of 4"; [ "$n" -eq 4 ]
