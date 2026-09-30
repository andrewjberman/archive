#!/usr/bin/env bash
# MX-r-6 AC2 (the SERVED host after the Schwab enable release): on i-07dccb1615503ac99 /health answers 200; the schwab,
# opal_discover and portal_index integration dirs are shipped; the host .env ENABLED_INTEGRATIONS names schwab AND the 5
# prior ids; and the LIVE gateway-schwab-read-role is allowed s3:GetObject on dim_transaction for both masters.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
T="${TMPDIR:-/tmp}/mx_r5_ac2_$$"; mkdir -p "$T"
python - "$T/params.json" <<'EOF'
import json, sys
cmd = ('echo "health=$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8080/health)"; '
       'for d in schwab opal_discover portal_index; do test -d /opt/opal-gateway/app/integrations/$d && echo "shipped=$d"; done; '
       'echo "enabled=$(grep -E \'^ENABLED_INTEGRATIONS=\' /opt/opal-gateway/.env | head -1)"')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
EOF
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(cygpath -w "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in 1 2 3 4 5 6 7 8 9 10; do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>/dev/null | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 3; done
o=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>/dev/null | tr -d '\r')
rm -rf "$T"
h=$(printf '%s\n' "$o" | sed -n 's/^health=//p'); sh=$(printf '%s\n' "$o" | grep -c '^shipped='); en=$(printf '%s\n' "$o" | sed -n 's/^enabled=//p')
need=0; for id in schwab ycharts opal_portal globgrph opal_discover portal_index; do printf '%s' "$en" | grep -qE "(=|[ ,])$id([ ,]|$)" && need=$((need+1)); done
RA=$(timeout 30 "$AWS" iam get-role --role-name gateway-schwab-read-role --query Role.Arn --output text 2>&1 | tr -d '\r')
allow=0; for m in 08242234 08335338; do d=$(timeout 60 "$AWS" iam simulate-principal-policy --policy-source-arn "$RA" --action-names s3:GetObject --resource-arns "arn:aws:s3:::opal-data-assets/schwab/$m/silver/dim_transaction/date=2026-09-30/data.parquet" --query 'EvaluationResults[0].EvalDecision' --output text 2>&1 | tr -d '\r'); echo "iam $m dim_transaction GetObject: $d"; [ "$d" = allowed ] && allow=$((allow+1)); done
echo "ssm command=${cid:-NONE} status=${st:-NONE}; /health=$h; shipped $sh of 3; ENABLED_INTEGRATIONS line='${en}'; ids enabled $need of 6; live reader-role GetObject on dim_transaction allowed $allow of 2"
if [ "$h" = 200 ] && [ "$sh" = 3 ] && [ "$need" = 6 ] && [ "$allow" = 2 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
