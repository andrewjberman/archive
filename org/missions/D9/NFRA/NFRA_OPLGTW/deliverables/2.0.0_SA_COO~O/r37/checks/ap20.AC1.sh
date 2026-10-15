#!/usr/bin/env bash
# OPLGTW OG-ap-20 AC1 (round-37 G5A-CV, PHASE A): the re-cut carries exactly the G5 wave A and category-views build, its hookups and the two grants' Terraform.
#  - W/g5a_release.json base_sha is the live ref BEFORE this release (EC2_MANIFEST deployed_commit at HEAD, or previous_deployed_commit once this release is the deployed one);
#  - base..release differs only in the allowed set (the three modules and four tests, the five hookup files, deploy-to-ec2.sh, the two grant files);
#  - the release's app/tools.py registers all six tools, and its SAFE_TOOLS and NATIVE_TOOLS carry all six names;
#  - the grant is exactly ONE aws_iam_role_policy (etfs_read_iam.tf): no "*" resource, only opal-data-etfs, the rival-funds gold and page prefixes of PRD v3.7 named, no Put or Delete.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/g5a_release.json"
[ -f "$REC" ] || { echo "g5a_release.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" || { echo "release_sha ${rel:-EMPTY} is not a commit here"; echo "RESULT: FAIL"; exit 1; }
read -r dep prev <<<"$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'];print(s.get('deployed_commit','NONE'),s.get('previous_deployed_commit','NONE'))" | tr -d '\r')"
live=$dep; [ "$dep" = "$rel" ] && live=$prev
ALLOW="^$GW/(app/(etfs_ownership|etfs_funds|portal_mdpf)\.py|app/tools\.py|app/destructive_ops\.py|app/data_entitlement\.py|tests/test_og_(et1|et2|pt5)\.py|tests/test_entitlement_admin\.py|tests/test_data_entitlement_family\.py|deploy-to-ec2\.sh)$|^infra/aws/terraform/opal-gateway/etfs_read_iam\.tf$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
reg=$(python - "$rel" <<'PYEOF'
import re, subprocess, sys
rel = sys.argv[1]
t = subprocess.run(["git", "show", "%s:infra/aws/terraform/opal-gateway/etfs_read_iam.tf" % rel], capture_output=True).stdout.decode("utf-8", "replace")
pol = len(re.findall(r'resource\s+"aws_iam_role_policy"', t))
wild = 1 if re.search(r'Resource\s*=\s*(\[\s*)?"\*"', t) else 0
arns = re.findall(r'arn:aws:s3:::[^"\s]+', t)
only = 1 if arns and all(a.startswith("arn:aws:s3:::opal-data-etfs") for a in arns) else 0
rival = 1 if any("rivalfunds/etfs/gold/" in a for a in arns) else 0
page = 1 if any("rivalfunds/etfs/platinum/page/" in a for a in arns) else 0
put = 1 if re.search(r's3:(Put|Delete)', t) else 0
print(pol, wild, only, rival, page, put)
PYEOF
)
g=$(printf '%s' "$g" | tr -d '\r')
read -r p1 w1 only rival page put <<<"$g"
echo "base ${base:0:10} is the live ref before this release: $([ "$base" = "$live" ] && echo yes || echo no) (manifest ${dep:0:10}/${prev:0:10}); release ${rel:0:10}"
echo "files differing $(printf '%s\n' "$files" | grep -c .); outside the G5A set $outside (want 0); tools registered $r of 6; SAFE $s of 6; NATIVE $n of 6"
echo "grant: etfs_read_iam.tf policies $p1 (want 1), wildcard resource $w1 (want 0), only opal-data-etfs $([ "$only" = 1 ] && echo yes || echo no), rival-funds gold prefix $([ "$rival" = 1 ] && echo yes || echo no), rival-funds page prefix $([ "$page" = 1 ] && echo yes || echo no), put or delete actions $put (want 0)"
[ "$base" = "$live" ] && [ "$outside" = 0 ] && [ "$r" = 6 ] && [ "$s" = 6 ] && [ "$n" = 6 ] && [ "$p1" = 1 ] && [ "$w1" = 0 ] && [ "$only" = 1 ] && [ "$rival" = 1 ] && [ "$page" = 1 ] && [ "$put" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
