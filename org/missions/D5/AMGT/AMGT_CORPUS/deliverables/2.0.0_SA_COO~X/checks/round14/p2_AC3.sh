#!/usr/bin/env bash
# AMGT_CORPUS round 14 -- check as a file (spine v3.19 L6): p2_AC3. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
base=$(git merge-base HEAD CLOUD); n=$(git diff --name-only "$base" HEAD | grep -v -E '^(org/missions/D5/AMGT/AMGT_CORPUS/(deliverables/0\.9\.0_WK_AMGT_CORPUS~2/|surprise-channel/investigations/INVESTIGATION_v1\.md$|task-orders/AMGT_CORPUS\.TO-CRPS\-p\-2\.)|lib/research/corpus/tests/test_induction_planted_drive\.py$)' | wc -l); echo "paths_outside_grant $n"
