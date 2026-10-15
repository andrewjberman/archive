#!/usr/bin/env bash
# OPLGTW OG-ap-21 AC2 (round-37 PERSON-ROLES, PHASE B, landed and served):
#  - ledger nfra-oplgtw-gateway-release-p21 is CLOSED at HEAD, its sentinel gone; the release LANDED (row Z-S119, time-anchored);
#  - W/P21_SERVED.json, read on the host through the INSTALLED code: the old instance-role news and invoke statements are GONE from IAM and the two internal-reader statements are live;
#    the five news tools and the published-analysis tool are served to an Opal stand-in through the internal role and refuse a non-Opal with zero reads/invokes;
#    the person reader answers (no record = today's behaviour; a stub record with stopped true denies; fail closed on an unreadable record), registry +1;
#    test_grant_writer_stages_the_contract_only_from_the_standard reads GREEN at the new deployed commit.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/_landed.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
slug=nfra-oplgtw-gateway-release-p21; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
rel=NONE; [ -f "$W/p21_release.json" ] && rel=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha','NONE'))" "$(native "$W/p21_release.json")" | tr -d '\r')
state=$(landed_state "$rel")
res=$(python - "$(native "$W/P21_SERVED.json")" <<'PYEOF'
import json, sys
try:
    b = json.load(open(sys.argv[1], encoding="utf-8")).get("body", {})
except Exception:
    b = {}
before, after = b.get("registry_before"), b.get("registry_count")
grew = isinstance(before, int) and isinstance(after, int) and after == before + 1
old_gone = b.get("old_instance_role_statements_gone") is True
new_live = b.get("internal_reader_statements_live") is True
tools_ok = b.get("news_and_published_served_through_internal_role") is True and b.get("non_opal_refused_zero_reads") is True
person = b.get("person_reader_arms_ok") is True
stage = b.get("contract_staging_test_green") is True
print("registry %s -> %s (+1); old instance-role statements gone %s; internal-reader statements live %s; six tools served via the internal role and refused with zero reads %s; person reader arms %s; contract-staging test green %s" % (
    before, after, "yes" if old_gone else "no", "yes" if new_live else "no", "yes" if tools_ok else "no", "yes" if person else "no", "yes" if stage else "no"))
print("OK" if grew and old_gone and new_live and tools_ok and person and stage else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent"
echo "release_sha=${rel:0:10}; landed=$state"
printf '%s\n' "$res" | sed '$d'
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$rel" != NONE ] && { [ "$state" = current ] || [ "$state" = superseded ]; } && [ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
