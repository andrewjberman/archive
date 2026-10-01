#!/usr/bin/env bash
# MS-ir-1 AC1 (the built text, names by the builder): mcpmsp_internal_reader.tf calls module opal_name with system
# "gateway", scope "global", function "internal-reader", kind "role", names the role from it, reads the bucket from
# scope_bucket["global"], carries no "opal-data-" literal and grants aws_iam_role.gw sts:AssumeRole;
# mcpmsp_gateway_firm_deny.tf holds an explicit "Deny" on s3:GetObject attached to aws_iam_role.gw; and the naming gate
# passes BOTH files (each graded as an addition, denominator 1).
. "$(dirname "$0")/_root.sh"
A="$TF_DIR/mcpmsp_internal_reader.tf"; B="$TF_DIR/mcpmsp_gateway_firm_deny.tf"
for f in "$A" "$B"; do [ -f "$f" ] || { echo "$f absent"; echo "RESULT: FAIL"; exit 1; }; done
res=$(python - "$A" "$B" <<'EOF' 2>&1 | tr -d '\r'
import re, sys
a = open(sys.argv[1], encoding='utf-8').read(); b = open(sys.argv[2], encoding='utf-8').read()
mods = re.findall(r'module\s+"([^"]+)"\s*\{([^}]*)\}', a, re.S)
rm = next((n for n, body in mods if 'modules/opal_name' in body and re.search(r'system\s*=\s*"gateway"', body) and re.search(r'scope\s*=\s*"global"', body) and re.search(r'function\s*=\s*"internal-reader"', body) and re.search(r'kind\s*=\s*"role"', body)), None)
c = {'role_module': bool(rm), 'role_named': bool(rm) and bool(re.search(r'name\s*=\s*module\.%s\.name' % re.escape(rm or 'x'), a)),
     'bucket_builder': 'scope_bucket["global"]' in a, 'no_literal_a': 'opal-data-' not in a,
     'assume_grant': 'sts:AssumeRole' in a and 'aws_iam_role.gw' in a,
     'deny_stmt': bool(re.search(r'"?Deny"?', b)) and 's3:GetObject' in b and 'aws_iam_role.gw' in b}
print(' '.join('%s=%s' % (k, 'y' if v else 'n') for k, v in c.items()), 'verdict=%s' % ('OK' if all(c.values()) else 'NO'))
EOF
)
ga=$(naming_gate_file "$A"); gb=$(naming_gate_file "$B")
echo "$res; naming gate internal_reader: $ga; firm_deny: $gb"
okg() { case "$1" in *"NAMING-GATE: PASS"*"|1"|*"NAMING-GATE: WARN"*"|1") return 0;; *) return 1;; esac; }
if printf '%s' "$res" | grep -q 'verdict=OK' && okg "$ga" && okg "$gb"; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
