#!/usr/bin/env bash
# AMGT_RESAPP round 39, AMGT-rn-1 AC1 -- FWD-29's own condition "no size below 11": the sizes column reads PASS on
# all six states inside main. usage: bash <this> <port> <out-dir-relative-to-repo-root>
set -u
PORT=${1:?port}; OUT=${2:?out dir}
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
mkdir -p "$ROOT/$OUT"
node scripts/ui-contract-check.mjs --port "$PORT" --scope main --out "$ROOT/$OUT" > "$ROOT/$OUT/run.log" 2>&1
echo "contract-check exit=$? (informational; the graded verdict is the sizes column below)"
awk -F'\t' '/== scope=main/{f=1;next} /^== /{f=0} f && NF>=11 && $1!="state" {print $1"\t"$5}' "$ROOT/$OUT/run.log" > "$ROOT/$OUT/sizes.tsv"
n=$(grep -c $'\tPASS$' "$ROOT/$OUT/sizes.tsv"); d=$(wc -l < "$ROOT/$OUT/sizes.tsv" | tr -d ' ')
cat "$ROOT/$OUT/sizes.tsv"
echo "SIZES PASS $n of $d states (scope=main, port $PORT)"
[ "$n" -eq 6 ] && [ "$d" -eq 6 ]
