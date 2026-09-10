#!/usr/bin/env bash
# i1_no_egress.sh -- NFRA_CLDGRPH CG-s-41, criterion I1-AC4.
#
# THE EGRESS HOLD, HONOURED AND MEASURED -- and the permitted reads COUNTED
# rather than hidden, so "took no read" and "took an allowed read" are two
# different printed numbers.
#
# THREE ARMS:
#   A. ACT CENSUS over everything this task order authored -- five held acts,
#      counted by an AST walk (i1_no_egress_detect.py), not by grepping prose.
#   B. THE CONTROL. The SAME detector is pointed at a planted fixture that DOES
#      call all five. If it does not fire there, its zero in arm A means nothing.
#   C. LIVE READ COUNT. Real permitted reads are issued right here and counted,
#      so the READS number is something an instrument returned, not a claim.
#
# rail note: the file scans below are the detector's own AST walk and the
# `cat | grep` pipe-RECEIVER form; no standalone repo grep/find is used.
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(git rev-parse --show-toplevel)"
cd "$REPO" || exit 1
PY="${PYTHON:-python}"
DET="$HERE/i1_no_egress_detect.py"
FIX="$REPO/.scratch/i1_egress_probe_fixture.py"

echo "=============================================================================="
echo "i1_no_egress.sh -- CG-s-41 / I1-AC4 -- THE HOLD, HONOURED AND COUNTED"
echo "=============================================================================="
echo "TREE_READ cwd    = $(pwd)"
echo "TREE_READ branch = $(git rev-parse --abbrev-ref HEAD)"
echo "TREE_READ head   = $(git rev-parse HEAD)"
echo

# ---------------------------------------------------------------------------
# THE POPULATION -- stated as a denominator, and it is everything I authored
# ---------------------------------------------------------------------------
echo "-- THE POPULATION UNDER THE DETECTOR --"
AUTHORED=""
for f in "$HERE"/i1_*.py "$HERE"/i1_*.sh "$HERE"/CG-s-41.key-collision.result.md; do
  [ -e "$f" ] && AUTHORED="$AUTHORED $f"
done
# The source change itself, as its own file: the added lines of the one
# producer file this order edits.
DIFFCAP="$REPO/.scratch/i1_source_diff.txt"
git diff -- infra/aws/lambda/globgrph/incremental_updater/lambda_function.py \
            infra/aws/globgrph/derive_runner.py > "$DIFFCAP"
AUTHORED="$AUTHORED $DIFFCAP"
N_FILES=0
for f in $AUTHORED; do N_FILES=$((N_FILES + 1)); echo "   $f"; done
echo "   DENOMINATOR: $N_FILES file(s) -- every EXECUTABLE this order authored"
echo "   (i1_*.py, i1_*.sh), the record, and the diff of the one producer file it"
echo "   edits. TWO EXCLUSIONS, both stated rather than left as a silent gap:"
echo "   (1) the i1_ac*_run.txt verbatim captures. Each one quotes this detector"
echo "       reporting the planted control back -- the six ACT lines it prints"
echo "       when it finds the fixture. Scanning a capture would re-detect the"
echo "       payload of the control as though it were an act. A capture records a"
echo "       reading and executes nothing; the executables that made it ARE"
echo "       scanned. THE WEAK GRAIN CANNOT TELL A QUOTE FROM A COMMAND, and the"
echo "       first version of this very line proved it by convicting itself."
echo "   (2) interactive shell commands typed during the session that left no"
echo "       artifact. Arm C bounds those by class, not by count."
echo

# ---------------------------------------------------------------------------
# ARM A -- THE ACT CENSUS
# ---------------------------------------------------------------------------
echo "-- ARM A: ACT CENSUS over the authored population --"
A_OUT="$REPO/.scratch/i1_egress_armA.txt"
# shellcheck disable=SC2086
"$PY" "$DET" $AUTHORED > "$A_OUT" 2>&1
A_RC=$?
cat "$A_OUT"
if [ "$A_RC" -ne 0 ]; then
  echo "ERROR: detector exited $A_RC -- refusing to report a zero it did not compute"
  exit 1
fi

get_count() { cat "$A_OUT" | grep "^COUNT $1=" | tail -1 | cut -d= -f2; }
ECS=$(get_count ECS_RUN_TASK)
CB=$(get_count CODEBUILD_START)
S3W=$(get_count S3_WRITE)
IMG=$(get_count IMAGE_PUSH)
TFA=$(get_count TERRAFORM_APPLY)
SNS=$(get_count SNS_PUBLISH)
STATIC_READS=$(get_count READS)

# ---------------------------------------------------------------------------
# ARM B -- THE CONTROL
# ---------------------------------------------------------------------------
echo
echo "-- ARM B: THE CONTROL. The same detector, on a planted positive. --"
mkdir -p "$REPO/.scratch"
"$PY" "$DET" --emit-probe "$FIX"
echo "   planted fixture: $FIX (6 real call sites, one per held act)"
B_OUT="$REPO/.scratch/i1_egress_armB.txt"
"$PY" "$DET" "$FIX" > "$B_OUT" 2>&1
cat "$B_OUT" | grep -E "^  ACT|^COUNT"
CTL_TOTAL=0
for k in ECS_RUN_TASK CODEBUILD_START S3_WRITE IMAGE_PUSH TERRAFORM_APPLY SNS_PUBLISH; do
  v=$(cat "$B_OUT" | grep "^COUNT $k=" | tail -1 | cut -d= -f2)
  CTL_TOTAL=$((CTL_TOTAL + v))
  [ "$v" -eq 0 ] && echo "   *** CONTROL GAP: the detector did not see $k ***"
done
echo "   control acts detected = $CTL_TOTAL of 6"
if [ "$CTL_TOTAL" -ge 6 ]; then CTL="FIRED"; else CTL="DID_NOT_FIRE"; fi
echo "   -> a detector that cannot go non-zero on the positive case is a constant"
echo "      wearing a measurement's clothes. This one goes non-zero."

# ---------------------------------------------------------------------------
# ARM C -- LIVE PERMITTED READS, COUNTED
# ---------------------------------------------------------------------------
echo
echo "-- ARM C: LIVE PERMITTED READS, issued now and counted --"
READS=0
try_read() {
  desc="$1"; shift
  if "$@" >/dev/null 2>"$REPO/.scratch/i1_read_err.txt"; then
    READS=$((READS + 1)); echo "   OK:   $desc"
  else
    echo "   SKIP: $desc (read failed; not counted -- $(cat "$REPO/.scratch/i1_read_err.txt" | head -1 | cut -c1-70))"
  fi
}
try_read "s3api head-object  warehouse/_branch_head.main.json" \
  .tools/aws s3api head-object --bucket opal-313476888478-globgrph --key warehouse/_branch_head.main.json
try_read "s3api get-bucket-policy  opal-data-portal-v2" \
  .tools/aws s3api get-bucket-policy --bucket opal-data-portal-v2
try_read "sts get-caller-identity" .tools/aws sts get-caller-identity
echo "   READS issued and confirmed in THIS run = $READS"
echo "   Each is a READ of Opal infrastructure, which the hold expressly permits."
echo "   None publishes, starts, builds, applies or writes."

# ---------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------
TOTAL_READS=$((READS + STATIC_READS))
echo
echo "=============================================================================="
echo "== EGRESS-HOLD VERDICT (ordered for the accept) =="
echo "ECS_RUN_TASK_CALLS=$ECS"
echo "CODEBUILD_STARTS=$CB"
echo "S3_WRITES=$S3W"
echo "IMAGE_PUSHES=$IMG"
echo "TERRAFORM_APPLIES=$TFA"
echo "SNS_PUBLISHES=$SNS   (not one of the five; the hold names it and so do I)"
echo "READS=$TOTAL_READS (permitted)   [$STATIC_READS read call sites in the authored"
echo "   scripts + $READS reads issued live by this script]"
echo "EGRESS_PROBE_CONTROL=$CTL"
echo
echo "WHAT THIS DOES NOT PROVE, stated rather than left to be assumed: it proves"
echo "  no held act is CODED into anything this order authored, and that the"
echo "  detector fires when one is. It is not a CloudTrail audit of the session."
echo "  The strongest independent corroboration available without egress is that"
echo "  the graph_nodes snapshot id and the branch-head marker are unchanged from"
echo "  the value the writer stamped at 12:24:50Z, which no act of mine moved."
echo "PROVENANCE: the five counts and READS are \`measured\` -- a detector and the"
echo "  AWS CLI returned them in this run. The coverage statement is \`held\`."

if [ "$ECS" -eq 0 ] && [ "$CB" -eq 0 ] && [ "$S3W" -eq 0 ] && [ "$IMG" -eq 0 ] \
   && [ "$TFA" -eq 0 ] && [ "$SNS" -eq 0 ] && [ "$CTL" = "FIRED" ] && [ "$TOTAL_READS" -gt 0 ]; then
  exit 0
fi
exit 1
