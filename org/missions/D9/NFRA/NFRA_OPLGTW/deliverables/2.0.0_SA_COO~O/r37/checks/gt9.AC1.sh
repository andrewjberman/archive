#!/usr/bin/env bash
# OPLGTW OG-gt-9 AC1 (round-37 G1-FIX, FWD-22): the three named offline tests of the window pruning pass.
#  ac01: partitions dated before the earliest fetched_at day of the page are NOT read (a recording client counts the reads);
#  ac02: difference control -- on a synthetic dataset where every sentiment row is scored on/after its fetch, the pruned answer
#        equals the unpruned answer, and a partition older than the cut holds a decoy row that the pruned read never returns;
#  ac03: the envelope denominator states partitions read of partitions total.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_gt9.py test_oggt9_ac01 test_oggt9_ac02 test_oggt9_ac03; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
