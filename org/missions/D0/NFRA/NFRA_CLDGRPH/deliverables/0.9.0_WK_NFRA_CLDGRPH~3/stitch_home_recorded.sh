#!/usr/bin/env bash
# E4-AC1 -- THE HOME IS DECIDED AND RECORDED.
#
# One parser (_stitch_home_parse.py), two files: the real record, and a control
# whose `reason` is four words while everything else is well formed. A cell
# whose verb is DECIDE has exactly one failure mode a shape-check cannot see --
# a decision with no reason behind it -- so that is what the control plants.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3
PY=${PYTHON:-python}

echo "=== E4-AC1 stitch_home_recorded.sh -- run at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse --short HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo

REAL=$("$PY" "$D/_stitch_home_parse.py" "$D/CG-s-20.stitch-home.result.md" --label REAL)
echo "$REAL"
echo

CTRL=$("$PY" "$D/_stitch_home_parse.py" "$D/plant_e4/planted_home_no_reason.md" --label CONTROL)
echo "$CTRL"
echo

CTRL_REJ=$(printf '%s\n' "$CTRL" | grep -c 'REJECTED ->')
CTRL_REC=$(printf '%s\n' "$CTRL" | grep -c 'RECORDED$')
echo "--- CONTROL GRADING ---"
echo "control rejections=$CTRL_REJ (must be >=1: the reason floor)"
echo "control lines ending RECORDED=$CTRL_REC (must be 0)"
echo

echo "--- E4-AC1 VERDICT LINES ---"
printf '%s\n' "$REAL" | sed -n 's/^STITCH_HOME=/STITCH_HOME=/p'
printf '%s\n' "$REAL" | sed -n 's/^PRODUCER_READ=/PRODUCER_READ=/p'
if [ "${CTRL_REJ:-0}" -ge 1 ] && [ "${CTRL_REC:-1}" -eq 0 ]; then
  echo "HOME_PROBE_CONTROL=FIRED"
else
  echo "HOME_PROBE_CONTROL=DEAD"
fi
