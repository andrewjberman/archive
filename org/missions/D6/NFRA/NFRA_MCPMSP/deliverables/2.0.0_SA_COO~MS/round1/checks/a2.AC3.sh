#!/usr/bin/env bash
# MS-a-2 AC3 (the control, C11: no firm is live until G-FIRM): the live writer's LIVE_FIRMS is absent or empty, so
# register_tenant refuses every firm until Andrew's word sets it.
. "$(dirname "$0")/_root.sh"
nm=$(python -c "import sys;sys.path.insert(0,'.');import lib.opal_naming as n;print(n.name('mcportal', None, 'grant-writer', 'lambda'))" 2>&1 | tr -d '\r' | tail -1)
v=$(timeout 30 "$AWS" lambda get-function-configuration --function-name "$nm" --query "Environment.Variables.LIVE_FIRMS" --output text 2>&1 | tr -d '\r' | tail -1)
echo "function $nm: LIVE_FIRMS=${v:-<empty>}"
if [ -z "$v" ] || [ "$v" = None ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
