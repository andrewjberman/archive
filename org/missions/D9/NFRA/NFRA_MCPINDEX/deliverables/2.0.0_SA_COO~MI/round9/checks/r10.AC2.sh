#!/usr/bin/env bash
# MX-r-10 AC2 (FWD-19 live, the SERVED host): /health 200; IN-PROCESS on the host under its own venv and .env, each
# reader whose census reads SERVED returns >= 1 row, every row's keys equal to the fixture's, scope as asked, as_of
# with claim measured, completeness stated; a GAP reader is skipped by branch. And the deployed discover routes
# "trade reconciliation" -> E-30, "billing" -> E-31 and (round-8 analysis E2) "statement" -> E-9, "S&P YTD" -> E-19
# first; FWD-18 reads 3 of 14 from the deployed catalog with C3 on 3 of 3; and an unknown model name reaches E-13
# carrying the five model codes. Probe r10_host.py.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
D=org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables
args=$(python - "$(native "$(pwd)/$D/0.9.0_WK_NFRA_MCPINDEX~30/census_trade_rec.json")" "$(native "$(pwd)/$D/0.9.0_WK_NFRA_MCPINDEX~31/census_billing.json")" <<'PYEOF'
import json, sys
out = []
for name, p in (("trade_rec", sys.argv[1]), ("billing", sys.argv[2])):
    c = json.load(open(p, encoding="utf-8"))
    out.append("%s=%s:%s" % (name, c.get("verdict"), c.get("probe_scope") or "-"))
print(" ".join(out))
PYEOF
)
args=$(printf '%s' "$args" | tr -d '\r')
want=$(printf '%s\n' $args | grep -c '=SERVED:')
T="${TMPDIR:-/tmp}/mx_r9_r10_$$"; mkdir -p "$T"
python - "$T/params.json" "$(native "$H/r10_host.py")" "$args" <<'PYEOF'
import base64, json, sys
src = base64.b64encode(open(sys.argv[2], "rb").read()).decode()
cmd = ('echo "health=$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8080/health)"; '
       'echo ' + src + ' | base64 -d > /tmp/r10_host.py; '
       'cd /opt/opal-gateway && sudo -u ec2-user ./.venv/bin/python /tmp/r10_host.py ' + sys.argv[3] +
       ' 2>&1 | grep -E "^(READ|ROUTE|FWD18|GUIDE) |Error" | tail -10; rm -f /tmp/r10_host.py')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
PYEOF
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(native "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>&1 | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 4; done
o=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>&1 | tr -d '\r')
rm -rf "$T"
h=$(printf '%s\n' "$o" | sed -n 's/^health=//p')
[ -n "$h" ] || echo "INSTRUMENT: empty health with status=${st:-NONE}; fetched output head: $(printf '%s' "$o" | head -c 300 | tr '\n' ' ')"
printf '%s\n' "$o" | grep -E '^(READ|ROUTE|FWD18|GUIDE) ' | cut -c1-200
good=$(printf '%s\n' "$o" | grep -E '^READ .* verdict=SERVED rows=' | awk '{for(i=1;i<=NF;i++){split($i,a,"="); v[a[1]]=a[2]} if (v["rows"]>0 && v["rows"]==v["exact"] && v["scope_ok"]=="True" && v["claim"]=="measured" && v["completeness"]=="stated") n++} END {print n+0}')
rt=$(printf '%s\n' "$o" | grep -E '^ROUTE ' | awk '{split($2,a,"=");split($3,b,"="); if (a[2]==b[2]) n++} END {print n+0}')
f18=$(printf '%s\n' "$o" | sed -n -E 's/^FWD18 served=([0-9]+) c3=([0-9]+).*/\1 \2/p')
gd=$(printf '%s\n' "$o" | sed -n -E 's/^GUIDE first=([^ ]*) codes=([0-9]+).*/\1 \2/p')
echo "ssm command=${cid:-NONE} status=${st:-NONE}; /health=$h; SERVED readers graded good $good of $want; routes first $rt of 4; fwd18 served,c3=${f18:-none}; guide=${gd:-none}"
if [ "$h" = 200 ] && [ "$good" = "$want" ] && [ "$rt" = 4 ] && [ "$f18" = "3 3" ] && [ "$gd" = "E-13 5" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
