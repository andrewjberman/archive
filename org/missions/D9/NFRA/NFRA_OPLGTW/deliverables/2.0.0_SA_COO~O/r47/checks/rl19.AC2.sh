#!/usr/bin/env bash
# OPLGTW OG-rl-19 AC2 (round 47, R3c, PHASE B): the order of acts held and the dual read is live. The ledger nfra-oplgtw-gateway-release-r3c is CLOSED; the sentinel is gone; the manifest's deployed_commit is the release (or was and is superseded).
# Record W/R3C_SERVED.json (field names fixed here):
#  {"body": {"base_reread_on_host_equals_base_sha": true, "health_after": 200, "marker_sha": <release sha>, "marker_equals_release": true, "tools_list": 103, "tools_list_before": 103, "registry_count": 103, "env_key_count": 65, "nrestarts_after_deploy": 0,
#   "host_md5": {"differ": 0, "missing_on_host": 0}, "systemd_failed_units": 0, "clock_read_before_close": true, "host_clock": {"leap_status": "Normal", "synchronised": true},
#   "readback": {"minutes": >= 15, "triggers_fired": 0, "nrestarts_during_readback": 0},
#   "order": {"r3a_confirmation_ref": "<the laptop MSTR's relay, a file name under org/mcp/inbox/...>", "r3a_confirmation_read_before_terraform_apply": true, "terraform_applied_before_gate_read": true, "gate_read_before_code_deploy": true},
#   "terraform": {"via": "safe-apply", "add": 0, "change": 2, "destroy": 0, "resources": ["aws_iam_role_policy.schwab_catalog_read_policy", "aws_iam_role_policy.schwab_data_read_policy"]},
#   "gate_read": {"as_role": "gateway-schwab-catalog-read-role", "get_object": "NoSuchKey", "list_key_count": 0, "prefix": "schwab/49financial/state/complete/", "bucket": "opal-data-49financial"},
#   "dual_read": {"master": "08403355", "dates_before": n >= 1, "dates_after": n, "newest_before": "YYYY-MM-DD", "newest_after": "YYYY-MM-DD", "marker_location": "old", "snapshot_status_before": s, "snapshot_status_after": s,
#                 "other_masters_unchanged": true, "planted_second_master_ignored": true}}}
#  Rules read here: gate_read.get_object is "NoSuchKey" and list_key_count is 0 (AccessDenied is NOT a pass: the record must say what the role saw); the order flags are all true; dates_after >= dates_before and newest_after >= newest_before;
#  marker_location is "old" (the new location is empty until the cutover); the snapshot status before and after are equal; terraform is exactly add 0 change 2 destroy 0 on the two policies.
# Overrides (dry-run controls only): RL19_SERVED_OVERRIDE, RL19_RELREC_OVERRIDE, RL19_FORCE_LANDED.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/../../r37/checks/_landed.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
REC="${RL19_SERVED_OVERRIDE:-$W/R3C_SERVED.json}"
slug=nfra-oplgtw-gateway-release-r3c; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$REC" ] || { echo "R3C_SERVED.json absent"; echo "RESULT: FAIL"; exit 1; }
rel=$(python3 -I -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha',''))" "$(native "${RL19_RELREC_OVERRIDE:-$W/rl19_release.json}")" 2>/dev/null | tr -d '\r')
landed=never; [ -n "$rel" ] && landed=$(landed_state "$rel")
[ -n "$RL19_SERVED_OVERRIDE" ] && landed=${RL19_FORCE_LANDED:-$landed}
res=$(python3 -I - "$(native "$REC")" "$rel" <<'PYEOF'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
d = d.get("body", d)
def isn(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)
md5 = d.get("host_md5") or {}; rb = d.get("readback") or {}; ck = d.get("host_clock") or {}; od = d.get("order") or {}; tf = d.get("terraform") or {}; gr = d.get("gate_read") or {}; dr = d.get("dual_read") or {}
marker = bool(sys.argv[2]) and d.get("marker_sha") == sys.argv[2] and d.get("marker_equals_release") is True
clk_ok = ck.get("leap_status") == "Normal" and ck.get("synchronised") is True and d.get("systemd_failed_units") == 0 and d.get("clock_read_before_close") is True
# amended 2026-10-21 (issuer): the monitor carries a 700 MB service-growth line (a default from OG-ap-34) that this order does not name; one fired line is accepted ONLY when the record states it as that monitor line and every trigger the order names reads clean (health never non-200, host memory under 85 percent, no restart)
mo = d.get("memory_observation") or {}
mon_line = isinstance(mo.get("monitor_line"), str) and "700 MB" in mo["monitor_line"] and "names no memory trigger" in mo["monitor_line"]
trig_ok = rb.get("triggers_fired") == 0 or (rb.get("triggers_fired") == 1 and mon_line and rb.get("health_not_200") == 0 and isn(rb.get("host_pct_max")) and rb["host_pct_max"] < 85)
rb_ok = isn(rb.get("minutes")) and rb["minutes"] >= 15 and trig_ok and rb.get("nrestarts_during_readback") == 0
od_ok = bool(od.get("r3a_confirmation_ref")) and od.get("r3a_confirmation_read_before_terraform_apply") is True and od.get("terraform_applied_before_gate_read") is True and od.get("gate_read_before_code_deploy") is True
tf_ok = tf.get("via") == "safe-apply" and tf.get("add") == 0 and tf.get("change") == 2 and tf.get("destroy") == 0 and sorted(tf.get("resources") or []) == ["aws_iam_role_policy.schwab_catalog_read_policy", "aws_iam_role_policy.schwab_data_read_policy"]
gr_ok = gr.get("as_role") == "gateway-schwab-catalog-read-role" and gr.get("get_object") == "NoSuchKey" and gr.get("list_key_count") == 0 and gr.get("prefix") == "schwab/49financial/state/complete/" and gr.get("bucket") == "opal-data-49financial"
dr_ok = (dr.get("master") == "08403355" and isn(dr.get("dates_before")) and dr["dates_before"] >= 1 and isn(dr.get("dates_after")) and dr["dates_after"] >= dr["dates_before"]
         and isinstance(dr.get("newest_before"), str) and isinstance(dr.get("newest_after"), str) and dr["newest_after"] >= dr["newest_before"] and dr.get("marker_location") == "old"
         and dr.get("snapshot_status_before") == dr.get("snapshot_status_after") and dr.get("snapshot_status_before") and dr.get("other_masters_unchanged") is True and dr.get("planted_second_master_ignored") is True)
ok = (d.get("base_reread_on_host_equals_base_sha") is True and d.get("health_after") == 200 and d.get("env_key_count") == 65 and d.get("registry_count") == 103 and d.get("tools_list") == 103 and d.get("tools_list_before") == 103 and marker and md5.get("differ") == 0
      and md5.get("missing_on_host") == 0 and clk_ok and rb_ok and od_ok and tf_ok and gr_ok and dr_ok and d.get("nrestarts_after_deploy") == 0)
print("base re-read on the host at the start of Phase B equals base_sha: %s" % ("yes" if d.get("base_reread_on_host_equals_base_sha") is True else "NO"))
print("tools/list %s before %s (want 103 and 103); marker equals the release sha %s; health %s; registry %s (want 103); env keys %s (want 65); host md5 differ %s, missing %s (want 0, 0); restarts after deploy %s (want 0)" % (
      d.get("tools_list"), d.get("tools_list_before"), "yes" if marker else "no", d.get("health_after"), d.get("registry_count"), d.get("env_key_count"), md5.get("differ"), md5.get("missing_on_host"), d.get("nrestarts_after_deploy")))
print("host clock %s synchronised %s, failed units %s, read BEFORE the ledger closed %s: %s; read-back %s minutes, triggers %s, restarts %s: %s" % (
      ck.get("leap_status"), ck.get("synchronised"), d.get("systemd_failed_units"), d.get("clock_read_before_close"), "ok" if clk_ok else "NOT OK", rb.get("minutes"), rb.get("triggers_fired"), rb.get("nrestarts_during_readback"), "ok" if rb_ok else "NOT OK"))
print("ORDER OF ACTS: R3a confirmation read before the apply, Terraform applied before the gate read, gate read before the code deploy: %s; Terraform via safe-apply, add %s change %s destroy %s on the two policies: %s" % (
      "ok" if od_ok else "NOT OK", tf.get("add"), tf.get("change"), tf.get("destroy"), "ok" if tf_ok else "NOT OK"))
print("GATE READ as the catalog role on %s/%s: GetObject %s, list keys %s (want NoSuchKey and 0; AccessDenied is NOT a pass): %s" % (gr.get("bucket"), gr.get("prefix"), gr.get("get_object"), gr.get("list_key_count"), "ok" if gr_ok else "NOT OK"))
print("DUAL READ live for %s: dates %s -> %s (not fewer), newest %s -> %s (not older), marker location %s, snapshot status %s -> %s, other masters unchanged %s, planted second-master file ignored %s: %s" % (
      dr.get("master"), dr.get("dates_before"), dr.get("dates_after"), dr.get("newest_before"), dr.get("newest_after"), dr.get("marker_location"), dr.get("snapshot_status_before"), dr.get("snapshot_status_after"), dr.get("other_masters_unchanged"), dr.get("planted_second_master_ignored"), "ok" if dr_ok else "NOT OK"))
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
