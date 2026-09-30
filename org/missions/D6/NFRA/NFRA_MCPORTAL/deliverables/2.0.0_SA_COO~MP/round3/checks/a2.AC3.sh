#!/usr/bin/env bash
# MP-a-2 AC3 (R-2's branch, picked from the measurement; the CTO's privacy condition @384fd85543: the capture logs claim
# KEYS only): the deployed writer's MCPORTAL_OWNER_KEY_CLAIM equals the claim the gateway's latest OWNER-HEADER-CLAIMS
# journal line proves the ALB carries -- oid when `oid` is among its keys, otherwise sub. When the claim is oid, the
# configured MCPORTAL_OWNER_KEY equals the measured oid ruling R-1 accepted (2e21f8e5-55ca-45c1-91b9-a4607bf28d4f).
# When it is sub, the value was supplied by the owner from his own whoami response; this check reads it as non-empty and
# names the close run's owner write as its proof. The line must carry NO claim value.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99; R1_OID="2e21f8e5-55ca-45c1-91b9-a4607bf28d4f"
nm=$(python -c "import sys;sys.path.insert(0,'.');import lib.opal_naming as n;print(n.name('mcportal', None, 'grant-writer', 'lambda'))" 2>&1 | tr -d '\r' | tail -1)
T="${TMPDIR:-/tmp}/mp_a2_ac3_$$"; mkdir -p "$T"
python - "$T/params.json" <<'EOF'
import json, sys
cmd = 'journalctl -u opal-gateway --no-pager -o cat | grep "OWNER-HEADER-CLAIMS" | tail -1'
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
EOF
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(cygpath -w "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in 1 2 3 4 5 6 7 8 9 10; do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>/dev/null | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 3; done
line=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>/dev/null | tr -d '\r' | grep 'OWNER-HEADER-CLAIMS' | tail -1)
timeout 30 "$AWS" lambda get-function-configuration --function-name "$nm" --query Environment.Variables --output json > "$T/env.json" 2>/dev/null
printf '%s' "$line" > "$T/line.txt"
res=$(python - "$T/line.txt" "$T/env.json" "$R1_OID" <<'EOF' 2>&1 | tr -d '\r'
import json, re, sys
line = open(sys.argv[1], encoding='utf-8').read().strip()
try:
    env = json.load(open(sys.argv[2], encoding='utf-8')) or {}
except Exception:
    env = {}
m = re.search(r'\bkeys=(\S*)', line)
keys = set((m.group(1) if m else '').split(',')) - {''}
has_value = bool(re.search(r'\b(oid|sub|email|name)=(?!ABSENT\b)(?!PRESENT\b)\S+', line.replace('keys=', 'k=')))
want = 'oid' if 'oid' in keys else ('sub' if 'sub' in keys else 'NONE')
have_c = env.get('MCPORTAL_OWNER_KEY_CLAIM', 'UNSET'); have_v = env.get('MCPORTAL_OWNER_KEY', '')
if want == 'oid':
    val_ok = have_v.lower() == sys.argv[3].lower()
else:
    val_ok = bool(have_v.strip())
ok = bool(line) and not has_value and want != 'NONE' and have_c == want and val_ok
print('line=%s values_in_line=%s want_claim=%s have_claim=%s value_ok=%s verdict=%s' % (
    'yes' if line else 'no', 'yes' if has_value else 'no', want, have_c, 'yes' if val_ok else 'no', 'OK' if ok else 'NO'))
EOF
)
rm -rf "$T"
echo "ssm command=${cid:-NONE} status=${st:-NONE}; $res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
