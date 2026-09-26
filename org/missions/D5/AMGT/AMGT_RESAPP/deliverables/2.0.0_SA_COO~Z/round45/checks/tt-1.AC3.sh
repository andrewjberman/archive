#!/usr/bin/env bash
# AMGT_RESAPP round 45, AMGT-tt-1 AC3 (BOUND) -- the export's unit tests pass.
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
PYTHONPATH="$ROOT" python -m pytest lib/research/print/tests -q 2>&1 | tail -3
exit ${PIPESTATUS[0]}
