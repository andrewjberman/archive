#!/usr/bin/env bash
# MX-r-13 AC2 (FWD-20 + FWD-21 live, the SERVED host): /health 200; IN-PROCESS on the host under its own venv and .env,
# the deployed tree's served tools each name a catalog index with depth and freshness claims (c11_index.py, denominator
# printed), and the deployed discover answers the two harvest subjects from harvest_datasets with the Schwab control
# intact (c10_discover.py). Probe r13_host.py.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
T="${TMPDIR:-/tmp}/mx_r12_r13_$$"; mkdir -p "$T"
python - "$T/params.json" "$(native "$H/r13_host.py")" "$(native "$H/c11_index.py")" "$(native "$H/c10_discover.py")" <<'PYEOF'
import base64, json, sys
b = lambda p: base64.b64encode(open(p, "rb").read()).decode()
cmd = ('echo "health=$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8080/health)"; '
       'echo ' + b(sys.argv[3]) + ' | base64 -d > /tmp/c11_index.py; '
       'echo ' + b(sys.argv[4]) + ' | base64 -d > /tmp/c10_discover.py; '
       'echo ' + b(sys.argv[2]) + ' | base64 -d > /tmp/r13_host.py; chmod 644 /tmp/c11_index.py /tmp/c10_discover.py /tmp/r13_host.py; '
       'cd /opt/opal-gateway && sudo -u ec2-user ./.venv/bin/python /tmp/r13_host.py 2>&1 | tail -24; '
       'rm -f /tmp/c11_index.py /tmp/c10_discover.py /tmp/r13_host.py')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
PYEOF
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(native "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in $(seq 1 30); do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>&1 | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 4; done
o=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>&1 | tr -d '\r')
rm -rf "$T"
h=$(printf '%s\n' "$o" | sed -n 's/^health=//p')
[ -n "$h" ] || echo "INSTRUMENT: empty health with status=${st:-NONE}; fetched output head: $(printf '%s' "$o" | head -c 300 | tr '\n' ' ')"
printf '%s\n' "$o" | grep -E '^(SERVED|PARTITION|DISCOVER|discover reads|  MISSING|RC|ERR) ' | cut -c1-220
ri=$(printf '%s\n' "$o" | sed -n 's/^RC index=//p'); rd=$(printf '%s\n' "$o" | sed -n 's/^RC discover=//p')
echo "ssm command=${cid:-NONE} status=${st:-NONE}; /health=$h; index rc=${ri:-none}; discover rc=${rd:-none}"
if [ "$h" = 200 ] && [ "$ri" = 0 ] && [ "$rd" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
