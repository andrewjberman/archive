#!/usr/bin/env bash
# OPLGTW OG-ap-36 AC2 (round 41, the fifth batched gateway release, PHASE B): the release landed, its ledger closed, the host marker names the release, and the SERVED read shows every arm.
# The record W/CODE6_SERVED.json = {"body": {"read_at", "live_commit", "health_status": 200, "env_key_count": n, "reader_env_keys_present": 7, "registry_count": 103, "per_tool_good": 27,
#  "host_md5": {"equal": n, "differ": 0}, "tools_list_before": n, "tools_list_after": n, "muse_env_present": false, "marker_sha": "<40 hex>",
#  "readback": {"minutes": n, "triggers_fired": 0, "service_window_calls": n},
#  "arms": {"e1_cursor_first_page", "e1_cursor_pages_to_window_start", "e1_within_page_newest_first", "e1_cursor_by_partition", "e8_memory_flat_and_returned",
#           "e9_health_answers_during_a_page", "e10_marker_equals_release_sha", "e11_pages_equal_live_code_row_for_row": bool}}}. Counts and booleans only.
#  - ledger nfra-oplgtw-gateway-release-batch6 CLOSED with its sentinel gone; the release is current or superseded (r37/checks/_landed.sh);
#  - health 200; reader env keys 7; registry count and per_tool_good unchanged; tools/list unchanged; MUSE_CLIENT_ID absent; host md5 differ 0; the marker sha equals the release sha; the read-back ran 30 minutes with no trigger; every arm true.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/../../r37/checks/_landed.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
REC="${AP36_SERVED_OVERRIDE:-$W/CODE6_SERVED.json}"
slug=nfra-oplgtw-gateway-release-batch6; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$REC" ] || { echo "CODE6_SERVED.json absent"; echo "RESULT: FAIL"; exit 1; }
rel=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha',''))" "$(native "${AP36_RELREC_OVERRIDE:-$W/ap36_release.json}")" 2>/dev/null | tr -d '\r')
landed=never; [ -n "$rel" ] && landed=$(landed_state "$rel")
[ -n "$AP36_SERVED_OVERRIDE" ] && landed=${AP36_FORCE_LANDED:-$landed}
res=$(python - "$(native "$REC")" "$rel" <<'PYEOF'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
if isinstance(d.get("body"), dict):
    d = d["body"]
arms = d.get("arms") or {}
need = ["e1_cursor_first_page", "e1_cursor_pages_to_window_start", "e1_within_page_newest_first", "e1_cursor_by_partition", "e8_memory_flat_and_returned",
        "e9_health_answers_during_a_page", "e10_marker_equals_release_sha", "e11_pages_equal_live_code_row_for_row", "e12_refusal_word_reaches_the_caller"]
armed = [k for k in need if arms.get(k) is True]
md5 = d.get("host_md5") or {}
rb = d.get("readback") or {}
marker = bool(sys.argv[2]) and d.get("marker_sha") == sys.argv[2]
# CTO decision 35541 (Z-S375): the served read may grade 26 of 27 ONLY with the one named exception and its row open
exc = d.get("per_tool_exception") or []
tool_ok = d.get("per_tool_good") == 27 or (d.get("per_tool_good") == 26 and exc == ["etfs_compare_peers"] and d.get("exception_row") == "NFRA_OPLGTW-Z-S375")
tool_txt = "27 of 27" if d.get("per_tool_good") == 27 else ("26 of 27 (exception etfs_compare_peers, row Z-S375, CTO 35541)" if tool_ok else "%s of 27 (NOT an accepted shape)" % d.get("per_tool_good"))
hr = d.get("harvest_research_md5") or {}
hex32 = lambda v: isinstance(v, str) and len(v) == 32 and all(c in "0123456789abcdef" for c in v)
hr_ok = hex32(hr.get("host")) and hr.get("host") == hr.get("expected") and hr.get("equal") is True   # the CTO's CT4: a peer's live change is never reverted
rb_ok = isinstance(rb.get("minutes"), (int, float)) and rb["minutes"] >= 30 and rb.get("triggers_fired") == 0 and isinstance(rb.get("service_window_calls"), int)
ok = (d.get("health_status") == 200 and d.get("reader_env_keys_present") == 7 and d.get("registry_count") == 103
      and tool_ok and md5.get("differ") == 0 and len(armed) == len(need) and marker and rb_ok
      and d.get("tools_list_before") is not None and d.get("tools_list_before") == d.get("tools_list_after")
      and d.get("muse_env_present") is False and hr_ok)
print("tools/list before %s after %s (want equal); MUSE_CLIENT_ID present %s (want False); host marker equals the release sha %s" % (
      d.get("tools_list_before"), d.get("tools_list_after"), d.get("muse_env_present"), "yes" if marker else "no"))
print("served: health %s; reader env keys %s of 7; registry %s (want 103); per-tool %s; host md5 differ %s (want 0); arms true %d of %d" % (
      d.get("health_status"), d.get("reader_env_keys_present"), d.get("registry_count"), tool_txt, md5.get("differ"), len(armed), len(need)))
print("harvest_research.py host md5 %s, its 1753c741d9 blob md5 %s; host md5 equals its 1753c741d9 blob: %s" % (hr.get("host"), hr.get("expected"), "yes" if hr_ok else "no"))
print("read-back: %s minutes, triggers fired %s (want 0), /mcp window calls served by the service %s" % (rb.get("minutes"), rb.get("triggers_fired"), rb.get("service_window_calls")))
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
