#!/usr/bin/env bash
# AMGT_CORPUS round 26 -- check as a file: ab5_AC2 -- the round-26 label tests with the currency-label suites. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -p no:cacheprovider integrations/bloomberg/research/tests/test_figure_currency_round26.py integrations/bloomberg/research/tests/test_figure_currency_round25.py integrations/bloomberg/research/tests/test_currency_labels.py 2>&1 | grep -E 'passed|failed|error|no tests ran' | tail -2
