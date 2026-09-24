#!/usr/bin/env bash
# AMGT_RESAPP round 39 -- the portal typecheck as a cell's seam probe (rn-1 AC2, rn-6 AC2): a component edit still
# compiles against every consumer. usage: bash <this>   (from the repo root; no server)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
timeout 300 npx tsc -b --noEmit > .scratch.typecheck.txt 2>&1; rc=$?
tail -5 .scratch.typecheck.txt; rm -f .scratch.typecheck.txt
echo "tsc -b --noEmit exit=$rc"
[ "$rc" -eq 0 ]
