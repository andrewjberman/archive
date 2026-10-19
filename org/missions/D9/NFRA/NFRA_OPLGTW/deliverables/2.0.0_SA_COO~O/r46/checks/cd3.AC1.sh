#!/usr/bin/env bash
# OPLGTW OG-cd-3 AC1 (round 46, PHASE A; the CTO's round-45 analysis A1 item 3): the one Terraform file infra/aws/terraform/opal-gateway/family_depth_read_iam.tf grants the gateway role exactly the READ actions
# events:DescribeRule, s3:GetObject and s3:ListBucket (no other action, no wildcard action or resource, no other resource type), the targeted plan reads "1 to add, 0 to change, 0 to destroy", and the ask for three halves exists.
# AMENDMENT A1 (CVO refusal @adba2df9a0, CTO msg 35935): the source-root ListBucket statement carries `s3:delimiter` = "/" (a root list without a delimiter is RECURSIVE), proved three ways: the .tf names `s3:delimiter` and `StringEquals`;
# the plan lists it; and W/FD_SIMULATE_PLAN.json (all cases as expected) holds the negative control "list a source root with NO delimiter" (s3:ListBucket, decision implicitDeny) and the positive "list a source root WITH delimiter /" (allowed).
# Overrides (dry-run controls only): CD3_TF_OVERRIDE, CD3_PLAN_OVERRIDE, CD3_ASK_OVERRIDE, CD3_SIM_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
TF="${CD3_TF_OVERRIDE:-infra/aws/terraform/opal-gateway/family_depth_read_iam.tf}"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
PLAN="${CD3_PLAN_OVERRIDE:-$W/FD_PLAN.txt}"; ASK="${CD3_ASK_OVERRIDE:-$W/NEVER_WIDEN_ASK_OG-cd-3.md}"; SIM="${CD3_SIM_OVERRIDE:-$W/FD_SIMULATE_PLAN.json}"
[ -f "$TF" ] && [ -f "$PLAN" ] && [ -f "$ASK" ] && [ -f "$SIM" ] || { echo "tf, plan, ask or simulation absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python -I - "$(native "$TF")" "$(native "$PLAN")" "$(native "$ASK")" "$(native "$SIM")" <<'PYEOF'
import json, re, sys
tf = open(sys.argv[1], encoding="utf-8").read()
plan = open(sys.argv[2], encoding="utf-8", errors="replace").read()
ask = open(sys.argv[3], encoding="utf-8").read()
sim = json.load(open(sys.argv[4], encoding="utf-8"))
s = re.sub(r"(?m)^\s*#.*$", "", tf)
policies = len(re.findall(r'resource\s+"aws_iam_role_policy"', s))
others = len(re.findall(r'resource\s+"(?!aws_iam_role_policy")', s))
actions = sorted(set(re.findall(r'"((?:events|s3|dynamodb|iam|sts|lambda|ssm|kms|sqs|sns|ec2|logs):[A-Za-z*]+)"', s)) - {"s3:prefix", "s3:delimiter"})
want = ["events:DescribeRule", "s3:GetObject", "s3:ListBucket"]
star = bool(re.search(r'Action\s*=\s*\[[^\]]*"\*"|Action\s*=\s*"\*"|:\*"', s)) or bool(re.search(r'Resource\s*=\s*(\[\s*)?"\*"', s))
m = re.search(r"(\d+) to add, (\d+) to change, (\d+) to destroy", plan)
plan_ok = bool(m) and m.groups() == ("1", "0", "0")
halves = all(re.search(r"(?mi)^#+ .*%s" % h, ask) for h in ("CTO", "COO", "CVO"))
res = sim.get("results") or []
neg = [r for r in res if r.get("action") == "s3:ListBucket" and re.search(r"(?i)source root.*NO delimiter|NO delimiter.*source root", r.get("name", "")) and r.get("decision") == "implicitDeny"]
pos = [r for r in res if r.get("action") == "s3:ListBucket" and re.search(r"(?i)source root.*WITH delimiter|WITH delimiter.*source root", r.get("name", "")) and r.get("decision") == "allowed"]
delim_tf = '"s3:delimiter"' in s and "StringEquals" in s and '"s3:delimiter"' in plan
sim_ok = sim.get("all_as_expected") is True and len(neg) >= 1 and len(pos) >= 1
print("delimiter bound: the .tf and the plan name s3:delimiter %s; simulation all as expected %s, root list with NO delimiter denied %d case(s), root list WITH delimiter allowed %d case(s): %s" % (delim_tf, sim.get("all_as_expected"), len(neg), len(pos), "ok" if (delim_tf and sim_ok) else "NOT OK"))
print("terraform: role policies %d (want 1); actions %s (want %s); wildcard action or resource %s (want False); other resource types %d (want 0)" % (policies, actions, want, star, others))
print("plan: 1 to add, 0 to change, 0 to destroy %s; ask has the three halves %s" % (plan_ok, halves))
print("OK" if policies == 1 and actions == want and not star and others == 0 and plan_ok and halves and delim_tf and sim_ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
