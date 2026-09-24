#!/usr/bin/env bash
# MP-t-6 AC3 (the SERVED host, read live over SSM, with its control): on i-07dccb1615503ac99, /health answers 200 (the
# control: the gateway is up) while /api/admin/whoami with NO identity header answers 401 or 403 (the owner gate is live
# on the served code), and / serves the bundle's HTML only through the same gate (401 or 403 without a header).
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
T="${TMPDIR:-/tmp}/mp_t6_ac3_$$"; mkdir -p "$T"
python - "$T/params.json" <<'EOF'
import json, sys
cmd = 'for p in /health /api/admin/whoami /; do echo "$p=$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8080$p)"; done'
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
EOF
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(cygpath -w "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in 1 2 3 4 5 6 7 8 9 10; do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>/dev/null | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 3; done
o=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>/dev/null | tr -d '\r')
rm -rf "$T"
h=$(printf '%s\n' "$o" | sed -n 's#^/health=##p'); w=$(printf '%s\n' "$o" | sed -n 's#^/api/admin/whoami=##p'); r=$(printf '%s\n' "$o" | sed -n 's#^/=##p')
echo "ssm command=${cid:-NONE} status=${st:-NONE}; /health=$h; /api/admin/whoami=$w; /=$r"
if [ "$h" = 200 ] && { [ "$w" = 401 ] || [ "$w" = 403 ]; } && { [ "$r" = 401 ] || [ "$r" = 403 ]; }; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
