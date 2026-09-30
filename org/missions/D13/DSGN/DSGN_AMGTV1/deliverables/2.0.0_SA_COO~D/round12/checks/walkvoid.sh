#!/usr/bin/env bash
# DSGN_AMGTV1 round 4, AV-w-1 AC1 -- THE SIGNED-OUT POSITIVE CONTROL for the walk harness (CVO ruling, row Z-S3).
# Runs the walker with --no-login (no account armed, no password read, no sign-in) against the local build on 5174. Every
# protected route then lands on the sign-in page, so a correct walker prints "WALK VOID: step <label> landed on the sign-in
# page" and exits non-zero. A walker that exits 0, or never prints WALK VOID, or touches the walker account (arm/status/
# secret/disarm lines) FAILS this control.
# usage: bash <this>   (from the repo root of the worktree under test; needs http://localhost:5174 serving the portal)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5174/ || true)
[ "$code" = "200" ] || { echo "SIGNED-OUT CONTROL: not runnable -- localhost:5174 answered '$code' (the portal dev build must be serving)"; exit 2; }
T="$(mktemp)"; trap 'rm -f "$T"' EXIT
timeout 110 node .claude/skills/ui-walk/walk.mjs --no-login --route /security-analysis --max-minutes 2 > "$T" 2>&1; rc=$?
void=$(grep -cE "WALK VOID: step .+ landed on the sign-in page" "$T")
acct=$(grep -cE "ARMED|DISARM|STATUS: row|SSM (PRESENT|ABSENT)" "$T")
echo "walker rc=$rc; WALK VOID lines=$void; account lines=$acct; last: $(tail -1 "$T" | cut -c1-160)"
if [ "$rc" != "0" ] && [ "$rc" != "124" ] && [ "$void" -gt 0 ] && [ "$acct" = "0" ]; then
  echo "SIGNED-OUT CONTROL: the walk FAILS on the sign-in page: YES"; exit 0
fi
echo "SIGNED-OUT CONTROL: the walk FAILS on the sign-in page: NO"; exit 1
