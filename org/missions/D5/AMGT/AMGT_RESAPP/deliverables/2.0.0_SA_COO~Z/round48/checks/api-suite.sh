#!/usr/bin/env bash
# AMGT_RESAPP round 48 -- the bound shared by ww-2 and ww-4: the scoped API's and the print path's own suites pass on this tree.
# usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
PYTHONPATH="$ROOT" timeout 115 python -m pytest -q -p no:cacheprovider lib/research/api/tests lib/research/print/tests 2>&1 | tail -2
exit "${PIPESTATUS[0]}"
