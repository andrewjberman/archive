#!/usr/bin/env bash
# E3-AC2 -- ZERO READERS OVER THE TOOL HOMES.
#
# Instrument: an ast walk (_readers_ast.py), not a text grep. Two runs of the
# SAME walker:
#   (1) the REAL scope -- .tools org/modules/graph org/modules/heatmap
#       infra/aws/globgrph, with the builder infra/aws/globgrph/kuzu_load.py
#       DECLARED and excluded by name;
#   (2) the CONTROL scope -- plant_e3/, which holds one file that opens both
#       stores and one file that only names them in docstrings/comments/prose.
# The control run must report exactly ONE reader (the opener) and ZERO from the
# docstring specimen. A walker that cannot fire on (2) makes (1) a constant.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3
PY=${PYTHON:-python}

echo "=== E3-AC2 no_readers.sh -- run at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse --short HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo

REAL=$("$PY" "$D/_readers_ast.py" .tools org/modules/graph org/modules/heatmap \
        infra/aws/globgrph --builder infra/aws/globgrph/kuzu_load.py --label REAL)
echo "$REAL"
echo

CTRL=$("$PY" "$D/_readers_ast.py" "$D/plant_e3" --label CONTROL)
echo "$CTRL"
echo

# --- grade the control -------------------------------------------------------
CTRL_READERS=$(printf '%s\n' "$CTRL" | sed -n 's/^READERS=\([0-9]*\) of.*/\1/p')
CTRL_DOCS_AS_READERS=$(printf '%s\n' "$CTRL" | grep -c '^  READER .*planted_docstring_only')
CTRL_OPENER_CAUGHT=$(printf '%s\n' "$CTRL" | grep -c '^  READER .*planted_reader')
CTRL_DOCS=$(printf '%s\n' "$CTRL" | sed -n 's/^DOCSTRING_MENTIONS=\([0-9]*\)/\1/p')

echo "--- CONTROL GRADING ---"
echo "control readers=$CTRL_READERS  opener_lines_caught=$CTRL_OPENER_CAUGHT" \
     " docstring_specimen_flagged_as_reader=$CTRL_DOCS_AS_READERS" \
     " docstring_mentions_seen=$CTRL_DOCS"
if [ "${CTRL_OPENER_CAUGHT:-0}" -ge 1 ] && [ "${CTRL_READERS:-0}" -ge 1 ]; then
  echo "READER_PROBE_CONTROL=FIRED  (the planted opener in $D/plant_e3/planted_reader.py was CAUGHT: the walker can return non-zero)"
else
  echo "READER_PROBE_CONTROL=DEAD  (the planted opener was NOT caught -- the REAL zero above is a constant, not a measurement)"
fi
if [ "${CTRL_DOCS_AS_READERS:-1}" -eq 0 ] && [ "${CTRL_DOCS:-0}" -ge 1 ]; then
  echo "READER_BAND_CONTROL=FIRED  (the docstring/comment/prose specimen was SEEN ($CTRL_DOCS docstring mentions) and counted as ZERO readers)"
else
  echo "READER_BAND_CONTROL=DEAD  (a prose-only mention scored as a reader, or the specimen was never seen)"
fi
echo

# --- the answer --------------------------------------------------------------
printf '%s\n' "$REAL" | grep -E '^(FILES_WALKED|PROSE_MENTIONS|DOCSTRING_MENTIONS|BUILDER_HITS|NEAR_MISS_LOOSE_TOKEN_HITS|PARSE_FAILURES)='
echo
echo "DENOMINATOR NOTE: the count after 'of' below is every .py file under the"
echo "four tool homes, walked and ast-parsed; PARSE_FAILURES is printed above so"
echo "an unread file can never hide inside the zero."
echo
echo "--- E3-AC2 VERDICT LINES ---"
printf '%s\n' "$REAL" | sed -n 's/^READERS=/READERS=/p'
printf '%s\n' "$REAL" | sed -n 's/^BUILDER_DECLARED=/BUILDER_DECLARED=/p'
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
