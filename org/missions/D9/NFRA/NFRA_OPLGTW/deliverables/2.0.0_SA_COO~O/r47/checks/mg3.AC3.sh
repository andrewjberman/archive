#!/usr/bin/env bash
# OPLGTW OG-mg-3 AC3 (round 47): the contract's capacity block names the real 8 GiB host in BOTH copies (byte-equal), the rest of the block is unchanged,
# and the worker's new test file tests/test_og_mg3.py passes beside the existing neighbours (the unit-limit test, the contract byte-equality test, the denial and tier gates).
. "$(dirname "$0")/_gwtests.sh"
a="$GW/deploy/NFRA_OPLGTW_CONTRACT.json"; b="org/standards/NFRA_OPLGTW_CONTRACT.json"
eq=no; cmp -s "$a" "$b" && eq=yes
cap=$(python3 -I - "$(native "$a")" <<'PY'
import json, sys
c = json.load(open(sys.argv[1], encoding="utf-8"))["capacity"]
want = {"target_instance_type": "t4g.large", "target_architecture": "arm64", "admission_existing_peak_rss_multiplier": 1.25,
        "admission_os_reserve_bytes": 134217728, "existing_workflow_p95_regression_max_fraction": 0.2, "activation_requires_benchmark": True}
rest = all(c.get(k) == v for k, v in want.items())
print("target_memory_mib %r (want 8192); the other capacity keys unchanged %s" % (c.get("target_memory_mib"), "yes" if rest else "NO"))
print("OK" if c.get("target_memory_mib") == 8192 and rest else "NO")
PY
)
cap=$(printf '%s' "$cap" | tr -d '\r')
echo "contract copies byte-equal: $eq"
printf '%s\n' "$cap" | sed '$d'
gwtests tests/test_og_mg3.py tests/test_og_un1.py tests/test_grant_calendar_months.py tests/test_og_en21.py tests/test_data_entitlement_guard.py tests/test_min_tier_gate.py tests/test_identity_scope.py > /tmp/mg3_ac3_$$.out 2>&1; grc=$?
grep -v '^RESULT' /tmp/mg3_ac3_$$.out; rm -f /tmp/mg3_ac3_$$.out
# the denial-envelope test goes through call_tool (the hooked path); it is order-dependent after test_og_en21 and test_data_entitlement_guard, so it runs ALONE
den=$(cd "$GW" && timeout 100 python3 -I -m pytest tests/test_schwab_denial_envelope.py -q --color=no -p no:cacheprovider 2>&1 | tail -1 | tr -d '\r')
echo "denial envelope (alone): $den"
dok=no; printf '%s' "$den" | grep -qE '^[1-9][0-9]* passed' && ! printf '%s' "$den" | grep -q failed && dok=yes
restore_audit
if [ "$dok" = yes ] && [ "$eq" = yes ] && [ "$(printf '%s\n' "$cap" | tail -1)" = OK ] && [ "$grc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
