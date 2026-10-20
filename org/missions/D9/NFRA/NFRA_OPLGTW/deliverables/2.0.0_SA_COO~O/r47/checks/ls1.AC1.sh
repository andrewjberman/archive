#!/usr/bin/env bash
# OPLGTW OG-ls-1 AC1 (round 47, PHASE A; the CTO's round-46 analysis "the */silver/* ListBucket narrowing"): the one Terraform file infra/aws/terraform/opal-gateway/family_depth_read_iam.tf lists silver prefixes ONLY under the eight sources of
# local.family_depth_sources (the statement FamilyDepthSilverPrefixListOnly no longer carries the any-first-component globs "*/silver/" and "*/silver/*"), the grant still holds exactly the actions events:DescribeRule, s3:GetObject, s3:ListBucket
# (no wildcard action or resource, no other resource type, FOUR statements), the targeted plan reads "0 to add, 1 to change, 0 to destroy" and names "silver/" under the per-source form, the simulation plan holds the negative controls below with all as expected,
# and the ask for three halves exists.
#   simulation cases (names carry these phrases): "ALLOWED: silver table list under a source" (s3:ListBucket, prefix schwab/x/silver/t/, allowed); "NEGATIVE: silver list under bloomberg" (prefix bloomberg/global/silver/, implicitDeny);
#   "NEGATIVE: silver list under gateway" (prefix gateway/global/silver/, implicitDeny); "NEGATIVE: silver list under yahoo" (prefix yahoo/g/silver/, implicitDeny); "NEGATIVE: list a source root with NO delimiter" (implicitDeny);
#   "ALLOWED: list a source root WITH delimiter /" (allowed).
# Overrides (dry-run controls only): LS1_TF_OVERRIDE, LS1_PLAN_OVERRIDE, LS1_ASK_OVERRIDE, LS1_SIM_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
TF="${LS1_TF_OVERRIDE:-infra/aws/terraform/opal-gateway/family_depth_read_iam.tf}"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
PLAN="${LS1_PLAN_OVERRIDE:-$W/LS_PLAN.txt}"; ASK="${LS1_ASK_OVERRIDE:-$W/NEVER_WIDEN_ASK_OG-ls-1.md}"; SIM="${LS1_SIM_OVERRIDE:-$W/LS_SIMULATE_PLAN.json}"
[ -f "$TF" ] && [ -f "$PLAN" ] && [ -f "$ASK" ] && [ -f "$SIM" ] || { echo "tf, plan, ask or simulation absent (plan $([ -f "$PLAN" ] && echo yes || echo no), ask $([ -f "$ASK" ] && echo yes || echo no), simulation $([ -f "$SIM" ] && echo yes || echo no))"; echo "RESULT: FAIL"; exit 1; }
res=$(python3 -I - "$(native "$TF")" "$(native "$PLAN")" "$(native "$ASK")" "$(native "$SIM")" <<'PYEOF'
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
statements = len(re.findall(r'\bSid\s*=', s))
broad = ('"*/silver/"' in s) or ('"*/silver/*"' in s)
sil = re.search(r'FamilyDepthSilverPrefixListOnly.*?(?=FamilyDepthSourceRootListOneLevelOnly|$)', s, re.S)
per_source = bool(sil) and "family_depth_sources" in sil.group(0) and "/*/silver/" in sil.group(0)
m = re.search(r"(\d+) to add, (\d+) to change, (\d+) to destroy", plan)
plan_ok = bool(m) and m.groups() == ("0", "1", "0")
halves = all(re.search(r"(?mi)^#+ .*%s" % h, ask) for h in ("CTO", "COO", "CVO"))
res = sim.get("results") or []
def case(phrase, action, decision):
    return [r for r in res if r.get("action") == action and re.search(phrase, r.get("name", ""), re.I) and r.get("decision") == decision]
checks = [("silver table list under a source allowed", case(r"ALLOWED: silver table list under a source", "s3:ListBucket", "allowed")),
          ("silver list under bloomberg denied", case(r"NEGATIVE: silver list under bloomberg", "s3:ListBucket", "implicitDeny")),
          ("silver list under gateway denied", case(r"NEGATIVE: silver list under gateway", "s3:ListBucket", "implicitDeny")),
          ("silver list under yahoo denied", case(r"NEGATIVE: silver list under yahoo", "s3:ListBucket", "implicitDeny")),
          ("source root with NO delimiter denied", case(r"NEGATIVE: list a source root with NO delimiter", "s3:ListBucket", "implicitDeny")),
          ("source root WITH delimiter allowed", case(r"ALLOWED: list a source root WITH delimiter", "s3:ListBucket", "allowed"))]
sim_ok = sim.get("all_as_expected") is True and all(len(c) >= 1 for _, c in checks)
print("narrowing: the broad globs */silver/ and */silver/* left in the .tf %s (want False); the silver statement is built from family_depth_sources %s (want True); plan names the per-source form %s" % (broad, per_source, "/*/silver/" in plan))
print("simulation all as expected %s; %s" % (sim.get("all_as_expected"), "; ".join("%s %d" % (n, len(c)) for n, c in checks)))
print("terraform: role policies %d (want 1); statements %d (want 4); actions %s (want %s); wildcard action or resource %s (want False); other resource types %d (want 0)" % (policies, statements, actions, want, star, others))
print("plan: 0 to add, 1 to change, 0 to destroy %s; ask has the three halves %s" % (plan_ok, halves))
print("OK" if policies == 1 and statements == 4 and actions == want and not star and others == 0 and plan_ok and halves and not broad and per_source and "/*/silver/" in plan and sim_ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
