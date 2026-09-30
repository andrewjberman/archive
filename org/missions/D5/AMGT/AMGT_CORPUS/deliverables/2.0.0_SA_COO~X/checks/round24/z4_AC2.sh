#!/usr/bin/env bash
# AMGT_CORPUS round 24 -- check as a file: z4_AC2 -- the per-site path tests for BP/_LN_Equity and BRK/B_US_Equity with the encoder's suite. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -p no:cacheprovider lib/research/identity/tests/test_slash_safe_key_sites.py lib/research/identity/tests/test_slash_safe_key.py 2>&1 | grep -E 'passed|failed|error|no tests ran' | tail -2
