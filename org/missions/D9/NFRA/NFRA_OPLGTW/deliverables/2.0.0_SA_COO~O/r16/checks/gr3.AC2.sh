#!/usr/bin/env bash
# OPLGTW OG-gr-3 AC2, AMENDED A1 (narrow): every gateway file the cell's worker commits touched (since the issuance
# 565223dd62's base 8e0fed682a) is app/integrations/schwab/{query.py,integration.py (A2, R9a)}, app/integrations/schwab/datasets.json, or a
# tests/test_schwab_*.py file (A1: fixture updates for R9's grain columns only), and GR3_TEST_EDITS.md names every
# EXISTING test file the cell edited, with its reason.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="0.9.0_WK_NFRA_OPLGTW~22 <"; S="$GW/app/integrations/schwab"
E="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~22/GR3_TEST_EDITS.md"
files=$(git log --author="$W" --format= --name-only 8e0fed682a..HEAD -- "$GW" | grep . | sort -u)
n=$(printf '%s\n' "$files" | grep -c .)
no=$(printf '%s\n' "$files" | grep . | grep -vxE "$S/query\.py|$S/datasets\.json|$S/integration\.py|$GW/tests/test_schwab_[a-z0-9_]+\.py" | grep -c .)
tf=$(printf '%s\n' "$files" | grep -xE "$GW/tests/test_schwab_[a-z0-9_]+\.py" | grep -v "test_schwab_grain_r9\.py")
nt=$(printf '%s\n' "$tf" | grep -c .)
unl=0
for f in $tf; do
  if [ ! -f "$E" ] || ! grep -qF "$(basename "$f")" "$E"; then unl=$((unl+1)); fi
done
echo "gateway files touched by the cell's commits since the issuance: $n; outside the allowed set: $no; edited existing test files $nt, not listed in GR3_TEST_EDITS.md $unl"
[ "$n" -ge 2 ] && [ "$no" = 0 ] && [ "$unl" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
