#!/usr/bin/env bash
# MP-pf-10 AC3 (a BOUND, passes at the base): the repair touches tests only. Between the branch point and HEAD, the only gateway files that differ are
# the two test files; no app/ file, no catalog, no Terraform, no manifest moved.
. "$(dirname "$0")/../../pc/checks/_root.sh"
base=$(git merge-base HEAD box/sitez 2>&1 | tr -d '\r')
git cat-file -e "${base}^{commit}" 2>/dev/null || { echo "no merge-base with box/sitez (read: $base)"; echo "RESULT: FAIL"; exit 1; }
changed=$(git diff --name-only "$base" HEAD -- infra/ 2>&1 | tr -d '\r')
n=$(printf '%s\n' "$changed" | grep -c .)
bad=$(printf '%s\n' "$changed" | grep -v -E '^infra/aws/ec2/opal-gateway/tests/test_admin_(gateway_breakdown|people)\.py$' | grep -c .)
echo "base=${base:0:12}; files under infra/ changed since: $n; outside the two test files: $bad"
if [ "$bad" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
