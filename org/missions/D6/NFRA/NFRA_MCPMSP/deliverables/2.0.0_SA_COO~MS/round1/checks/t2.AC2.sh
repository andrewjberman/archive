#!/usr/bin/env bash
# MS-t-2 AC2 (the seam probe against the REAL neighbour, the live account through Terraform's own plan, read-only and
# unlocked): a plan of infra/aws/terraform/opal-gateway targeted at every resource mcpmsp_firm_roles.tf declares reads
# "Plan: N to add, 0 to change, 0 to destroy" with N >= 3 (the role, its policy, the gateway's AssumeRole grant).
. "$(dirname "$0")/_root.sh"
F="$TF_DIR/mcpmsp_firm_roles.tf"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
targets=$(python - "$F" <<'EOF' 2>/dev/null | tr -d '\r'
import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
print(' '.join('-target=%s.%s' % (a, b) for a, b in re.findall(r'^resource\s+"([^"]+)"\s+"([^"]+)"', t, re.M)))
EOF
)
[ -n "$targets" ] || { echo "no resource blocks in $F"; echo "RESULT: FAIL"; exit 1; }
# A linked worktree carries no .terraform (gitignored) and `init` would fetch providers (egress): borrow the MAIN tree's.
MAIN="$(cd "$(git rev-parse --git-common-dir)/.." && pwd)"
export TF_DATA_DIR="$MAIN/$TF_DIR/.terraform"
[ -d "$TF_DATA_DIR" ] || { echo "no initialised $TF_DATA_DIR in the main tree"; echo "RESULT: FAIL"; exit 1; }
# Every plan here evaluates filebase64sha256 over MCPORTAL's gitignored layer zip. The issuer restored the DEPLOYED
# layer's exact bytes into the main tree at the cut (hash = the live CodeSha256); copy it into this worktree if absent.
LZ="infra/aws/lambda/layers/mcportal-grant-writer-deps/.build/mcportal-grant-writer-deps.zip"
[ -f "$LZ" ] || { mkdir -p "$(dirname "$LZ")"; cp "$MAIN/$LZ" "$LZ" 2>/dev/null || { echo "no $LZ in the main tree"; echo "RESULT: FAIL"; exit 1; }; }
# The writer's two owner-key variables are required by the directory but read by no resource this plan targets:
# plan-only placeholders, never an apply value.
out=$(cd "$TF_DIR" && timeout 110 terraform plan -lock=false -input=false -no-color -var mcportal_owner_key_claim=sub -var mcportal_owner_key=PLAN-ONLY-PLACEHOLDER $targets 2>&1 | tr -d '\r')
line=$(printf '%s\n' "$out" | grep -m1 -E '^Plan: [0-9]+ to add' || printf '%s\n' "$out" | grep -m1 -E 'No changes|Error' || echo "(no plan line)")
echo "targets: $targets"; echo "plan: $line"
add=$(printf '%s' "$line" | sed -nE 's/^Plan: ([0-9]+) to add, ([0-9]+) to change, ([0-9]+) to destroy.*/\1 \2 \3/p')
set -- $add
if [ -n "$add" ] && [ "$1" -ge 3 ] && [ "$2" = 0 ] && [ "$3" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
