#!/usr/bin/env bash
# ADVI_49F.P14-VEHICLE -- DETACHED campaign-driver launcher (1.0.0_SA_CTO ruling 80002).
#
# WHY THIS EXISTS. Two `run_in_background` driver tasks in the 0.7.0_AE_CloudOps~L session
# died with the harness's own word `killed` (1h33m and ~4m lifetimes -- not a cap), with no
# TaskStop, the host up, and no fabric reaper (kill-orphans PATTERNS cannot match
# CAMPAIGN_DRIVER.py; 0 KILL/register audit lines in the window). A kill writes NOTHING --
# no ledger row, no host event, no refusal -- so every ledger instrument reads healthy while
# the campaign sits dead. The substrate was the defect; this takes the driver off it.
#
# WHY THIS IS NOT AN ORPHAN, per the ruling and honoured rather than dodged:
#   OWNER   0.7.0_AE_CloudOps~L, then any successor seat (the ledger names both).
#   ORACLE  pid alive AND the ledger advancing. Cadence ~110 s/date, so:
#             pid gone                      -> dead
#             pid alive + ledger silent >5m -> wedged
#           Both visible; neither requires this launcher to be trusted.
#   KILLER  a NAMED, documented command (printed below and written to the ledger row):
#             kill $(cat <pidfile>)         # Git Bash
#             Stop-Process -Id (Get-Content <pidfile>)   # PowerShell
#   EFFECT  none beyond the ledger it already writes. An orphan watcher STEALS mail; this
#           process's liveness is exactly CORRELATED with its ledger, not anti-correlated.
#
# Rule-16: nohup + & + disown. `setsid` is NOT a Git Bash 3.6.7 default and is not used.
# Convention borrowed from .tools/commit-worker-launch.sh rather than invented tonight.

set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRIVER="$HERE/ADVI_49F.P14-VEHICLE_CAMPAIGN_DRIVER.py"
PIDFILE="$HERE/ADVI_49F.P14-VEHICLE_DRIVER.pid"
LOGF="$HERE/ADVI_49F.P14-VEHICLE_DRIVER.log"

[ -f "$DRIVER" ] || { echo "ERROR: driver not found: $DRIVER" >&2; exit 2; }

# SINGLETON: never race a second driver against the entrypoint mutex. The campaign is
# strictly sequential by design; two drivers would contend for the same host.
if [ -f "$PIDFILE" ]; then
  _old="$(cat "$PIDFILE" 2>/dev/null || true)"
  if [ -n "$_old" ] && kill -0 "$_old" 2>/dev/null; then
    echo "REFUSED: a driver is already live (pid $_old, $PIDFILE). Kill it first:"
    echo "  kill $_old"
    exit 1
  fi
  echo "NOTE: stale pidfile (pid ${_old:-<empty>} not alive) -- replacing."
fi

# Detached: nohup ignores SIGHUP, & backgrounds, disown drops it from this shell's job
# table so it survives the launcher AND the calling session. </dev/null so it never
# blocks on stdin. -u so python does NOT block-buffer stdout (the buffering that made
# every previous task's log lag its own ledger).
nohup python -u "$DRIVER" --run --confirm-campaign-start </dev/null >>"$LOGF" 2>&1 &
_pid=$!
disown "$_pid" 2>/dev/null || true
echo "$_pid" > "$PIDFILE"

sleep 2
if kill -0 "$_pid" 2>/dev/null; then
  echo "OK: campaign driver launched DETACHED"
  echo "  pid      $_pid"
  echo "  pidfile  $PIDFILE"
  echo "  log      $LOGF"
  echo "  KILL     kill $_pid    (or: kill \$(cat '$PIDFILE'))"
  echo "  ORACLE   pid alive AND the ledger advancing (~110 s/date)"
  exit 0
fi
echo "ERROR: driver did not survive its first 2 seconds -- see $LOGF" >&2
exit 1
