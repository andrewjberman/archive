#!/usr/bin/env bash
# OPLGTW OG-ap-28 AC2 (round 38, the batched gateway release, PHASE B): the release landed, its ledger closed, and the SERVED read through the installed code shows every round-38 arm.
# The record W/CODE2_SERVED.json = {"read_at", "live_commit", "health_status": 200, "env_key_count": n, "reader_env_keys_present": 7, "registry_count": 103, "per_tool_good": 27,
#  "host_md5": {"equal": n, "differ": 0}, "tools_list_before": n, "tools_list_after": n, "muse_env_present": false, "arms": {"e4_unit_currency": true, "e5_news_floor": true, "e6_chatter_lag": true, "e8_muse_inert": true, "e9_not_found_404": true,
#  "e10_429_audited": true, "e12_bd49f_live": true}}. Counts and booleans only (no account number, no person's name, no object content).
#  - ledger nfra-oplgtw-gateway-release-batch2 CLOSED with its sentinel gone; the release is current or superseded (the time-anchored landing read of r37/checks/_landed.sh);
#  - health 200; reader_env_keys_present 7 (the six vendor keys plus BLACKDIAMOND49FLIVE_READER_ROLE_ARN); registry count and per_tool_good unchanged (no tool added);
#  - host md5 differ 0; every arm true.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/../../r37/checks/_landed.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
REC="${AP28_SERVED_OVERRIDE:-$W/CODE2_SERVED.json}"
slug=nfra-oplgtw-gateway-release-batch2; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$REC" ] || { echo "CODE2_SERVED.json absent"; echo "RESULT: FAIL"; exit 1; }
rel=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha',''))" "$(native "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/ap28_release.json")" 2>/dev/null | tr -d '\r')
landed=never; [ -n "$rel" ] && landed=$(landed_state "$rel")
[ -n "$AP28_SERVED_OVERRIDE" ] && landed=${AP28_FORCE_LANDED:-$landed}
res=$(python - "$(native "$REC")" <<'PYEOF'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
if isinstance(d.get("body"), dict):
    d = d["body"]
arms = d.get("arms") or {}
need = ["e4_unit_currency", "e5_news_floor", "e6_chatter_lag", "e8_muse_inert", "e9_not_found_404", "e10_429_audited", "e12_bd49f_live"]
armed = [k for k in need if arms.get(k) is True]
md5 = d.get("host_md5") or {}
ok = (d.get("health_status") == 200 and d.get("reader_env_keys_present") == 7 and d.get("registry_count") == 103
      and d.get("per_tool_good") == 27 and md5.get("differ") == 0 and len(armed) == len(need)
      and d.get("tools_list_before") is not None and d.get("tools_list_before") == d.get("tools_list_after")
      and d.get("muse_env_present") is False)
print("tools/list before %s after %s (want equal); MUSE_CLIENT_ID present %s (want False)" % (d.get("tools_list_before"), d.get("tools_list_after"), d.get("muse_env_present")))
print("served: health %s; reader env keys %s of 7; registry %s (want 103); per-tool %s of 27; host md5 differ %s (want 0); arms true %d of %d" % (
      d.get("health_status"), d.get("reader_env_keys_present"), d.get("registry_count"), d.get("per_tool_good"), md5.get("differ"), len(armed), len(need)))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent; landed=$landed"
printf '%s\n' "$res" | sed '$d'
echo "served verdict: $(printf '%s\n' "$res" | tail -1)"
restore_audit
[ "$closed" = 1 ] && [ "$sent" = 0 ] && { [ "$landed" = current ] || [ "$landed" = superseded ]; } && [ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
