#!/usr/bin/env bash
# f9_hook_wait.sh -- deliverable step 4. 0.9.0_WK_NFRA_CLDGRPH~5, TO-CG-F-9 (CG-s-29).
#
# Polls this laptop's device hook file (READ ONLY, absolute path) every 60 s for up to
# 30 minutes, waiting for 0.0.0_AB_MSTR's device act to remove the stitch-refresh pair.
# Prints the clock each minute. Exits 0 the moment the pair is gone; exits 4 at the
# deadline with the pair still present (F9-AC3 then FAILS honestly and the order stays
# OPEN). Never edits the hook file.
set -u
HOOK="C:/Users/AndrewBerman/Desktop/ajb_workspace/.git/hooks/post-commit"
DEADLINE_MIN="${1:-30}"
echo "F9 STEP 4 -- polling for MSTR's device act"
echo "HOOK_PATH=$HOOK"
echo "POLL_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)  DEADLINE_MIN=$DEADLINE_MIN"
i=0
while [ "$i" -le "$DEADLINE_MIN" ]; do
  if [ -f "$HOOK" ]; then
    N="$(cat "$HOOK" | grep -c 'stitch-refresh')"
  else
    N="NOFILE"
  fi
  echo "t=+${i}m  $(date -u +%Y-%m-%dT%H:%M:%SZ)  STITCH_LINES=$N"
  if [ "$N" = "0" ]; then
    echo "DEVICE_ACT_LANDED=true at $(date -u +%Y-%m-%dT%H:%M:%SZ) after ${i} minute(s) of polling"
    exit 0
  fi
  i=$((i + 1))
  [ "$i" -le "$DEADLINE_MIN" ] && sleep 60
done
echo "DEVICE_ACT_LANDED=false -- deadline reached with the stitch-refresh pair STILL PRESENT"
exit 4
