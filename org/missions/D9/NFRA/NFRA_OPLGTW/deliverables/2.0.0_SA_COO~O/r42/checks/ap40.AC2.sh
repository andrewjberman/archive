#!/usr/bin/env bash
# OPLGTW OG-ap-40 AC2 (round 42, the eighth batched gateway release, PHASE B): the listener release landed, the ledger closed AFTER the host clock and failed units were read, the 27-tool read passes 27 of 27 under the guard,
# and the service itself was driven THROUGH THE LISTENER: etfs_compare_peers answered with the service heap printed before and after (the Z-S375 disarm evidence) and a full window chain with the service heap flat (the Z-S338 evidence).
# Record W/CODE9_SERVED.json = {"body": {the CODE8 fields of ap39.AC2 (health_status, env_key_count 65, reader_env_keys_present 7, registry_count 103, per_tool_good 27, harness_guard, host_md5, tools_list_before/after, muse_env_present, marker_sha,
#  unit_limits, host_clock, systemd_failed_units, clock_read_before_close, readback with nrestarts_during_readback),
#  "probe": {"lease_minutes": n, "audit_label": "probe:OG-ap-40",
#     "peers": {"answered": true, "service_heap_before_mb": x, "service_heap_after_mb": y, "vmrss_after_mb": n (CT3), "service_pid": same pid before and after},
#     "window_chain": {"pages": n, "answered": true, "heap_growth_median_mb": g, "first_page_wall_s": s (CT4: under 15), "max_vmrss_mb": m (CT3: 1200 or less after each page), "service_pid_stable": true},
#     "other_tool_refused": true, "other_account_refused": true, "expired_refused": true, "listener_closed_at_rest": true, "nrestarts_after_probes": 0}}}
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/../../r37/checks/_landed.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
REC="${AP40_SERVED_OVERRIDE:-$W/CODE9_SERVED.json}"
slug=nfra-oplgtw-gateway-release-batch9; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$REC" ] || { echo "CODE9_SERVED.json absent"; echo "RESULT: FAIL"; exit 1; }
rel=$(python -I -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha',''))" "$(native "${AP40_RELREC_OVERRIDE:-$W/ap40_release.json}")" 2>/dev/null | tr -d '\r')
landed=never; [ -n "$rel" ] && landed=$(landed_state "$rel")
[ -n "$AP40_SERVED_OVERRIDE" ] && landed=${AP40_FORCE_LANDED:-$landed}
res=$(python -I - "$(native "$REC")" "$rel" <<'PYEOF'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
if isinstance(d.get("body"), dict):
    d = d["body"]
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
md5 = d.get("host_md5") or {}; rb = d.get("readback") or {}; ul = d.get("unit_limits") or {}; ck = d.get("host_clock") or {}; pr = d.get("probe") or {}
pe = pr.get("peers") or {}; wc = pr.get("window_chain") or {}
GUARDS = ("oom_score_adj_1000_rlimit_as_1400mb", "oom_score_adj_1000_cgroup_memmax_1400mb")
marker = bool(sys.argv[2]) and d.get("marker_sha") == sys.argv[2]
limits_ok = (ul.get("memory_max_bytes") == 1468006400 and ul.get("memory_high_bytes") == 1258291200 and ul.get("oom_score_adj") == 300 and ul.get("cgroup_memory_max_bytes") == 1468006400)
clk_ok = ck.get("leap_status") == "Normal" and ck.get("synchronised") is True and d.get("systemd_failed_units") == 0 and d.get("clock_read_before_close") is True
rb_ok = isn(rb.get("minutes")) and rb["minutes"] >= 30 and rb.get("triggers_fired") == 0 and rb.get("nrestarts_during_readback") == 0
tool_ok = d.get("per_tool_good") == 27 and d.get("harness_guard") in GUARDS
peers_ok = (pe.get("answered") is True and isn(pe.get("service_heap_before_mb")) and isn(pe.get("service_heap_after_mb")) and isn(pe.get("service_pid"))
            and pe["service_heap_after_mb"] - pe["service_heap_before_mb"] <= 700 and isn(pe.get("vmrss_after_mb")) and pe["vmrss_after_mb"] <= 1200)
chain_ok = (wc.get("answered") is True and isn(wc.get("pages")) and wc["pages"] >= 2 and isn(wc.get("heap_growth_median_mb")) and wc["heap_growth_median_mb"] <= 20 and wc.get("service_pid_stable") is True
            and isn(wc.get("first_page_wall_s")) and wc["first_page_wall_s"] < 15 and isn(wc.get("max_vmrss_mb")) and wc["max_vmrss_mb"] <= 1200)
probe_ok = (peers_ok and chain_ok and isn(pr.get("lease_minutes")) and 0 < pr["lease_minutes"] <= 60 and pr.get("audit_label") == "probe:OG-ap-40"
            and pr.get("other_tool_refused") is True and pr.get("other_account_refused") is True and pr.get("expired_refused") is True
            and pr.get("listener_closed_at_rest") is True and pr.get("nrestarts_after_probes") == 0)
ok = (d.get("health_status") == 200 and d.get("reader_env_keys_present") == 7 and d.get("registry_count") == 103 and tool_ok and md5.get("differ") == 0 and marker and limits_ok and clk_ok and rb_ok and probe_ok
      and d.get("tools_list_before") is not None and d.get("tools_list_before") == d.get("tools_list_after") and d.get("muse_env_present") is False)
print("tools/list before %s after %s (want equal); marker equals the release sha %s; health %s; registry %s (want 103); the 27-tool read %s of 27 under the hard guard %s; host md5 differ %s (want 0)" % (
      d.get("tools_list_before"), d.get("tools_list_after"), "yes" if marker else "no", d.get("health_status"), d.get("registry_count"), d.get("per_tool_good"), "yes" if d.get("harness_guard") in GUARDS else "NO", md5.get("differ")))
print("unit limits live %s; host clock %s synchronised %s, failed units %s, read BEFORE the ledger closed %s: %s; read-back %s minutes, triggers %s, service restarts %s: %s" % (
      "ok" if limits_ok else "NOT OK", ck.get("leap_status"), ck.get("synchronised"), d.get("systemd_failed_units"), d.get("clock_read_before_close"), "ok" if clk_ok else "NOT OK", rb.get("minutes"), rb.get("triggers_fired"), rb.get("nrestarts_during_readback"), "ok" if rb_ok else "NOT OK"))
print("THROUGH THE LISTENER (lease %s minutes, label %s): etfs_compare_peers answered %s with the service heap %s -> %s MB; window chain %s pages answered %s, median heap growth %s MB (limit 20), first page %s s (limit 15), highest VmRSS %s MB (limit 1200), pid stable %s; other tool refused %s, other account refused %s, expired lease refused %s, listener closed at rest %s, restarts after the probes %s: %s" % (
      pr.get("lease_minutes"), pr.get("audit_label"), pe.get("answered"), pe.get("service_heap_before_mb"), pe.get("service_heap_after_mb"), wc.get("pages"), wc.get("answered"), wc.get("heap_growth_median_mb"), wc.get("first_page_wall_s"), wc.get("max_vmrss_mb"), wc.get("service_pid_stable"),
      pr.get("other_tool_refused"), pr.get("other_account_refused"), pr.get("expired_refused"), pr.get("listener_closed_at_rest"), pr.get("nrestarts_after_probes"), "ok" if probe_ok else "NOT OK"))
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
