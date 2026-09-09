#!/bin/bash
# E1-AC6 -- the commit gate over EVERY Python file THIS task order touches, plus the thin-client
# battery whose refusal of `--mode` is the property the retired routes now point away from.
#
# THE NAME CARRIES THE ORDER (pass 2, row W2-S34). This probe was `commit_gate_all.sh` at pass 1 --
# a name TO-CG-D-7's probe already held in this same slot folder, so writing it overwrote D-7's
# evidence. The issuer's amendment renamed E1-AC6's invocation to `e1_commit_gate_all.sh` and every
# probe this order writes now carries the `e1_` prefix; D-7's `commit_gate_all.sh` was restored from
# de466829e0 by `git show` and verified byte-identical (sha256 54df937de6cf2fad..., 3251 bytes,
# printed in the record) so D-7's criterion re-runs as written.
#
# THE LIST IS THE ORDER'S OWN EDIT SET, WRITTEN DOWN, not `git status`. A gate fed by the change set
# can only certify what changed; this order's claim is about a NAMED population. If the two ever
# diverge, THAT is the finding.
#
# .tools/tool_index.py IS IN THE LIST NOW, AND IT WAS NOT AT PASS 1. It is a GENERATED artifact and
# was never hand-edited; at pass 1 its compiler REFUSED (PopulationDivergence) so the file could not
# be touched at all and listing it would have gated bytes this order did not produce. Pass 2 fixed
# the compiler's input -- `.tools/gen_tool_classification.py` now takes its POPULATION from
# org/modules/graph/comp-coverage-map.yaml, the sole authority, instead of from the CVO's profile --
# and REGENERATED it, so this order now produces those bytes and gates them. Same for
# org/modules/graph/TOOL_MASTER.yaml, which is not Python and is therefore not in this list.
#
# NOT IN THE LIST, AND WHY -- an unstated omission is the defect this note exists to prevent:
#   .tools/comp-describe, .tools/comp-cluster -- bash shims, not Python. commit-gate.sh dispatches
#     by SUFFIX and would refuse them; they are syntax-checked with `bash -n` below, each with its
#     own printed verdict, rather than handed to a gate that cannot see them.
#   .tools/comp-which -- a Python file with NO .py suffix (a shebang tool on PATH). Same suffix
#     problem, so it is byte-compiled explicitly below. An unchecked file that produces rc=0 is
#     exactly what this note prevents.
#   The four YAML carriers and the manifest -- not Python. Their instruments are E1-AC4
#     (comp-manifest-check completeness) and E1-AC5 (comp_coverage_view --verify).
#
# Exit: 0 = gate clean on every Python file AND the thin-client battery PASS; 1 = either failed;
#       2 = BLOCKED (a named file is absent -- a gate cannot certify a file it never read).
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2

FILES="
org/modules/graph/comp_aws_cli.py
org/modules/graph/debtscan/comp_similar.py
org/modules/graph/debtscan/summary_corpus.py
.tools/gen_tool_classification.py
.tools/tool_index.py
"

SUFFIXLESS_PY=".tools/comp-which"
SHELL_SHIMS=".tools/comp-describe .tools/comp-cluster"

N=0
for f in $FILES $SUFFIXLESS_PY $SHELL_SHIMS; do
  if [ ! -f "$f" ]; then
    echo "BLOCKED: $f is absent -- the gate cannot certify a file it never read"
    exit 2
  fi
  N=$((N + 1))
done
echo "e1_commit_gate_all.sh: population $N file(s) -- 5 .py to commit-gate.sh, 1 suffix-less python, 2 bash shims"

# shellcheck disable=SC2086
bash .tools/commit-gate.sh $FILES
GATE_RC=$?

echo "e1_commit_gate_all.sh: suffix-less python checked separately: $SUFFIXLESS_PY"
python -c "import py_compile; py_compile.compile('.tools/comp-which', doraise=True); print('  .tools/comp-which compiles')"
CW_RC=$?

SH_RC=0
for f in $SHELL_SHIMS; do
  if bash -n "$f"; then
    echo "  $f parses (bash -n)"
  else
    echo "  $f FAILED bash -n"
    SH_RC=1
  fi
done

echo ""
echo "e1_commit_gate_all.sh: thin-client battery -- the client's REFUSAL of --mode is the property"
echo "  the retired routes now point away from, so it is quoted here rather than asserted:"
timeout 300 python .tools/tests/test_cg6_thin_client_battery.py 2>&1 | sed 's/^/  | /'
BATTERY_RC=${PIPESTATUS[0]}
echo "  thin-client battery rc=$BATTERY_RC"

echo ""
echo "e1_commit_gate_all.sh: comp-similar self-test -- the repointed C3c leg, whose three arms are"
echo "  the served-header capture this order moved (W2-S32):"
timeout 300 python org/modules/graph/debtscan/comp_similar.py --self-test 2>&1 | sed 's/^/  | /'
SIM_RC=${PIPESTATUS[0]}
echo "  comp-similar self-test rc=$SIM_RC"

if [ "$GATE_RC" -eq 0 ] && [ "$CW_RC" -eq 0 ] && [ "$SH_RC" -eq 0 ] && [ "$BATTERY_RC" -eq 0 ] && [ "$SIM_RC" -eq 0 ]; then
  echo "pre-commit gate clean ($N of $N file(s): commit-gate rc=0, comp-which compile rc=0, bash -n rc=0; thin-client battery PASS; comp-similar self-test PASS)"
  exit 0
fi
echo "pre-commit gate NOT clean: commit-gate.sh rc=$GATE_RC, comp-which rc=$CW_RC, bash -n rc=$SH_RC, battery rc=$BATTERY_RC, comp-similar rc=$SIM_RC"
exit 1
