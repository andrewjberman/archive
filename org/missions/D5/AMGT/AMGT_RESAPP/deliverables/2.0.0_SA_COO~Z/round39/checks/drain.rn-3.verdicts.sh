#!/usr/bin/env bash
# AMGT_RESAPP round 39, AMGT-rn-3 AC3 (BOUND) -- prose, docstring and token-reference edits move NO graded verdict:
# the scope=main table (state + the eight verdict columns) is byte-identical to the round-38 terminal baseline.
# usage: bash <this> <port> <out-dir-relative-to-repo-root>
set -u
PORT=${1:?port}; OUT=${2:?out dir}
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
mkdir -p "$ROOT/$OUT"
node scripts/ui-contract-check.mjs --port "$PORT" --scope main --out "$ROOT/$OUT" > "$ROOT/$OUT/run.log" 2>&1
awk -F'\t' 'BEGIN{OFS="\t"} /== scope=main/{f=1;next} /^== /{f=0} f && NF>=11 && $1!="state" {print $1,$2,$3,$4,$5,$6,$7,$8,$9}' "$ROOT/$OUT/run.log" > "$ROOT/$OUT/main.verdicts.tsv"
BASE="$ROOT/org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round39/checks/baseline.main.tsv"
if cmp -s "$ROOT/$OUT/main.verdicts.tsv" "$BASE"; then echo "main-scope verdicts IDENTICAL to the round-38 baseline ($(wc -l < "$BASE" | tr -d ' ') states)"; exit 0; fi
echo "main-scope verdicts DIFFER from the baseline:"; diff "$BASE" "$ROOT/$OUT/main.verdicts.tsv"; exit 1
