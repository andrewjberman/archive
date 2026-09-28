#!/usr/bin/env bash
# AMGT_RESAPP round 46, AMGT-uu-3 AC3 -- the bound: the case-rule, export and producer-guard suites pass on this tree.
# usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
PYTHONPATH="$ROOT" timeout 110 python -m pytest -q -p no:cacheprovider \
  lib/research/api/tests/test_model_cases.py lib/research/print/tests \
  integrations/bloomberg/research/tests/test_model_cases_guard.py integrations/bloomberg/research/tests/test_band_basis.py 2>&1 | tail -2
exit "${PIPESTATUS[0]}"
