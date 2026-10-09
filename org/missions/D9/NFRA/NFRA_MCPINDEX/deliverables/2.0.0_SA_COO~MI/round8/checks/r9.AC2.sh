#!/usr/bin/env bash
# MX-r-9 AC2 (FWD-13 live, the SERVED host): /health 200, and IN-PROCESS on the host under its own venv and .env, the
# deployed discover states for model benchmarks, aum-metrics and aggregate-aua-timeseries the SAME as-of the served
# object carries (read independently on the host), claim measured: 3 of 3. Probe r9_host.py (.env parsed in Python).
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
T="${TMPDIR:-/tmp}/mx_r8_r9_$$"; mkdir -p "$T"
python - "$T/params.json" "$(native "$H/r9_host.py")" <<'PYEOF'
import base64, json, sys
src = base64.b64encode(open(sys.argv[2], "rb").read()).decode()
cmd = ('echo "health=$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8080/health)"; '
       'echo ' + src + ' | base64 -d > /tmp/r9_host.py; '
       'cd /opt/opal-gateway && sudo -u ec2-user ./.venv/bin/python /tmp/r9_host.py 2>&1 | grep -E "^(FRESH|ROUTE) |Error" | tail -14; '
       'rm -f /tmp/r9_host.py')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
PYEOF
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(native "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>/dev/null | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 4; done
o=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>&1 | tr -d '\r')
rm -rf "$T"
h=$(printf '%s\n' "$o" | sed -n 's/^health=//p')
if [ -z "$h" ]; then echo "INSTRUMENT: empty health with status=${st:-NONE}; fetched output head: $(printf '%s' "$o" | head -c 300 | tr '\n' ' ')"; fi
printf '%s\n' "$o" | grep -E '^FRESH ' | cut -c1-160
eq=$(printf '%s\n' "$o" | grep -E '^FRESH ' | awk '{split($3,a,"=");split($4,b,"=");split($5,c,"="); if (a[2]==c[2] && b[2]=="measured") n++} END {print n+0}')
echo "ssm command=${cid:-NONE} status=${st:-NONE}; /health=$h; stated as-of equals served (claim measured) $eq of 3"
if [ "$h" = 200 ] && [ "$eq" = 3 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
