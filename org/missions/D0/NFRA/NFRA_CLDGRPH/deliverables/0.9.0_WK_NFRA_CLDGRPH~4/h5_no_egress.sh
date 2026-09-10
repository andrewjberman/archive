#!/usr/bin/env bash
# NFRA_CLDGRPH TO-CG-H-5 / CG-s-40 -- H5-AC4.
#
# THE EGRESS HOLD HONOURED, MEASURED RATHER THAN ASSERTED.
#
# THE HOLD: CLAUDE.md excludes ALL egress off Opal infrastructure from standing agent autonomy, and
# every globgrph ECS derive publishes to a topic carrying a LIVE SMS SUBSCRIPTION TO A PERSONAL
# MOBILE (rows W2-S72/S104/S106, RESERVED FOR ANDREW). Forbidden to this order: `ecs run-task`, a
# CodeBuild start, an image act, `safe-apply`, an S3 WRITE, and any act whose effect is an SNS
# publish. A READ of the served graph or an Opal S3 object is permitted and this order took exactly
# one class of those (the projection-service Cypher reads in h5_disagreement.py).
#
# INSTRUMENT / COVERAGE: the population is EVERY PATH THIS ORDER TOUCHED IN THIS WORKTREE -- the
#   union of `git status --porcelain` (working-tree changes, tracked or not) and
#   `git diff --name-only <cut>` (anything already committed on this branch). That union is the
#   complete set of bytes this order could have added, so a held act it does not contain was not
#   written by this order. Denominator printed.
# GRAIN: one hit per (file, pattern). Patterns are INVOCATION-SHAPED (`aws ecs run-task`, not the
#   word "ECS"), because the carrier this order wrote NAMES the held acts in prose in order to
#   forbid them, and a word-shaped pattern would count a prohibition as a violation.
# BASELINE ENVIRONMENT: no stored baseline. The control is a probe file this script writes into
#   .scratch/ on this run and scans with the SAME function, so a zero on the real population is a
#   measurement rather than an absence of looking.
#
# THE ONE THING THIS CANNOT SEE, said plainly: an act that leaves no byte in this worktree (a live
# AWS call typed at a shell and never written down). That is bounded by the fact that this order's
# whole output is the files below, and by the open_deploys / change-management ledger being empty of
# any entry from this serial -- checked as the last arm.
#
# 0 MUTATIONS outside .scratch. ASCII only.
set -u

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT" || { echo "BLOCKED: cannot cd to worktree root"; exit 2; }
CUT="2fd5cae09f"
SELF="org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/h5_no_egress.sh"
PROBE=".scratch/h5_egress_probe.txt"

echo "=== H5-AC4 -- THE HOLD MEASURED, WITH A CONTROL THAT FIRES ==="
echo "ROOT=$ROOT  BRANCH=$(git rev-parse --abbrev-ref HEAD)  CUT=$CUT"

mkdir -p .scratch
{
  echo "H5 EGRESS PROBE -- a PLANTED POSITIVE. If the detector below does not find all five of"
  echo "these, its zeros on the real population mean nothing."
  echo "aws ecs run-task --cluster x --task-definition y"
  echo "aws codebuild start-build --project-name z"
  echo "aws s3 cp ./thing s3://bucket/key"
  echo "docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/img:latest"
  echo "bash .tools/safe-apply.sh -auto-approve"
} > "$PROBE"

# ---- the population --------------------------------------------------------------------------
POP_FILE=".scratch/h5_population.txt"
{
  git status --porcelain -uall | sed 's/^...//' | sed 's/^.* -> //'
  git diff --name-only "$CUT"
} | sed 's/"//g' | sort -u | grep -v '^$' > "$POP_FILE"
POP_ALL=$(wc -l < "$POP_FILE" | tr -d ' \r')
# .scratch is this order's scratch and holds the PROBE itself; excluded by name and printed.
grep -v '^\.scratch/' "$POP_FILE" | grep -v "^${SELF}\$" > "${POP_FILE}.scan"
POP=$(wc -l < "${POP_FILE}.scan" | tr -d ' \r')
# AN ACT IS AN INVOCATION, AND A DOCUMENT DOES NOT INVOKE. The five counters are scoped to files a
# runtime can EXECUTE (.sh/.py/.tf/.tfvars/.yaml/.yml/.json/.ps1/.bat/.cmd). The remainder -- the
# carrier, the result record, the captures -- is scanned too and reported SEPARATELY as
# PROSE_MENTIONS, because this order's own deliverables NAME the held acts in order to forbid them
# and to document these patterns. Nothing is hidden: both lists and both counts are printed.
grep -E '\.(sh|py|tf|tfvars|ya?ml|json|ps1|bat|cmd)$' "${POP_FILE}.scan" > "${POP_FILE}.exec" || true
grep -Ev '\.(sh|py|tf|tfvars|ya?ml|json|ps1|bat|cmd)$' "${POP_FILE}.scan" > "${POP_FILE}.prose" || true
POP_EXEC=$(wc -l < "${POP_FILE}.exec" | tr -d ' \r')
POP_PROSE=$(wc -l < "${POP_FILE}.prose" | tr -d ' \r')
echo "POPULATION=git status --porcelain -uall UNION git diff --name-only $CUT"
echo "  paths in union            : $POP_ALL"
echo "  minus .scratch/ (the probe lives there) and this detector's own file: $POP"
echo "  EXCLUDED_BY_NAME=$SELF (it contains every pattern by construction)"
echo "  split: EXECUTABLE-CLASS=$POP_EXEC  PROSE/CAPTURE=$POP_PROSE  (the five counters below are"
echo "    scoped to the EXECUTABLE-CLASS half; the other half is counted separately as"
echo "    PROSE_MENTIONS and its members are listed, so the scoping is visible and not silent)"
while IFS= read -r pf; do echo "    PROSE_MEMBER=$pf"; done < "${POP_FILE}.prose"

SCAN_OPENED=0
scan() { # scan <file-list> <label>
  local list="$1"; local n_ecs=0 n_cb=0 n_s3=0 n_img=0 n_tf=0 f opened=0
  while IFS= read -r f; do
    [ -f "$f" ] || continue
    opened=$((opened+1))
    grep -qF -e 'aws ecs run-task' -e 'ecs.run_task(' -e '.run_task(' "$f" 2>/dev/null && n_ecs=$((n_ecs+1))
    grep -qF -e 'codebuild start-build' -e '.start_build(' "$f" 2>/dev/null && n_cb=$((n_cb+1))
    grep -qF -e 'aws s3 cp ' -e 'aws s3 sync ' -e 's3api put-object' -e '.put_object(' -e '.upload_file(' "$f" 2>/dev/null && n_s3=$((n_s3+1))
    grep -qF -e 'docker push' -e 'docker build' -e 'ecr get-login' -e 'put-image' "$f" 2>/dev/null && n_img=$((n_img+1))
    grep -qF -e 'terraform apply' -e 'safe-apply.sh' "$f" 2>/dev/null && n_tf=$((n_tf+1))
  done < "$list"
  echo "$n_ecs $n_cb $n_s3 $n_img $n_tf $opened"
}

read -r E C S I T OPENED <<< "$(scan "${POP_FILE}.exec")"
read -r QE QC QS QI QT QOPENED <<< "$(scan "${POP_FILE}.prose")"
echo ""
echo "ECS_RUN_TASK_CALLS=$E"
echo "CODEBUILD_STARTS=$C"
echo "S3_WRITES=$S"
echo "IMAGE_PUSHES=$I"
echo "TERRAFORM_APPLIES=$T"
echo "  (each is a count of EXECUTABLE-CLASS FILES in the population carrying an invocation-shaped"
echo "   pattern -- an act this order took would have to live in one of them)"
echo "  SCANNED_FILES_ACTUALLY_OPENED=$OPENED of $POP_EXEC listed -- a zero here would make every"
echo "  count above VACUOUS, so it is printed beside them rather than assumed"
echo "PROSE_MENTIONS (the other half, disclosed not hidden): ecs=$QE codebuild=$QC s3=$QS image=$QI"
echo "  terraform=$QT over $QOPENED file(s) opened. These are this order's carrier, result record and"
echo "  captures NAMING the held acts in order to forbid them and to document these very patterns."
echo "  A markdown file cannot invoke anything; a non-zero here is a citation, not an act."

# ---- producer + scorer surfaces untouched --------------------------------------------------------
PROD_PATHS="infra/aws/globgrph org/modules/graph/canon-patterns.yaml org/modules/graph/debtscan"
# shellcheck disable=SC2086
P1=$(git diff --name-only "$CUT" -- $PROD_PATHS | wc -l | tr -d ' \r')
# shellcheck disable=SC2086
P2=$(git status --porcelain -- $PROD_PATHS | wc -l | tr -d ' \r')
echo "PRODUCER_FILES_MODIFIED=$((P1 + P2))"
echo "  surfaces: $PROD_PATHS"
echo "  committed-arm=$P1 working-tree-arm=$P2 (two arms; each is blind to what the other sees)"
echo "  this covers BOTH boundary-edge producers (derive_runner.py, derive_stitch.py), BOTH scorers,"
echo "  the ratified canon and the debtscan module home -- not just the files the cell named."

# ---- the deploy ledger, the one plane a byte-scan cannot see ---------------------------------------
LEDGER_HITS=0
if [ -d org/critical_paths/change_management ]; then
  LEDGER_HITS=$(grep -rl "0.9.0_WK_NFRA_CLDGRPH~4" org/critical_paths/change_management 2>/dev/null | wc -l | tr -d ' \r')
fi
echo "CHANGE_MANAGEMENT_ENTRIES_BY_THIS_SERIAL=$LEDGER_HITS"
echo "  (a confirmed deploy opens an entry here at START; zero entries from this serial is the"
echo "   independent-plane arm on 'no deploy was begun', not a second reading of the same bytes)"

# ---- the control -------------------------------------------------------------------------------
echo "$PROBE" > .scratch/h5_probe_list.txt
read -r PE PC PS PI PT POPENED <<< "$(scan .scratch/h5_probe_list.txt)"
echo ""
echo "--- CONTROL: the SAME scan() over a planted positive ---"
echo "  probe=$PROBE  ecs=$PE codebuild=$PC s3=$PS image=$PI terraform=$PT (each must be 1); files opened=$POPENED"
if [ "$PE" -eq 1 ] && [ "$PC" -eq 1 ] && [ "$PS" -eq 1 ] && [ "$PI" -eq 1 ] && [ "$PT" -eq 1 ]; then
  echo "EGRESS_PROBE_CONTROL=FIRED"
else
  echo "EGRESS_PROBE_CONTROL=DID-NOT-FIRE"
fi
echo "OK: hold measured."
exit 0
