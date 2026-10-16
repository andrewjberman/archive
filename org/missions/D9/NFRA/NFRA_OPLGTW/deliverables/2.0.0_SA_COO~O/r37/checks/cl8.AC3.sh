#!/usr/bin/env bash
# OPLGTW OG-cl-8 AC3 (round-37, CTO ruling @d97ea3ae82 section 1): infra/logic/registry/name_rulings.json carries a none_owed row for each of the four Black Diamond upstream identifiers
# the naming gate refused (unique per (name, type), the evidence naming file:line), and the unread orion/4698 alias key is gone from client_core.py.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
res=$(python - <<'PYEOF'
import json, re
d = json.load(open("infra/logic/registry/name_rulings.json", encoding="utf-8"))
rows = d.get("name_rulings") or []
if isinstance(rows, dict):
    rows = [dict(v, name=v.get("name", k)) for k, v in rows.items()]
want = ("bd_account_id", "bd_account_number", "fact_bd_allocation", "market_value_profile")
keyset = [(r.get("name"), r.get("type")) for r in rows if isinstance(r, dict)]
unique = len(keyset) == len(set(keyset))
have = {}
for r in rows:
    if isinstance(r, dict) and r.get("name") in want and r.get("none_owed") and not r.get("canonical") and re.search(r"client_adapter_bd49f\.py:\d+", str(r.get("evidence", ""))):
        have[r["name"]] = r
src = open("infra/aws/ec2/opal-gateway/app/client_core.py", encoding="utf-8").read()
alias_gone = "orion/4698" not in src
print("name_rulings: rows for the 4 identifiers %d of 4 (none_owed, evidence file:line); unique per (name, type) %s; orion/4698 alias gone %s" % (len(have), unique, alias_gone))
print("OK" if len(have) == 4 and unique and alias_gone else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
