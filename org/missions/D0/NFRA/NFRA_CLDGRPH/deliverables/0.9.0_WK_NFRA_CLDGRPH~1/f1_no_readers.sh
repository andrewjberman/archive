#!/usr/bin/env bash
# F1-AC3 -- ZERO READERS AND NO BUILDER.
#
# The SAME AST walk the E-3 order ran (_readers_ast.py, slot ~3's deliverables),
# re-run at THIS HEAD after infra/aws/globgrph/kuzu_load.py is retired. The
# difference from E-3's run is the point of it: the builder exclusion is now
# EMPTY -- no --builder flag is passed -- so a hit anywhere in the four tool
# homes counts, and the census must still read 0.
#
# Two runs of one walker:
#   (1) REAL   -- .tools org/modules/graph org/modules/heatmap infra/aws/globgrph
#   (2) CONTROL -- slot ~3's plant_e3/, one file that OPENS both stores and one
#       that names them only in a docstring/comment/prose string.
# A walker that cannot fire on (2) makes (1) a constant, not a measurement.
#
# BUILDER_PRESENT is measured on BOTH planes: at HEAD (git show) and in the
# worktree (test -f). false requires both to be absent.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
E3=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3
PY=${PYTHON:-python}
BUILDER=infra/aws/globgrph/kuzu_load.py

echo "=== f1_no_readers.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo "WALKER=$E3/_readers_ast.py (E-3's instrument, reused; SURFACES grants the read)"
echo

REAL=$("$PY" "$E3/_readers_ast.py" .tools org/modules/graph org/modules/heatmap \
        infra/aws/globgrph --label REAL)
echo "$REAL"
echo

CTRL=$("$PY" "$E3/_readers_ast.py" "$E3/plant_e3" --label CONTROL)
echo "$CTRL"
echo

CTRL_READERS=$(printf '%s\n' "$CTRL" | sed -n 's/^READERS=\([0-9]*\) of.*/\1/p')
CTRL_DOCS_AS_READERS=$(printf '%s\n' "$CTRL" | grep -c '^  READER .*planted_docstring_only')
CTRL_OPENER_CAUGHT=$(printf '%s\n' "$CTRL" | grep -c '^  READER .*planted_reader')
CTRL_DOCS=$(printf '%s\n' "$CTRL" | sed -n 's/^DOCSTRING_MENTIONS=\([0-9]*\)/\1/p')

echo "--- CONTROL GRADING ---"
echo "control_readers=$CTRL_READERS opener_lines_caught=$CTRL_OPENER_CAUGHT docstring_specimen_scored_as_reader=$CTRL_DOCS_AS_READERS docstring_mentions_seen=$CTRL_DOCS"
echo

echo "--- THE BUILDER, ON BOTH PLANES ---"
git show "HEAD:$BUILDER" > /dev/null 2>&1
AT_HEAD_RC=$?
echo "git show HEAD:$BUILDER -> rc=$AT_HEAD_RC (128 = absent at HEAD)"
if [ -f "$BUILDER" ]; then WT=present; else WT=absent; fi
echo "worktree test -f $BUILDER -> $WT"
echo "POSITIVE CONTROL on the same verb and plane:"
git show "HEAD:infra/aws/globgrph/projection_client.py" > /dev/null 2>&1
echo "git show HEAD:infra/aws/globgrph/projection_client.py -> rc=$? (0 = the read verb works here)"
echo

echo "--- F1-AC3 VERDICT LINES ---"
printf '%s\n' "$REAL" | sed -n 's/^READERS=/READERS=/p'
printf '%s\n' "$REAL" | sed -n 's/^PARSE_FAILURES=/PARSE_FAILURES=/p'
printf '%s\n' "$REAL" | sed -n 's/^PROSE_MENTIONS=/PROSE_MENTIONS=/p'
printf '%s\n' "$REAL" | sed -n 's/^DOCSTRING_MENTIONS=/DOCSTRING_MENTIONS=/p'
echo "BUILDER_EXCLUSION=EMPTY (no --builder flag passed; nothing is excluded by name)"
if [ "$AT_HEAD_RC" -ne 0 ] && [ "$WT" = absent ]; then
  echo "BUILDER_PRESENT=false"
else
  echo "BUILDER_PRESENT=true (at_head_rc=$AT_HEAD_RC worktree=$WT)"
fi
if [ "${CTRL_OPENER_CAUGHT:-0}" -ge 1 ] && [ "${CTRL_READERS:-0}" -ge 1 ]; then
  echo "READER_PROBE_CONTROL=FIRED"
else
  echo "READER_PROBE_CONTROL=DEAD"
fi
if [ "${CTRL_DOCS_AS_READERS:-1}" -eq 0 ] && [ "${CTRL_DOCS:-0}" -ge 1 ]; then
  echo "READER_BAND_CONTROL=FIRED"
else
  echo "READER_BAND_CONTROL=DEAD"
fi
echo "=== f1_no_readers.sh END ==="
