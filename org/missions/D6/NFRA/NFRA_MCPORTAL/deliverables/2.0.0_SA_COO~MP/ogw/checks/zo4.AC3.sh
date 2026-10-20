#!/usr/bin/env bash
# MP-zo-4 AC3 (CVO note W1'; PRD v0.10 FWD-26, the gateway side): in the gateway release that is LIVE (EC2_MANIFEST.json
# services.opal-gateway.deployed_commit), admin_api.py mounts admin_people_access.routes and BOTH of that module's handlers
# sit behind owner_only. Read from git at the deployed commit, never the working tree.
. "$(dirname "$0")/../../pd/checks/_root.sh"
dc=$(python -c "import json;print(json.load(open('infra/aws/ec2/EC2_MANIFEST.json'))['services']['opal-gateway']['deployed_commit'])" | tr -d '\r')
G=infra/aws/ec2/opal-gateway/app
mod=$(git show "$dc:$G/admin_people_access.py" 2>/dev/null | tr -d '\r'); [ -n "$mod" ] && have=yes || have=no
mounted=$(git show "$dc:$G/admin_api.py" 2>/dev/null | tr -d '\r' | grep -c 'admin_people_access\.routes')
decor=$(printf '%s\n' "$mod" | grep -c '^@owner_only')
echo "deployed_commit=${dc:0:10}; admin_people_access.py at it: $have; mounted in admin_api.py=$mounted; @owner_only decorators=$decor"
if [ "$have" = yes ] && [ "$mounted" -ge 1 ] && [ "$decor" -ge 2 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
