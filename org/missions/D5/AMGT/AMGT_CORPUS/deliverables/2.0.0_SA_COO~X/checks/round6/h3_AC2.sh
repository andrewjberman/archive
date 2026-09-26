#!/usr/bin/env bash
# AMGT_CORPUS round 6 -- check as a file (spine v3.19 L6): h3_AC2. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
python -m lib.research.corpus.readonly_proof --code-census 2>&1 | grep -E '^(tristate|library_write_calls|unresolved_site)' | tail -8
