#!/usr/bin/env bash
# OPLGTW OG-gt-6 AC2 (round-37 G1-TYPED, FWD-22): a bound and a regression.
#  - app/harvest_typed.py and app/harvest_read.py are byte-unchanged against the fork point of this branch;
#  - the five tests of tests/test_og_gt0.py still pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
base=$(git merge-base HEAD box/sitez 2>/dev/null | tr -d '\r')
ch=$(git diff --name-only "$base" HEAD -- "$GW/app/harvest_typed.py" "$GW/app/harvest_read.py" | grep -c .)
un=no; [ "$ch" = 0 ] && un=yes
pytest_named tests/test_og_gt0.py test_oggt0_ac01 test_oggt0_ac02 test_oggt0_ac03 test_oggt0_ac04 test_oggt0_ac05; r0=$?
echo "harvest_typed.py and harvest_read.py unchanged vs the base: $un"
restore_audit
[ "$r0" = 0 ] && [ "$un" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
