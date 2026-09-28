#!/usr/bin/env bash
# AMGT_RESAPP round 46 -- check as a file: uu-1 AC3. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
base=$(git merge-base HEAD CLOUD); n=$(git diff --name-only "$base" HEAD | grep -v -E '^org/missions/D5/AMGT/AMGT_RESAPP/(deliverables/0\.9\.0_WK_AMGT_RESAPP~167/|surprise-channel/investigations/INVESTIGATION_v1\.md$|task-orders/AMGT_RESAPP\.TO-AMGT-uu-1\.)' | wc -l); echo "paths_outside_grant $n"; [ "$n" = 0 ]
