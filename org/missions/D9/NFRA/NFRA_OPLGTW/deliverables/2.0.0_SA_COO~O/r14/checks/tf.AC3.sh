#!/usr/bin/env bash
# OPLGTW OG-tf-1 AC3 (root hygiene): HEAD tracks no saved plan file and no stray org/ telemetry inside the opal-gateway
# terraform root.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
R="infra/aws/terraform/opal-gateway"
files=$(git ls-tree -r --name-only HEAD "$R")
plans=$(printf '%s\n' "$files" | grep -cE '(^|/)[^/]*tfplan[^/]*$')
stray=$(printf '%s\n' "$files" | grep -c "^$R/org/")
echo "tracked under $R: $(printf '%s\n' "$files" | grep -c .) files; saved plans $plans; stray org/ files $stray"
if [ "$plans" = 0 ] && [ "$stray" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
