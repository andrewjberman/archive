#!/usr/bin/env bash
# OA-f-14 AC3 (the bounds): against the commit this order was cut at, the gateway tree changed ONLY in the five files
# the order names, the tracked audit.jsonl is byte-identical, and the tracked allowlist overlay is byte-identical.
. "$(dirname "$0")/_root.sh"
BASE="${OA_F14_BASE:-821fca2410}"
G=infra/aws/ec2/opal-gateway
git cat-file -e "$BASE^{commit}" 2>&1 || { echo "base $BASE is not a commit here"; echo "RESULT: FAIL"; exit 1; }
allowed="$G/app/graph_scope_map.py $G/app/identity_scope.py $G/app/token_broker.py $G/app/server.py $G/tests/test_scoped_consent_r253.py"
changed=$(git diff --name-only "$BASE" HEAD -- "$G" | tr -d '\r')
total=$(printf '%s\n' "$changed" | grep -c .)
outside=0; names=""
for f in $changed; do case " $allowed " in *" $f "*) ;; *) outside=$((outside+1)); names="$names $f";; esac; done
newmap=$(printf '%s\n' "$changed" | grep -cx "$G/app/graph_scope_map.py")
audit=$(git diff --name-only "$BASE" HEAD -- "$G/audit.jsonl" | grep -c .)
overlay=$(git diff --name-only "$BASE" HEAD -- "$G/identity_tool_allowlist.txt" | grep -c .)
dirty=$(git status --porcelain -- "$G" | grep -c .)
echo "gateway files changed vs $BASE: $total; outside the order: $outside; scope map file changed: $newmap; audit.jsonl changed: $audit; allowlist overlay changed: $overlay; uncommitted gateway paths: $dirty"
[ -n "$names" ] && echo "outside:$names"
if [ "$total" -ge 1 ] && [ "$outside" = 0 ] && [ "$newmap" = 1 ] && [ "$audit" = 0 ] && [ "$overlay" = 0 ] && [ "$dirty" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
