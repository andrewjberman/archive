#!/usr/bin/env bash
# OPLGTW OG-rl-17 AC2 (round 47, batch16, PHASE B): the release landed, the ledger nfra-oplgtw-gateway-release-batch16 closed AFTER the host clock and failed units were read, the 27-tool read passes 27 of 27 under the guard, UNARMED ONLY,
# the access-log counts (journal POST /mcp lines against audit-lake records over the SAME 30-minute read-back window; the lake leg's failure counter reads 0), and the in-flight guard is LIVE in the running service.
# Record W/CODE16_SERVED.json (the RZ2_SERVED.json field names): health_after 200, marker_equals_release true, marker_sha = the release, unit_memory_high "5600M", unit_memory_max "6400M", tools_list 103 = tools_list_before,
#  registry_count 103, tools_27_of_27 true, per_tool_good 27, harness_guard, nrestarts_after_deploy 0, env_key_count 65, muse_env_present false, host_md5 {differ 0, missing_on_host 0}, systemd_failed_units 0, clock_read_before_close true,
#  host_clock {leap_status Normal, synchronised true}, readback {minutes >= 30, triggers_fired 0, nrestarts_during_readback 0}, probe {armings 0, unarmed_status 403, unarmed_error probe_not_armed, lease_parameter_absent_before/after true, listener_bound ["127.0.0.1"]},
#  access_log {as in ap50}, audit_failure_counter {journal_lines_readback 0, counter_value 0}, inflight {guard_in_deployed_tree true, limit 4, wait_s 20.0, deployed_call_tool_hook true}.
# Overrides (dry-run controls only): RL17_SERVED_OVERRIDE, RL17_RELREC_OVERRIDE, RL17_FORCE_LANDED.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/../../r37/checks/_landed.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
REC="${RL17_SERVED_OVERRIDE:-$W/CODE16_SERVED.json}"
slug=nfra-oplgtw-gateway-release-batch16; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$REC" ] || { echo "CODE16_SERVED.json absent"; echo "RESULT: FAIL"; exit 1; }
rel=$(python3 -I -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha',''))" "$(native "${RL17_RELREC_OVERRIDE:-$W/rl17_release.json}")" 2>/dev/null | tr -d '\r')
landed=never; [ -n "$rel" ] && landed=$(landed_state "$rel")
[ -n "$RL17_SERVED_OVERRIDE" ] && landed=${RL17_FORCE_LANDED:-$landed}
res=$(python3 -I - "$(native "$REC")" "$rel" <<'PYEOF'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
if isinstance(d.get("body"), dict):
    d = d["body"]
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
md5 = d.get("host_md5") or {}; rb = d.get("readback") or {}; ck = d.get("host_clock") or {}; pr = d.get("probe") or {}; al = d.get("access_log") or {}; inf = d.get("inflight") or {}; afc = d.get("audit_failure_counter") or {}
GUARDS = ("oom_score_adj_1000_rlimit_as_1400mb", "oom_score_adj_1000_cgroup_memmax_1400mb")
marker = bool(sys.argv[2]) and d.get("marker_sha") == sys.argv[2] and d.get("marker_equals_release") is True
limits_ok = d.get("unit_memory_high") == "5600M" and d.get("unit_memory_max") == "6400M"
clk_ok = ck.get("leap_status") == "Normal" and ck.get("synchronised") is True and d.get("systemd_failed_units") == 0 and d.get("clock_read_before_close") is True
rb_ok = isn(rb.get("minutes")) and rb["minutes"] >= 30 and rb.get("triggers_fired") == 0 and rb.get("nrestarts_during_readback") == 0
tool_ok = d.get("per_tool_good") == 27 and d.get("tools_27_of_27") is True and d.get("harness_guard") in GUARDS
probe_ok = (pr.get("armings") == 0 and pr.get("unarmed_status") == 403 and pr.get("unarmed_error") == "probe_not_armed" and pr.get("lease_parameter_absent_before") is True
            and pr.get("lease_parameter_absent_after") is True and pr.get("listener_bound") == ["127.0.0.1"])
al_ok = (isn(al.get("post_mcp_lines_readback")) and al["post_mcp_lines_readback"] > 0 and isn(al.get("audit_records_readback")) and al["audit_records_readback"] > 0
         and al["post_mcp_lines_readback"] >= 0.25 * al["audit_records_readback"] and al.get("window_minutes") == 30 and bool(al.get("method")))
afc_ok = isn(afc.get("journal_lines_readback")) and afc["journal_lines_readback"] == 0 and afc.get("counter_value") == 0 and bool(afc.get("method"))
inf_ok = inf.get("guard_in_deployed_tree") is True and inf.get("limit") == 4 and inf.get("wait_s") == 20.0 and inf.get("deployed_call_tool_hook") is True
ok = (d.get("health_after") == 200 and d.get("env_key_count") == 65 and d.get("registry_count") == 103 and tool_ok and md5.get("differ") == 0 and md5.get("missing_on_host") == 0 and marker and limits_ok and clk_ok and rb_ok
      and probe_ok and al_ok and afc_ok and inf_ok and d.get("tools_list") == 103 and d.get("tools_list_before") == 103 and d.get("muse_env_present") is False and d.get("nrestarts_after_deploy") == 0)
print("tools/list %s before %s (want 103 and 103); marker equals the release sha %s; health %s; registry %s (want 103); env keys %s (want 65); the 27-tool read %s of 27 under the hard guard %s; host md5 differ %s, missing %s (want 0, 0)" % (
      d.get("tools_list"), d.get("tools_list_before"), "yes" if marker else "no", d.get("health_after"), d.get("registry_count"), d.get("env_key_count"), d.get("per_tool_good"), "yes" if d.get("harness_guard") in GUARDS else "NO", md5.get("differ"), md5.get("missing_on_host")))
print("unit limits live %s; host clock %s synchronised %s, failed units %s, read BEFORE the ledger closed %s: %s; read-back %s minutes, triggers %s, service restarts %s: %s" % (
      "ok" if limits_ok else "NOT OK", ck.get("leap_status"), ck.get("synchronised"), d.get("systemd_failed_units"), d.get("clock_read_before_close"), "ok" if clk_ok else "NOT OK", rb.get("minutes"), rb.get("triggers_fired"), rb.get("nrestarts_during_readback"), "ok" if rb_ok else "NOT OK"))
print("listener read UNARMED only: armings %s (want 0), unarmed answer %s %s, lease parameter absent before %s and after %s, bound %s: %s" % (
      pr.get("armings"), pr.get("unarmed_status"), pr.get("unarmed_error"), pr.get("lease_parameter_absent_before"), pr.get("lease_parameter_absent_after"), pr.get("listener_bound"), "ok" if probe_ok else "NOT OK"))
print("ACCESS LOG BACK: POST /mcp journal lines %s against %s audit records over the same %s-minute window (rule: lines > 0 and lines >= 0.25 x records): %s" % (
      al.get("post_mcp_lines_readback"), al.get("audit_records_readback"), al.get("window_minutes"), "ok" if al_ok else "NOT OK"))
print("AUDIT FAILURE COUNTER (the lake-put failure line, expected 0): journal failure lines %s over the read-back, counter value %s: %s" % (afc.get("journal_lines_readback"), afc.get("counter_value"), "ok" if afc_ok else "NOT OK"))
print("IN-FLIGHT GUARD LIVE: in the deployed tree %s, limit %s, wait %s s, call_tool hook present %s: %s" % (inf.get("guard_in_deployed_tree"), inf.get("limit"), inf.get("wait_s"), inf.get("deployed_call_tool_hook"), "ok" if inf_ok else "NOT OK"))
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
