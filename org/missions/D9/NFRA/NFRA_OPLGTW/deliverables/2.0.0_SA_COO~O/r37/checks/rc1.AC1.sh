#!/usr/bin/env bash
# OPLGTW OG-rc-1 AC1 (round-37 round-close hygiene): the round-close check no longer lists OG-cl-7, OG-cl-8 or OG-gf-1 as PROOF-BAD.
#  - OG-gf-1's proof instance carries the order's slug (NFRA_OPLGTW.TO-OG-gf-1.gf-wave-b-remainder.proof_of_spec.json);
#  - OG-cl-7's and OG-cl-8's instances record AC2 as PASS on the re-run at the current trunk (the naming gate now reads name_rulings.json).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(timeout 100 python .tools/round-close-check.py --project NFRA_OPLGTW --round 37 2>&1 | tr -d '\r')
bad=$(printf '%s\n' "$out" | grep -E 'PROOF-BAD' | grep -cE 'TO-OG-(cl-7|cl-8|gf-1):')
total=$(printf '%s\n' "$out" | grep -c 'PROOF-BAD')
echo "round-close PROOF-BAD lines for cl-7, cl-8, gf-1: $bad (want 0); PROOF-BAD lines in all: $total"
[ "$bad" = 0 ] && [ -n "$out" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
