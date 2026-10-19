#!/usr/bin/env bash
# OPLGTW OG-ap-50 AC2 (round 46, the thirteenth batched gateway release, PHASE B): the release landed, the ledger closed AFTER the host clock and failed units were read, the 27-tool read passes 27 of 27 under the guard, UNARMED ONLY,
# the ACCESS LOG counts as in OG-ap-48 (journal POST /mcp lines against audit-lake records over the SAME 30-minute read-back window; the lake leg's failure counter reads 0), and THE NEW ROUTE IS MOUNTED BEHIND THE OWNER GATE ON THE RUNNING SERVICE:
#  "route": {"before_status": 404 (the route read on the host BEFORE the deploy), "unauth_status": 401 (no identity header, after), "whoami_control_status": 401, "missing_control_status": 404 (a path under /api/admin that is not a route), "probe": "<how: a local request to the service port, no ALB, no header>"}.
# Record W/CODE14_SERVED.json = {"body": {the CODE13 fields of ap48.AC2 (health_status, env_key_count 65, reader_env_keys_present 7, registry_count 103, per_tool_good 27, harness_guard, host_md5, tools_list_before/after, muse_env_present, marker_sha,
#  unit_limits, host_clock, systemd_failed_units, clock_read_before_close, readback with nrestarts_during_readback), "probe": {listener, as in ap48}, "access_log": {as in ap48}, "audit_failure_counter": {as in ap48}, "route": {above}}}
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/../../r37/checks/_landed.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
REC="${AP50_SERVED_OVERRIDE:-$W/CODE14_SERVED.json}"
slug=nfra-oplgtw-gateway-release-batch14; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$REC" ] || { echo "CODE14_SERVED.json absent"; echo "RESULT: FAIL"; exit 1; }
rel=$(python -I -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha',''))" "$(native "${AP50_RELREC_OVERRIDE:-$W/ap50_release.json}")" 2>/dev/null | tr -d '\r')
landed=never; [ -n "$rel" ] && landed=$(landed_state "$rel")
[ -n "$AP50_SERVED_OVERRIDE" ] && landed=${AP50_FORCE_LANDED:-$landed}
res=$(python -I - "$(native "$REC")" "$rel" <<'PYEOF'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
if isinstance(d.get("body"), dict):
    d = d["body"]
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
md5 = d.get("host_md5") or {}; rb = d.get("readback") or {}; ul = d.get("unit_limits") or {}; ck = d.get("host_clock") or {}; pr = d.get("probe") or {}; al = d.get("access_log") or {}

GUARDS = ("oom_score_adj_1000_rlimit_as_1400mb", "oom_score_adj_1000_cgroup_memmax_1400mb")
marker = bool(sys.argv[2]) and d.get("marker_sha") == sys.argv[2]
limits_ok = (ul.get("memory_max_bytes") == 1468006400 and ul.get("memory_high_bytes") == 1258291200 and ul.get("oom_score_adj") == 300 and ul.get("cgroup_memory_max_bytes") == 1468006400)
clk_ok = ck.get("leap_status") == "Normal" and ck.get("synchronised") is True and d.get("systemd_failed_units") == 0 and d.get("clock_read_before_close") is True
rb_ok = isn(rb.get("minutes")) and rb["minutes"] >= 30 and rb.get("triggers_fired") == 0 and rb.get("nrestarts_during_readback") == 0
tool_ok = d.get("per_tool_good") == 27 and d.get("harness_guard") in GUARDS
probe_ok = (pr.get("armings") == 0 and pr.get("unarmed_status") == 403 and pr.get("unarmed_error") == "probe_not_armed" and pr.get("lease_parameter_absent_before") is True
            and pr.get("lease_parameter_absent_after") is True and pr.get("listener_bound") == ["127.0.0.1"] and pr.get("nrestarts_after") == 0)
al_ok = (isn(al.get("post_mcp_lines_readback")) and al["post_mcp_lines_readback"] > 0 and isn(al.get("audit_records_readback")) and al["audit_records_readback"] > 0
         and al["post_mcp_lines_readback"] >= 0.25 * al["audit_records_readback"] and isn(al.get("listener_requests_made")) and al["listener_requests_made"] >= 3 and al.get("listener_access_lines") == al.get("listener_requests_made") and al.get("window_minutes") == 30 and bool(al.get("method")))
rt = d.get("route") or {}
rt_ok = (rt.get("before_status") == 404 and rt.get("unauth_status") == 401 and rt.get("whoami_control_status") == 401 and rt.get("missing_control_status") == 404 and bool(rt.get("probe")))
afc = d.get("audit_failure_counter") or {}
afc_ok = (isn(afc.get("journal_lines_readback")) and afc["journal_lines_readback"] == 0 and afc.get("counter_value") == 0 and bool(afc.get("method")))
ok = (d.get("health_status") == 200 and d.get("reader_env_keys_present") == 7 and d.get("registry_count") == 103 and tool_ok and md5.get("differ") == 0 and marker and limits_ok and clk_ok and rb_ok and probe_ok and al_ok and afc_ok and rt_ok
      and d.get("tools_list_before") is not None and d.get("tools_list_before") == d.get("tools_list_after") and d.get("muse_env_present") is False)
print("tools/list before %s after %s (want equal); marker equals the release sha %s; health %s; registry %s (want 103); the 27-tool read %s of 27 under the hard guard %s; host md5 differ %s (want 0)" % (
      d.get("tools_list_before"), d.get("tools_list_after"), "yes" if marker else "no", d.get("health_status"), d.get("registry_count"), d.get("per_tool_good"), "yes" if d.get("harness_guard") in GUARDS else "NO", md5.get("differ")))
print("unit limits live %s; host clock %s synchronised %s, failed units %s, read BEFORE the ledger closed %s: %s; read-back %s minutes, triggers %s, service restarts %s: %s" % (
      "ok" if limits_ok else "NOT OK", ck.get("leap_status"), ck.get("synchronised"), d.get("systemd_failed_units"), d.get("clock_read_before_close"), "ok" if clk_ok else "NOT OK", rb.get("minutes"), rb.get("triggers_fired"), rb.get("nrestarts_during_readback"), "ok" if rb_ok else "NOT OK"))
print("listener read UNARMED only: armings %s (want 0), unarmed answer %s %s, lease parameter absent before %s and after %s, bound %s, restarts after %s: %s" % (
      pr.get("armings"), pr.get("unarmed_status"), pr.get("unarmed_error"), pr.get("lease_parameter_absent_before"), pr.get("lease_parameter_absent_after"), pr.get("listener_bound"), pr.get("nrestarts_after"), "ok" if probe_ok else "NOT OK"))
print("ACCESS LOG BACK: POST /mcp journal lines %s against %s audit records over the same %s-minute window (rule: lines > 0 and lines >= 0.25 x records; listener access lines must equal the listener requests made), listener access lines %s of %s requests made: %s" % (
      al.get("post_mcp_lines_readback"), al.get("audit_records_readback"), al.get("window_minutes"), al.get("listener_access_lines"), al.get("listener_requests_made"), "ok" if al_ok else "NOT OK"))
print("AUDIT FAILURE COUNTER (the new lake-put failure line, expected 0): journal failure lines %s over the read-back, counter value %s: %s" % (afc.get("journal_lines_readback"), afc.get("counter_value"), "ok" if afc_ok else "NOT OK"))
print("ROUTE /api/admin/gateway/families on the running service (local request, no identity header): before the deploy %s (want 404), after %s (want 401, owner-gated), whoami control %s (want 401), missing-route control %s (want 404): %s" % (rt.get("before_status"), rt.get("unauth_status"), rt.get("whoami_control_status"), rt.get("missing_control_status"), "ok" if rt_ok else "NOT OK"))
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
