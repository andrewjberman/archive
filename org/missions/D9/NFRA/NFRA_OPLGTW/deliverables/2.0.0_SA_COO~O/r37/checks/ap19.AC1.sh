#!/usr/bin/env bash
# OPLGTW OG-ap-19 AC1 (round-37 G3-G6, PHASE A): the re-cut carries exactly the G3 and G6 build, its hookups and the two grants' Terraform.
#  - W/g36_release.json base_sha is the live ref BEFORE this release (EC2_MANIFEST deployed_commit at HEAD, or previous_deployed_commit once this release is the deployed one);
#  - base..release differs only in the allowed set (the three modules and four tests, the five hookup files, deploy-to-ec2.sh, the two grant files);
#  - the release's app/tools.py registers all thirteen tools, and its SAFE_TOOLS and NATIVE_TOOLS carry all thirteen names;
#  - the two grants are exactly ONE aws_iam_role_policy each (news_read_iam.tf, portal_tiered_read_iam.tf), no "*" resource, and the G3 policy names only the json-tiered/market-overview/ prefix.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/g36_release.json"
[ -f "$REC" ] || { echo "g36_release.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" || { echo "release_sha ${rel:-EMPTY} is not a commit here"; echo "RESULT: FAIL"; exit 1; }
read -r dep prev <<<"$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'];print(s.get('deployed_commit','NONE'),s.get('previous_deployed_commit','NONE'))" | tr -d '\r')"
live=$dep; [ "$dep" = "$rel" ] && live=$prev
ALLOW="^$GW/(app/(portal_models|portal_macro|news_typed|typed_scope)\.py|app/tools\.py|app/destructive_ops\.py|app/data_entitlement\.py|tests/test_og_(pt1|pt2|nw1|gt6|gt10)\.py|tests/test_entitlement_admin\.py|tests/test_data_entitlement_family\.py|deploy-to-ec2\.sh)$|^infra/aws/terraform/opal-gateway/(news_read_iam|portal_tiered_read_iam)\.tf$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
reg=$(python - "$rel" <<'PYEOF'
import subprocess, sys
rel = sys.argv[1]
names = ['portal_get_model_positioning', 'portal_get_model_attribution', 'portal_get_market_returns', 'portal_get_market_regime', 'portal_get_macro', 'portal_get_valuation', 'portal_get_security_scan', 'portal_get_pipeline_freshness', 'news_search_articles', 'news_trending_topics', 'news_keyword_intelligence', 'news_market_mood', 'news_for_security']
def blob(p):
    return subprocess.run(["git", "show", "%s:infra/aws/ec2/opal-gateway/app/%s" % (rel, p)], capture_output=True).stdout.decode("utf-8", "replace")
t, d, e = blob("tools.py"), blob("destructive_ops.py"), blob("data_entitlement.py")
r = sum(1 for n in names if ("def %s(" % n) in t)
s = sum(1 for n in names if ('"%s"' % n) in d)
n_ = sum(1 for n in names if ('"%s"' % n) in e)
print("%d %d %d" % (r, s, n_))
PYEOF
)
reg=$(printf '%s' "$reg" | tr -d '\r')
read -r r s n <<<"$reg"
g=$(python - "$rel" <<'PYEOF'
import re, subprocess, sys
rel = sys.argv[1]
def blob(p):
    return subprocess.run(["git", "show", "%s:infra/aws/terraform/opal-gateway/%s" % (rel, p)], capture_output=True).stdout.decode("utf-8", "replace")
out = []
for f in ("news_read_iam.tf", "portal_tiered_read_iam.tf"):
    t = blob(f)
    out.append(len(re.findall(r'resource\s+"aws_iam_role_policy"', t)))
    out.append(1 if re.search(r'Resource\s*=\s*(\[\s*)?"\*"', t) else 0)
t = blob("portal_tiered_read_iam.tf")
arns = re.findall(r'arn:aws:s3:::[^"\s]+', t)
only = 1 if arns and all("json-tiered/market-overview/" in a for a in arns) else 0
print(out[0], out[1], out[2], out[3], only)
PYEOF
)
g=$(printf '%s' "$g" | tr -d '\r')
read -r p1 w1 p2 w2 only <<<"$g"
echo "base ${base:0:10} is the live ref before this release: $([ "$base" = "$live" ] && echo yes || echo no) (manifest ${dep:0:10}/${prev:0:10}); release ${rel:0:10}"
echo "files differing $(printf '%s\n' "$files" | grep -c .); outside the G3-G6 set $outside (want 0); tools registered $r of 13; SAFE $s of 13; NATIVE $n of 13"
echo "grants: news_read_iam.tf policies $p1 (want 1), wildcard resource $w1 (want 0); portal_tiered_read_iam.tf policies $p2 (want 1), wildcard resource $w2 (want 0), only the json-tiered/market-overview prefix $([ "$only" = 1 ] && echo yes || echo no)"
[ "$base" = "$live" ] && [ "$outside" = 0 ] && [ "$r" = 13 ] && [ "$s" = 13 ] && [ "$n" = 13 ] && [ "$p1" = 1 ] && [ "$w1" = 0 ] && [ "$p2" = 1 ] && [ "$w2" = 0 ] && [ "$only" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
