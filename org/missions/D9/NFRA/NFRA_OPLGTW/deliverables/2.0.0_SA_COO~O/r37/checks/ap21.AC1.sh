#!/usr/bin/env bash
# OPLGTW OG-ap-21 AC1 (round-37 PERSON-ROLES, PHASE A): the re-cut carries exactly the person reader, the two role moves and the published-analysis tool.
#  - W/p21_release.json base_sha is the live ref BEFORE this release (EC2_MANIFEST deployed_commit at HEAD, or previous_deployed_commit once this release is the deployed one);
#  - base..release differs only in the allowed set (the app modules, tests, both contract copies, deploy-to-ec2.sh, the Terraform below);
#  - harvest_get_published_analysis is registered, SAFE and NATIVE in the release;
#  - the release's person reader exists (data_entitlement.person_access) and both identity-scope floors call person_widens;
#  - Terraform: news_read_internal_iam.tf is ONE policy on aws_iam_role.int_reader (Query and GetItem, four named resources, no "*"); harvest_published_invoke_iam.tf targets aws_iam_role.int_reader and names ONE function ARN; no Put/Delete/Scan action anywhere in them.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/p21_release.json"
[ -f "$REC" ] || { echo "p21_release.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" || { echo "release_sha ${rel:-EMPTY} is not a commit here"; echo "RESULT: FAIL"; exit 1; }
read -r dep prev <<<"$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'];print(s.get('deployed_commit','NONE'),s.get('previous_deployed_commit','NONE'))" | tr -d '\r')"
live=$dep; [ "$dep" = "$rel" ] && live=$prev
ALLOW="^$GW/(app/(access_state|data_entitlement|destructive_ops|tools|internal_role|news_typed|harvest_published)\.py|app/integrations/base\.py|deploy/NFRA_OPLGTW_CONTRACT\.json|deploy-to-ec2\.sh|tests/test_(og_cp1|og_nw2|og_gt5|og_gt13|access_state|admin_people_access|entitlement_admin|data_entitlement_family)\.py)$|^org/standards/NFRA_OPLGTW_CONTRACT\.json$|^infra/aws/terraform/opal-gateway/(news_read_internal_iam|harvest_published_invoke_iam|news_read_iam)\.tf$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
res=$(python - "$rel" <<'PYEOF'
import re, subprocess, sys
rel = sys.argv[1]
def blob(p):
    return subprocess.run(["git", "show", "%s:%s" % (rel, p)], capture_output=True).stdout.decode("utf-8", "replace")
GWP = "infra/aws/ec2/opal-gateway/"
n = "harvest_get_published_analysis"
reg = 1 if ("def %s(" % n) in blob(GWP + "app/tools.py") else 0
safe = 1 if ('"%s"' % n) in blob(GWP + "app/destructive_ops.py") else 0
nat = 1 if ('"%s"' % n) in blob(GWP + "app/data_entitlement.py") else 0
de = blob(GWP + "app/data_entitlement.py")
reader = 1 if "def person_access(" in de and "def person_widens(" in de else 0
floors = (1 if "person_widens" in blob(GWP + "app/tools.py") else 0) + (1 if "person_widens" in blob(GWP + "app/integrations/base.py") else 0)
TF = "infra/aws/terraform/opal-gateway/"
nw = blob(TF + "news_read_internal_iam.tf")
inv = blob(TF + "harvest_published_invoke_iam.tf")
nw_pol = len(re.findall(r'resource\s+"aws_iam_role_policy"', nw))
nw_role = 1 if "aws_iam_role.int_reader" in nw and "aws_iam_role.gw" not in nw else 0
nw_act = 1 if re.search(r'"dynamodb:Query"', nw) and re.search(r'"dynamodb:GetItem"', nw) else 0
nw_res = len(re.findall(r'arn:aws:dynamodb:[^"\s]+', nw))
inv_role = 1 if "aws_iam_role.int_reader" in inv and "aws_iam_role.gw.id" not in inv else 0
inv_one = len(re.findall(r'function:[A-Za-z0-9_-]+', inv))
bad = 1 if re.search(r'dynamodb:(Put|Delete|Update|Scan|Batch)|lambda:(Create|Update|Delete)|s3:(Put|Delete)', nw + inv) else 0
wild = 1 if re.search(r'Resource\s*=\s*(\[\s*)?"\*"', nw + inv) else 0
print(reg, safe, nat, reader, floors, nw_pol, nw_role, nw_act, nw_res, inv_role, inv_one, bad, wild)
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
read -r reg safe nat reader floors nw_pol nw_role nw_act nw_res inv_role inv_one bad wild <<<"$res"
echo "base ${base:0:10} is the live ref before this release: $([ "$base" = "$live" ] && echo yes || echo no) (manifest ${dep:0:10}/${prev:0:10}); release ${rel:0:10}"
echo "files differing $(printf '%s\n' "$files" | grep -c .); outside the PERSON-ROLES set $outside (want 0); published-analysis tool registered $reg, SAFE $safe, NATIVE $nat; person reader present $reader, floors calling person_widens $floors of 2"
echo "terraform: news policy count $nw_pol (want 1) on the internal reader $nw_role, Query+GetItem $nw_act, resources $nw_res (want 4); invoke policy on the internal reader $inv_role, function ARNs $inv_one (want 1); forbidden actions $bad (want 0), wildcard resource $wild (want 0)"
[ "$base" = "$live" ] && [ "$outside" = 0 ] && [ "$reg" = 1 ] && [ "$safe" = 1 ] && [ "$nat" = 1 ] && [ "$reader" = 1 ] && [ "$floors" = 2 ] && [ "$nw_pol" = 1 ] && [ "$nw_role" = 1 ] && [ "$nw_act" = 1 ] && [ "$nw_res" = 4 ] && [ "$inv_role" = 1 ] && [ "$inv_one" = 1 ] && [ "$bad" = 0 ] && [ "$wild" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
