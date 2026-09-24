#!/usr/bin/env bash
# AMGT_RESAPP round 40, AMGT-ro-3 AC1 -- the thesis payload carries the SAME describes-the-business verdict the header
# applies: the cell's own test module `lib/research/api/tests/test_thesis_description_verdict.py` exists and passes.
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
T=lib/research/api/tests/test_thesis_description_verdict.py
[ -s "$T" ] || { echo "absent: $T"; exit 1; }
python -m pytest -q "$T" -p no:cacheprovider 2>&1 | tail -2
exit "${PIPESTATUS[0]}"
