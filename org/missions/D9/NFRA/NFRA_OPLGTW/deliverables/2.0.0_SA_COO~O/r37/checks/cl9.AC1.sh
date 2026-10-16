#!/usr/bin/env bash
# OPLGTW OG-cl-9 AC1 (round-37, CTO msg 34709): infra/logic/registry/name_rulings.json carries ONE none_owed row for `etfs` (type 'hand-kept carrier', evidence naming portal_json_served.py:<line>),
# unique per (name, type), and the file is still valid JSON with the 4 Black Diamond rows of OG-cl-8 untouched.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
res=$(python - <<'PYEOF'
import json, re
d = json.load(open("infra/logic/registry/name_rulings.json", encoding="utf-8"))
rows = [r for r in d.get("name_rulings", []) if isinstance(r, dict)]
keys = [(r.get("name"), r.get("type")) for r in rows]
unique = len(keys) == len(set(keys))
e = [r for r in rows if r.get("name") == "etfs" and r.get("type") == "hand-kept carrier" and r.get("none_owed") and not r.get("canonical") and re.search(r"portal_json_served\.py:\d+", str(r.get("evidence", "")))]
bd = sum(1 for n in ("bd_account_id", "bd_account_number", "fact_bd_allocation", "market_value_profile") if any(r.get("name") == n for r in rows))
print("name_rulings: etfs rows %d of 1; unique per (name, type) %s; black diamond rows kept %d of 4" % (len(e), unique, bd))
print("OK" if len(e) == 1 and unique and bd == 4 else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
