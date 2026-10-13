#!/usr/bin/env bash
# MX-c-8 AC1 (FWD-20, offline): the DEPLOYED gateway's served tools (code and enabled set read at
# services.opal-gateway.deployed_commit in infra/aws/ec2/EC2_MANIFEST.json, never the trunk) each name a catalog index
# in THIS worktree's DATA_CATALOG.yaml, with history depth and freshness each carrying a claim. Instrument c10_index.py.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
dc=$(python -c "import json;print(json.load(open('infra/aws/ec2/EC2_MANIFEST.json',encoding='utf-8'))['services']['opal-gateway']['deployed_commit'])" 2>&1 | tr -d '\r')
git cat-file -e "$dc^{commit}" 2>&1 || { echo "deployed commit '$dc' not in this repo"; echo "RESULT: FAIL"; exit 1; }
en=$(git show "$dc:$GW/deploy-to-ec2.sh" | grep -oE 'ENABLED_INTEGRATIONS="[^"]*"' | head -1 | sed 's/^ENABLED_INTEGRATIONS="//; s/"$//')
[ -n "$en" ] || { echo "no ENABLED_INTEGRATIONS in deploy-to-ec2.sh at $dc"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/mx_r10_c8ac1_$$"; mkdir -p "$T"
git archive "$dc" "$GW/app" | tar -x -C "$T" || { rm -rf "$T"; echo "archive of $dc failed"; echo "RESULT: FAIL"; exit 1; }
echo "deployed_commit=$dc enabled=[$en]"
out=$(timeout 180 python "$(native "$H/c10_index.py")" "$(native "$T/$GW")" "$(native "$(pwd)/$GW/app/refs/DATA_CATALOG.yaml")" "$en" 2>&1 | tr -d '\r'); rc=$?
rm -rf "$T"
printf '%s\n' "$out" | tail -16
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
