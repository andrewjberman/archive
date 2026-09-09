#!/usr/bin/env bash
# E4-AC4 -- NO LOCAL REBUILD PATH TO THE PROJECTION.
#
# The bound both answers carry: neither the stitch consumer nor the stitch
# builder may import, call or name the canonical loader, its rebuild
# entrypoint, its path constant or its store. One walker, two runs: the two
# real files, and a control that does all four things at once.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3
PY=${PYTHON:-python}

echo "=== E4-AC4 no_projection_rebuild_path.sh -- run at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse --short HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo

REAL=$("$PY" "$D/_rebuild_path_ast.py" infra/aws/globgrph/comp_debt.py \
        infra/aws/globgrph/kuzu_stitch_load.py --label REAL)
echo "$REAL"
echo

CTRL=$("$PY" "$D/_rebuild_path_ast.py" "$D/plant_e4/planted_rebuild_path.py" --label CONTROL)
echo "$CTRL"
echo

CTRL_HITS=$(printf '%s\n' "$CTRL" | sed -n 's/^PROJECTION_REBUILD_PATHS=\([0-9]*\) of.*/\1/p')
REAL_LINE=$(printf '%s\n' "$REAL" | sed -n 's/^PROJECTION_REBUILD_PATHS=/PROJECTION_REBUILD_PATHS=/p')
REAL_FAIL=$(printf '%s\n' "$REAL" | sed -n 's/^PARSE_FAILURES=\([0-9]*\)/\1/p')

echo "--- CONTROL GRADING ---"
echo "control hits=$CTRL_HITS (must be >=4: an import, an import-from, the call and the constant)"
echo "real parse failures=$REAL_FAIL (must be 0 -- an unparsed file may not hide inside the zero)"
echo
echo "--- E4-AC4 VERDICT LINES ---"
echo "$REAL_LINE"
if [ "${CTRL_HITS:-0}" -ge 4 ] && [ "${REAL_FAIL:-1}" -eq 0 ]; then
  echo "REBUILD_PROBE_CONTROL=FIRED"
else
  echo "REBUILD_PROBE_CONTROL=DEAD"
fi
