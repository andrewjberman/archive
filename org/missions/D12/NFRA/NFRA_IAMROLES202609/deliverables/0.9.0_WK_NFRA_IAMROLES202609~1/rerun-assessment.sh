#!/bin/bash
# NFRA_IAMROLES202609.TO-IAM-s-9 -- the RE-RUN HARNESS (FWD-8).
#
# COMPOSES the estate's existing read-only IAM assessment instruments -- this script
# re-implements NONE of comp-iam-usage / comp-iam / comp-find; it only calls them, in the
# same order every time, and prints their own denominator + vintage lines back out so a run
# today can be put beside a run next quarter (build-ladder rung 2: COMPOSE, do not mint).
#
# RE-RUNNABLE ON DEMAND BY A PERSON WHO DID NOT BUILD IT. Invoke it by hand:
#   rerun-assessment.sh --dry-run                 (prints the steps, touches nothing, exit 0)
#   rerun-assessment.sh [--role NAME] [--lookback DAYS]   (actually runs the steps)
# This file mints no timer of any kind, no notification and no monitor of any kind. It never
# wakes itself up. G-21 (the standing alerting/monitor moratorium) is honoured by never
# acquiring one -- re-run cadence stays a human decision, every single time.
#
# READ-ONLY, ALWAYS: every composed instrument below is ADVISORY and never deletes, narrows or
# applies anything. This harness is not a licence to widen scope; it only re-asks the question.
#
# ACCESS ANALYZER IS NEVER CALLED (C-ANALYZER-PRICED-FIRST / G-25): only IAM Access Advisor
# (iam:GetServiceLastAccessedDetails), reached via comp-iam-usage, exactly as IAM-s-1 through
# IAM-s-3 already used it. No per-role Access Analyzer price has been read by anyone, and
# availability is not authorization.
#
# SCOPE CAVEAT CARRIED FORWARD FROM IAM-s-2, VERBATIM IN SUBSTANCE -- DO NOT DROP ON A RE-RUN:
#   "This is a ROLLUP OF IAM-s-1 AND NOTHING ELSE ... it is a posture number for the one role
#   IAM-s-1 exercised, not for the estate's role population." (POSTURE_NUMBER.md)
# The permission-grain step below (step 2) reproduces THAT one-role figure. It is never read as
# an estate-wide posture claim. The role-population step (step 4) is a DIFFERENT plane (which
# roles exist at all) and its count is never folded into step 2's numerator or denominator.
#
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR" && git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$REPO_ROOT" ]; then
  echo "ERROR: cannot resolve the repo root from $SCRIPT_DIR (git rev-parse --show-toplevel failed) -- refusing to guess a path" >&2
  exit 1
fi

# Explicit .tools/ paths, not bare names: a comp-tool invoked by bare name from a linked
# worktree censuses the MAIN checkout instead of this tree (measured this round, IAM-s-9's own
# BATTERY FINDINGS). An explicit path keeps the denominator honest about which tree it read.
COMP_IAM_USAGE="$REPO_ROOT/.tools/comp-iam-usage"
COMP_IAM="$REPO_ROOT/.tools/comp-iam"
COMP_FIND="$REPO_ROOT/.tools/comp-find"

DRY_RUN=0
ROLE="opal-data-refresh-lambda-role"   # the role IAM-s-1/IAM-s-2 exercised; override with --role
LOOKBACK=90                             # days; IAM-s-1/IAM-s-2's own lookback; override with --lookback
STEP_BUDGET=90                          # seconds per AWS-touching step, INTERNAL to this harness

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --role)
      ROLE="$2"
      shift 2
      ;;
    --lookback)
      LOOKBACK="$2"
      shift 2
      ;;
    *)
      echo "unrecognized argument: $1" >&2
      exit 2
      ;;
  esac
done

VINTAGE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

STEP1_DESC="STEP 1/4 -- role-grain coldness sample (identity plane, RoleLastUsed):  $COMP_IAM_USAGE role-cold --limit 10"
STEP2_DESC="STEP 2/4 -- permission-grain usage for ONE role (IAM-s-1/IAM-s-2's own grain, ONE-ROLE SCOPE -- never the estate):  $COMP_IAM_USAGE permission-cold --role $ROLE --lookback $LOOKBACK"
STEP3_DESC="STEP 3/4 -- Terraform-declared IAM cross-reference (parse-plane denominator, a DIFFERENT plane from steps 1/2):  $COMP_IAM stats"
STEP4_DESC="STEP 4/4 -- live role-population plane (DECLARED vs LIVE-no-DECLARED; yet another plane -- never folded into step 2's numerator):  $COMP_FIND '.' --corpus aws IAM_ROLE --all --budget $STEP_BUDGET"

echo "=== NFRA_IAMROLES202609 re-run harness -- invoked $VINTAGE (UTC) ==="
echo "ROLE=$ROLE LOOKBACK=${LOOKBACK}d DRY_RUN=$DRY_RUN"
echo
echo "Assessment steps, in the order this harness always runs them:"
echo "  $STEP1_DESC"
echo "  $STEP2_DESC"
echo "  $STEP3_DESC"
echo "  $STEP4_DESC"
echo

if [ "$DRY_RUN" -eq 1 ]; then
  echo "DRY RUN -- none of the four steps above executed. No AWS API was touched."
  echo "VINTAGE (dry-run call time, UTC): $VINTAGE"
  exit 0
fi

echo "--- running step 1/4 ---"
timeout "$STEP_BUDGET" "$COMP_IAM_USAGE" role-cold --limit 10
RC1=$?

echo
echo "--- running step 2/4 ---"
timeout "$STEP_BUDGET" "$COMP_IAM_USAGE" permission-cold --role "$ROLE" --lookback "$LOOKBACK"
RC2=$?

echo
echo "--- running step 3/4 ---"
timeout "$STEP_BUDGET" "$COMP_IAM" stats
RC3=$?

echo
echo "--- running step 4/4 ---"
timeout "$STEP_BUDGET" "$COMP_FIND" '.' --corpus aws IAM_ROLE --all --budget "$STEP_BUDGET"
RC4=$?

echo
echo "=== COMPARABILITY FOOTER -- read this beside any other run's footer, never the raw numbers alone ==="
echo "VINTAGE (this run, UTC): $VINTAGE"
echo "SCOPE: step 2's DENOMINATOR/numerator above is a PERMISSION-GRAIN figure for ONE role"
echo "  ($ROLE) only -- exactly IAM-s-2's scope, never an estate-wide posture claim."
echo "  Step 4's DECLARED / LIVE-no-DECLARED counts are a SEPARATE plane (which roles exist at"
echo "  all). IAM-s-6 independently measured at least one member of that LIVE-no-DECLARED band"
echo "  (seeking-alpha-scraper-role) as a comp-find classifier false positive -- print step 4's"
echo "  count as comp-find's own reported figure, named as such, not as a settled undeclared-role"
echo "  count. Put this run's step-2 DENOMINATOR beside a prior run's step-2 DENOMINATOR to"
echo "  compare posture; put step-4's beside step-4's to compare role-population drift. The two"
echo "  planes are never combined into one number."
echo
echo "Step exit codes: role-cold=$RC1 permission-cold=$RC2 comp-iam-stats=$RC3 comp-find-aws=$RC4"

STATUS=0
for rc in "$RC1" "$RC2" "$RC3" "$RC4"; do
  if [ "$rc" -ne 0 ]; then
    STATUS=1
  fi
done
exit $STATUS
