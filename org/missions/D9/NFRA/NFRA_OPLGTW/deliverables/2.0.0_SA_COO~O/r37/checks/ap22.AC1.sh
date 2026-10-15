#!/usr/bin/env bash
# OPLGTW OG-ap-22 AC1 (round-37 RIVAL-REL, PHASE A): the re-cut carries exactly the ten rival-funds tools and their hookups and NO Terraform (the read grant is live from OG-ap-20).
#  - W/rv_release.json base_sha is the live ref BEFORE this release (EC2_MANIFEST deployed_commit at HEAD, or previous_deployed_commit once this release is the deployed one);
#  - W/rv_release.json base_sha is the live ref BEFORE this release (EC2_MANIFEST deployed_commit at HEAD, or previous_deployed_commit once this release is the deployed one);
#  - base..release differs only in the allowed set (the two modules and two tests, the five hookup files); no Terraform, no deploy script;
#  - the release's app/tools.py registers all ten tools, and its SAFE_TOOLS and NATIVE_TOOLS carry all ten names.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/rv_release.json"
[ -f "$REC" ] || { echo "rv_release.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" || { echo "release_sha ${rel:-EMPTY} is not a commit here"; echo "RESULT: FAIL"; exit 1; }
read -r dep prev <<<"$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'];print(s.get('deployed_commit','NONE'),s.get('previous_deployed_commit','NONE'))" | tr -d '\r')"
live=$dep; [ "$dep" = "$rel" ] && live=$prev
ALLOW="^$GW/(app/(etfs_rivals|etfs_rivals_flow)\.py|app/tools\.py|app/destructive_ops\.py|app/data_entitlement\.py|tests/test_og_(rv1|rv2)\.py|tests/test_entitlement_admin\.py|tests/test_data_entitlement_family\.py)$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
tf=$(git diff --name-only "$base" "$rel" | grep -c '\.tf$' | tr -d '\r')

read -r r s n <<<"$(python - "$rel" <<'PYEOF2'
import re, subprocess, sys
rel = sys.argv[1]
G = "infra/aws/ec2/opal-gateway/app/"
def show(f):
    return subprocess.run(["git", "show", "%s:%s%s" % (rel, G, f)], capture_output=True).stdout.decode("utf-8", "replace")
names = ["etfs_get_peer_group_members", "etfs_get_rival_fund_holdings", "etfs_who_holds", "etfs_get_security_reference", "etfs_get_coverage", "etfs_get_fund_trades", "etfs_get_fund_flows", "etfs_compare_peers", "etfs_get_research_notes", "etfs_get_rival_page_status"]
tools, safe, native = show("tools.py"), show("destructive_ops.py"), show("data_entitlement.py")
r = sum(1 for x in names if re.search(r"def\s+%s\s*\(" % x, tools))
sa = sum(1 for x in names if '"%s"' % x in safe or "'%s'" % x in safe)
na = sum(1 for x in names if '"%s"' % x in native or "'%s'" % x in native)
print(r, sa, na)
PYEOF2
)"
echo "base ${base:0:10} is the live ref before this release: $([ "$base" = "$live" ] && echo yes || echo no) (manifest ${dep:0:10}/${prev:0:10}); release ${rel:0:10}"
echo "files differing $(printf '%s\n' "$files" | grep -c .); outside the rival-funds set $outside (want 0); terraform files differing $tf (want 0); tools registered $r of 10; SAFE $s of 10; NATIVE $n of 10"
[ "$base" = "$live" ] && [ "$outside" = 0 ] && [ "$tf" = 0 ] && [ "$r" = 10 ] && [ "$s" = 10 ] && [ "$n" = 10 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
