#!/usr/bin/env bash
# AMGT_CORPUS round 16 -- check as a file (spine v3.19 L6): r1_AC3. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
base=$(git merge-base HEAD CLOUD); n=$(git diff --name-only "$base" HEAD | grep -v -E '^(org/missions/D5/AMGT/AMGT_CORPUS/(deliverables/0\.9\.0_WK_AMGT_CORPUS~1/|surprise-channel/investigations/INVESTIGATION_v1\.md$|task-orders/AMGT_CORPUS\.TO-CRPS\-r\-1\.)|lib/research/corpus/(schedule_induction\.ps1|induction_scheduled\.py|tests/test_induction_schedule\.py)$)' | wc -l); echo "paths_outside_grant $n"
