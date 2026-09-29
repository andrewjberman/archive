#!/usr/bin/env bash
# AMGT_RESAPP round 47, AMGT-vv-3 AC1 -- the three page harnesses that cannot load today LOAD and PASS: shell, posture, tabs
# (rows Z-W167-S1: '@/api/api-client' via HeaderBrief's TimelinePanel; tabs: '@/ui/components/graphic/HeroGraphic').
# Each must exit 0 with no module-resolution error. usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
pass=0
for h in shell posture tabs; do
  out="$(timeout 35 node src/pages/SecurityAnalysis/__harness__/$h.harness.cjs 2>&1)"; rc=$?
  err="$(printf '%s\n' "$out" | grep -m1 -E 'Cannot find module|Error:')"
  echo "$h: rc=$rc ${err:+-- $err}"
  [ "$rc" = "0" ] && [ -z "$err" ] && pass=$((pass+1))
done
echo "HARNESSES LOAD AND PASS: $pass of 3"
[ "$pass" = "3" ]
