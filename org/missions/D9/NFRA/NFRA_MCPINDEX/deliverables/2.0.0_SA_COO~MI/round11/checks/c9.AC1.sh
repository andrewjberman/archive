#!/usr/bin/env bash
# MX-c-9 AC1 (FWD-20 index + durable link key, offline): the DEPLOYED gateway's served tools (code and enabled set read
# at services.opal-gateway.deployed_commit in infra/aws/ec2/EC2_MANIFEST.json) graded on the tree AS IT WILL SHIP: the
# deployed tree with THIS worktree's three shippable files laid over it (the Z-S112 lesson: never the base alone).
# Instrument c11_index.py.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
dc=$(python -c "import json;print(json.load(open('infra/aws/ec2/EC2_MANIFEST.json',encoding='utf-8'))['services']['opal-gateway']['deployed_commit'])" 2>&1 | tr -d '\r')
git cat-file -e "$dc^{commit}" 2>&1 || { echo "deployed commit '$dc' not in this repo"; echo "RESULT: FAIL"; exit 1; }
en=$(git show "$dc:$GW/deploy-to-ec2.sh" | grep -oE 'ENABLED_INTEGRATIONS="[^"]*"' | head -1 | sed 's/^ENABLED_INTEGRATIONS="//; s/"$//')
[ -n "$en" ] || { echo "no ENABLED_INTEGRATIONS in deploy-to-ec2.sh at $dc"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/mx_r11_c9ac1_$$"; mkdir -p "$T"
git archive "$dc" "$GW/app" | tar -x -C "$T" || { rm -rf "$T"; echo "archive of $dc failed"; echo "RESULT: FAIL"; exit 1; }
ov=0
for f in app/refs/DATA_CATALOG.yaml app/integrations/opal_discover/integration.py app/admin_gateway_breakdown.py; do
  cmp -s "$GW/$f" "$T/$GW/$f" || { cp "$GW/$f" "$T/$GW/$f" && ov=$((ov+1)); }
done
echo "deployed_commit=$dc enabled=[$en] overlaid from this worktree: $ov of 3 shippable file(s) differ from the deployed tree"
out=$(timeout 180 python "$(native "$H/c11_index.py")" "$(native "$T/$GW")" "$(native "$T/$GW/app/refs/DATA_CATALOG.yaml")" "$en" 2>&1 | tr -d '\r'); rc=$?
rm -rf "$T"
printf '%s\n' "$out" | tail -16
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
