#!/usr/bin/env bash
# OPLGTW OG-db-1 AC2 (round-34 E9, row NFRA_MCPINDEX-Z-S92/S99; CTO~Z msg 33316): the gateway deploy wrapper's preflight,
# exercised in a REAL sparse worktree at HEAD (cone: infra/aws/ec2 lib .tools org/modules/graph):
#  (1) `deploy-to-ec2.sh --preflight-only` in the clean sparse tree exits 0 and prints PREFLIGHT OK;
#  (2) the same call after one shipped file is dirtied exits non-zero, printing REFUSED and naming the dirty tree;
#  (3) a sparse tree WITHOUT org/modules/graph exits non-zero, printing REFUSED and naming the missing import closure
#      (the manifest auto-commit's comp_constants_cli), so a deploy that would land and then fail its manifest commit
#      stops before any write.
# No AWS call is made by --preflight-only; the temp worktrees are removed.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
R=$(pwd); T1="$R/../.og-db1-ac2-a.$$"; T2="$R/../.og-db1-ac2-b.$$"
cleanup() { git worktree remove --force "$T1" >/dev/null 2>&1; git worktree remove --force "$T2" >/dev/null 2>&1; }
trap cleanup EXIT
mk() { git worktree add --no-checkout --detach "$1" HEAD >/dev/null 2>&1 && git -C "$1" sparse-checkout set --cone $2 >/dev/null 2>&1 && git -C "$1" checkout -q >/dev/null 2>&1; }
D=infra/aws/ec2/opal-gateway/deploy-to-ec2.sh
mk "$T1" "infra/aws/ec2 lib .tools org/modules/graph" || { echo "could not build sparse tree"; echo "RESULT: FAIL"; exit 1; }
o1=$(cd "$T1" && timeout 60 bash "$D" --preflight-only 2>&1 | tr -d '\r'); r1=$?
echo "$o1" | grep -q "PREFLIGHT OK"; p1=$?
echo "# dirty" >> "$T1/infra/aws/ec2/opal-gateway/app/server.py"
o2=$(cd "$T1" && timeout 60 bash "$D" --preflight-only 2>&1 | tr -d '\r'); r2=$?
echo "$o2" | grep -qiE "REFUSED.*dirty|dirty.*REFUSED"; p2=$?
mk "$T2" "infra/aws/ec2 lib .tools" || { echo "could not build second sparse tree"; echo "RESULT: FAIL"; exit 1; }
o3=$(cd "$T2" && timeout 60 bash "$D" --preflight-only 2>&1 | tr -d '\r'); r3=$?
echo "$o3" | grep -qiE "REFUSED.*(closure|comp_constants_cli|org/modules/graph)"; p3=$?
echo "clean sparse tree: rc=$r1 PREFLIGHT OK=$([ $p1 = 0 ] && echo yes || echo no)"
echo "dirty sparse tree: rc=$r2 refused naming dirty=$([ $p2 = 0 ] && echo yes || echo no)"
echo "sparse tree without the import closure: rc=$r3 refused naming the closure=$([ $p3 = 0 ] && echo yes || echo no)"
[ "$r1" = 0 ] && [ "$p1" = 0 ] && [ "$r2" != 0 ] && [ "$p2" = 0 ] && [ "$r3" != 0 ] && [ "$p3" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
