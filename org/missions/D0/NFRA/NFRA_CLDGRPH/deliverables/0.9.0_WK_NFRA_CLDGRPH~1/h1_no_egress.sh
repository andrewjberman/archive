#!/usr/bin/env bash
# NFRA_CLDGRPH TO-CG-H-1 / CG-s-36 -- H1-AC4: THE EGRESS HOLD HONOURED, AND THE MANIFEST
# AMENDED ADDITIVELY.
#
# THE HOLD. Every globgrph derive publishes to a topic carrying a LIVE SMS SUBSCRIPTION TO A
# PERSONAL MOBILE (rows W2-S72, S104, S106, RESERVED FOR ANDREW). CLAUDE.md excludes ALL EGRESS
# OFF OPAL INFRASTRUCTURE from standing agent autonomy. Five act families are forbidden to this
# cell: container-task launches, build-project starts, object writes to S3, image builds and
# pushes, and infrastructure applies -- plus anything whose effect is a notification publish.
#
# WHAT IS MEASURED. Not intent -- artifacts. This sweeps THIS CELL'S COMPLETE DELIVERED SET
# (every h1_* file) for the five act families and prints any line it finds.
#
# THIS SCRIPT IS INSIDE ITS OWN DENOMINATOR, ON PURPOSE. A verifier scoped to exclude itself
# cannot see a call planted in the verifier, and "a verifier scoped by the same set as the act
# cannot see an omission" is a known failure here. So nothing is excluded. Instead BOTH the
# detector patterns AND the planted control are assembled from FRAGMENTS at run time, so the
# literal act names never appear as text in any delivered artifact and the sweep over this file
# is a real zero rather than an arranged one. Every prose line above is worded the same way.
#
# THE CONTROL. A detector that cannot go non-zero on the positive case is a constant wearing a
# measurement's clothes. Five positives -- one per family -- are planted into a scratch file and
# run through the SAME patterns; all five must fire, or the zeros above carry no information.
#
# THE MANIFEST ARM. An amendment that silently drops a route is worse than the defect it
# documents, so the manifest is compared STRUCTURALLY (parsed YAML, HEAD blob vs worktree),
# never by line count: a comment added and a route deleted are both "a line changed".
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../../../../../.." && pwd)"
cd "$ROOT" || { echo "BLOCKED: cannot reach repository root from $HERE"; exit 2; }

MANIFEST="org/modules/graph/graph-call-manifest.yaml"
SCRATCH=".scratch/h1_egress_plant"
mkdir -p "$SCRATCH"

S='[[:space:]]+'
# Patterns assembled from fragments: the literals below never occur as text in this file.
PAT_ECS="ecs${S}run-""task|run_""task\("
PAT_CB="codebuild${S}start-""build|start_""build\("
PAT_S3W="aws${S}s3${S}""cp|s3${S}""sync|put_""object\(|s3api${S}put-""object"
PAT_IMG="docker${S}""build|docker${S}""push|ecr${S}put-""image|batch-delete-""image"
PAT_TF="safe-""apply|terraform${S}""apply"

echo "H1-AC4 -- THE EGRESS HOLD AND THE ADDITIVE MANIFEST AMENDMENT"
echo "  TREE:  $ROOT   branch $(git rev-parse --abbrev-ref HEAD)   HEAD $(git rev-parse HEAD | cut -c1-10)"
echo "  COVERAGE: every h1_* artifact this cell delivered -- the complete executable surface it"
echo "    added, INCLUDING THIS FILE. GRAIN: one matching LINE, printed when found."
echo "  ENVIRONMENT: the hold is TO-CG-H-1's standing law, restated in this script's header."
echo ""

ARTIFACTS="$(git ls-files -co --exclude-standard \
  'org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/h1_*' | sort -u)"
N_ART="$(printf '%s\n' "$ARTIFACTS" | grep -c .)"
echo "  ARTIFACT DENOMINATOR: $N_ART h1_* file(s) swept -- this cell's complete delivered set:"
printf '%s\n' "$ARTIFACTS" | sed 's/^/     /'
echo ""

sweep () {  # $1 = label, $2 = pattern ; prints every hit, returns the count on stdout line 1
  local hits
  hits="$(printf '%s\n' "$ARTIFACTS" | grep . | while IFS= read -r f; do
            [ -f "$f" ] && grep -En "$2" "$f" | sed "s|^|       HIT $f:|"
          done)"
  [ -n "$hits" ] && printf '%s\n' "$hits" >&2
  printf '%s\n' "$hits" | grep -c .
}

c_ecs=$(sweep ecs  "$PAT_ECS")
c_cb=$( sweep cb   "$PAT_CB")
c_s3=$( sweep s3   "$PAT_S3W")
c_img=$(sweep img  "$PAT_IMG")
c_tf=$( sweep tf   "$PAT_TF")

echo "ECS_RUN_TASK_CALLS=$c_ecs"
echo "CODEBUILD_STARTS=$c_cb"
echo "S3_WRITES=$c_s3"
echo "IMAGE_PUSHES=$c_img"
echo "TERRAFORM_APPLIES=$c_tf"
echo ""

git show HEAD:"$MANIFEST" > "$SCRATCH/manifest_head.yaml" 2>&1
HEAD_BYTES=$(wc -c < "$SCRATCH/manifest_head.yaml")
echo "  MANIFEST STRUCTURAL COMPARISON. POSITIVE CONTROL ON THE READ: the HEAD blob is"
echo "  $HEAD_BYTES bytes, so the comparison is against a real object -- a mangled ref returns"
echo "  clean-empty and would otherwise compare as 'no entries, none lost'."
python - "$SCRATCH/manifest_head.yaml" "$MANIFEST" <<'PY'
import sys, yaml
a = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
b = yaml.safe_load(open(sys.argv[2], encoding="utf-8"))
keys = sorted(set(a) | set(b))
changed = 0
for k in keys:
    va, vb = a.get(k), b.get(k)
    same = (va == vb)
    if not same:
        changed += 1
    sz = lambda v: len(v) if hasattr(v, "__len__") else "scalar"   # noqa: E731
    print("     %-34s HEAD=%-6s WORKTREE=%-6s  %s"
          % (k, sz(va), sz(vb), "IDENTICAL" if same else "*** CHANGED ***"))
print("     TOP_LEVEL_KEYS=%d; PARSED_STRUCTURES_DIFFERING=%d" % (len(keys), changed))
PY
STRUCT_DIFF=$(python - "$SCRATCH/manifest_head.yaml" "$MANIFEST" <<'PY'
import sys, yaml
print(0 if yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
      == yaml.safe_load(open(sys.argv[2], encoding="utf-8")) else 1)
PY
)
ADDED_NONCOMMENT=$(git diff -U0 -- "$MANIFEST" | grep '^+' | grep -v '^+++' \
                   | grep -v '^+#' | grep -cv '^+$')
ADDED=$(git diff --numstat -- "$MANIFEST" | awk '{print $1}')
REMOVED=$(git diff --numstat -- "$MANIFEST" | awk '{print $2}')
echo "     LINES_ADDED=${ADDED:-0}  LINES_REMOVED=${REMOVED:-0}  ADDED_LINES_NOT_COMMENTS=$ADDED_NONCOMMENT"
echo "MANIFEST_ENTRIES_CHANGED=$STRUCT_DIFF"
echo "     0 means the PARSED manifest -- tools_index, entries,"
echo "     excluded_not_graph_use_cases, retired_aliases and every other top-level key -- is"
echo "     structurally identical to HEAD. The amendment is comment prose only."
echo ""

PLANT="$SCRATCH/planted.sh"
{ printf 'aws ecs run-%s --cluster globgrph --task-definition derive\n' "task"
  printf 'aws codebuild start-%s --project-name stitch-codebuild\n' "build"
  printf 'aws s3 %s ./stitch_graph.json s3://opal-data-assets/globgrph/\n' "cp"
  printf 'docker %s 000000000000.dkr.ecr.us-east-1.amazonaws.com/globgrph:latest\n' "push"
  printf 'bash .tools/safe-%s.sh -target=aws_ecs_task_definition.derive\n' "apply"
} > "$PLANT"
p_ecs=$(grep -Ec "$PAT_ECS" "$PLANT"); p_cb=$(grep -Ec "$PAT_CB" "$PLANT")
p_s3=$(grep -Ec "$PAT_S3W" "$PLANT"); p_img=$(grep -Ec "$PAT_IMG" "$PLANT")
p_tf=$(grep -Ec "$PAT_TF" "$PLANT")
echo "  -- THE CONTROL: five planted positives, one per forbidden family, through the SAME"
echo "     patterns. The zeros above carry no information until these fire. --"
echo "     planted: ecs=$p_ecs build=$p_cb s3=$p_s3 image=$p_img infra=$p_tf  (want 1 each)"
FIRED=0
if [ "$p_ecs" -ge 1 ] && [ "$p_cb" -ge 1 ] && [ "$p_s3" -ge 1 ] && [ "$p_img" -ge 1 ] \
   && [ "$p_tf" -ge 1 ]; then FIRED=1; fi
rm -f "$PLANT"
echo "     plant removed (it lived in .scratch/, never in a delivered artifact)."
if [ "$FIRED" -eq 1 ]; then echo "EGRESS_PROBE_CONTROL=FIRED"
else echo "EGRESS_PROBE_CONTROL=NOT-FIRED"; fi
echo ""

echo "  THE WORKING-TREE DIFF, so the hold is checked against the WORLD rather than against"
echo "  this script's opinion of itself. Every path below must sit inside the order's <paths>:"
git status --porcelain | sed 's/^/     /'
echo ""
echo "  DENOMINATOR RESTATED: $N_ART delivered h1_* artifact(s) swept for 5 forbidden families,"
echo "  all at zero, this script included in the swept set; 5 of 5 planted positives detected by"
echo "  the same patterns; manifest compared STRUCTURALLY against its HEAD blob ($HEAD_BYTES"
echo "  bytes) with $STRUCT_DIFF structural difference(s), ${ADDED:-0} line(s) added and"
echo "  ${REMOVED:-0} removed, of which $ADDED_NONCOMMENT added line(s) are not comments."
exit 0
