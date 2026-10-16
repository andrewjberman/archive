#!/usr/bin/env bash
# OPLGTW OG-sv-1 AC2 (round-37, FWD-22, PRD v3.13): W/SV1_ROWS.json covers EXACTLY the seven json-served catalog rows, the stale one is RULED_OUT with its measurement,
# every BUILT row names a tool function defined in app/portal_json_served.py, and the worker's probe (RE-RUN here) read the real bucket for each BUILT tool.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~113"
MOD="infra/aws/ec2/opal-gateway/app/portal_json_served.py"
[ -f "$W/SV1_ROWS.json" ] && [ -f "$MOD" ] || { echo "SV1_ROWS.json or the module absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$W/SV1_ROWS.json")" "$(native "$MOD")" <<'PYEOF'
import json, re, sys
rows = json.load(open(sys.argv[1], encoding="utf-8")).get("rows", {})
src = open(sys.argv[2], encoding="utf-8").read()
want = sorted("opal_data_portal_v2_served_" + n for n in ("correlation_data", "etf_returns", "factor_tilts", "model_portfolio_timeseries", "model_portfolios_views", "peer_performance", "trending_latest"))
have = sorted(rows)
built = sorted(v.get("tool") for v in rows.values() if v.get("class") == "BUILT" and v.get("tool"))
ruled = [k for k, v in rows.items() if v.get("class") == "RULED_OUT"]
reasoned = all(isinstance(rows[k].get("reason"), str) and re.search(r"\d", rows[k]["reason"]) for k in ruled)
exist = sum(1 for t in built if re.search(r"def\s+%s\s*\(" % re.escape(t), src))
views_out = rows.get("opal_data_portal_v2_served_model_portfolios_views", {}).get("class") == "RULED_OUT"
print("rows: wanted %d of %d, built %d, ruled out %d; set equal %s; views ruled out %s; ruled-out reasons carry a measurement %s; built tools defined %d of %d" % (len(want), len(have), len(built), len(ruled), want == have, views_out, reasoned, exist, len(built)))
print("OK" if want == have and views_out and reasoned and exist == len(built) and len(built) + len(ruled) == 7 and len(built) >= 5 else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
P="$W/probe_sv1.py"; pn=0
if [ -f "$P" ]; then out=$(timeout 115 python "$P" 2>&1 | tr -d '\r'); printf '%s\n' "$out" | grep -E "^probe sv:" | tail -n 3; pn=$(printf '%s\n' "$out" | grep -cE "^probe sv: .* answered True as_of [0-9]{4}-[0-9]{2}-[0-9]{2}"); fi
echo "built tools probed $pn (the worker's probe lines)"
nb=$(printf '%s' "$res" | sed -n 's/.*defined [0-9]* of \([0-9]*\)$/\1/p' | head -1)
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && [ "$pn" -ge "${nb:-99}" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
