#!/usr/bin/env bash
# MX-g-1 AC2 (independent planted arms, against the registry AT HEAD): one unified diff ADDS the six hyphenated
# research-table prefixes as `prefix:` lines of the gateway catalog, plus one marker file, graded with --enforce twice:
#   (+) the marker sits under NFRA_MCPINDEX's project home (the rows' reader)    -> exit 0, 0 REFUSE lines;
#   (-) the marker sits under NFRA_OPLGTW's project home (another real project)  -> exit 1, >= 6 REFUSE lines.
# The committing project is DERIVED from the staged paths' project home, never a free field (laptop CTO condition 1,
# CTO~Z msg 33943). The message file is the same neutral text in both arms, so it cannot be what decides.
# AMENDED A5 (2.0.0_SA_COO~MI, ~03:2xZ): once the catalog commit lands, the six literals EXIST at HEAD and the gate
# rightly grades a re-add as WARN (existing), so the negative arm means something only while they are NEW. With
# G1_AT=<commit> (the gate-branch commit, BEFORE the catalog), both arms run in a SPARSE detached worktree at that commit:
# the branch is present there and the literals are not yet in the catalog.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
T="${TMPDIR:-/tmp}/mx_g1ac2_$$"; mkdir -p "$T"
F=infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml
{ echo "diff --git a/$F b/$F"; echo "--- a/$F"; echo "+++ b/$F"; echo "@@ -1,0 +1,6 @@"
  for t in research-backlog research-continuation research-dossier research-fund-form research-model-typecast research-sector-template; do
    echo "+    prefix: amgt/harvest/gold/$t/"; done; } > "$T/cat.diff"
home() { printf 'diff --git a/%s b/%s\nnew file mode 100644\n--- /dev/null\n+++ b/%s\n@@ -0,0 +1,1 @@\n+g1 planted marker\n' "$1" "$1" "$1"; }
{ cat "$T/cat.diff"; home "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~34/g1_plant.md"; } > "$T/own.diff"
{ cat "$T/cat.diff"; home "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/g1_plant.md"; } > "$T/other.diff"
printf 'cell(g1 planted arm): six harvest rows\n' > "$T/msg"
ROOT="$(pwd)"; WT=""
if [ -n "${G1_AT:-}" ]; then
  WT="${TMPDIR:-/tmp}/mx_g1_wt_$$"
  git worktree add --detach --no-checkout "$WT" "$G1_AT" >/dev/null 2>&1 || { echo "worktree at $G1_AT failed"; echo "RESULT: FAIL"; exit 1; }
  git -C "$WT" sparse-checkout set --no-cone .tools lib infra/logic org/standards "/org/missions/*.yaml" "/org/missions/*.json" "/org/ref/*.json" org/missions/D9/NFRA/NFRA_MCPINDEX/project.json org/missions/D9/NFRA/NFRA_OPLGTW/project.json >/dev/null 2>&1
  git -C "$WT" checkout -q "$G1_AT" 2>&1 | tail -1
  cd "$WT"; echo "graded at $G1_AT in a sparse worktree"
fi
o1=$(timeout 120 python .tools/naming-gate.py --enforce --diff "$(native "$T/own.diff")" --message-file "$(native "$T/msg")" 2>&1 | tr -d '\r'); r1=$?
o2=$(timeout 120 python .tools/naming-gate.py --enforce --diff "$(native "$T/other.diff")" --message-file "$(native "$T/msg")" 2>&1 | tr -d '\r'); r2=$?
rm -rf "$T"
if [ -n "$WT" ]; then cd "$ROOT"; git worktree remove --force "$WT" >/dev/null 2>&1; fi
f1=$(printf '%s\n' "$o1" | grep -c 'NAMING REFUSE')
f2=$(printf '%s\n' "$o2" | grep -c 'NAMING REFUSE')
printf '%s\n' "$o1" | grep -E 'NAMING-GATE' | tail -1; printf '%s\n' "$o2" | grep -E 'NAMING-GATE' | tail -1
echo "own reader (NFRA_MCPINDEX home): rc=$r1 refuse-lines=$f1; other reader (NFRA_OPLGTW home): rc=$r2 refuse-lines=$f2"
if [ "$r1" = 0 ] && [ "$f1" = 0 ] && [ "$r2" = 1 ] && [ "$f2" -ge 6 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
