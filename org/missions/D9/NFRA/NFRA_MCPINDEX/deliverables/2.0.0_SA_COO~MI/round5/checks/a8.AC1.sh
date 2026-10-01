#!/usr/bin/env bash
# MX-a-8 AC1: the refreshed Black Diamond analysis record carries all 9 MX-a-3 sections (as headings) and a live read dated 2026-09-30 or later.
. "$(dirname "$0")/_root.sh"
F="org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~21/analysis-blackdiamond.r5.result.md"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
n=0; for h in "Live prefixes" "Grain" "Freshness" "Scope rule" "Never-sum" "Common questions" "Question to tool" "Read fence" "No-data"; do
  if grep -qiE "^#+ .*$h" "$F"; then n=$((n+1)); else echo "MISSING heading: $h"; fi; done
d=$(grep -oE "^read_at: 20[0-9]{2}-[0-9]{2}-[0-9]{2}" "$F" | head -1 | sed 's/read_at: //')
echo "sections $n of 9; read_at=${d:-absent}"
if [ "$n" = 9 ] && [ -n "$d" ] && [ ! "$d" \< "2026-09-30" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
