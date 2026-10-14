#!/usr/bin/env bash
# _landed.sh -- sourced by a release order's AC2 (row Z-S119). "deployed_commit equals release_sha" is a property of being the
# NEWEST release, so it flips to FAIL on work that was graded PASS. landed_state grades the landing with a time anchor:
#   current     the manifest's deployed_commit IS the release;
#   superseded  the manifest recorded the release as its deployed_commit at some commit of this history (a later release displaced it);
#   never       neither.
landed_state() {
  local rel="$1" dep c d
  dep=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
  [ "$dep" = "$rel" ] && { echo current; return; }
  for c in $(git log --format=%H -S"$rel" -- infra/aws/ec2/EC2_MANIFEST.json); do
    d=$(git show "$c:infra/aws/ec2/EC2_MANIFEST.json" | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
    [ "$d" = "$rel" ] && { echo superseded; return; }
  done
  echo never
}
