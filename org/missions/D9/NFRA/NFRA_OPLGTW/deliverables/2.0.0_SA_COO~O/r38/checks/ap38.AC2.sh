#!/usr/bin/env bash
# OPLGTW OG-ap-38 AC2 (round 41, the sixth batched gateway release, PHASE B): the release landed, the ledger closed AFTER the host clock and failed units were read, the unit's limits are ACTIVE, the call that ran away is bounded on the installed code,
# and the 27-tool served read passes 27 of 27 under a hard guard (the hazard Z-S375 is repaired).
# Record W/CODE7_SERVED.json = {"body": {"read_at", "live_commit", "health_status": 200, "env_key_count": 65, "reader_env_keys_present": 7, "registry_count": 103, "per_tool_good": 27, "harness_guard": "oom_score_adj_1000_rlimit_as_1400mb",
#  "host_md5": {"equal": n, "differ": 0}, "tools_list_before": n, "tools_list_after": n, "muse_env_present": false, "marker_sha": "<40 hex>",
#  "unit_limits": {"memory_max_bytes": 1468006400, "memory_high_bytes": 1258291200, "oom_score_adj": 300, "cgroup_memory_max_bytes": 1468006400},
#  "host_clock": {"leap_status": "Normal", "synchronised": true}, "systemd_failed_units": 0, "clock_read_before_close": true,
#  "readback": {"minutes": n, "triggers_fired": 0, "service_window_calls": n},
#  "arms": {"e10_marker_equals_release_sha": bool, "e13_peers_bounded_on_installed_code": bool, "e14_unit_limits_active": bool, "e15_window_pages_equal_phase_a": bool}}}
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/../../r37/checks/_landed.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
REC="${AP38_SERVED_OVERRIDE:-$W/CODE7_SERVED.json}"
slug=nfra-oplgtw-gateway-release-batch7; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$REC" ] || { echo "CODE7_SERVED.json absent"; echo "RESULT: FAIL"; exit 1; }
rel=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha',''))" "$(native "${AP38_RELREC_OVERRIDE:-$W/ap38_release.json}")" 2>/dev/null | tr -d '\r')
landed=never; [ -n "$rel" ] && landed=$(landed_state "$rel")
[ -n "$AP38_SERVED_OVERRIDE" ] && landed=${AP38_FORCE_LANDED:-$landed}
res=$(python - "$(native "$REC")" "$rel" <<'PYEOF'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
if isinstance(d.get("body"), dict):
    d = d["body"]
arms = d.get("arms") or {}
need = ["e10_marker_equals_release_sha", "e13_peers_bounded_on_installed_code", "e14_unit_limits_active", "e15_window_pages_equal_phase_a"]
armed = [k for k in need if arms.get(k) is True]
md5 = d.get("host_md5") or {}
rb = d.get("readback") or {}
ul = d.get("unit_limits") or {}
ck = d.get("host_clock") or {}
marker = bool(sys.argv[2]) and d.get("marker_sha") == sys.argv[2]
limits_ok = (ul.get("memory_max_bytes") == 1468006400 and ul.get("memory_high_bytes") == 1258291200 and ul.get("oom_score_adj") == 300
             and ul.get("cgroup_memory_max_bytes") == 1468006400)
clk_ok = ck.get("leap_status") == "Normal" and ck.get("synchronised") is True and d.get("systemd_failed_units") == 0 and d.get("clock_read_before_close") is True
GUARDS = ("oom_score_adj_1000_rlimit_as_1400mb", "oom_score_adj_1000_cgroup_memmax_1400mb")
tool_ok = d.get("per_tool_good") == 27 and d.get("harness_guard") in GUARDS
rb_ok = isinstance(rb.get("minutes"), (int, float)) and rb["minutes"] >= 30 and rb.get("triggers_fired") == 0 and isinstance(rb.get("service_window_calls"), int)
ok = (d.get("health_status") == 200 and d.get("reader_env_keys_present") == 7 and d.get("registry_count") == 103 and tool_ok and md5.get("differ") == 0
      and len(armed) == len(need) and marker and rb_ok and limits_ok and clk_ok
      and d.get("tools_list_before") is not None and d.get("tools_list_before") == d.get("tools_list_after") and d.get("muse_env_present") is False)
print("tools/list before %s after %s (want equal); MUSE_CLIENT_ID present %s (want False); host marker equals the release sha %s" % (d.get("tools_list_before"), d.get("tools_list_after"), d.get("muse_env_present"), "yes" if marker else "no"))
print("served: health %s; reader env keys %s of 7; registry %s (want 103); the 27-tool read %s of 27 under the hard guard %s; host md5 differ %s (want 0); arms true %d of %d" % (
      d.get("health_status"), d.get("reader_env_keys_present"), d.get("registry_count"), d.get("per_tool_good"), "yes" if d.get("harness_guard") in GUARDS else "NO", md5.get("differ"), len(armed), len(need)))
print("unit limits live: MemoryMax %s, MemoryHigh %s, OOMScoreAdjust %s, cgroup memory.max %s: %s" % (ul.get("memory_max_bytes"), ul.get("memory_high_bytes"), ul.get("oom_score_adj"), ul.get("cgroup_memory_max_bytes"), "ok" if limits_ok else "NOT OK"))
print("host clock: leap status %s, synchronised %s; systemctl --failed units %s; read BEFORE the ledger closed %s: %s" % (ck.get("leap_status"), ck.get("synchronised"), d.get("systemd_failed_units"), d.get("clock_read_before_close"), "ok" if clk_ok else "NOT OK"))
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
