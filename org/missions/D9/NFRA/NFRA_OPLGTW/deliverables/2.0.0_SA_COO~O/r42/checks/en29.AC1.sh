#!/usr/bin/env bash
# OPLGTW OG-en-29 AC1 (round 42): the window page size PAGE_PARTITIONS in app/client_adapter_bd49f.py equals the size the host sweep chose (W/PAGE_SWEEP.json chosen_partitions, graded by ev6.AC1), and the new named test passes.
# Overrides (dry-run controls only): EN29_SWEEP_OVERRIDE, EN29_ADAPTER_OVERRIDE (skips the named test, which needs the real tree).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
SW="${EN29_SWEEP_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/PAGE_SWEEP.json}"
AD="${EN29_ADAPTER_OVERRIDE:-$GW/app/client_adapter_bd49f.py}"
[ -f "$SW" ] && [ -f "$AD" ] || { echo "PAGE_SWEEP.json or the adapter absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python -I - "$(native "$SW")" "$(native "$AD")" <<'PYEOF'
import ast, json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); b = d.get("body", d)
chosen = b.get("chosen_partitions")
t = ast.parse(open(sys.argv[2], encoding="utf-8").read())
vals = [n.value.value for n in t.body if isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id == "PAGE_PARTITIONS" for x in n.targets) and isinstance(n.value, ast.Constant)]
cur = vals[0] if len(vals) == 1 else None
print("PAGE_PARTITIONS assigned %d time(s) as a literal; value %s; the sweep chose %s" % (len(vals), cur, chosen))
print("OK" if (len(vals) == 1 and isinstance(chosen, int) and cur == chosen and chosen in (30, 60, 120)) else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
named=skipped
if [ -z "$EN29_ADAPTER_OVERRIDE" ]; then
  nm=$(bash "$(dirname "$0")/../../r38/checks/_named.sh" tests/test_og_en29.py test_ogen29_ac01 test_ogen29_ac02 2>&1 | tr -d '\r'); printf '%s\n' "$nm" | head -1
  printf '%s\n' "$nm" | tail -1 | grep -q "RESULT: PASS" && named=pass || named=fail
fi
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { [ "$named" = pass ] || [ "$named" = skipped ]; } && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
