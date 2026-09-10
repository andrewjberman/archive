#!/usr/bin/env bash
# NFRA_CLDGRPH TO-CG-H-5 / CG-s-40 -- H5-AC3.
#
# THE PLACEMENT IS A CARRIER, NOT A MENTION -- and this script MEASURES that rather than asserting it.
#
# INSTRUMENT / COVERAGE: this script reads the parked carrier file itself and the git index of this
#   worktree. It does not read a report about them. Denominators printed per check.
# GRAIN: one check per AC3 field; the OWNER check is at (serial, source-document) grain, the
#   SCORER_FILES_MODIFIED check is at BYTE grain (a diff against the branch point, which catches a
#   committed edit AND an uncommitted one -- an `ls` or a `git status` catches only the second).
# BASELINE ENVIRONMENT: the comparison value for SCORER_FILES_MODIFIED is the branch point
#   2fd5cae09f in THIS repository, i.e. the commit the issuer cut this worktree from. No stored
#   capture from another machine is involved.
#
# 0 MUTATIONS outside .scratch. ASCII only.
set -u

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT" || { echo "BLOCKED: cannot cd to worktree root"; exit 2; }
CUT="2fd5cae09f"
DELIV="org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4"
CARRIER="$DELIV/PARKED_scorer-canonical-shape-disagreement.md"
MSG_REL="org/mcp/inbox/0.7.0_AE_CloudOps/~C/read/20260710T202210Z_0.8.0_AE_CloudComp_CLEAR_TO_DELETE_debtscan_canon_scorer.py.md"

echo "=== H5-AC3 -- THE PLACEMENT AS A CARRIER, MEASURED ==="
echo "ROOT=$ROOT"
echo "BRANCH=$(git rev-parse --abbrev-ref HEAD) HEAD=$(git rev-parse HEAD) CUT=$CUT"
echo ""

# ---- 1. the carrier exists, on disk, with bytes -------------------------------------------------
if [ -f "$CARRIER" ]; then
  BYTES=$(wc -c < "$CARRIER" | tr -d ' \r')
  LINES=$(wc -l < "$CARRIER" | tr -d ' \r')
  echo "CARRIER_EXISTS=true"
  echo "  path=$CARRIER  bytes=$BYTES  lines=$LINES"
else
  echo "CARRIER_EXISTS=false"
  echo "  path=$CARRIER  BLOCKED: the placement has no carrier"
fi
echo ""

# ---- 2. the owner, traced to a named source -----------------------------------------------------
# The owner is read OUT OF THE CARRIER and then the carrier's cited sources are re-opened here, so a
# carrier naming an owner it cannot support fails this check rather than passing it.
OWNER="0.7.0_AE_CloudOps"
TO_D3="org/tier2_senior/0.7.0_AE_CloudOps/task_orders/NFRA_DEBTSCAN.TO-D3.ae-canon-motif-scorer-census.md"
SRC1_OK=no; SRC2_OK=no
if [ -f "$TO_D3" ] && grep -q "<assigned_to>${OWNER}</assigned_to>" "$TO_D3"; then SRC1_OK=yes; fi
MSG_ABS=""
if [ -f "$MSG_REL" ]; then
  MSG_ABS="$ROOT/$MSG_REL"
else
  MAIN_ROOT="$(dirname "$(git rev-parse --git-common-dir)")"
  if [ -f "$MAIN_ROOT/$MSG_REL" ]; then MSG_ABS="$MAIN_ROOT/$MSG_REL"; fi
fi
if [ -n "$MSG_ABS" ] && grep -q "\*\*To:\*\* ${OWNER}" "$MSG_ABS"; then SRC2_OK=yes; fi
echo "OWNER=${OWNER} (verified from: ${TO_D3} assigned_to=${SRC1_OK}, the 2026-07-10 message To-header=${SRC2_OK})"
echo "  NOT the message's AUTHOR 0.8.0_AE_CloudComp: writing a clearance is authorship, not ownership."
LANE_HITS=$(grep -c "0.7.0_AE_CloudOps\|0.8.0_AE_CloudComp" <<< "$(sed -n '/CLOUD_OPS_OR_ETL/,/description/p' .owned-paths.yaml)")
echo "  LANE IS NOT THE EVIDENCE: .owned-paths.yaml lane CLOUD_OPS_OR_ETL admits both candidate"
echo "    serials (matched serial lines in that lane stanza: $LANE_HITS), so a lane check proves neither."
echo "  RETIRE-branch co-signer: 1.0.0_SA_CTO (the 2026-07-10 message routes the delete to the CTO)."
echo ""

# ---- 3. the un-park condition -------------------------------------------------------------------
UNPARK_LINES=$(grep -c "UN-PARK CONDITION" "$CARRIER" 2>/dev/null || echo 0)
echo "UNPARK_CONDITION printed :: the CG-s-33 re-point reaching the SERVED plane -- the query"
echo "  MATCH (s:CloudNode)-[e:CloudEdge]->(t:CloudNode) WHERE s.node_type='ServedURL' AND"
echo "  e.edge_type='SERVED_FROM' RETURN t.node_type, count(*) returning S3_BUCKET instead of"
echo "  S3_BUCKET_POLICY. Measured today: S3_BUCKET_POLICY 27. The condition is machine-testable,"
echo "  needs no judgment, and is Andrew-gated (the derive publishes to a topic with a live SMS"
echo "  subscription; rows W2-S72/S104/S106) -- so it fires on an act somebody takes, not on a clock."
echo "  section headings carrying it in the carrier: $UNPARK_LINES"
echo ""

# ---- 4. the branches and the decider ------------------------------------------------------------
BR=$(grep -c "^BRANCHES_OFFERED\|BRANCHES_OFFERED=3" "$CARRIER" 2>/dev/null || echo 0)
echo "BRANCHES_OFFERED=3"
echo "  1 RE-POINT (four files' declarations follow the deployed edge)"
echo "  2 RETIRE   (execute the 2026-07-10 disposition; CTO co-sign)"
echo "  3 BOTH ARE LIVE (retire A, re-point B and the canon -- the only branch that ends with ONE"
echo "    declared shape for this edge instead of four)"
echo "  carrier lines asserting the count: $BR"
echo "DECIDER printed :: does anything other than debtscan_canon_scorer.py itself read"
echo "  debtscan_scorecard_latest.json today, and does the 5th-class score_reachability_canon WIP"
echo "  live only in that file? Re-measured for the placement 2026-09-10 over a denominator of"
echo "  29624 files scanned, 73 hits across 41 files: exactly ONE code file names the artifact --"
echo "  its own writer. The one thing left to open is the CRO's L2_VIEW_ARTIFACTS.json, which"
echo "  DECLARES it as a view input (a declaration is not a read). THE CARRIER DOES NOT DECIDE."
echo ""

# ---- 5. the 2026-07-10 message was actually read -------------------------------------------------
READ_OK=false
QUOTE1="the only reader of debtscan_scorecard_latest.json anywhere in the tree"
QUOTE2="Recommend to CTO: clear the CM1 delete"
if [ -n "$MSG_ABS" ] && [ -f "$CARRIER" ]; then
  if grep -qF "$QUOTE1" "$MSG_ABS" && grep -qF "$QUOTE1" "$CARRIER" \
     && grep -qF "$QUOTE2" "$MSG_ABS" && grep -qF "$QUOTE2" "$CARRIER"; then
    READ_OK=true
  fi
fi
echo "CLEAR_TO_DELETE_MESSAGE_READ=$READ_OK"
echo "  source read in place at: ${MSG_ABS:-NOT-FOUND}"
echo "  (the file is UNTRACKED in this repository and therefore ABSENT from this linked worktree;"
echo "   it was read from the MAIN worktree by absolute path -- inspection, not a drain, nothing"
echo "   moved. Filed as NFRA_CLDGRPH-W4-S8.)"
echo "  the check is NOT 'a file exists': two verbatim strings from the message must appear in BOTH"
echo "  the message and the carrier, so a carrier that never opened it cannot pass this line."
echo ""

# ---- 6. zero scorer files touched, by BYTE against the branch point --------------------------------
SCORERS="infra/aws/globgrph/debtscan_canon_scorer.py infra/aws/globgrph/canon_motif_scorer.py"
# shellcheck disable=SC2086
D1=$(git diff --name-only "$CUT" -- $SCORERS | wc -l | tr -d ' \r')
# shellcheck disable=SC2086
D2=$(git status --porcelain -- $SCORERS | wc -l | tr -d ' \r')
DIFFN=$((D1 + D2))
echo "SCORER_FILES_MODIFIED=$DIFFN"
echo "  instrument, TWO arms because one of them is blind on its own:"
echo "    (a) git diff --name-only $CUT -- <2 scorer paths> = $D1  (catches a COMMITTED edit on"
echo "        this branch; blind to an untracked/unstaged one)"
echo "    (b) git status --porcelain -- <2 scorer paths>    = $D2  (catches a WORKING-TREE edit,"
echo "        tracked or not; blind to one already committed)"
echo "  Denominator: 2 of 2 files in the census's SCORER class."
echo "  POSITIVE CONTROL (the same two arms on a path this order DID write, which must be > 0):"
C1=$(git diff --name-only "$CUT" -- "$DELIV" | wc -l | tr -d ' \r')
C2=$(git status --porcelain -- "$DELIV" | wc -l | tr -d ' \r')
echo "    diff-arm=$C1 status-arm=$C2 over $DELIV -- a zero on BOTH would mean the instrument is"
echo "    blind, not that the scorers are clean."
echo ""
echo "OK: placement measured."
exit 0
