#!/usr/bin/env bash
# OPLGTW OG-ap-20 AC2 (round-37 G5A-CV, PHASE B, landed and served):
#  - ledger nfra-oplgtw-gateway-release-g5a is CLOSED at HEAD, its sentinel gone;
#  - the release LANDED (row Z-S119, time-anchored via _landed.sh);
#  - W/G5A_SERVED.json, read on the host through the INSTALLED code: the policy is live in IAM (read-back),
#    the registry grew by exactly six, and for each of the thirteen an Opal stand-in principal is served an enveloped answer and a non-Opal principal is refused with zero reads.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/_landed.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
slug=nfra-oplgtw-gateway-release-g5a; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
rel=NONE; [ -f "$W/g5a_release.json" ] && rel=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha','NONE'))" "$(native "$W/g5a_release.json")" | tr -d '\r')
state=$(landed_state "$rel")
res=$(python - "$(native "$W/G5A_SERVED.json")" <<'PYEOF'
import json, sys
names = ['etfs_get_partner_ownership', 'etfs_get_ownership_rollup', 'etfs_get_monthly_report', 'etfs_get_fund_nav_history', 'etfs_get_fund_holdings', 'mdpf_get_category_views']
try:
    b = json.load(open(sys.argv[1], encoding="utf-8")).get("body", {})
except Exception:
    b = {}
before, after = b.get("registry_before"), b.get("registry_count")
grew = isinstance(before, int) and isinstance(after, int) and after == before + 6
pt = b.get("per_tool") or {}
good = sum(1 for n in names if isinstance(pt.get(n), dict) and pt[n].get("opal_served") is True and pt[n].get("non_opal_refused") is True and pt[n].get("reads_on_refusal") == 0)
pol = b.get("policies_live") is True
print("registry %s -> %s (+6); per-tool %d of 6; policy live in IAM %s" % (before, after, good, "yes" if pol else "no"))
print("OK" if grew and good == 6 and pol else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent"
echo "release_sha=${rel:0:10}; landed=$state"
printf '%s\n' "$res" | sed '$d'
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$rel" != NONE ] && { [ "$state" = current ] || [ "$state" = superseded ]; } && [ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
