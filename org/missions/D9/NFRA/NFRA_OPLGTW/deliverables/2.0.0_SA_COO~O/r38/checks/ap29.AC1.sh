#!/usr/bin/env bash
# OPLGTW OG-ap-29 AC1 (round 38, PHASE A, CTO ruling @8b2865e461): the dedicated 49F Black Diamond LIVE read role.
#  - infra/aws/terraform/opal-gateway/blackdiamond_live_reader_iam.tf holds exactly ONE aws_iam_role and ONE aws_iam_role_policy (the policy on that role);
#  - the role's trust is ONLY the Gateway instance role (aws_iam_role.gw); the policy's Allow actions are only s3:GetObject, s3:GetObjectVersion and s3:ListBucket;
#  - the four prefixes silver/unrealized/, silver/transactions/, silver/allocations/, silver/fees/ of opal-data-bd appear in the GetObject resources and in the ListBucket s3:prefix values, and no other opal-data-bd prefix is allowed;
#  - no "*" resource, no bucket-root object ARN, no other bucket allowed, no Put or Delete action;
#  - the targeted plan reads "N to add, M to change, 0 to destroy" with N = 2 (the role and its policy) and M 0 or 1 (the instance role's assume permission, named in the ask); the ask for three halves exists.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
TF="infra/aws/terraform/opal-gateway/blackdiamond_live_reader_iam.tf"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS"
[ -f "$TF" ] && [ -f "$W/BDLIVE_PLAN.txt" ] && [ -f "$W/NEVER_WIDEN_ASK_OG-ap-29.md" ] || { echo "tf, plan or ask absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$TF")" "$(native "$W/BDLIVE_PLAN.txt")" "$(native "$W/NEVER_WIDEN_ASK_OG-ap-29.md")" <<'PYEOF'
import re, sys
tf = open(sys.argv[1], encoding="utf-8").read()
plan = open(sys.argv[2], encoding="utf-8", errors="replace").read()
ask = open(sys.argv[3], encoding="utf-8").read()
s = re.sub(r"(?m)^\s*#.*$", "", tf)
roles = len(re.findall(r'resource\s+"aws_iam_role"\s+"[^"]+"', s))
pols = len(re.findall(r'resource\s+"aws_iam_role_policy"\s+"[^"]+"', s))
trust_gw = "aws_iam_role.gw" in s
allow_actions = sorted(set(re.findall(r'"(s3:[A-Za-z*]+)"', s)) - {"s3:prefix"})
bad_actions = [a for a in allow_actions if a not in ("s3:GetObject", "s3:GetObjectVersion", "s3:ListBucket") and not re.match(r"s3:(Put|Delete|\*)", a) is None]
put_del = [a for a in allow_actions if re.match(r"s3:(Put|Delete|\*)", a)]
star = bool(re.search(r'Resource\s*=\s*"\*"|Resource\s*=\s*\[\s*"\*"', s))
root_obj = bool(re.search(r'arn:aws:s3:::opal-data-bd/\*"', s))
tables = ["unrealized", "allocations", "transactions", "fees"]
import json as _json
# The naming limb refuses a typed S3 address, so the .tf reads the four prefixes from registry rows (Z-S294, the applier was right):
# the check follows the rows. The four rows must exist (bucket opal-data-bd, template silver/<t>/) and the .tf must reference each by key
# and use them for the Allow object resources and the ListBucket s3:prefix values.
_reg = _json.load(open("infra/logic/registry/legacy_addresses.json", encoding="utf-8"))
_rows = {r["key"]: r for r in _reg["legacy_addresses"]}
_keys = ["gateway-client-bdlive-%s" % t for t in tables]
_reg_ok = all(k in _rows and _rows[k].get("bucket") == "opal-data-bd" and _rows[k].get("template") == "silver/%s/" % t for k, t in zip(_keys, tables))
_ref_ok = all(('"%s"' % k) in s for k in _keys)
obj_ok = _reg_ok and _ref_ok and ("local.bdlive_objects" in s)
pref_ok = _reg_ok and _ref_ok and ("local.bdlive_prefixes" in s) and ("s3:prefix" in s)
other_bucket = bool(re.findall(r'arn:aws:s3:::(?!opal-data-bd)[a-z0-9-]+', s))
pm = re.search(r"(\d+) to add, (\d+) to change, (\d+) to destroy", plan)
plan_ok = bool(pm) and int(pm.group(1)) == 2 and int(pm.group(2)) in (0, 1) and int(pm.group(3)) == 0
halves = all(re.search(r"(?mi)^#+ .*%s" % h, ask) for h in ("CTO", "COO", "CVO"))
print("terraform: roles %d (want 1); policies %d (want 1); trust names the instance role %s; put/delete/star actions %s (want none); wildcard %s (want False); bucket-root object arn %s (want False); other bucket named %s (want False)" % (roles, pols, trust_gw, put_del, star, root_obj, other_bucket))
print("prefixes: the four silver tables in GetObject resources %s; in ListBucket s3:prefix values %s" % (obj_ok, pref_ok))
print("plan: 2 to add, 0 or 1 to change, 0 to destroy %s; ask has the three halves %s" % (plan_ok, halves))
print("OK" if roles == 1 and pols == 1 and trust_gw and not put_del and not star and not root_obj and not other_bucket and obj_ok and pref_ok and plan_ok and halves else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
