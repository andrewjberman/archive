#!/usr/bin/env bash
# OPLGTW OG-ap-44 AC2 (round 43, the tenth batched gateway release, PHASE B): the release landed, the ledger closed AFTER the host clock and failed units were read, the 27-tool read passes 27 of 27 under the guard, UNARMED ONLY,
# and THE ACCESS LOG IS BACK (the CTO's criterion, msg 35769): the journal shows the service's own `POST /mcp` lines again under traffic, counted against the audit lake over the SAME 30-minute read-back window.
# Rule fixed before the run: post_mcp_lines_readback > 0 AND post_mcp_lines_readback >= 0.25 * audit_records_readback (the OG-ap-38 windows read about 0.55: roughly 164 lines to 295 records); listener lines in the journal: 0 (the listener's own access log stays off, so none to confuse).
# Record W/CODE11_SERVED.json = {"body": {the CODE10 fields of ap42.AC2 (health_status, env_key_count 65, reader_env_keys_present 7, registry_count 103, per_tool_good 27, harness_guard, host_md5, tools_list_before/after, muse_env_present, marker_sha,
#  unit_limits, host_clock, systemd_failed_units, clock_read_before_close, readback with nrestarts_during_readback),
#  "probe": {"armings": 0, "unarmed_status": 403, "unarmed_error": "probe_not_armed", "lease_parameter_absent_before": true, "lease_parameter_absent_after": true, "listener_bound": ["127.0.0.1"], "nrestarts_after": 0},
#  "access_log": {"window_minutes": 30, "post_mcp_lines_readback": n, "audit_records_readback": m, "post_mcp_lines_before_ap40_30min": n0 (the OG-ap-38 window, for the baseline), "listener_lines_in_journal": 0, "method": "<how the lines were counted>"}}}
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/../../r37/checks/_landed.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
REC="${AP44_SERVED_OVERRIDE:-$W/CODE11_SERVED.json}"
slug=nfra-oplgtw-gateway-release-batch11; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$REC" ] || { echo "CODE11_SERVED.json absent"; echo "RESULT: FAIL"; exit 1; }
rel=$(python -I -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha',''))" "$(native "${AP44_RELREC_OVERRIDE:-$W/ap44_release.json}")" 2>/dev/null | tr -d '\r')
landed=never; [ -n "$rel" ] && landed=$(landed_state "$rel")
[ -n "$AP44_SERVED_OVERRIDE" ] && landed=${AP44_FORCE_LANDED:-$landed}
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
         and al["post_mcp_lines_readback"] >= 0.25 * al["audit_records_readback"] and al.get("listener_lines_in_journal") == 0 and al.get("window_minutes") == 30 and bool(al.get("method")))
ok = (d.get("health_status") == 200 and d.get("reader_env_keys_present") == 7 and d.get("registry_count") == 103 and tool_ok and md5.get("differ") == 0 and marker and limits_ok and clk_ok and rb_ok and probe_ok and al_ok
      and d.get("tools_list_before") is not None and d.get("tools_list_before") == d.get("tools_list_after") and d.get("muse_env_present") is False)
print("tools/list before %s after %s (want equal); marker equals the release sha %s; health %s; registry %s (want 103); the 27-tool read %s of 27 under the hard guard %s; host md5 differ %s (want 0)" % (
      d.get("tools_list_before"), d.get("tools_list_after"), "yes" if marker else "no", d.get("health_status"), d.get("registry_count"), d.get("per_tool_good"), "yes" if d.get("harness_guard") in GUARDS else "NO", md5.get("differ")))
print("unit limits live %s; host clock %s synchronised %s, failed units %s, read BEFORE the ledger closed %s: %s; read-back %s minutes, triggers %s, service restarts %s: %s" % (
      "ok" if limits_ok else "NOT OK", ck.get("leap_status"), ck.get("synchronised"), d.get("systemd_failed_units"), d.get("clock_read_before_close"), "ok" if clk_ok else "NOT OK", rb.get("minutes"), rb.get("triggers_fired"), rb.get("nrestarts_during_readback"), "ok" if rb_ok else "NOT OK"))
print("listener read UNARMED only: armings %s (want 0), unarmed answer %s %s, lease parameter absent before %s and after %s, bound %s, restarts after %s: %s" % (
      pr.get("armings"), pr.get("unarmed_status"), pr.get("unarmed_error"), pr.get("lease_parameter_absent_before"), pr.get("lease_parameter_absent_after"), pr.get("listener_bound"), pr.get("nrestarts_after"), "ok" if probe_ok else "NOT OK"))
print("ACCESS LOG BACK: POST /mcp journal lines %s against %s audit records over the same %s-minute window (rule: lines > 0 and lines >= 0.25 x records), listener lines in the journal %s: %s" % (
      al.get("post_mcp_lines_readback"), al.get("audit_records_readback"), al.get("window_minutes"), al.get("listener_lines_in_journal"), "ok" if al_ok else "NOT OK"))
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
