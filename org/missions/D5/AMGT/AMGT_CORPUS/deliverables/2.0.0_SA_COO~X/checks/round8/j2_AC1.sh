#!/usr/bin/env bash
# AMGT_CORPUS round 8 -- check as a file (spine v3.19 L6): j2_AC1. Run from the repo root under the worker timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH=.
out=$(python -m lib.research.corpus.readonly_proof --code-census 2>&1); rc=$?
t=$(printf '%s\n' "$out" | grep -E '^tristate library ' | tail -1)
lib=$(printf '%s\n' "$t" | sed -n 's/^tristate library \([0-9]*\) unresolved.*/\1/p'); un=$(printf '%s\n' "$t" | sed -n 's/.* unresolved \([0-9]*\) clear.*/\1/p')
printf '%s\n' "$out" | grep -E '^unresolved_site ' | head -10
echo "j2 tristate_unresolved ${un:-UNREAD} library ${lib:-UNREAD} rc $rc"
