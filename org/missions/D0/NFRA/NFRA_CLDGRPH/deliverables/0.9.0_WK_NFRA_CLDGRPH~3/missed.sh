#!/bin/bash
# missed.sh -- TO-CG-D-11 / cell CG-x-8 / criterion D11-AC2.
# THE MISSED-NIGHT READ: the SAME status read, the SAME code path, pointed by
# COMP_GRAPH_POINTER_URI at a PLANTED pointer+manifest pair whose newest `full` vintage predates
# today's 02:00Z boundary by more than a day. That plant is the night "known not to have run" --
# known BY CONSTRUCTION.
#
# WHY A FIXTURE AND NOT A REAL MISS: the estate's nightly has not missed a night on the record
# this project holds, and PROVOKING a miss (disabling the schedule, stopping the rule) is a
# production change no worker may make -- it is a NEVER on this order's face. So the arm that
# must be able to FAIL is exercised on the plant. Whether the plant stands for a real missed
# night is D11-AC4 and belongs to 3.0.0_SA_CVO; this script only produces the reading.
#
# READS ONLY. The plant is a local read-only fixture committed with TO-CG-D-4. This script does
# not write it, does not touch the LIVE pointer, and does not touch the live marker.
# Same three hazards as morning.sh: rc printed on every read (S57), CR stripped (W1-S18),
# no bare before/after convicts anything (W1-S19).

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS="$(cd "$SCRIPT_DIR" && git rev-parse --show-toplevel)"
cd "$WS" || { echo "FATAL: cannot cd to workspace root"; exit 1; }

PLANT_REL="org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/plant/current.json"
PROC_PATTERN='kuzu_nessie_load|derive_runner|projection_worker'
POSITIVE_CONTROL_PATTERN='bash'
TMP="$WS/.scratch/d11"
mkdir -p "$TMP"

count_procs() {
  local pattern="$1" snap rc rows n
  snap="$(ps -ef 2>"$TMP/ps_missed.err")"
  rc=$?
  rows="$(printf '%s\n' "$snap" | wc -l | tr -d ' \r')"
  if [ "$rc" -ne 0 ] || [ "$rows" -lt 2 ]; then
    PROC_COUNT="UNREADABLE(ps rc=$rc rows=$rows)"; PROC_ROWS="$rows"; return
  fi
  n="$(printf '%s\n' "$snap" | grep -E "$pattern" | grep -v grep | wc -l | tr -d ' \r')"
  PROC_COUNT="$n"; PROC_ROWS="$rows"
}

echo "=============================================================================="
echo "MISSED-NIGHT READ -- TO-CG-D-11 / CG-x-8 / 0.9.0_WK_NFRA_CLDGRPH~3"
echo "The SAME read, the SAME code path, pointed at the PLANT. Nothing in the real world"
echo "was stopped, disabled, provoked or rerun to obtain this reading."
echo "=============================================================================="
WALL_CLOCK="$(date -u +%FT%TZ)"
echo "WALL_CLOCK_UTC=$WALL_CLOCK"
echo "COMP_GRAPH_POINTER_URI=$PLANT_REL"
echo

echo "--- THE PLANT, READ BACK BEFORE IT IS USED (a fixture is evidence only if it is the one named) ---"
echo "  plant pointer bytes:"
cat "$PLANT_REL"; echo
PLANT_DIR="$(dirname "$PLANT_REL")"
echo "  plant tree:"
ls -1 "$PLANT_DIR"
echo "  plant vintage dirs:"
ls -1 "$PLANT_DIR" | grep -v current.json
PLANT_MANIFEST="$(ls -1d "$PLANT_DIR"/*/ | head -1)_build_manifest.json"
echo "  plant manifest path=$PLANT_MANIFEST"
echo "  plant manifest sha256(actual)=$(sha256sum "$PLANT_MANIFEST" | cut -d' ' -f1)"
echo "  plant pointer manifest_sha256(claimed)=$(python -c "import json,sys;print(json.load(open(sys.argv[1]))['manifest_sha256'])" "$PLANT_REL")"
echo "  (they must match or the straddle read refuses and the answer would be UNVERIFIABLE,"
echo "   not NO -- so this equality is what makes the NO an ANSWER rather than an error)"
echo "  plant manifest fields:"
python -c "import json,sys;m=json.load(open(sys.argv[1]));print('    vintage=%s\n    built_at=%s\n    writer_id=%s\n    producer.mode=%s\n    schema_version=%s\n    field_count=%d' % (m.get('vintage'),m.get('built_at'),m.get('writer_id'),(m.get('producer') or {}).get('mode'),m.get('schema_version'),len(m)))" "$PLANT_MANIFEST"
echo

echo "--- PROCESS TABLE BEFORE (grep -v grep; denominator printed) ---"
count_procs "$PROC_PATTERN"
PROCS_BEFORE="$PROC_COUNT"; ROWS_BEFORE="$PROC_ROWS"
echo "  pattern='$PROC_PATTERN'  matches=$PROCS_BEFORE  ps_rows(denominator)=$ROWS_BEFORE"
count_procs "$POSITIVE_CONTROL_PATTERN"
echo "  POSITIVE CONTROL pattern='$POSITIVE_CONTROL_PATTERN'  matches=$PROC_COUNT (probe alive)"
echo

echo "--- THE READ: COMP_GRAPH_POINTER_URI=<plant> bash .tools/comp-graph status (verbatim) ---"
COMP_GRAPH_POINTER_URI="$PLANT_REL" timeout 90 bash "$WS/.tools/comp-graph" status \
    >"$TMP/missed.out" 2>"$TMP/missed.err"
STATUS_RC=$?
cat "$TMP/missed.out"
echo "  status_rc=$STATUS_RC"
echo "  status_stderr=$(cat "$TMP/missed.err")"
echo

echo "--- PROCESS TABLE AFTER ---"
count_procs "$PROC_PATTERN"
PROCS_AFTER="$PROC_COUNT"; ROWS_AFTER="$PROC_ROWS"
echo "  pattern='$PROC_PATTERN'  matches=$PROCS_AFTER  ps_rows(denominator)=$ROWS_AFTER"
echo

echo "--- THE PLANT AFTER THE READ: the fixture is unchanged, so the read wrote nothing ---"
echo "  plant manifest sha256(after)=$(sha256sum "$PLANT_MANIFEST" | cut -d' ' -f1)"
echo "  plant pointer sha256(after)=$(sha256sum "$PLANT_REL" | cut -d' ' -f1)"
echo

echo "=============================================================================="
echo "MISSED_READ=$(grep -o 'REFRESHED LAST NIGHT: .*' "$TMP/missed.out" | head -1)"
echo "MISSED_READ_VINTAGE=$(grep -A4 'projection.last_night' "$TMP/missed.out" | grep -m1 'vintage:' | sed 's/^ *vintage: *//')"
echo "MISSED_READ_BOUNDARY=$(grep -m1 'boundary:' "$TMP/missed.out" | sed 's/^ *boundary: *//')"
echo "MISSED_STATUS_RC=$STATUS_RC"
echo "MISSED_PROCS_BEFORE=$PROCS_BEFORE"
echo "MISSED_PROCS_AFTER=$PROCS_AFTER"
echo "PS_ROWS_DENOMINATOR=$ROWS_BEFORE/$ROWS_AFTER"
echo "=============================================================================="
exit 0
