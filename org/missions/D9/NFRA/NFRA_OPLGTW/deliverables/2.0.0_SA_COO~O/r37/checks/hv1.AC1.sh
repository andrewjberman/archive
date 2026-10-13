#!/usr/bin/env bash
# OPLGTW OG-hv-1 AC1 (round-37 R4, FWD-21): the gateway's harvest_list / harvest_read tools.
#  - the five named tests in tests/test_og_hv1.py pass (ac05, PRD v2.8: the research-only arm);
#  - app/harvest_read.py SERVED_PREFIXES equals, as a set, the 24 prefixes of list v4 @7e0da2dfee (the "v4 -- CURRENT"
#    row "the 24 top-level prefixes"), parsed HERE independently of the worker's test;
#  - the family, guard and entitlement-admin suites add no failing id beyond the baseline.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_hv1.py test_oghv1_ac01 test_oghv1_ac02 test_oghv1_ac03 test_oghv1_ac04 test_oghv1_ac05; r0=$?
cmp=$(python - <<'EOF'
import ast, re, subprocess, sys
src = subprocess.run(["git", "show", "7e0da2dfee:org/tier1_exec/1.0.0_SA_CTO/deliverables/SERVABLE_PREFIXES_OPAL_DATA_HARVEST_20261013.md"],
                     capture_output=True).stdout.decode("utf-8")
row = [l for l in src.split("\n") if l.startswith("| the 24 top-level prefixes")]
want = set(re.findall(r"`([a-z0-9-]+/)`", row[0])) if row else set()
try:
    tree = ast.parse(open("infra/aws/ec2/opal-gateway/app/harvest_read.py", encoding="utf-8").read())
    got = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "SERVED_PREFIXES" for t in n.targets):
            got = set(ast.literal_eval(n.value))
except Exception:
    got = set()
print("SERVED_PREFIXES equals list v4: %d of %d, extra %d" % (len(want & got), len(want), len(got - want)))
print("OK" if len(want) == 24 and want == got else "NO")
EOF
)
cmp=$(printf '%s' "$cmp" | tr -d '\r'); printf '%s\n' "$cmp" | head -1; pok=$(printf '%s\n' "$cmp" | tail -1)
out=$(cd "$GW" && timeout 110 python -m pytest tests/test_data_entitlement_family.py tests/test_data_entitlement_guard.py tests/test_entitlement_admin.py -rA -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
new=$(printf '%s\n' "$out" | grep -E '^FAILED ' | sed -E 's/^FAILED ([^ ]+).*/\1/' | tr '\\' '/' | while read -r id; do grep -qxF "$id" "$GW/tests/baseline/failing_ids_full.txt" || echo "$id"; done | grep -c .)
echo "family+guard+admin suites: failing ids not in the baseline: $new (want 0)"
restore_audit
[ "$r0" = 0 ] && [ "$pok" = OK ] && [ "$new" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
