#!/usr/bin/env bash
# AMGT_RESAPP round 40, AMGT-ro-1 AC3 (BOUND) -- the print package's tests pass, the cell's new ones among them.
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
python -m pytest -q lib/research/print -p no:cacheprovider 2>&1 | tail -2
exit "${PIPESTATUS[0]}"
