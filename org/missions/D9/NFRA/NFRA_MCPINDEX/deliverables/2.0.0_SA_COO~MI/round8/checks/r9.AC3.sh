#!/usr/bin/env bash
# MX-r-9 AC3 (FWD-14, FWD-17 live, the SERVED host): the deployed discover's FIRST match for each of Alyssa's six
# phrasings and the three write asks is its expected need entry: Q28 E-16, Q29 E-4, Q30 E-9, Q31 E-20, Q32 E-21, Q33 E-19,
# Q34 E-21, Q35 E-23, Q36 E-24; the three write asks (Q34-Q36) carry op_class write and a grant field.
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
n=0; w=0
for pair in Q28:E-16 Q29:E-4 Q30:E-9 Q31:E-20 Q32:E-21 Q33:E-19 Q34:E-21 Q35:E-23 Q36:E-24; do
  q=${pair%%:*}; e=${pair#*:}; l=$(printf '%s\n' "$o" | grep -E "^ROUTE $q " | tail -1)
  printf '%s' "$l" | grep -q " first=$e " && n=$((n+1)) || echo "MISS $q expected $e: ${l:-absent}"
  case $q in Q34|Q35|Q36) printf '%s' "$l" | grep -q ' op_class=write ' && ! printf '%s' "$l" | grep -q ' grant=None' && w=$((w+1));; esac
done
echo "ssm command=${cid:-NONE} status=${st:-NONE}; /health=$h; first match expected $n of 9; write asks with class+grant $w of 3"
if [ "$h" = 200 ] && [ "$n" = 9 ] && [ "$w" = 3 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
