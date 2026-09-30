#!/usr/bin/env bash
# AMGT_CORPUS round 18 -- check as a file: t3_AC2 -- the bound (a read-only cell). Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
base=$(git merge-base HEAD CLOUD); n=$(git diff --name-only "$base" HEAD | grep -v -E '^org/missions/D5/AMGT/AMGT_CORPUS/(deliverables/0\.9\.0_WK_AMGT_CORPUS~3/|surprise-channel/investigations/INVESTIGATION_v1\.md$|task-orders/AMGT_CORPUS\.TO-CRPS\-t\-3\.)' | wc -l); echo "paths_outside_grant $n"
