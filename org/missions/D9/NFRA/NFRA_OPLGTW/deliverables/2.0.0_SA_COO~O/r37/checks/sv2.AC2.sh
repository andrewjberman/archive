#!/usr/bin/env bash
# OPLGTW OG-sv-2 AC2 (round-37, FWD-22, CTO ruling @131991960e): W/SV2_ROW.json decides the cma_assumptions row, its tool is defined in app/portal_json_served.py,
# and the worker's probe (RE-RUN here) read the real bucket and refused a non-Opal principal with zero reads.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~113"
MOD="infra/aws/ec2/opal-gateway/app/portal_json_served.py"
[ -f "$W/SV2_ROW.json" ] && [ -f "$MOD" ] || { echo "SV2_ROW.json or the module absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$W/SV2_ROW.json")" "$(native "$MOD")" <<'PYEOF'
import json, re, sys
row = json.load(open(sys.argv[1], encoding="utf-8")).get("row", {})
src = open(sys.argv[2], encoding="utf-8").read()
ent_ok = row.get("entity") == "opal_data_portal_v2_served_cma_assumptions"
tool = row.get("tool")
exist = 1 if tool == "portal_get_cma_assumptions" and re.search(r"def\s+%s\s*\(" % re.escape(tool), src) else 0
edition = isinstance(row.get("edition"), str) and re.search(r"20\d\d", row["edition"]) is not None
print("row: entity ok %s; class %s; tool defined %d of 1; edition read from the object %s" % (ent_ok, row.get("class"), exist, edition))
print("OK" if ent_ok and row.get("class") == "BUILT" and exist == 1 and edition else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
P="$W/probe_sv2.py"; pn=0
if [ -f "$P" ]; then out=$(timeout 115 python "$P" 2>&1 | tr -d '\r'); printf '%s\n' "$out" | grep -E "^probe sv2:" | tail -n 2; pn=$(printf '%s\n' "$out" | grep -cE "^probe sv2: portal_get_cma_assumptions answered True as_of [0-9]{4} non_opal_refused True reads_on_refusal 0"); fi
echo "cma tool probed $pn of 1 (the worker's probe line)"
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && [ "$pn" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
