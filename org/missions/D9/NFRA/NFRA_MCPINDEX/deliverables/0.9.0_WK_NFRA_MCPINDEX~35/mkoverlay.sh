#!/usr/bin/env bash
# Build a dangling commit = the deployed gateway commit's tree + this worktree's changed gateway app file(s) (MX-c-10: opal_discover/integration.py).
# Adapted from round 11's mkoverlay.sh (deliverables/0.9.0_WK_NFRA_MCPINDEX~34/). Prints the commit sha.
set -e
DC=$(python -c "import json;print(json.load(open('infra/aws/ec2/EC2_MANIFEST.json',encoding='utf-8'))['services']['opal-gateway']['deployed_commit'])" | tr -d '\r')
GW=infra/aws/ec2/opal-gateway
export GIT_INDEX_FILE="$(pwd)/.scratch/overlay.index"
rm -f "$GIT_INDEX_FILE"
git read-tree $DC
for f in app/integrations/opal_discover/integration.py; do
  h=$(git hash-object -w "$GW/$f")
  git update-index --cacheinfo 100644,$h,$GW/$f
done
t=$(git write-tree)
c=$(echo "overlay of deployed $DC with the MX-c-10 gateway files" | git commit-tree $t -p $DC)
rm -f "$GIT_INDEX_FILE"
echo $c
