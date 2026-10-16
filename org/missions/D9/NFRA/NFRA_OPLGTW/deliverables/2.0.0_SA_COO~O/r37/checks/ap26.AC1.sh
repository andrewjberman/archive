#!/usr/bin/env bash
# OPLGTW OG-ap-26 AC1 (round-37 CLASS-INCREMENT, PHASE A): the etf-classifications read grant MOVES from the gateway instance role to the internal reader role.
#  - infra/aws/terraform/opal-gateway/etf_classification_read_iam.tf holds ONE aws_iam_role_policy whose role is the internal reader role, Allow dynamodb:GetItem on the etf-classifications table ARN only, no wildcard;
#  - the targeted plan reads "1 to add, 0 to change, 1 to destroy" (a replacement: the policy leaves the instance role and lands on the internal reader role);
#  - the ask for three halves exists.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
TF="infra/aws/terraform/opal-gateway/etf_classification_read_iam.tf"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS"
[ -f "$TF" ] && [ -f "$W/CLS2_PLAN.txt" ] && [ -f "$W/NEVER_WIDEN_ASK_OG-ap-26.md" ] || { echo "tf, plan or ask absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$TF")" "$(native "$W/CLS2_PLAN.txt")" "$(native "$W/NEVER_WIDEN_ASK_OG-ap-26.md")" <<'PYEOF'
import re, sys
tf = open(sys.argv[1], encoding="utf-8").read()
plan = open(sys.argv[2], encoding="utf-8", errors="replace").read()
ask = open(sys.argv[3], encoding="utf-8").read()
stripped = re.sub(r"(?m)^\s*#.*$", "", tf)
m = re.search(r'resource\s+"aws_iam_role_policy"\s+"[^"]+"\s*\{(.*?)\n\}', stripped, re.S)
body = m.group(1) if m else ""
role = re.search(r'(?m)^\s*role\s*=\s*(\S+)', body)
role_s = role.group(1) if role else ""
internal = bool(re.search(r"int(ernal)?_?reader", role_s, re.I)) and "aws_iam_role.gw." not in role_s
actions = sorted(set(re.findall(r'"(dynamodb:[A-Za-z*]+)"', stripped)))
arns = re.findall(r'arn:aws:dynamodb:[^"]*', stripped)
arn_ok = len(arns) >= 1 and all(a.endswith(":table/etf-classifications") for a in arns)
star = bool(re.search(r'Resource\s*=\s*"\*"|Resource\s*=\s*\[\s*"\*"', stripped)) or "dynamodb:*" in stripped
policies = len(re.findall(r'resource\s+"aws_iam_role_policy"', stripped))
pm = re.search(r"(\d+) to add, (\d+) to change, (\d+) to destroy", plan)
plan_ok = bool(pm) and pm.groups() == ("1", "0", "1")
halves = all(re.search(r"(?mi)^#+ .*%s" % h, ask) for h in ("CTO", "COO", "CVO"))
print("terraform: policies %d (want 1); role is the internal reader %s (role expr %s); dynamodb actions %s; table arn ok %s; wildcard %s (want False)" % (policies, internal, role_s, actions, arn_ok, star))
print("plan: 1 to add, 0 to change, 1 to destroy %s; ask has the three halves %s" % (plan_ok, halves))
print("OK" if policies == 1 and internal and actions == ["dynamodb:GetItem"] and arn_ok and not star and plan_ok and halves else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
