#!/usr/bin/env bash
# MX-r-8 AC2 (the SERVED host after the slot-4 release): /health 200, and IN-PROCESS on the host under its own venv and
# .env, opal_discover names blackdiamond_list_fees for the BD fees ask and etfs_get_positioning for "ETF positioning".
# The host probe is r8_host.py: .venv/bin/python, .env parsed in Python (never sourced by a shell -- it echoes values).
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
HP="$(dirname "$0")/r8_host.py"
T="${TMPDIR:-/tmp}/mx_r6_r8_$$"; mkdir -p "$T"
python - "$T/params.json" "$(native "$HP")" <<'EOF'
import base64, json, sys
src = base64.b64encode(open(sys.argv[2], "rb").read()).decode()
cmd = ('echo "health=$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8080/health)"; '
       'echo ' + src + ' | base64 -d > /tmp/r8_host.py; '
       'cd /opt/opal-gateway && sudo -u ec2-user ./.venv/bin/python /tmp/r8_host.py 2>&1 | grep -E "^(bd|etf)=|Error" | tail -4; '
       'rm -f /tmp/r8_host.py')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
EOF
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(native "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in 1 2 3 4 5 6 7 8 9 10 11 12; do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>/dev/null | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 4; done
o=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>&1 | tr -d '\r')
rm -rf "$T"
h=$(printf '%s\n' "$o" | sed -n 's/^health=//p'); bd=$(printf '%s\n' "$o" | sed -n 's/^bd=//p'); etf=$(printf '%s\n' "$o" | sed -n 's/^etf=//p')
echo "ssm command=${cid:-NONE} status=${st:-NONE}; /health=$h; BD ask next_tools=[$bd]; ETF ask next_tools=[$etf]"
if [ "$h" = 200 ] && printf '%s' ",$bd," | grep -q ',blackdiamond_list_fees,' && printf '%s' ",$etf," | grep -q ',etfs_get_positioning,'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
