#!/usr/bin/env bash
# OPLGTW OG-ap-25 AC1 (round-37 CLASS-INCREMENT, PHASE A): the one Terraform file grants exactly dynamodb:GetItem on the etf-classifications table ARN to the gateway role, the plan is "1 to add, 0 to change, 0 to destroy", and the ask for three halves exists.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
TF="infra/aws/terraform/opal-gateway/etf_classification_read_iam.tf"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS"
[ -f "$TF" ] && [ -f "$W/CLS_PLAN.txt" ] && [ -f "$W/NEVER_WIDEN_ASK_OG-ap-25.md" ] || { echo "tf, plan or ask absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$TF")" "$(native "$W/CLS_PLAN.txt")" "$(native "$W/NEVER_WIDEN_ASK_OG-ap-25.md")" <<'PYEOF'
import re, sys
tf = open(sys.argv[1], encoding="utf-8").read()
plan = open(sys.argv[2], encoding="utf-8", errors="replace").read()
ask = open(sys.argv[3], encoding="utf-8").read()
stripped = re.sub(r"(?m)^\s*#.*$", "", tf)
policies = len(re.findall(r'resource\s+"aws_iam_role_policy"', stripped))
actions = sorted(set(re.findall(r'"(dynamodb:[A-Za-z*]+)"', stripped)))
arns = re.findall(r'arn:aws:dynamodb:[^"]*', stripped)
arn_ok = len(arns) >= 1 and all(a.endswith(":table/etf-classifications") for a in arns)
star = bool(re.search(r'"Resource"\s*=\s*"\*"|Resource\s*=\s*\[\s*"\*"', stripped)) or "dynamodb:*" in stripped
others = len(re.findall(r'resource\s+"(?!aws_iam_role_policy")', stripped))
m = re.search(r"(\d+) to add, (\d+) to change, (\d+) to destroy", plan)
plan_ok = bool(m) and m.groups() == ("1", "0", "0")
halves = all(re.search(r"(?mi)^#+ .*%s" % h, ask) for h in ("CTO", "COO", "CVO"))
print("terraform: policies %d (want 1); dynamodb actions %s (want ['dynamodb:GetItem']); table arn ends table/etf-classifications %s; wildcard action or resource %s (want False); other resources %d (want 0)" % (policies, actions, arn_ok, star, others))
print("plan: 1 to add, 0 to change, 0 to destroy %s; ask has the three halves %s" % (plan_ok, halves))
print("OK" if policies == 1 and actions == ["dynamodb:GetItem"] and arn_ok and not star and others == 0 and plan_ok and halves else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
