#!/usr/bin/env bash
# OPLGTW OG-ap-7 AC1 (NFRA_CTLPLN CT-i-11 release, Phase B1): the release in W/ap7_release.json ({"base_sha","release_sha"})
# sits on the live gateway ref c3af8687e4 and carries EXACTLY CT-i-11's gateway hunks as built: git patch-id --stable of
# base..release equals that of 863e37d1f9~1..4d722ff458 over infra/aws/ec2/opal-gateway/. It touches only teams_route.py,
# server.py and tests/test_teams_route.py.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/ap7_release.json"
LIVE=c3af8687e44a1e641259b37f992033ae02cdce3d
[ -f "$REC" ] || { echo "ap7_release.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" || { echo "release_sha ${rel:-EMPTY} is not a commit here"; echo "RESULT: FAIL"; exit 1; }
p_built=$(git diff 863e37d1f9~1 4d722ff458 -- infra/aws/ec2/opal-gateway/ | git patch-id --stable | awk '{print $1}')
p_rel=$(git diff "$base" "$rel" | git patch-id --stable | awk '{print $1}')
files=$(git diff --name-only "$base" "$rel" | tr -d '\r')
ALLOW='^infra/aws/ec2/opal-gateway/(app/teams_route\.py|app/server\.py|tests/test_teams_route\.py)$'
outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
echo "base ${base:0:10} is the live ref c3af8687e4: $([ "$base" = "$LIVE" ] && echo yes || echo no); release ${rel:0:10}"
echo "patch-id built=${p_built:0:12} release=${p_rel:0:12} equal=$([ -n "$p_built" ] && [ "$p_built" = "$p_rel" ] && echo yes || echo no)"
echo "files differing $(printf '%s\n' "$files" | grep -c .); outside CT-i-11's paths $outside (want 0)"
[ "$base" = "$LIVE" ] && [ -n "$p_built" ] && [ "$p_built" = "$p_rel" ] && [ "$outside" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
