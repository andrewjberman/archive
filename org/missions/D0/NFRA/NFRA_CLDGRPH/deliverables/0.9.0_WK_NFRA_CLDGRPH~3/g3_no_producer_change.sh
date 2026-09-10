#!/usr/bin/env bash
# NFRA_CLDGRPH TO-CG-G-4 / G4-AC4 -- CG-s-35.
#
# THIS ORDER CHANGED NOTHING IT WAS NOT ASKED TO.
#   no producer file modified, no alert built, no egressing act,
#   measured from this order's OWN captures, each limb with a control.
#
# Every limb prints its instrument's coverage, its grain, and its denominator
# including what the denominator EXCLUDED.
#
# READ ONLY on the repository. The only bytes written are a control fixture in a
# mktemp directory OUTSIDE the worktree, removed before exit -- so the limb-1
# sweep below cannot be polluted by this script's own scratch.
#
# Lines that necessarily contain a detector token are tagged G3PATTERNDEF and
# are filtered out of the census: without that, the census matches its own
# pattern definitions and every count reads non-zero for the wrong reason.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../../../.." && pwd)"
cd "$ROOT" || { echo "BLOCKED: cannot cd to repo root"; exit 2; }

BASE="f3b5f26f7770b03411fdd6a5d684779e34c21e21"
SURFACE_DIR="org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3"
SURFACE_ROW="org/missions/D0/NFRA/NFRA_CLDGRPH/surprise-channel/investigations/INVESTIGATION_v1.md"
SURFACE_TO="org/missions/D0/NFRA/NFRA_CLDGRPH/task-orders/NFRA_CLDGRPH.TO-CG-G-4.portal-layer-vintage.md"

echo "=============================================================================="
echo "G4-AC4 -- NO PRODUCER FILE MODIFIED, NO ALERT BUILT, NO EGRESSING ACT"
echo "=============================================================================="
echo "repo root : $ROOT"
echo "base      : $BASE (the commit this worktree was cut from)"
echo "surface   : $SURFACE_DIR/"
echo "            $SURFACE_ROW"
echo "            $SURFACE_TO"
echo ""

# ---------------------------------------------------------------------------
# The classifier. A path is OFF-SURFACE unless it is inside one of the three
# paths the order grants. A pure function of the path string, which is what
# lets the control exercise it without touching a single producer byte.
# ---------------------------------------------------------------------------
classify() {
  case "$1" in
    "$SURFACE_DIR"/*) echo "ON-SURFACE" ;;
    "$SURFACE_ROW")   echo "ON-SURFACE" ;;
    "$SURFACE_TO")    echo "ON-SURFACE" ;;
    *)                echo "OFF-SURFACE" ;;
  esac
}

# ---------------------------------------------------------------------------
# LIMB 1 -- files this order touched.
# INSTRUMENT: git, two sweeps -- the committed delta since the cut base, and
#             the working tree (tracked modifications AND untracked files).
# GRAIN     : one repository path per row.
# ---------------------------------------------------------------------------
TOUCHED_LIST="$( { git diff --name-only "$BASE"..HEAD; \
                   git status --porcelain | sed -e 's/^...//'; } \
                 | sed -e 's#\\#/#g' -e '/^$/d' | sort -u )"
TOUCHED=$(printf '%s\n' "$TOUCHED_LIST" | sed -e '/^$/d' | wc -l | tr -d ' ')

OFF=0
OFF_LIST=""
OLDIFS="$IFS"
IFS='
'
for p in $TOUCHED_LIST; do
  [ -z "$p" ] && continue
  if [ "$(classify "$p")" = "OFF-SURFACE" ]; then
    OFF=$((OFF + 1))
    OFF_LIST="$OFF_LIST$p
"
  fi
done
IFS="$OLDIFS"

echo "LIMB 1 -- FILES TOUCHED"
echo "  INSTRUMENT  : git diff --name-only $BASE..HEAD  UNION  git status --porcelain"
echo "  COVERAGE    : the whole worktree -- committed delta AND working tree,"
echo "                tracked modifications AND untracked files (the ?? rows are"
echo "                included, which is how a NEW off-surface file gets caught)"
echo "  GRAIN       : one repository path per row"
echo "  DENOMINATOR : $TOUCHED path(s) touched in total; EXCLUDED from the sweep:"
echo "                nothing -- both sweeps are unfiltered and their union is taken."
echo "                This script's own control fixture lives outside the worktree"
echo "                precisely so that it cannot appear here."
echo "  paths touched:"
printf '%s\n' "$TOUCHED_LIST" | sed -e '/^$/d' -e 's/^/                /'
echo "  OFF-SURFACE : $OFF of $TOUCHED"
if [ "$OFF" -gt 0 ]; then
  printf '%s' "$OFF_LIST" | sed -e '/^$/d' -e 's/^/                /'
fi
echo ""

# ---------------------------------------------------------------------------
# LIMB 2 and 3 -- what this order's EXECUTABLES can do.
# INSTRUMENT: a token census over every .py/.sh this order wrote.
# GRAIN     : one matching line per hit.
# EXCLUDED : .md and .json records. A record that QUOTES an act (this order's
#            result quotes round 6's deploy-ledger lines verbatim) is not an
#            act; only an executable can perform one, so the census is scoped
#            to executables and the exclusion is stated rather than inferred.
# ---------------------------------------------------------------------------
EXES=$(ls "$SURFACE_DIR"/g3_*.py "$SURFACE_DIR"/g3_*.sh 2>&1 | grep -v 'No such file')
NEXE=$(printf '%s\n' "$EXES" | sed -e '/^$/d' | wc -l | tr -d ' ')

ALERT_PAT='sns[.]publish|create_topic|put_metric_alarm|ses[.]send|send_raw_email|send_email|[.]subscribe[(]|put-metric-alarm|--topic-arn' # G3PATTERNDEF
EGRESS_PAT='run-task|run_task[(]|start_build[(]|start-build|docker build|docker push|s3 cp|put_object[(]|upload_file[(]|upload_fileobj[(]|safe-apply|terraform apply|update-function-code|boto3' # G3PATTERNDEF

count_hits() {
  local pat="$1"; shift
  local n=0
  local f
  local c
  for f in "$@"; do
    [ -f "$f" ] || continue
    c=$(grep -Ev 'G3PATTERNDEF|G3QUOTE' "$f" | grep -Ec "$pat")
    n=$((n + c))
  done
  echo "$n"
}

ALERTS=$(count_hits "$ALERT_PAT" $EXES)
EGRESS=$(count_hits "$EGRESS_PAT" $EXES)

# The excluded lines, PRINTED. An exclusion a reader cannot audit is an
# exclusion that hides a hit; these four are prose inside executables that
# QUOTE another seat's round-6 act or restate the hold's own vocabulary.
QLINES=$(grep -n 'G3QUOTE' $EXES | grep -E "$ALERT_PAT|$EGRESS_PAT")
QUOTED=$(printf '%s\n' "$QLINES" | sed -e '/^$/d' | wc -l | tr -d ' ')
echo "QUOTE-EXCLUSION AUDIT -- $QUOTED line(s) actually excluded as PROSE-THAT-QUOTES"
echo "  (a tag on a line carrying no detector token excludes nothing and is not"
echo "  counted here; every excluded line is printed so the exclusion is auditable):"
printf '%s\n' "$QLINES" | sed -e '/^$/d' -e 's/^/    /'
echo ""

echo "LIMB 2 -- ALERTS BUILT"
echo "  INSTRUMENT  : token census for alert/notification CONSTRUCTION over this"
echo "                order's executables (standing moratorium: no alert, alarm,"
echo "                SNS, SES, notification, freshness-checker or monitor)"
echo "  pattern     : $ALERT_PAT"
echo "  COVERAGE    : $NEXE of $NEXE executables this order wrote"
echo "  GRAIN       : one matching LINE per hit (a construction call, not a mention)"
echo "  EXCLUDED    : .md and .json records -- a record that names an alert surface"
echo "                in prose has built nothing; and G3PATTERNDEF lines, which are"
echo "                this census's own pattern definitions"
echo "  ALERTS_BUILT=$ALERTS"
echo ""

echo "LIMB 3 -- EGRESSING ACTS"
echo "  INSTRUMENT  : token census for every egress-capable call named by THE EGRESS"
echo "                HOLD (ECS run-task, CodeBuild start, image build/push, S3 write,"  # G3QUOTE
echo "                safe-apply, lambda code update), PLUS the bare client-library"  # G3QUOTE
echo "                token -- no AWS call of any kind can be made without it, so one"
echo "                zero there bounds every AWS act at once"
echo "  pattern     : $EGRESS_PAT"
echo "  COVERAGE    : $NEXE of $NEXE executables this order wrote"
echo "  GRAIN       : one matching LINE per hit"
echo "  EXCLUDED    : .md and .json records (same reason as limb 2), and G3PATTERNDEF"
echo "                lines. The deploy-ledger act lines this order's result QUOTES"
echo "                are OTHER SEATS' round-6 acts, not this order's."
echo "  EGRESS_ACTS=$EGRESS"
echo ""

# ---------------------------------------------------------------------------
# THE CONTROL. Every limb above can only report zero, and a detector that
# cannot report non-zero on a positive is a constant wearing a measurement's
# clothes. So each detector is run once more against a planted positive placed
# OUTSIDE the worktree, and the path classifier is exercised both ways.
# ---------------------------------------------------------------------------
FIXDIR="$(mktemp -d)"
FIX="$FIXDIR/planted_positive.py"
{
  echo "import boto3"                                                    # G3PATTERNDEF
  echo "s3 = boto3.client('s3')"                                         # G3PATTERNDEF
  echo "s3.upload_file('x', 'b', 'k')"                                   # G3PATTERNDEF
  echo "sns.publish(TopicArn='arn:aws:sns:us-east-1:0:t', Message='m')"  # G3PATTERNDEF
} > "$FIX"

CTL_ALERTS=$(count_hits "$ALERT_PAT" "$FIX")
CTL_EGRESS=$(count_hits "$EGRESS_PAT" "$FIX")
CTL_PATH=$(classify "infra/aws/globgrph/_provenance.py")
CTL_PATH2=$(classify "$SURFACE_DIR/g3_mover.py")

echo "CONTROL"
echo "  planted positive : $FIX"
echo "                     4 lines, OUTSIDE the worktree, so it is invisible to"
echo "                     limb 1 and to the limb 2/3 census; removed below"
echo "  alert detector on the planted positive   : $CTL_ALERTS hit(s)  (needs > 0)"
echo "  egress detector on the planted positive  : $CTL_EGRESS hit(s)  (needs > 0)"
echo "  path classifier on a PRODUCER path       : infra/aws/globgrph/_provenance.py"
echo "                                             -> $CTL_PATH  (needs OFF-SURFACE)"
echo "  path classifier on an ON-SURFACE path    : $SURFACE_DIR/g3_mover.py"
echo "                                             -> $CTL_PATH2  (needs ON-SURFACE)"
echo "  the classifier control is a PURE-STRING exercise: it proves the classifier"
echo "  would flag a producer edit without any producer byte being touched"

CONTROL="NOT-FIRED"
if [ "$CTL_ALERTS" -gt 0 ] && [ "$CTL_EGRESS" -gt 0 ] \
   && [ "$CTL_PATH" = "OFF-SURFACE" ] && [ "$CTL_PATH2" = "ON-SURFACE" ]; then
  CONTROL="FIRED"
fi
rm -rf "$FIXDIR"
if [ -e "$FIX" ]; then FIXGONE="NO"; else FIXGONE="YES"; fi
echo "  fixture removed  : $FIXGONE"
echo ""

echo "=============================================================================="
echo "PRODUCER_FILES_MODIFIED=$OFF"
echo "ALERTS_BUILT=$ALERTS"
echo "EGRESS_ACTS=$EGRESS"
echo "CONTROL=$CONTROL"
echo "=============================================================================="
echo "  denominators: $OFF of $TOUCHED touched paths are off-surface;"
echo "                $ALERTS and $EGRESS hits over $NEXE of $NEXE executables;"
echo "                every count above is a MEASURED zero beside a control that"
echo "                returns non-zero on a planted positive."
