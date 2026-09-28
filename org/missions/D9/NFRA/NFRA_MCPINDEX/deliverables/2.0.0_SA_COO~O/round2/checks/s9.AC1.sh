#!/usr/bin/env bash
# MX-s-9 AC1 (the firm line): a bd bronze module for the asset-dim REST pull exists under
# data/black_diamond/scripts/bronze/ (a .py whose name contains "asset"), it imports nothing from data/cot/ or any
# cot_* module, and NO file under data/cot/ changed between the issuance base and HEAD.
. "$(dirname "$0")/_root.sh"
BASE="${MXS9_BASE:-$(git log -1 --format=%H --grep='issue(NFRA_MCPINDEX.TO-MX-s-9' HEAD)}"
[ -n "$BASE" ] || { echo "issuance commit not found -- RESULT: FAIL"; exit 1; }
mods=$(git ls-files 'data/black_diamond/scripts/bronze/*asset*.py')
n=$(printf '%s\n' "$mods" | grep -c .)
cotimp=0; for m in $mods; do grep -qE '(^|[^A-Za-z_])(data\.cot|data/cot|cot_bronze_ingest|from cot|import cot)' "$m" && cotimp=$((cotimp+1)); done
cotdiff=$(git diff --name-only "$BASE" HEAD -- data/cot/ | grep -c .)
echo "bd bronze asset modules=$n; modules importing cot=$cotimp; data/cot files changed since issue=$cotdiff"
if [ "$n" -ge 1 ] && [ "$cotimp" = 0 ] && [ "$cotdiff" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
