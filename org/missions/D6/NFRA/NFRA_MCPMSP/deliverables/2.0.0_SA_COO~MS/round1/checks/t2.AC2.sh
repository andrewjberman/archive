#!/usr/bin/env bash
# MS-t-2 AC2 (AMENDMENT 1 -- the seam probe against the REAL neighbour, the live account through Terraform's own plan,
# read-only and unlocked): a plan of infra/aws/terraform/opal-gateway targeted at every resource and module
# mcpmsp_firm_roles.tf declares reads "Plan: N to add, 0 to change, 0 to destroy" with N >= 3, and the planned role
# name is the builder's output name('gateway','inflection','firm-reader','role').
. "$(dirname "$0")/_root.sh"
F="$TF_DIR/mcpmsp_firm_roles.tf"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
targets=$(python - "$F" <<'EOF' 2>/dev/null
import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
r = ['-target=%s.%s' % (a, b) for a, b in re.findall(r'^resource\s+"([^"]+)"\s+"([^"]+)"', t, re.M)]
print(' '.join(r))
EOF
)
targets=$(printf '%s' "$targets" | tr -d '\r')
[ -n "$targets" ] || { echo "no resource blocks in $F"; echo "RESULT: FAIL"; exit 1; }
nm=$(opal_name gateway inflection firm-reader role)
MAIN="$(cd "$(git rev-parse --git-common-dir)/.." && pwd)"
# A PRIVATE data dir: the main tree's providers and backend state copied (no init, which would fetch providers), then
# `terraform get` registers the LOCAL module opal_name (a local path: no network). The main tree's .terraform is never
# written.
PD="$(mktemp -d "${TMPDIR:-/tmp}/ms_t2_ac2.XXXXXX")"
cp -r "$MAIN/$TF_DIR/.terraform/providers" "$PD/" 2>/dev/null && cp "$MAIN/$TF_DIR/.terraform/terraform.tfstate" "$PD/" 2>/dev/null \
  || { echo "no initialised .terraform in the main tree"; rm -rf "$PD"; echo "RESULT: FAIL"; exit 1; }
export TF_DATA_DIR="$PD"
# Every plan here evaluates filebase64sha256 over MCPORTAL's gitignored layer zip; the issuer restored the DEPLOYED
# layer's exact bytes into the main tree (hash = the live CodeSha256). Copy it in if absent.
LZ="infra/aws/lambda/layers/mcportal-grant-writer-deps/.build/mcportal-grant-writer-deps.zip"
[ -f "$LZ" ] || { mkdir -p "$(dirname "$LZ")"; cp "$MAIN/$LZ" "$LZ" 2>/dev/null || { echo "no $LZ in the main tree"; rm -rf "$PD"; echo "RESULT: FAIL"; exit 1; }; }
(cd "$TF_DIR" && timeout 60 terraform get -no-color >/dev/null 2>&1)
# The writer's two owner-key variables are required by the directory but read by nothing this plan targets:
# plan-only placeholders, never an apply value.
out=$(cd "$TF_DIR" && timeout 110 terraform plan -lock=false -input=false -no-color -var mcportal_owner_key_claim=sub -var mcportal_owner_key=PLAN-ONLY-PLACEHOLDER $targets 2>&1 | tr -d '\r')
rm -rf "$PD"
line=$(printf '%s\n' "$out" | grep -m1 -E '^Plan: [0-9]+ to add' || printf '%s\n' "$out" | grep -m1 -E 'No changes|Error' || echo "(no plan line)")
named=$(printf '%s\n' "$out" | grep -cE "name +(=|\+) +\"$nm\"|\+ name += \"$nm\"")
echo "targets: $targets"; echo "plan: $line; planned role name $nm seen=$named"
add=$(printf '%s' "$line" | sed -nE 's/^Plan: ([0-9]+) to add, ([0-9]+) to change, ([0-9]+) to destroy.*/\1 \2 \3/p')
set -- $add
if [ -n "$add" ] && [ "$1" -ge 3 ] && [ "$2" = 0 ] && [ "$3" = 0 ] && [ "$named" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
