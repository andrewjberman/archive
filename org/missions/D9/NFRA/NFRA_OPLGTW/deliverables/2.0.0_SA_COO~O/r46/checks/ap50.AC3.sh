#!/usr/bin/env bash
# OPLGTW OG-ap-50 AC3 (round 46, PHASE B; the FWD-20 PROOF as the PRD writes it: "one family's cadence against its live schedule; one family's depth against backfill-status and the served data's earliest date"):
# W/FWD20_DRIVEN_READ.json is the ONE driven read of the DEPLOYED family_depth module, run once on the host in a fresh process under the hard guard as the gateway instance role AFTER the release is live:
#  code_sha equals the release sha; families > 0 equal to the denominator; every value carries a claim (claims measured + inferred + absent = values_total, claim-less 0), every absent value carries its reason;
#  schedule_check: the record's value for one family EQUALS the same rule's ScheduleExpression read independently with the AWS CLI; depth_check: the record's frontier and earliest served date for one family's table EQUAL the values read independently from backfill-status.json and a bounded S3 listing;
#  writes_attempted 0; no email-shaped string and no run of 9 or more digits in the record.
# Overrides (dry-run controls only): AP50_DRV_OVERRIDE, AP50_RELREC_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
REC="${AP50_DRV_OVERRIDE:-$W/FWD20_DRIVEN_READ.json}"; RELREC="${AP50_RELREC_OVERRIDE:-$W/ap50_release.json}"
[ -f "$REC" ] && [ -f "$RELREC" ] || { echo "FWD20_DRIVEN_READ.json or ap50_release.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python -I - "$(native "$REC")" "$(native "$RELREC")" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); d = d.get("body", d)
rel = json.load(open(sys.argv[2], encoding="utf-8")).get("release_sha", "")
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
GUARDS = ("oom_score_adj_1000_rlimit_as_1400mb", "oom_score_adj_1000_cgroup_memmax_1400mb")
cl = d.get("claims") or {}
tot = d.get("values_total")
claims_ok = all(isn(cl.get(k)) for k in ("measured", "inferred", "absent")) and isn(tot) and cl["measured"] + cl["inferred"] + cl["absent"] == tot and tot > 0 and d.get("claim_less_values") == 0
absent_ok = d.get("absent_with_reason") == cl.get("absent")
fam_ok = isn(d.get("families")) and d["families"] > 0 and d.get("denominator") == d.get("families")
code_ok = bool(rel) and d.get("code_sha") == rel and d.get("guard") in GUARDS and d.get("identity") == "gateway_instance_role"
sc = d.get("schedule_check") or {}
sc_ok = bool(sc.get("family")) and bool(sc.get("record_value")) and sc.get("record_value") == sc.get("independent_value") and bool(sc.get("independent_source"))
dc = d.get("depth_check") or {}
dc_ok = (bool(dc.get("family")) and bool(dc.get("record_frontier")) and dc.get("record_frontier") == dc.get("independent_frontier")
         and bool(dc.get("record_earliest")) and dc.get("record_earliest") == dc.get("independent_earliest") and bool(dc.get("independent_source")))
emails = len(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw))
digits = len(re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40,64}"', '""', raw)))
ok = claims_ok and absent_ok and fam_ok and code_ok and sc_ok and dc_ok and d.get("writes_attempted") == 0 and emails == 0 and digits == 0
print("driven read of the deployed module (code sha equals the release %s; hard guard %s; as the instance role %s): families %s of denominator %s: %s" % (
      "yes" if d.get("code_sha") == rel and rel else "NO", "yes" if d.get("guard") in GUARDS else "NO", "yes" if d.get("identity") == "gateway_instance_role" else "NO", d.get("families"), d.get("denominator"), "ok" if (fam_ok and code_ok) else "NOT OK"))
print("values %s: measured %s, inferred %s, absent %s (each with its reason %s), claim-less %s (want 0): %s" % (tot, cl.get("measured"), cl.get("inferred"), cl.get("absent"), d.get("absent_with_reason"), d.get("claim_less_values"), "ok" if (claims_ok and absent_ok) else "NOT OK"))
print("cadence: family %s, the record says %s and the CLI says %s: %s" % (sc.get("family"), sc.get("record_value"), sc.get("independent_value"), "equal" if sc_ok else "NOT EQUAL"))
print("depth: family %s, frontier record %s vs independent %s, earliest served date record %s vs independent %s: %s" % (dc.get("family"), dc.get("record_frontier"), dc.get("independent_frontier"), dc.get("record_earliest"), dc.get("independent_earliest"), "equal" if dc_ok else "NOT EQUAL"))
print("writes attempted %s (want 0); email-shaped strings %d (want 0); digit runs of 9 or more %d (want 0)" % (d.get("writes_attempted"), emails, digits))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
