#!/usr/bin/env bash
# OPLGTW OG-rl-17 AC3 (round 47, batch16, PHASE B): the PROOFS on the running release, W/RL17_PROOFS.json (written by the applier inside the 30-minute read-back, before the ledger closes; counts and flags only, no account number):
#  d1  one live client_resolve_account per vendor through the served gateway as the owner principal: orion, eclipse and commonwealth each {"answered": true, "absent_reason" not "firm_not_served", "candidate_count" >= 1};
#      the fences hold: a control call for an unserved pair (orion with the cottonwood firm) still answers "firm_not_served";
#  d2  Cottonwood D2: client_get_transactions for one Cottonwood account over a window inside the rolling file's dates returns {"transactions" >= 1} (the false zero is gone);
#  load  the parallel-load proof (Z-S425, Z-S420): 8 calls at once of the large tools (mdpf_get_aggregate_aua, opal_discover, search_files) through the served gateway: {"calls": 8, "completed": c, "gateway_busy": b, "c + b == 8",
#      "other_errors": 0, "health_200_samples": s, "health_non_200_samples": 0, "service_peak_mb" below memory_high_mb 5600};
#  projection  mdpf_get_aggregate_aua and opal_discover each answered at most 51200 bytes as served (indent=2) with "truncated" true where cut;
#  index_pairs  the breakdown (owner route's compute, read from the deployed tree under the hard guard) carries index_pairs on every tool of the two segmented buckets: {"segmented_tools": n >= 1, "with_index_pairs": n}.
# Override (dry-run controls only): RL17_PROOFS_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
REC="${RL17_PROOFS_OVERRIDE:-$W/RL17_PROOFS.json}"
[ -f "$REC" ] || { echo "RL17_PROOFS.json absent"; echo "RESULT: FAIL"; exit 1; }
PA="${RL17_PA_OVERRIDE:-$W/PHASE_A_OG-rl-17.json}"
res=$(python3 -I - "$(native "$REC")" "$(native "$PA")" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); d = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
d1 = d.get("d1") or {}
v_ok = all((d1.get(v) or {}).get("answered") is True and (d1.get(v) or {}).get("absent_reason") != "firm_not_served" and isn((d1.get(v) or {}).get("candidate_count")) and d1[v]["candidate_count"] >= 1 for v in ("orion", "eclipse", "commonwealth"))
cu = d1.get("control_unserved_pair") or {}
ctl_tool = cu.get("absent_reason") == "firm_not_served"
# amended 2026-10-21 (issuer): client_resolve_account takes no vendor argument, so the control cannot be driven through the tool; the second route is the Phase A catalog control counts (an unserved pair holds 0 segments), read from the applier's Phase A record
try:
    pa = json.load(open(sys.argv[2], encoding="utf-8")); pa = pa.get("body", pa)
    cc = ((pa.get("fences") or {}).get("controls_unserved_pairs")) or {}
except Exception:
    cc = {}
ctl_cat = (not ctl_tool and "not reproduced by the tool" in str(cu.get("note", "")) and cu.get("absent_reason") is None
           and sorted(cc) == ["commonwealth_with_inflection", "eclipse_with_49financial", "orion_with_cottonwood_firm"] and all(cc[k] == 0 for k in cc))
ctl_ok = ctl_tool or ctl_cat
ctl_via = "" if ctl_tool or not ctl_cat else " (via the Phase A catalog controls: 0, 0, 0)"
d2 = d.get("d2") or {}
d2_ok = isn(d2.get("transactions")) and d2["transactions"] >= 1
ld = d.get("load") or {}
ld_ok = (ld.get("calls") == 8 and isn(ld.get("completed")) and isn(ld.get("gateway_busy")) and ld["completed"] + ld["gateway_busy"] == 8 and ld["completed"] >= 1 and ld.get("other_errors") == 0
         and isn(ld.get("health_200_samples")) and ld["health_200_samples"] >= 5 and ld.get("health_non_200_samples") == 0 and isn(ld.get("service_peak_mb")) and 0 < ld["service_peak_mb"] < 5600)
pj = d.get("projection") or {}
pj_ok = all(isn(pj.get(k)) and 0 < pj[k] <= 51200 for k in ("aggregate_aua_bytes", "opal_discover_bytes"))
ip = d.get("index_pairs") or {}
ip_ok = isn(ip.get("segmented_tools")) and ip["segmented_tools"] >= 1 and ip.get("with_index_pairs") == ip.get("segmented_tools")
emails = len(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw))
digits = len(re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40,64}"', '""', raw)))
ok = v_ok and ctl_ok and d2_ok and ld_ok and pj_ok and ip_ok and emails == 0 and digits == 0
print("D1 one live call per vendor: orion %s, eclipse %s, commonwealth %s candidate(s), none firm_not_served; control pair still firm_not_served %s%s: %s" % (
      (d1.get("orion") or {}).get("candidate_count"), (d1.get("eclipse") or {}).get("candidate_count"), (d1.get("commonwealth") or {}).get("candidate_count"), ctl_ok, ctl_via, "ok" if (v_ok and ctl_ok) else "NOT OK"))
print("D2 Cottonwood transactions returned %s (want >= 1): %s" % (d2.get("transactions"), "ok" if d2_ok else "NOT OK"))
print("LOAD 8 parallel large calls: completed %s, gateway_busy %s, other errors %s, /health 200 samples %s, non-200 %s, service peak %s MB (below 5600): %s" % (
      ld.get("completed"), ld.get("gateway_busy"), ld.get("other_errors"), ld.get("health_200_samples"), ld.get("health_non_200_samples"), ld.get("service_peak_mb"), "ok" if ld_ok else "NOT OK"))
print("PROJECTION aggregate AUA %s bytes, opal_discover %s bytes (each <= 51200): %s" % (pj.get("aggregate_aua_bytes"), pj.get("opal_discover_bytes"), "ok" if pj_ok else "NOT OK"))
print("INDEX_PAIRS on %s of %s segmented tools: %s; email-shaped strings %d (want 0); digit runs of 9 or more %d (want 0)" % (ip.get("with_index_pairs"), ip.get("segmented_tools"), "ok" if ip_ok else "NOT OK", emails, digits))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
