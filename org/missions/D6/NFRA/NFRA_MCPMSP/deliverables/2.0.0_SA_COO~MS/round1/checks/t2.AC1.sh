#!/usr/bin/env bash
# MS-t-2 AC1 (the built behaviour, read from the Terraform text): infra/aws/terraform/opal-gateway/mcpmsp_firm_roles.tf
# names the role with the builder's output (name('gateway','inflection','firm-reader','role')); trusts the gateway role;
# allows s3:GetObject on opal-data-inf/* and on opal-data-portal-v2/platinum/mdpf/inflection/*; carries a Deny naming
# opal-data-cot, opal-data-bd and opal-data-49financial; and grants the gateway role sts:AssumeRole.
. "$(dirname "$0")/_root.sh"
F="$TF_DIR/mcpmsp_firm_roles.tf"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
nm=$(opal_name gateway inflection firm-reader role)
res=$(python - "$F" "$nm" <<'EOF' 2>&1 | tr -d '\r'
import re, sys
t = open(sys.argv[1], encoding='utf-8').read(); nm = sys.argv[2]
checks = {
  'role_name': nm in t,
  'trust_gateway_role': 'opal-gateway-role' in t or 'aws_iam_role.opal_gateway' in t or 'aws_iam_role.gateway' in t,
  'allow_inf': 'opal-data-inf/*' in t,
  'allow_portal_prefix': 'opal-data-portal-v2/platinum/mdpf/inflection/*' in t,
  'deny_block': bool(re.search(r'"?Deny"?', t)),
  'deny_cot': 'opal-data-cot' in t, 'deny_bd': 'opal-data-bd' in t, 'deny_49f': 'opal-data-49financial' in t,
  'assume_grant': 'sts:AssumeRole' in t,
}
print(' '.join('%s=%s' % (k, 'y' if v else 'n') for k, v in checks.items()), 'verdict=%s' % ('OK' if all(checks.values()) else 'NO'))
EOF
)
echo "name()=$nm; $res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
