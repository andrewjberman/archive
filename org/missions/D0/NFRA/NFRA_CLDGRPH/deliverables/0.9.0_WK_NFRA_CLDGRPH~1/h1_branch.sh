#!/usr/bin/env bash
# NFRA_CLDGRPH TO-CG-H-1 / CG-s-36 -- H1-AC3: THE BRANCH, STATED AND PROVEN.
#
# BOTH BRANCHES ARE PASSES. What cannot pass is a run that does not say which branch it took.
# This script states the branch on its first evidence line and then prints every measurement
# that forced it, re-measured in THIS run rather than quoted from another script's capture.
#
# COVERAGE: the whole repository corpus. GRAIN: one occurrence, rolled up to one file.
# ENVIRONMENT: the decision rule is TO-CG-H-1's own. TREE: printed by the engine below.
# READ ONLY -- no producer run, no AWS call, no edit to any surface.
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../../../../../.." && pwd)"
cd "$ROOT" || { echo "BLOCKED: cannot reach repository root from $HERE"; exit 2; }

echo "H1-AC3 -- CG-s-36 THE STORED_IN RETIREMENT DECISION"
echo "  engine: h1_branch_evidence.py (same classifier as h1_reader_census.py, re-run here)"
echo "  cwd:    $ROOT"
echo ""

python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/h1_branch_evidence.py
rc=$?
echo ""
echo "ENGINE_RC=$rc"
exit $rc
