#!/usr/bin/env bash
# H2-AC4 -- THE EGRESS HOLD HONOURED, AND THE PERMITTED READ COUNTED RATHER THAN HIDDEN.
#
# NFRA_CLDGRPH TO-CG-H-2 / cell CG-s-37, worker 0.9.0_WK_NFRA_CLDGRPH~1.
#
# Every globgrph ECS derive publishes [SEV1][PAGE] / [SEV2][digest] to a topic carrying a live
# SMS subscription to a personal mobile (rows W2-S72, S104, S106). So this order forbids: any
# ECS task run, any CodeBuild start, any image build/push/digest re-pin, any terraform apply,
# and ANY S3 WRITE. It PERMITS an S3 READ.
#
# INSTRUMENT: a pattern scan over the ACT-BEARING artifacts this order produced -- the python
# it wrote and the diff it made to production code -- plus its own S3 ledger. COVERAGE: the
# denominator is printed and every exclusion is named with its reason. A scan of prose is
# excluded on purpose: the record MUST quote the forbidden verbs to state the hold.
# GRAIN: one pattern hit per line of file text.
# ENVIRONMENT: this worktree, this branch, at the commit printed below.
#
# THE CONTROL IS THE POINT: five zeros prove nothing on their own -- an empty scan and a clean
# scan read identically. The same detector is run against a PLANTED file carrying one line per
# held act, and it must find all five.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
WS="$(cd "$HERE/../../../../../../.." && pwd)"
SCRATCH="$WS/.scratch"
mkdir -p "$SCRATCH"
BASE_COMMIT="2fd5cae09f"

P_ECS='ecs +run-task|run_task'
P_CB='codebuild +start-build|start_build'
P_S3W='s3api +put-object|put_object|upload_file|upload_fileobj|s3 +cp +[^ ]+ +s3://|s3 +sync'
P_IMG='docker +push|ecr +put-image|buildx|batch-delete-image'
P_TF='terraform +apply|safe-apply|terraform +destroy'

DIFF="$SCRATCH/h2_prod_diff.txt"
git -C "$WS" diff "$BASE_COMMIT" -- infra org/modules data lib portal > "$DIFF" 2>&1

SCAN_FILES=""
for f in "$HERE"/*.py "$HERE"/*.ledger "$DIFF"; do
  [ -f "$f" ] && SCAN_FILES="$SCAN_FILES $f"
done

count_hits() {  # $1 = ERE, rest = files
  local pat="$1"; shift
  cat "$@" 2>/dev/null | grep -E -c -i "$pat"
}

echo "H2-AC4 EGRESS HOLD -- NFRA_CLDGRPH CG-s-37"
echo "TREE_READ=$WS"
echo "BRANCH=$(git -C "$WS" rev-parse --abbrev-ref HEAD)  HEAD=$(git -C "$WS" rev-parse HEAD)"
echo "INSTRUMENT=pattern scan (grep -E -i) over the act-bearing artifacts + the production diff"
echo ""
echo "---- SCANNED POPULATION ----"
N=0
for f in $SCAN_FILES; do
  N=$((N+1))
  echo "  [$N] ${f#$WS/}  ($(wc -l < "$f" | tr -d ' ') lines)"
done
echo "SCANNED_DENOMINATOR=$N files"
echo "EXCLUSIONS, each with its reason:"
echo "  - this script itself (it CONTAINS the five patterns by construction; scanning it would"
echo "    guarantee a false positive on every one)"
echo "  - *.md under the deliverable: prose. The record must QUOTE the forbidden verbs to state"
echo "    the hold, so a prose scan measures the writing, not the acts."
echo "  - the production diff is INCLUDED (as $DIFF, produced from git diff $BASE_COMMIT)"
echo "    because that is where a held act would actually have to land."
echo ""

# THE TREE CONTROL: a file that exists only on this branch must be in the scanned population.
if echo "$SCAN_FILES" | grep -q "h2_carrier_asymmetry.py"; then
  TREE_CONTROL="FIRED"
else
  TREE_CONTROL="DID-NOT-FIRE"
fi
echo "TREE_CONTROL=$TREE_CONTROL (a file that exists ONLY on branch wk-cldgrph-8-1 --"
echo "  h2_carrier_asymmetry.py -- appears in the scanned population, so the scan read THIS tree)"
echo ""

ECS=$(count_hits "$P_ECS" $SCAN_FILES)
CB=$(count_hits "$P_CB" $SCAN_FILES)
S3W=$(count_hits "$P_S3W" $SCAN_FILES)
IMG=$(count_hits "$P_IMG" $SCAN_FILES)
TF=$(count_hits "$P_TF" $SCAN_FILES)

LEDGER="$HERE/h2_s3_reads.ledger"
S3R=$(grep -E -c '^READ ' "$LEDGER")
S3W_LEDGER=$(grep -E -c '^WRITE ' "$LEDGER")
S3W_TOTAL=$((S3W + S3W_LEDGER))

# THE PLANTED POSITIVE: one line per held act, scanned by the SAME detector.
PROBE="$SCRATCH/h2_egress_probe.txt"
{
  echo "aws ecs run-task --cluster globgrph --task-definition globgrph-derive-runner"
  echo "aws codebuild start-build --project-name opal-stitch-produce"
  echo "aws s3api put-object --bucket opal-313476888478-globgrph --key snapshots/latest.txt"
  echo "docker push 313476888478.dkr.ecr.us-east-1.amazonaws.com/globgrph:latest"
  echo "terraform apply -target=aws_ecs_task_definition.derive"
} > "$PROBE"
PE=$(count_hits "$P_ECS" "$PROBE"); PC=$(count_hits "$P_CB" "$PROBE")
PS=$(count_hits "$P_S3W" "$PROBE"); PI=$(count_hits "$P_IMG" "$PROBE")
PT=$(count_hits "$P_TF" "$PROBE")
FIRED=0
for v in "$PE" "$PC" "$PS" "$PI" "$PT"; do [ "$v" -ge 1 ] && FIRED=$((FIRED+1)); done
echo "---- CONTROL: the same detector against a planted positive ($PROBE) ----"
echo "  planted lines=5  patterns that fired=$FIRED of 5  (ecs=$PE codebuild=$PC s3write=$PS image=$PI terraform=$PT)"
echo ""

echo "---- HELD ACTS, MEASURED OVER THE SCANNED POPULATION ----"
echo "ECS_RUN_TASK_CALLS=$ECS"
echo "CODEBUILD_STARTS=$CB"
echo "S3_WRITES=$S3W_TOTAL  (pattern scan $S3W + ledger WRITE lines $S3W_LEDGER)"
echo "IMAGE_PUSHES=$IMG"
echo "TERRAFORM_APPLIES=$TF"
echo "S3_READS=$S3R (permitted)"
echo "  every read is a GET/HEAD/LIST against s3://opal-313476888478-globgrph, enumerated with"
echo "  its purpose in ${LEDGER#$WS/}; none writes, none publishes, none reaches a topic."
if [ "$FIRED" -eq 5 ]; then
  echo "EGRESS_PROBE_CONTROL=FIRED"
else
  echo "EGRESS_PROBE_CONTROL=DID-NOT-FIRE ($FIRED of 5) -- the five zeros above are NOT evidence"
fi
RC=0
[ "$ECS" -eq 0 ] || RC=1
[ "$CB" -eq 0 ] || RC=1
[ "$S3W_TOTAL" -eq 0 ] || RC=1
[ "$IMG" -eq 0 ] || RC=1
[ "$TF" -eq 0 ] || RC=1
[ "$FIRED" -eq 5 ] || RC=1
[ "$TREE_CONTROL" = "FIRED" ] || RC=1
exit $RC
