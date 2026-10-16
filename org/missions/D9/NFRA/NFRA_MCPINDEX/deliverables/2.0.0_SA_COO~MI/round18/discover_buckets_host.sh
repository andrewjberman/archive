#!/usr/bin/env bash
# discover_buckets_host.sh -- the issuer's real run of the PRD "done by" line ON the gateway host: opal_discover returns a row for every bucket, asked in plain words.
# discover_buckets.py is shipped through SSM and run under the host's own venv against its deployed catalog (read-only; nothing is written on the host).
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/../round17/checks/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
T="${TMPDIR:-/tmp}/mx_discb_$$"; mkdir -p "$T"
python - "$T/params.json" "$(native "$H/discover_buckets.py")" <<'PYEOF'
import base64, json, sys
b = lambda p: base64.b64encode(open(p, "rb").read()).decode()
cmd = ('echo "health=$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8080/health)"; '
       'echo ' + b(sys.argv[2]) + ' | base64 -d > /tmp/discover_buckets.py; chmod 644 /tmp/discover_buckets.py; '
       'cd /opt/opal-gateway && sudo -u ec2-user ./.venv/bin/python /tmp/discover_buckets.py /opt/opal-gateway 2>&1 | tail -14; echo "RC=${PIPESTATUS[0]}"; '
       'rm -f /tmp/discover_buckets.py')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
PYEOF
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(native "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in $(seq 1 40); do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>&1 | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 3; done
o=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>&1 | tr -d '\r')
rm -rf "$T"
printf '%s\n' "$o" | grep -E '^(health=|BUCKET|buckets served|buckets whose|RC=|Traceback|.*Error)' | cut -c1-250
echo "ssm command=${cid:-NONE} status=${st:-NONE}"
if printf '%s\n' "$o" | grep -q '^RC=0' && printf '%s\n' "$o" | grep -q '^health=200'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
