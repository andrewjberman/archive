#!/usr/bin/env bash
# AMGT_CORPUS round 17 -- check as a file (spine v3.19 L6): s1_AC3 -- the bound. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
base=$(git merge-base HEAD CLOUD); n=$(git diff --name-only "$base" HEAD | grep -v -E '^org/missions/D5/AMGT/AMGT_CORPUS/(deliverables/0\.9\.0_WK_AMGT_CORPUS~1/|surprise-channel/investigations/INVESTIGATION_v1\.md$|task-orders/AMGT_CORPUS\.TO-CRPS\-s\-1\.)' | wc -l); echo "paths_outside_grant $n"
