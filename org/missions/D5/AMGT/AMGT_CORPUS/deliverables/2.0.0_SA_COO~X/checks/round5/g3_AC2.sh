#!/usr/bin/env bash
# AMGT_CORPUS round 5 -- check as a file (spine v3.19 L6): g3_AC2. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
python -m lib.research.corpus.backlog --coverage-dry-run 2>&1 | grep -v -E 'fitz|MuPDF' | tail -4
