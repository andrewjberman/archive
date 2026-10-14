#!/usr/bin/env bash
# OPLGTW OG-ap-18 AC1 (round-37 G1-TYPED, PHASE A): the re-cut carries exactly the G1 build and its hookups.
#  - W/gt_release.json base_sha is the live ref BEFORE this release (EC2_MANIFEST deployed_commit at HEAD, or, once this
#    release is the deployed one, its previous_deployed_commit);
#  - base..release differs only in the G1 files and their five hookup files, and OG-gt-5's module is NOT in it;
#  - the release's app/tools.py registers all ten tools, and its SAFE_TOOLS and NATIVE_TOOLS carry all ten names.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/gt_release.json"
[ -f "$REC" ] || { echo "gt_release.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" || { echo "release_sha ${rel:-EMPTY} is not a commit here"; echo "RESULT: FAIL"; exit 1; }
read -r dep prev <<<"$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'];print(s.get('deployed_commit','NONE'),s.get('previous_deployed_commit','NONE'))" | tr -d '\r')"
live=$dep; [ "$dep" = "$rel" ] && live=$prev
ALLOW="^$GW/(app/(harvest_typed|harvest_identity|harvest_press|harvest_figures|harvest_research)\.py|app/tools\.py|app/destructive_ops\.py|app/data_entitlement\.py|tests/test_og_gt[0-4]\.py|tests/test_entitlement_admin\.py|tests/test_data_entitlement_family\.py)$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
pub=no; printf '%s\n' "$files" | grep -q "app/harvest_published\.py" && pub=yes
reg=$(python - "$rel" <<'EOF'
import subprocess, sys
rel = sys.argv[1]
names = ['harvest_resolve_security', 'harvest_security_coverage', 'harvest_get_chatter', 'harvest_search_articles', 'harvest_get_article', 'harvest_get_fundamentals', 'harvest_query_columns', 'harvest_get_research', 'harvest_get_filing_analysis', 'harvest_get_peers_and_scores']
def blob(p):
    return subprocess.run(["git", "show", "%s:infra/aws/ec2/opal-gateway/app/%s" % (rel, p)], capture_output=True).stdout.decode("utf-8", "replace")
t, d, e = blob("tools.py"), blob("destructive_ops.py"), blob("data_entitlement.py")
r = sum(1 for n in names if ("def %s(" % n) in t)
s = sum(1 for n in names if ('"%s"' % n) in d)
n_ = sum(1 for n in names if ('"%s"' % n) in e)
print("%d %d %d" % (r, s, n_))
EOF
)
reg=$(printf '%s' "$reg" | tr -d '\r')
read -r r s n <<<"$reg"
echo "base ${base:0:10} is the live ref before this release: $([ "$base" = "$live" ] && echo yes || echo no) (manifest ${dep:0:10}/${prev:0:10}); release ${rel:0:10}"
echo "files differing $(printf '%s\n' "$files" | grep -c .); outside the G1 set $outside (want 0); tools registered $r of 10; SAFE $s of 10; NATIVE $n of 10; OG-gt-5 module in release: $pub"
[ "$base" = "$live" ] && [ "$outside" = 0 ] && [ "$r" = 10 ] && [ "$s" = 10 ] && [ "$n" = 10 ] && [ "$pub" = no ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
