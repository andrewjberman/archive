#!/usr/bin/env bash
# AMGT_RESAPP round 41, AMGT-rp-1 AC4 -- JUDGMENT, RECORDED, NO VERDICT: every row of the population table that is not OK,
# printed whole, for a person to decide whether each names an EXPORT defect, a PAGE defect or a DATA gap.
# usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
TSV=org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/fwd30_population.tsv
[ -f "$TSV" ] || { echo "FAIL: no table"; exit 1; }
head -1 "$TSV"
awk -F'\t' 'NR>1 && $19!="OK"' "$TSV"
echo "rows not OK: $(awk -F'\t' 'NR>1 && $19!="OK"' "$TSV" | wc -l) of $(awk 'NR>1' "$TSV" | wc -l)"
