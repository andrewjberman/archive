#!/usr/bin/env bash
# MX-r-3 AC3 (the SERVED host, read live over SSM, shipped DORMANT): on i-07dccb1615503ac99, /health answers 200 (the
# control); both new integration directories exist under /opt/opal-gateway/app/integrations/ (shipped); and the host
# .env's ENABLED_INTEGRATIONS line names neither opal_discover nor portal_index (dormant: DELTA=0 on the tool surface
# until G-A).
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
T="${TMPDIR:-/tmp}/mx_r3_ac3_$$"; mkdir -p "$T"
python - "$T/params.json" <<'EOF'
import json, sys
cmd = ('echo "health=$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8080/health)"; '
       'for d in opal_discover portal_index; do test -d /opt/opal-gateway/app/integrations/$d && echo "shipped=$d"; done; '
       'echo "enabled=$(grep -E \'^ENABLED_INTEGRATIONS=\' /opt/opal-gateway/.env | head -1)"')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
EOF
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(cygpath -w "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in 1 2 3 4 5 6 7 8 9 10; do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>/dev/null | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 3; done
o=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>/dev/null | tr -d '\r')
rm -rf "$T"
h=$(printf '%s\n' "$o" | sed -n 's/^health=//p'); sh=$(printf '%s\n' "$o" | grep -c '^shipped='); en=$(printf '%s\n' "$o" | sed -n 's/^enabled=//p')
new_enabled=$(printf '%s' "$en" | grep -cE 'opal_discover|portal_index')
echo "ssm command=${cid:-NONE} status=${st:-NONE}; /health=$h; new integrations shipped $sh of 2; ENABLED_INTEGRATIONS line='${en}'; new ones enabled=$new_enabled"
if [ "$h" = 200 ] && [ "$sh" = 2 ] && [ -n "$en" ] && [ "$new_enabled" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
