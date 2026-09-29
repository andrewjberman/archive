#!/usr/bin/env bash
# AMGT_RESAPP round 47, AMGT-vv-3 AC2 -- leadPanelPattern.harness.cjs reads NO check the wrong way (row Z-W167-S2; at the cut:
# rows_rendered, source_caption_wraps, disclosure_own_line, caption_facts_unchanged). usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
out="$(timeout 100 node src/pages/SecurityAnalysis/__harness__/leadPanelPattern.harness.cjs 2>&1)"; rc=$?
n=$(printf '%s\n' "$out" | grep -c '^CHECK ')
wrong="$(printf '%s\n' "$out" | grep -m1 '^CHECKS-WRONG-WAY' )"
echo "leadPanelPattern: rc=$rc; checks printed $n; ${wrong:-CHECKS-WRONG-WAY none}"
[ "$rc" = "0" ] && [ -z "$wrong" ] && [ "$n" -gt 0 ]
