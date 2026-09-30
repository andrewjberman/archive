#!/usr/bin/env bash
# AMGT_CORPUS round 25 -- check as a file: aa1_AC2 -- the label-rule tests with the existing currency-label suite. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -p no:cacheprovider integrations/bloomberg/research/tests/test_figure_currency_round25.py integrations/bloomberg/research/tests/test_currency_labels.py 2>&1 | grep -E 'passed|failed|error|no tests ran' | tail -2
