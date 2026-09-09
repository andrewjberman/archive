#!/usr/bin/env bash
# E3-AC1 -- EVERY ARTIFACT DISPOSITIONED ON THE RECORD.
#
# One parser (_dispositions_parse.py), two files:
#   REAL    CG-s-19.residual-stores.result.md -- four artifacts, each needing a
#           disposition from the CLOSED vocabulary, an owner SERIAL and a reason
#           over an 80-char floor; plus a p7_row_id that must RESOLVE to a row
#           in the project's investigation channel.
#   CONTROL plant_e3/planted_bad_record.md -- four artifacts of which three are
#           defective (no owner / a disposition outside the vocabulary / a
#           one-word reason). If the same parser scores that 4 of 4, the pass on
#           the real record is a constant and this script says so.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3
CHANNEL=org/missions/D0/NFRA/NFRA_CLDGRPH/surprise-channel/investigations/INVESTIGATION_v1.md
PY=${PYTHON:-python}

echo "=== E3-AC1 dispositions_recorded.sh -- run at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse --short HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo

REAL=$("$PY" "$D/_dispositions_parse.py" "$D/CG-s-19.residual-stores.result.md" \
        --channel "$CHANNEL" --expect-artifacts 4 --label REAL)
echo "$REAL"
echo

CTRL=$("$PY" "$D/_dispositions_parse.py" "$D/plant_e3/planted_bad_record.md" \
        --expect-artifacts 4 --label CONTROL)
echo "$CTRL"
echo

CTRL_OK=$(printf '%s\n' "$CTRL" | sed -n 's/^DISPOSITIONS=\([0-9]*\) of.*/\1/p')
CTRL_REJECTED=$(printf '%s\n' "$CTRL" | grep -c '^  ENTRY [0-9]* REJECTED')
echo "--- CONTROL GRADING ---"
echo "control entries accepted=$CTRL_OK of 4  rejected=$CTRL_REJECTED (3 defects planted:"
echo "  no owner / a disposition outside the closed vocabulary / a one-word reason)"
echo

REAL_OK=$(printf '%s\n' "$REAL" | sed -n 's/^DISPOSITIONS=\([0-9]*\) of \([0-9]*\) RECORDED/\1/p')
REAL_N=$(printf '%s\n' "$REAL" | sed -n 's/^DISPOSITIONS=\([0-9]*\) of \([0-9]*\) RECORDED/\2/p')
ROW=$(printf '%s\n' "$REAL" | sed -n 's/^P7_ROW_FILED=//p')

echo "--- E3-AC1 VERDICT LINES ---"
echo "DISPOSITIONS=$REAL_OK of $REAL_N RECORDED"
echo "P7_ROW_FILED=$ROW"
if [ "${CTRL_REJECTED:-0}" -eq 3 ] && [ "${CTRL_OK:-4}" -eq 1 ]; then
  echo "DISPOSITION_PROBE_CONTROL=FIRED"
else
  echo "DISPOSITION_PROBE_CONTROL=DEAD"
fi
