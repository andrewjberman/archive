#!/usr/bin/env bash
# F6-AC3 -- NO BUILDER OF A LOCAL KUZU STORE REMAINS BESIDE THE PROJECTION.
#
# One walker (f6_local_builder_ast.py), THREE runs:
#   (1) REAL-WIDE  -- infra/aws/globgrph + the four tool homes, which is the
#                     scope the criterion names ("infra/aws/globgrph/ and the
#                     tool homes"). This is the DECIDING line.
#   (2) REAL-CELL  -- infra/aws/globgrph alone, which is the scope the CELL's
#                     accept names ("no builder BESIDE THE PROJECTION remains").
#                     Printed beside (1) so the two scopes are never conflated.
#   (3) CONTROL    -- f6_plant/planted_builder.py, which write-opens a repo path,
#                     read-opens the same path, and names the retired store in a
#                     docstring and a comment. A walker that cannot fire on (3)
#                     makes (1) a constant.
#
# The four projection builders are EXCLUDED BY NAME and printed as excluded, so
# the exclusion is visible rather than silent.
#
# STITCH_LOADER_AT_HEAD is measured on BOTH planes: git show HEAD (the record)
# and test -f (the worktree). false requires both to be absent, beside a positive
# control on the same verb.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~7
WALK="$D/f6_local_builder_ast.py"
PY=${PYTHON:-python}
LOADER=infra/aws/globgrph/kuzu_stitch_load.py
EXCL=kuzu_nessie_load.py,kuzu_incremental_refresh.py,projection_worker.py,projection_server.py

echo "=== f6_no_local_builder.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo "WALKER=$WALK"
echo

WIDE=$("$PY" "$WALK" infra/aws/globgrph .tools org/modules/graph org/modules/heatmap \
        --exclude "$EXCL" --label REAL-WIDE)
echo "$WIDE"
echo

CELL=$("$PY" "$WALK" infra/aws/globgrph --exclude "$EXCL" --label REAL-CELL-SCOPE)
echo "$CELL"
echo

CTRL=$("$PY" "$WALK" "$D/f6_plant" --label CONTROL)
echo "$CTRL"
echo

WIDE_N=$(printf '%s\n' "$WIDE" | sed -n 's/^LOCAL_KUZU_BUILDERS=\([0-9]*\) of.*/\1/p')
WIDE_LINE=$(printf '%s\n' "$WIDE" | sed -n 's/^LOCAL_KUZU_BUILDERS=/LOCAL_KUZU_BUILDERS=/p')
WIDE_FAIL=$(printf '%s\n' "$WIDE" | sed -n 's/^PARSE_FAILURES=\([0-9]*\)/\1/p')
WIDE_UNRES=$(printf '%s\n' "$WIDE" | sed -n 's/^WRITE_OPENS_UNRESOLVED=\([0-9]*\)/\1/p')
CELL_LINE=$(printf '%s\n' "$CELL" | sed -n 's/^LOCAL_KUZU_BUILDERS=/LOCAL_KUZU_BUILDERS_BESIDE_PROJECTION=/p')
CTRL_N=$(printf '%s\n' "$CTRL" | sed -n 's/^LOCAL_KUZU_BUILDERS=\([0-9]*\) of.*/\1/p')
CTRL_RO=$(printf '%s\n' "$CTRL" | sed -n 's/^READ_ONLY_OPENS=\([0-9]*\)/\1/p')

echo "--- THE RETIRED LOADER, ON BOTH PLANES ---"
git show "HEAD:$LOADER" > /dev/null
AT_HEAD_RC=$?
echo "git show HEAD:$LOADER -> rc=$AT_HEAD_RC (non-zero = absent at HEAD)"
if [ -f "$LOADER" ]; then WT=present; else WT=absent; fi
echo "worktree test -f $LOADER -> $WT"
echo "POSITIVE CONTROL on the same verb and plane:"
git show "HEAD:infra/aws/globgrph/projection_client.py" > /dev/null
echo "git show HEAD:infra/aws/globgrph/projection_client.py -> rc=$? (0 = the read verb works here)"
echo

echo "--- CONTROL GRADING ---"
echo "control builders caught=$CTRL_N (must be >=1) read_only opens correctly not counted=$CTRL_RO (must be >=1)"
echo "real parse failures=$WIDE_FAIL (must be 0 -- an unparsed file may not hide inside the count)"
echo "real unresolved write-opens=$WIDE_UNRES (enumerated above; NOT folded into the count)"
echo

echo "--- F6-AC3 VERDICT LINES ---"
echo "$WIDE_LINE"
echo "$CELL_LINE"
if [ "$AT_HEAD_RC" -ne 0 ] && [ "$WT" = absent ]; then
  echo "STITCH_LOADER_AT_HEAD=false"
else
  echo "STITCH_LOADER_AT_HEAD=true (at_head_rc=$AT_HEAD_RC worktree=$WT)"
fi
if [ "${CTRL_N:-0}" -ge 1 ] && [ "${CTRL_RO:-0}" -ge 1 ] && [ "${WIDE_FAIL:-1}" -eq 0 ]; then
  echo "BUILDER_PROBE_CONTROL=FIRED"
else
  echo "BUILDER_PROBE_CONTROL=DEAD"
fi
echo "=== f6_no_local_builder.sh END ==="
