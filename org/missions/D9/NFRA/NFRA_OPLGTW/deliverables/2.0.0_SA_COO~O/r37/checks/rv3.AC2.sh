#!/usr/bin/env bash
# OPLGTW OG-rv-3 AC2 (round-37 RIVAL-HOOKUP, FWD-22): the classification and the bound.
#  - SAFE_TOOLS and NATIVE_TOOLS carry the ten tools names, and DATA_GRANT_TOOLS carries none;
#  - the five files this cell may touch are the only files that differ from the base of this branch (no tool module, no other test);
#  - the non-data family test passes at 96.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
names="etfs_get_peer_group etfs_get_rival_fund_holdings etfs_who_holds etfs_get_security_reference etfs_get_coverage etfs_get_fund_trades etfs_get_fund_flows etfs_compare_peers etfs_get_research_notes etfs_get_rival_page_status"
safe=0; nat=0; grant=0
for n in $names; do
  grep -q "\"$n\"" "$GW/app/destructive_ops.py" && safe=$((safe+1))
  grep -q "\"$n\"" "$GW/app/data_entitlement.py" && nat=$((nat+1))
done
grant=$(python - <<'EOF'
import re
t = open("infra/aws/ec2/opal-gateway/app/data_entitlement.py", encoding="utf-8").read()
m = re.search(r"DATA_GRANT_TOOLS\s*=\s*frozenset\(\{(.*?)\}\)", t, re.S)
body = m.group(1) if m else ""
names = "etfs_get_peer_group etfs_get_rival_fund_holdings etfs_who_holds etfs_get_security_reference etfs_get_coverage etfs_get_fund_trades etfs_get_fund_flows etfs_compare_peers etfs_get_research_notes etfs_get_rival_page_status".split()
print(sum(1 for n in names if ('"%s"' % n) in body))
EOF
)
grant=$(printf '%s' "$grant" | tr -d '\r')
base=$(git merge-base HEAD box/sitez 2>/dev/null | tr -d '\r')
outside=$(git diff --name-only "$base" HEAD | grep -vE "^$GW/(app/tools\.py|app/data_entitlement\.py|app/destructive_ops\.py|tests/test_entitlement_admin\.py|tests/test_data_entitlement_family\.py)$|^org/missions/D9/NFRA/NFRA_OPLGTW/(task-orders|deliverables|surprise-channel)/" | grep -c .)
echo "classified: SAFE $safe of 10, NATIVE $nat of 10, in DATA_GRANT_TOOLS $grant (want 0); files outside this cell's five (and its records) $outside (want 0)"
pytest_named tests/test_data_entitlement_family.py test_ogpf1_ac01; r0=$?
restore_audit
[ "$safe" = 10 ] && [ "$nat" = 10 ] && [ "$grant" = 0 ] && [ "$outside" = 0 ] && [ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
