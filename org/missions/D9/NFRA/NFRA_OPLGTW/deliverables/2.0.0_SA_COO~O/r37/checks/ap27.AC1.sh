#!/usr/bin/env bash
# OPLGTW OG-ap-27 AC1 (round-37, PHASE A): the internal reader role gets the four read grants the OG-ap-23 served read found missing (row Z-S164).
#  - infra/aws/terraform/opal-gateway/gateway_release_gap_read_iam.tf holds exactly TWO aws_iam_role_policy resources, both on the internal reader role;
#  - actions are only s3:GetObject and s3:ListBucket; every ListBucket statement carries an s3:prefix condition; no "*" resource, no bucket-root object ARN;
#  - the four required prefix stems each appear in a GetObject resource AND in a ListBucket s3:prefix value;
#  - the targeted plan reads "2 to add, 0 to change, 0 to destroy"; the ask for three halves exists.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
TF="infra/aws/terraform/opal-gateway/gateway_release_gap_read_iam.tf"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS"
[ -f "$TF" ] && [ -f "$W/GAP_PLAN.txt" ] && [ -f "$W/NEVER_WIDEN_ASK_OG-ap-27.md" ] || { echo "tf, plan or ask absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$TF")" "$(native "$W/GAP_PLAN.txt")" "$(native "$W/NEVER_WIDEN_ASK_OG-ap-27.md")" <<'PYEOF'
import re, sys
tf = open(sys.argv[1], encoding="utf-8").read()
plan = open(sys.argv[2], encoding="utf-8", errors="replace").read()
ask = open(sys.argv[3], encoding="utf-8").read()
stripped = re.sub(r"(?m)^\s*#.*$", "", tf)
blocks = re.findall(r'resource\s+"aws_iam_role_policy"\s+"[^"]+"\s*\{(.*?)\n\}', stripped, re.S)
roles = [re.search(r'(?m)^\s*role\s*=\s*(\S+)', b) for b in blocks]
internal = len(blocks) == 2 and all(r and re.search(r"int(ernal)?_?reader", r.group(1), re.I) and "aws_iam_role.gw." not in r.group(1) for r in roles)
actions = sorted(set(a for a in re.findall(r'"(s3:[A-Za-z*]+)"', stripped) if a != "s3:prefix"))
actions_ok = actions == ["s3:GetObject", "s3:ListBucket"]
star = bool(re.search(r'Resource\s*=\s*"\*"|Resource\s*=\s*\[\s*"\*"', stripped)) or "s3:*" in stripped
root_obj = bool(re.search(r'arn:aws:s3:::opal-data-(?:etfs|mdpf)/\*"', stripped))
list_cond = all("s3:prefix" in s for s in re.findall(r'\{[^{}]*s3:ListBucket[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', stripped)) and "s3:prefix" in stripped
stems = ["bbg/", "snapshots/", "mdpf/etfs/gold/new_securities/", "mdpf/feeds/model_composition/"]
obj_res = re.findall(r'"arn:aws:s3:::opal-data-(?:etfs|mdpf)/([^"]*)"', stripped)
pref_vals = re.findall(r'"([A-Za-z0-9_./-]+/\*)"', stripped)
obj_ok = all(any(r.startswith(s) for r in obj_res) for s in stems)
pref_ok = all(any(p.startswith(s) for p in pref_vals) for s in stems)
pm = re.search(r"(\d+) to add, (\d+) to change, (\d+) to destroy", plan)
plan_ok = bool(pm) and pm.groups() == ("2", "0", "0")
halves = all(re.search(r"(?mi)^#+ .*%s" % h, ask) for h in ("CTO", "COO", "CVO"))
print("terraform: policies %d (want 2); both on the internal reader %s; actions %s; wildcard %s (want False); bucket-root object arn %s (want False)" % (len(blocks), internal, actions, star, root_obj))
print("prefixes: four stems in GetObject resources %s; in ListBucket s3:prefix values %s; list confined %s" % (obj_ok, pref_ok, list_cond))
print("plan: 2 to add, 0 to change, 0 to destroy %s; ask has the three halves %s" % (plan_ok, halves))
print("OK" if internal and actions_ok and not star and not root_obj and obj_ok and pref_ok and list_cond and plan_ok and halves else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
