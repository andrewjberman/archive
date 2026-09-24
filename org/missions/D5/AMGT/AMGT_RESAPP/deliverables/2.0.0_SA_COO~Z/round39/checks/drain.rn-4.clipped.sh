#!/usr/bin/env bash
# AMGT_RESAPP round 39, AMGT-rn-4 AC2 (BOUND) -- with the ancestor-aware arm live, the six states still read
# clippedTextBlocks 0 in BOTH scopes (the one live case was fixed by rm-5; the arm must not manufacture clips).
# usage: bash <this> <port> <out-dir-relative-to-repo-root>
set -u
PORT=${1:?port}; OUT=${2:?out dir}
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
mkdir -p "$ROOT/$OUT"
node scripts/ui-contract-check.mjs --port "$PORT" --scope main --out "$ROOT/$OUT" > "$ROOT/$OUT/run.log" 2>&1
m=$(awk -F'\t' '/== scope=main/{f=1;next} /^== /{f=0} f && NF>=11 && $1!="state" && $12=="0" {c++} END{print c+0}' "$ROOT/$OUT/run.log")
b=$(awk -F'\t' '/== scope=body/{f=1;next} /^== /{f=0} f && NF>=11 && $1!="state" && $12=="0" {c++} END{print c+0}' "$ROOT/$OUT/run.log")
echo "clippedTextBlocks == 0: main $m of 6, body $b of 6 (port $PORT)"
[ "$m" -eq 6 ] && [ "$b" -eq 6 ]
