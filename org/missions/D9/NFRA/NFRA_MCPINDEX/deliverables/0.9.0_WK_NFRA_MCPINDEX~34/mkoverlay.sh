#!/usr/bin/env bash
# Build a dangling commit = the deployed gateway commit's tree + this worktree's two changed gateway app .py files.
set -e
DC=$(python -c "import json;print(json.load(open('infra/aws/ec2/EC2_MANIFEST.json',encoding='utf-8'))['services']['opal-gateway']['deployed_commit'])" | tr -d '')   # A3: the manifest now names b0c75d24f1 (was 7eff14b2e6)
GW=infra/aws/ec2/opal-gateway
export GIT_INDEX_FILE="$(pwd)/.scratch/overlay.index"
rm -f "$GIT_INDEX_FILE"
git read-tree $DC
for f in app/integrations/opal_discover/integration.py app/admin_gateway_breakdown.py; do
  h=$(git hash-object -w "$GW/$f")
  git update-index --cacheinfo 100644,$h,$GW/$f
done
t=$(git write-tree)
c=$(echo "overlay of deployed $DC with the MX-c-9 gateway files" | git commit-tree $t -p $DC)
rm -f "$GIT_INDEX_FILE"
echo $c
