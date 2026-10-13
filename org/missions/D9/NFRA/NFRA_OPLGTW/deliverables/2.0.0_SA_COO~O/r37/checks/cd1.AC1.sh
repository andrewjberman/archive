#!/usr/bin/env bash
# OPLGTW OG-cd-1 AC1 (round-37 R3, PRD v2.6 FWD-20): app/family_depth.py builds the per-family cadence and depth read.
# Three named offline tests in tests/test_og_cd1.py (AWS stubbed):
#  ac01 -- the family list is DERIVED: a planted extra integration / silver family appears with no code change, and a
#          channel with no sweep family reads claim "absent" with a reason;
#  ac02 -- every value carries a claim in {measured, inferred, absent}; the schedule is the stubbed EventBridge rule's
#          ScheduleExpression, never a typed string; depth comes from backfill-status and the earliest served partition;
#  ac03 -- read-only: a stub client that raises on any write/invoke API is never tripped, and an unreadable source yields
#          claim "absent" with its reason, never a default value.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_cd1.py test_ogcd1_ac01 test_ogcd1_ac02 test_ogcd1_ac03; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
