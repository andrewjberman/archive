#!/usr/bin/env bash
# OPLGTW OG-yr-1 AC2 (round-37 YEARINREVIEW, PHASE B, landed and served):
#  - ledger nfra-oplgtw-gateway-release-yr is CLOSED at HEAD, its sentinel gone;
#  - the release LANDED (row Z-S119, time-anchored via _landed.sh);
#  - W/YR_SERVED.json: the page served by the installed host equals the source (md5) and carries the data date "2026-10-11"; the public endpoint's md5 is recorded (equal, or gated with the reason).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/_landed.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
closed=0; sent=0; slug=nfra-oplgtw-gateway-release-yr
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
rel=NONE; [ -f "$W/yr_release.json" ] && rel=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha','NONE'))" "$(native "$W/yr_release.json")" | tr -d '\r')
state=$(landed_state "$rel")
res=$(python - "$(native "$W/YR_SERVED.json")" <<'PY'
import json, sys
try:
    b = json.load(open(sys.argv[1], encoding="utf-8")).get("body", {})
except Exception:
    b = {}
src, host = b.get("md5_source"), b.get("md5_served_host")
eq = src == "0d828b51d433a24f7e2ef2e6ea7967ee" and src == host
until = b.get("contains_until_2026_10_11") is True
op = b.get("opal_user_admitted") is True and b.get("guest_refused") is True
pub = b.get("public_md5_equal") is True or (b.get("public_md5_equal") is False and bool(b.get("public_note")))
print("served page: host md5 equals the source %s; carries the data date 2026-10-11 %s; an Opal user is admitted and a guest refused %s; public endpoint recorded %s" % ("yes" if eq else "no", "yes" if until else "no", "yes" if op else "no", "yes" if pub else "no"))
print("OK" if eq and until and op and pub else "NO")
PY
)
res=$(printf '%s' "$res" | tr -d '\r')
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent"
echo "release_sha=${rel:0:10}; landed=$state"
printf '%s\n' "$res" | sed '$d'
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$rel" != NONE ] && { [ "$state" = current ] || [ "$state" = superseded ]; } && [ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
