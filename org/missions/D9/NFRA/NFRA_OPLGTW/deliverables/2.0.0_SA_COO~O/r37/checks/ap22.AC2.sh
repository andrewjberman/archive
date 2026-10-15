#!/usr/bin/env bash
# OPLGTW OG-ap-22 AC2 (round-37 RIVAL-REL, PHASE B, landed and served):
#  - ledger nfra-oplgtw-gateway-release-rv is CLOSED at HEAD, its sentinel gone;
#  - the release LANDED (row Z-S119, time-anchored via _landed.sh);
#  - W/RV_SERVED.json, read on the host through the INSTALLED code: the grant of OG-ap-20 is still live in IAM (read-back),
#    the registry grew by exactly ten, and for each of the ten an Opal stand-in principal is served an enveloped answer and a non-Opal principal is refused with zero reads.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/_landed.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
slug=nfra-oplgtw-gateway-release-rv; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
rel=NONE; [ -f "$W/rv_release.json" ] && rel=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha','NONE'))" "$(native "$W/rv_release.json")" | tr -d '\r')
state=$(landed_state "$rel")
res=$(python - "$(native "$W/RV_SERVED.json")" <<'PYEOF'
import json, sys
names = ['etfs_get_peer_group_members', 'etfs_get_rival_fund_holdings', 'etfs_who_holds', 'etfs_get_security_reference', 'etfs_get_coverage', 'etfs_get_fund_trades', 'etfs_get_fund_flows', 'etfs_compare_peers', 'etfs_get_research_notes', 'etfs_get_rival_page_status']
try:
    b = json.load(open(sys.argv[1], encoding="utf-8")).get("body", {})
except Exception:
    b = {}
before, after = b.get("registry_before"), b.get("registry_count")
grew = isinstance(before, int) and isinstance(after, int) and after == before + 10
pt = b.get("per_tool") or {}
good = sum(1 for n in names if isinstance(pt.get(n), dict) and pt[n].get("opal_served") is True and pt[n].get("non_opal_refused") is True and pt[n].get("reads_on_refusal") == 0)
pol = b.get("policies_live") is True and b.get("page_status_manifest_read") is True and (b.get("trades_rows_returned") or 0) > 0
print("registry %s -> %s (+10); per-tool %d of 10; grant live in IAM %s" % (before, after, good, "yes" if pol else "no"))
print("OK" if grew and good == 10 and pol else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent"
echo "release_sha=${rel:0:10}; landed=$state"
printf '%s\n' "$res" | sed '$d'
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$rel" != NONE ] && { [ "$state" = current ] || [ "$state" = superseded ]; } && [ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
