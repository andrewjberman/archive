#!/usr/bin/env bash
# OPLGTW OG-ap-6 AC2 (NEVER-2, Phase B2): both acts are landed and closed -- the policy ledger nfra-oplgtw-e2-put-policy
# and the deploy ledger nfra-oplgtw-gateway-release-e2 are each committed CLOSED at HEAD with their sentinels gone -- and
# EC2_MANIFEST's opal-gateway deployed_commit at HEAD is the re-cut release the applier recorded in W/ap6_release.json.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/ap6_release.json"
ok=1
for slug in nfra-oplgtw-e2-put-policy nfra-oplgtw-gateway-release-e2; do
  entries=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${slug}_deploy_completion\.md$")
  e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
  closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
  sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
  echo "$slug: entries at HEAD $entries; status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
  [ "$entries" -ge 1 ] && [ "$closed" = yes ] && [ "$sent" = 0 ] || ok=0
done
rel=NONE; [ -f "$REC" ] && rel=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha','NONE'))" "$(native "$REC")" | tr -d '\r')
dep=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
echo "manifest deployed_commit=${dep:0:10}; applier's release_sha=${rel:0:10}; equal=$([ "$dep" = "$rel" ] && echo yes || echo no)"
[ "$ok" = 1 ] && [ "$rel" != NONE ] && [ "$dep" = "$rel" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
