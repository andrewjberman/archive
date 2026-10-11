#!/usr/bin/env bash
# AMGT_CORPUS round 48, CRPS-ax-1 -- the RENDERED page read on the DEV-built portal tree against the live function, one name per team-sheet class
# (master, own_new, own_model) and the D1-S7 name. Issuer's file.
#   bash ax1_page_walk.sh <label> <portal worktree path>        e.g.  bash ax1_page_walk.sh dev-live13 /c/tmp/wk-AMGT_CORPUS-47-2/portal
# Stops whatever listens on 5174, starts `bun run dev:live --port 5174` from the given portal tree (the build under read), waits for it,
# runs the ui-walk walker on TSM US (master), SAN FP (own_new), ROG SW (own_model) and CLX US (the D1-S7 name), and prints
#   WALKOUT <label> <output dir>   then   BUILD <label> <portal HEAD>.
# The walker arms and disarms the dormant service account itself and prints `DISARM ... REFUSED`; the shots stay local (gitignored).
set -u
LABEL="$1"; TREE="$2"
ROOT="$(git rev-parse --show-toplevel)"
LOG="${TMPDIR:-/tmp}/ax1_walk_${LABEL}.log"
for pid in $(netstat -ano | grep ":5174 " | grep LISTEN | awk '{print $5}' | sort -u); do
  powershell.exe -NoProfile -Command "Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue" >/dev/null 2>&1
done
sleep 2
( cd "$TREE" && nohup bun run dev:live --port 5174 > "$LOG.dev" 2>&1 & )
for i in $(seq 1 40); do
  c=$(curl -s -o /dev/null -m 3 -w "%{http_code}" http://localhost:5174/ 2>/dev/null)
  [ "$c" = "200" ] && break
  sleep 3
done
echo "BUILD $LABEL $(git -C "$TREE" rev-parse --short HEAD) server=$c"
cd "$ROOT" && timeout 1500 node .claude/skills/ui-walk/walk.mjs --route /security-analysis \
  --security "TSM US" --security "SAN FP" --security "ROG SW" --security "CLX US" --max-minutes 24 > "$LOG" 2>&1
echo "rc=$?"
grep -E "DISARM|REFUSED|SUMMARY|WALK VOID" "$LOG" | cut -c1-200
echo "WALKOUT $LABEL $(grep -o 'OUT .*' "$LOG" | tail -1 | sed 's/^OUT //')"
