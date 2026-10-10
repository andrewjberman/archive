#!/usr/bin/env bash
# MX-f-1r AC1: infra/aws/terraform/bd-pipeline PLANS at the worktree HEAD -- init rc=0, plan -detailed-exitcode rc 0 or 2,
# 0 'Unsupported attribute' and 0 '^Error' lines (row NFRA_IAMROLES202609-Z-S29 read 4 of each). Read-only: plan, never apply.
# Run from the worktree root.
M=infra/aws/terraform/bd-pipeline
T="${TMPDIR:-/tmp}/f1r_ac1_$$"; mkdir -p "$T"
terraform -chdir="$M" init -input=false -no-color > "$T/init.txt" 2>&1; irc=$?
terraform -chdir="$M" plan -input=false -no-color -lock=false -detailed-exitcode > "$T/plan.txt" 2>&1; prc=$?
u=$(grep -c 'Unsupported attribute' "$T/plan.txt"); e=$(grep -c '^Error' "$T/plan.txt")
echo "init rc=$irc; plan rc=$prc; Unsupported attribute=$u; Error lines=$e; plan lines=$(wc -l < "$T/plan.txt")"
grep -E '^Plan:|^No changes' "$T/plan.txt"
[ "$irc" != 0 ] && tail -5 "$T/init.txt"
rm -rf "$T"
if [ "$irc" = 0 ] && { [ "$prc" = 0 ] || [ "$prc" = 2 ]; } && [ "$u" = 0 ] && [ "$e" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
