#!/usr/bin/env bash
# OPLGTW OG-ap-4 AC1 (NEVER-2): the allowlist deploy's ledger nfra-oplgtw-og-tl-1-allowlist is committed CLOSED at HEAD with
# its sentinel gone, and EC2_MANIFEST's opal-gateway deployed_commit at HEAD is no longer r29 91811b648a nor MP-x-4's base
# alone -- it is the release the applier recorded in W/ap4_release.json ({"release_sha"}).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
slug=nfra-oplgtw-og-tl-1-allowlist
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/ap4_release.json"
entries=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${slug}_deploy_completion\.md$")
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
rel=NONE; [ -f "$REC" ] && rel=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha','NONE'))" "$(native "$REC")" | tr -d '\r')
dep=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
echo "$slug: entries at HEAD $entries; status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
echo "manifest deployed_commit=${dep:0:10}; applier's release_sha=${rel:0:10}; equal=$([ "$dep" = "$rel" ] && echo yes || echo no)"
[ "$entries" -ge 1 ] && [ "$closed" = yes ] && [ "$sent" = 0 ] && [ "$rel" != NONE ] && [ "$dep" = "$rel" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
