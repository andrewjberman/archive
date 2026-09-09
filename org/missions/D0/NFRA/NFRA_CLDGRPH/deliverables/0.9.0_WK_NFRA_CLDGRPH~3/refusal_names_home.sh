#!/usr/bin/env bash
# E4-AC2 -- comp-debt's REFUSAL TEXT NAMES THE DECISION.
#
# One reader (_refusal_ast.py), two files: comp_debt.py and a control whose two
# stitch refusals name neither the home nor the cell. The reader collects EVERY
# string constant inside each `raise SystemExit(...)` -- the texts are
# %-formatted implicit concatenations, so reading args[0] would grade one
# fragment and miss the rest -- and scopes the denominator to the two refusals
# inside _stitch_freshness, printing the third (the NESSIE surface's) by name.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3
PY=${PYTHON:-python}
HOME_TOKEN=JOIN_PROJECTION

echo "=== E4-AC2 refusal_names_home.sh -- run at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse --short HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo

REAL=$("$PY" "$D/_refusal_ast.py" infra/aws/globgrph/comp_debt.py \
        --home "$HOME_TOKEN" --cell CG-s-20 --label REAL)
echo "$REAL"
echo

CTRL=$("$PY" "$D/_refusal_ast.py" "$D/plant_e4/planted_refusal_unnamed.py" \
        --home "$HOME_TOKEN" --cell CG-s-20 --label CONTROL)
echo "$CTRL"
echo

CTRL_OK=$(printf '%s\n' "$CTRL" | sed -n 's/^REFUSAL_TEXTS_NAME_HOME=\([0-9]*\) of.*/\1/p')
CTRL_N=$(printf '%s\n' "$CTRL" | sed -n 's/^REFUSAL_TEXTS_NAME_HOME=[0-9]* of \([0-9]*\)/\1/p')
REAL_OK=$(printf '%s\n' "$REAL" | sed -n 's/^REFUSAL_TEXTS_NAME_HOME=\([0-9]*\) of.*/\1/p')
REAL_N=$(printf '%s\n' "$REAL" | sed -n 's/^REFUSAL_TEXTS_NAME_HOME=[0-9]* of \([0-9]*\)/\1/p')

echo "--- CONTROL GRADING ---"
echo "control: $CTRL_OK of $CTRL_N stitch refusals named the home (must be 0 of 2 --"
echo "  the control has the same two raise sites and neither text carries the token)"
echo
echo "--- E4-AC2 VERDICT LINES ---"
echo "REFUSAL_TEXTS_NAME_HOME=$REAL_OK of $REAL_N"
if [ "${CTRL_OK:-9}" -eq 0 ] && [ "${CTRL_N:-0}" -eq 2 ]; then
  echo "REFUSAL_PROBE_CONTROL=FIRED"
else
  echo "REFUSAL_PROBE_CONTROL=DEAD"
fi
