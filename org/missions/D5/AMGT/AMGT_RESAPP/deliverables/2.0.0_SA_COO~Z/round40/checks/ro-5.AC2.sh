#!/usr/bin/env bash
# AMGT_RESAPP round 40, AMGT-ro-5 AC2 (BOUND) -- the posture package's tests pass.
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
python -m pytest -q lib/research/posture -p no:cacheprovider 2>&1 | tail -2
exit "${PIPESTATUS[0]}"
