#!/usr/bin/env bash
# AMGT_RESAPP round 43, AMGT-rr-2 AC3 (BOUND) -- the portal typechecks after the Model tab change (tsc -b --noEmit).
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
bash org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round39/checks/typecheck.sh
