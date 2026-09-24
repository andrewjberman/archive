#!/usr/bin/env bash
# OA-w-3 AC3 (the workflow): opal_ai/.github/workflows/ci.yml at the nested HEAD parses as YAML, triggers on push, and
# has a step whose run line invokes opal/checks/run_checks.sh (the same file AC1 and AC2 exercised).
. "$(dirname "$0")/_root.sh"
y=$(git -C opal_ai show HEAD:.github/workflows/ci.yml 2>/dev/null)
[ -n "$y" ] || { echo "opal_ai HEAD:.github/workflows/ci.yml absent"; echo "RESULT: FAIL"; exit 1; }
r=$(printf '%s' "$y" | python -c "
import sys, yaml
d = yaml.safe_load(sys.stdin.read())
on = d.get('on', d.get(True))
push = 'push' in (on if isinstance(on, (dict, list)) else [on])
runs = [s.get('run', '') for j in (d.get('jobs') or {}).values() for s in (j.get('steps') or [])]
print('push=%s steps_invoking_run_checks=%d' % (push, sum(1 for x in runs if 'opal/checks/run_checks.sh' in (x or ''))))" 2>&1 | tail -1)
echo "$r"
if printf '%s' "$r" | grep -Eq '^push=True steps_invoking_run_checks=[1-9]'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
