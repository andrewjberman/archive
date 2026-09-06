#!/bin/bash
# D7-AC7 -- the commit gate over EVERY .py this task order touches.
#
# THE LIST IS THE CENSUS'S REPOINTED ROWS PLUS THE REPOINTED TESTS, not `git status`: a gate
# fed by the change set can only certify what was changed, while this order's claim is about a
# named population. The two agree today; if they ever diverge, the divergence is the finding.
#
# `.tools/comp-find` is a Python file with no `.py` suffix (a shebang tool on PATH). commit-gate.sh
# dispatches by SUFFIX, so it would REFUSE the name (rc=2) rather than check it. It is therefore
# compiled explicitly below, with its own printed verdict, instead of being handed to a gate that
# cannot see it -- an unchecked file that produces rc=0 is the failure this note prevents.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2

FILES="
infra/aws/globgrph/projection_client.py
infra/aws/globgrph/comp_detect.py
infra/aws/globgrph/comp_debt.py
infra/aws/globgrph/comp_cluster_cli.py
infra/aws/globgrph/canon_motif_scorer.py
infra/aws/globgrph/debtscan_canon_scorer.py
org/modules/graph/cli.py
org/modules/graph/comp_blast_universe.py
org/modules/graph/comp_iam_live.py
org/modules/graph/comp_marker_read.py
.tools/tool_index.py
.tools/tests/test_comp_find_battery.py
.tools/tests/test_g2_disclosure_battery.py
"

N=0
for f in $FILES; do
  if [ ! -f "$f" ]; then
    echo "BLOCKED: $f is absent -- the gate cannot certify a file it never read"
    exit 2
  fi
  N=$((N + 1))
done
echo "commit_gate_all.sh: dispatching $N .py file(s) to .tools/commit-gate.sh"

# shellcheck disable=SC2086
bash .tools/commit-gate.sh $FILES
GATE_RC=$?

echo "commit_gate_all.sh: suffix-less tool checked separately: .tools/comp-find"
python -c "import py_compile,sys; py_compile.compile('.tools/comp-find', doraise=True); print('  .tools/comp-find compiles')"
CF_RC=$?

if [ "$GATE_RC" -eq 0 ] && [ "$CF_RC" -eq 0 ]; then
  echo "pre-commit gate clean ($N .py file(s) + .tools/comp-find; denominator 14 of 14)"
  exit 0
fi
echo "pre-commit gate NOT clean: commit-gate.sh rc=$GATE_RC, comp-find compile rc=$CF_RC"
exit 1
