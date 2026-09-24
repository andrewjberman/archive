#!/usr/bin/env bash
# AMGT_RESAPP round 39, AMGT-rn-2 AC3 (BOUND + the cell's own test) -- the peers package's tests stay green, the
# cell's new test among them. usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
python -m pytest -q lib/research/peers/tests -p no:cacheprovider 2>&1 | tail -3
exit "${PIPESTATUS[0]}"
