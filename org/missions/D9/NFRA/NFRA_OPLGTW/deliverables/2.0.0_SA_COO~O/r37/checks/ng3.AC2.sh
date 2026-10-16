#!/usr/bin/env bash
# OPLGTW OG-ng-3 AC2 (round-37, row Z-S161): the gateway tests of the two touched modules still pass (portal_served via test_og_gp1, etfs_silver via test_og_gf1), and the bloomberg_profile
# row is in name_rulings.json (one none_owed row, type INSTANCE_PROFILE, evidence naming etfs_silver.py:<line>) while the module no longer types the scope label "mdpf" in portal_served.py.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd "$GW" && timeout 115 python -m pytest tests/test_og_gp1.py tests/test_og_gf1.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
passed=$(printf '%s\n' "$out" | grep -oE '[0-9]+ passed' | head -1 | grep -oE '[0-9]+'); failed=$(printf '%s\n' "$out" | grep -oE '[0-9]+ failed' | head -1 | grep -oE '[0-9]+')
res=$(python - <<'PYEOF'
import json, re
d = json.load(open("infra/logic/registry/name_rulings.json", encoding="utf-8"))
rows = [r for r in d.get("name_rulings", []) if isinstance(r, dict)]
b = [r for r in rows if r.get("name") == "bloomberg_profile" and r.get("type") == "INSTANCE_PROFILE" and r.get("none_owed") and not r.get("canonical") and re.search(r"etfs_silver\.py:\d+", str(r.get("evidence", "")))]
keys = [(r.get("name"), r.get("type")) for r in rows]
src = open("infra/aws/ec2/opal-gateway/app/portal_served.py", encoding="utf-8").read()
typed = len(re.findall(r'Scope\(\s*"mdpf"', src))
print("name_rulings: bloomberg_profile rows %d of 1; unique per (name, type) %s; portal_served.py typed Scope(\"mdpf\") sites %d (want 0)" % (len(b), len(keys) == len(set(keys)), typed))
print("OK" if len(b) == 1 and len(keys) == len(set(keys)) and typed == 0 else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
echo "gp1 and gf1 suites: pytest rc=$rc; passed ${passed:-0}; failed ${failed:-0} (want 0)"
restore_audit
[ "$rc" = 0 ] && [ "${failed:-0}" = 0 ] && [ "${passed:-0}" -ge 8 ] && [ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
