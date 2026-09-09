#!/usr/bin/env bash
# E3-AC5 -- the commit gate on every .py this order touches.
#
# The order names one tracked edit (infra/aws/globgrph/kuzu_load.py). The other
# files are this order's own deliverable instruments and control specimens,
# which are committed in the same act and therefore pass the same gate: a gate
# run on a subset of what is committed answers a narrower question than the
# commit asks.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3

FILES="infra/aws/globgrph/kuzu_load.py
$D/_readers_ast.py
$D/_dispositions_parse.py
$D/_manifest_claims.py
$D/apply_manifest_claims.py
$D/plant_e3/planted_reader.py
$D/plant_e3/planted_docstring_only.py"

echo "=== E3-AC5 commit_gate_all.sh -- run at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse --short HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
n=0
for f in $FILES; do n=$((n + 1)); echo "  $n. $f"; done
echo "DENOMINATOR: $n .py file(s) -- the ONE tracked edit plus every .py this"
echo "order adds under its deliverables folder."
echo
# shellcheck disable=SC2086
bash .tools/commit-gate.sh $FILES
rc=$?
echo "COMMIT_GATE_RC=$rc"
exit $rc
