#!/usr/bin/env bash
# OPLGTW OG-ap-18 AC2 (round-37 G1-TYPED, PHASE B, landed and served):
#  - ledger nfra-oplgtw-gateway-release-gt is CLOSED at HEAD, its sentinel gone;
#  - the release LANDED (row Z-S119, time-anchored): the manifest's deployed_commit is the release, or recorded it before a later release displaced it; runbook 7.2 (rb.AC2) is graded only while it is the live one;
#  - W/GT_SERVED.json, read on the host through the INSTALLED code: the registry grew by exactly ten, and for each of the ten
#    tools an Opal stand-in principal is served an enveloped answer and a non-Opal principal is refused with zero S3 calls.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/_landed.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
closed=0; sent=0
for slug in nfra-oplgtw-gateway-release-gt; do
  e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
  [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=$((closed+1))
  sent=$((sent + $(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)))
done
rel=NONE; [ -f "$W/gt_release.json" ] && rel=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha','NONE'))" "$(native "$W/gt_release.json")" | tr -d '\r')
dep=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
full() { git rev-parse --verify --quiet "$1^{commit}" 2>&1 | tr -d '\r' | grep -E "^[0-9a-f]{40}$" || printf '%s' "$1"; }
[ "$rel" != NONE ] && rel=$(full "$rel"); [ "$dep" != NONE ] && dep=$(full "$dep")
state=$(landed_state "$rel")
rb=FAIL; bash org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/round2/checks/rb.AC2.sh >/dev/null 2>&1 && rb=PASS
res=$(python - "$(native "$W/GT_SERVED.json")" <<'EOF'
import json, sys
names = ['harvest_resolve_security', 'harvest_security_coverage', 'harvest_get_chatter', 'harvest_search_articles', 'harvest_get_article', 'harvest_get_fundamentals', 'harvest_query_columns', 'harvest_get_research', 'harvest_get_filing_analysis', 'harvest_get_peers_and_scores']
try:
    b = json.load(open(sys.argv[1], encoding="utf-8")).get("body", {})
except Exception:
    b = {}
before, after = b.get("registry_before"), b.get("registry_count")
grew = isinstance(before, int) and isinstance(after, int) and after == before + 10
pt = b.get("per_tool") or {}
good = sum(1 for n in names if isinstance(pt.get(n), dict) and pt[n].get("opal_served") is True and pt[n].get("non_opal_refused") is True and pt[n].get("s3_calls_on_refusal") == 0)
tl = b.get("tools_listed")
listed = isinstance(tl, list) and set(names) <= set(tl)
print("registry %s -> %s (+10); per-tool %d of 10; tools listed %s" % (before, after, good, "yes" if listed else "no"))
print("OK" if grew and good == 10 and listed else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r')
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent"
echo "manifest deployed_commit=${dep:0:10}; release_sha=${rel:0:10}; landed=$state; rb.AC2 $([ "$state" = current ] && echo "$rb" || echo "skipped (superseded)")"
printf '%s\n' "$res" | sed '$d'
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$rel" != NONE ] && { [ "$state" = superseded ] || { [ "$state" = current ] && [ "$rb" = PASS ]; }; } && [ "$(printf '%s\n' "$res" | tail -1)" = OK ] \
  && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
