#!/usr/bin/env bash
# OPLGTW OG-cl-10 AC1 (round-37, CTO msg 34732): the `etfs` row of infra/logic/registry/name_rulings.json names the ruling it rests on in its evidence field, the CTO's ruling file path;
# the row is otherwise unchanged (still one row, type 'hand-kept carrier', none_owed, the portal_json_served.py evidence), and the four Black Diamond rows are untouched.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
res=$(python - <<'PYEOF'
import json, re
d = json.load(open("infra/logic/registry/name_rulings.json", encoding="utf-8"))
rows = [r for r in d.get("name_rulings", []) if isinstance(r, dict)]
RUL = "org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_OPLGTW_CL7_NAMING_GATE_AND_MCPINDEX_AI_CLASSIFIED_20261016_Z.md"
e = [r for r in rows if r.get("name") == "etfs" and r.get("type") == "hand-kept carrier"]
one = len(e) == 1
cites = one and RUL in str(e[0].get("evidence", ""))
kept = one and bool(e[0].get("none_owed")) and not e[0].get("canonical") and re.search(r"portal_json_served\.py:\d+", str(e[0].get("evidence", ""))) is not None
bd = sum(1 for n in ("bd_account_id", "bd_account_number", "fact_bd_allocation", "market_value_profile") if any(r.get("name") == n and r.get("none_owed") for r in rows))
keys = [(r.get("name"), r.get("type")) for r in rows]
print("name_rulings: etfs row 1 of 1 %s; evidence cites the CTO ruling file %s; row otherwise kept %s; black diamond rows kept %d of 4; unique per (name, type) %s" % (one, cites, kept, bd, len(keys) == len(set(keys))))
print("OK" if one and cites and kept and bd == 4 and len(keys) == len(set(keys)) else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
