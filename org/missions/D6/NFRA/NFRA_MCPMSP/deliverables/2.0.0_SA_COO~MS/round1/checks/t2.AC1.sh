#!/usr/bin/env bash
# MS-t-2 AC1 (AMENDMENT 1 -- the built behaviour, names by the builder): infra/aws/terraform/opal-gateway/mcpmsp_firm_roles.tf
# (1) calls the HCL builder module opal_name with system "gateway", scope "inflection", function "firm-reader", kind
#     "role", and names the role from that module's output;
# (2) builds the served prefix from the module's scope_bucket["global"] and "platinum/mdpf/";
# (3) grants the gateway role sts:AssumeRole and references aws_iam_role.gw;
# (4) carries NO literal bucket name (no "opal-data-" string);
# (5) passes the commit-time naming gate (lib/opal_naming.py grade via .tools/naming-gate.py) with 0 REFUSE.
. "$(dirname "$0")/_root.sh"
F="$TF_DIR/mcpmsp_firm_roles.tf"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$F" <<'EOF' 2>&1 | tr -d '\r'
import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
mods = re.findall(r'module\s+"([^"]+)"\s*\{([^}]*)\}', t, re.S)
def has_mod(fn, kind):
    for name, body in mods:
        if ('modules/opal_name' in body and re.search(r'system\s*=\s*"gateway"', body) and re.search(r'scope\s*=\s*"inflection"', body)
                and re.search(r'function\s*=\s*"%s"' % fn, body) and re.search(r'kind\s*=\s*"%s"' % kind, body)):
            return name
    return None
rm = has_mod('firm-reader', 'role')
c = {
  'role_module': bool(rm),
  'role_named_by_module': bool(rm) and bool(re.search(r'name\s*=\s*module\.%s\.name' % re.escape(rm or 'x'), t)),
  'served_bucket_from_builder': 'scope_bucket["global"]' in t,
  'mdpf_prefix': 'platinum/mdpf/' in t,
  'assume_grant': 'sts:AssumeRole' in t and 'aws_iam_role.gw' in t,
  'no_bucket_literal': 'opal-data-' not in t,
}
print(' '.join('%s=%s' % (k, 'y' if v else 'n') for k, v in c.items()), 'verdict=%s' % ('OK' if all(c.values()) else 'NO'))
EOF
)
# (5) the naming gate over the WHOLE file graded as an addition (a diff from /dev/null), the grader safe-commit uses.
D="$(mktemp "${TMPDIR:-/tmp}/ms_t2_ac1.XXXXXX")"
git diff --no-color --no-ext-diff --no-index /dev/null "$F" > "$D" 2>/dev/null
go=$(python .tools/naming-gate.py --diff "$D" 2>&1 | tr -d '\r')
g=$(printf '%s\n' "$go" | grep -m1 'NAMING-GATE:')
den=$(printf '%s\n' "$go" | grep -oE 'DENOMINATOR: [0-9]+ path' | grep -oE '[0-9]+')
rm -f "$D"
echo "$res; naming gate: ${g:-NONE} (paths in the graded diff: ${den:-0})"
if printf '%s' "$res" | grep -q 'verdict=OK' && [ "${den:-0}" -ge 1 ] && printf '%s' "$g" | grep -qE '^NAMING-GATE: (PASS|WARN)'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
