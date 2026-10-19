#!/usr/bin/env bash
# OPLGTW OG-ap-50 AC1 (round 46, the thirteenth batched gateway release; PHASE A): the family_depth route mounted behind the owner gate (OG-cd-2: app/admin_api.py and tests/test_og_cd2.py), a NEW served route.
#  - W/ap50_release.json {base_sha, release_sha, trunk_sha, live_ref_host}; base_sha IS the live ref read on the host (live_ref_host, the file /opt/opal-gateway/.deployed_commit; expected 6b1a9bd292, the twelfth release, unless dell1 has deployed since);
#    base..release differs ONLY in app/admin_api.py and tests/test_og_cd2.py, each byte-equal to its blob at trunk_sha; every other file (dell1's harvest files, app/family_depth.py and audit.py included) is byte-equal between base and release.
#  - W/PHASE_A_OG-ap-50.json (every host run under a HARD GUARD): `route_leg` = in a fresh process the admin app has one more route, /gateway/families is present, no identity answers 401, a verified non-owner 403, the whoami control 401, a missing-route control 404,
#    and family_depth.read() was not called on a refusal; `host_read` = family_depth.read() run once on the host as the gateway instance role (the IAM of OG-cd-3 applied): families > 0 equal to its denominator, values measured > 0, claim-less 0, bounded wall time and memory;
#    `process_wide_state` names what the change touches (CVO verdict 35844); NO ARMING.
#  - W/NEVER_WIDEN_ASK_OG-ap-50.md has the three halves AND a line "process-wide state this change touches:" naming the list, or "none, read".
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
GW=infra/aws/ec2/opal-gateway
W=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1
SEC="${AP50_SEC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~153/SSRF_AUDIT_R43.json}"   # outbound HTTP code unchanged by this release; still read
REC="${AP50_REC_OVERRIDE:-$W/ap50_release.json}"
PA="${AP50_PA_OVERRIDE:-$W/PHASE_A_OG-ap-50.json}"
ASK="${AP50_ASK_OVERRIDE:-$W/NEVER_WIDEN_ASK_OG-ap-50.md}"
[ -f "$SEC" ] && [ -f "$REC" ] && [ -f "$PA" ] && [ -f "$ASK" ] || { echo "SSRF_AUDIT.json, ap50_release.json, PHASE_A_OG-ap-50.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
secv=$(python -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));b=d.get('body',d);print(b.get('verdict',''),b.get('controllable_yes',''))" "$(native "$SEC")" | tr -d '\r')
read -r base rel trunk hostlive <<<"$(python -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''),d.get('trunk_sha',''),d.get('live_ref_host',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" && git cat-file -e "${base}^{commit}" && git cat-file -e "${trunk}^{commit}" || { echo "base, release or trunk sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
live=$hostlive
[ -n "$AP50_LIVE_OVERRIDE" ] && live=$AP50_LIVE_OVERRIDE
DELL=6575999df5d22c0123abfc0c88cd1c6f1efe8c96
git merge-base --is-ancestor "$DELL" "$base" && dellanc=yes || dellanc=no
TAKE="$GW/app/admin_api.py $GW/tests/test_og_cd2.py"
ALLOW="^($GW/(app/admin_api\.py|tests/test_og_cd2\.py))$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
missing=0; for p in $TAKE; do printf '%s\n' "$files" | grep -qx "$p" || missing=$((missing+1)); done
neq=0; for p in $files; do a=$(git rev-parse "$rel:$p" 2>/dev/null | tr -d '\r'); b=$(git rev-parse "$trunk:$p" 2>/dev/null | tr -d '\r'); [ -n "$a" ] && [ "$a" = "$b" ] || neq=$((neq+1)); done
barred=$(printf '%s\n' "$files" | grep -cE "$GW/app/(client_[a-z0-9_]+|typed_scope|etfs_rivals_flow|tools|destructive_ops|server|graph|probe_listener|audit|family_depth|owner_gate)\.py|$GW/deploy-to-ec2\.sh|$GW/deploy/opal-gateway\.service|infra/aws/ec2/EC2_MANIFEST\.json|\.tf$")
rec=$(python -I - "$(native "$PA")" "$rel" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
GUARDS = ("oom_score_adj_1000_rlimit_as_1400mb", "oom_score_adj_1000_cgroup_memmax_1400mb")
same = b.get("release_sha") == sys.argv[2]
rl = b.get("route_leg") or {}
rl_ok = (isn(rl.get("routes_before")) and isn(rl.get("routes_after")) and rl["routes_after"] == rl["routes_before"] + 1 and rl.get("families_route_present_after") is True
         and rl.get("unauth_status") == 401 and rl.get("nonowner_status") == 403 and rl.get("whoami_control_unauth_status") == 401 and rl.get("missing_route_control_status") == 404
         and rl.get("read_called_on_refusal") is False and rl.get("guard") in GUARDS)
hr = b.get("host_read") or {}
hr_ok = (isn(hr.get("families")) and hr["families"] > 0 and hr.get("denominator") == hr.get("families") and isn(hr.get("values_total")) and hr["values_total"] > 0
         and isn(hr.get("measured_values")) and hr["measured_values"] > 0 and hr.get("claim_less_values") == 0 and isn(hr.get("wall_s")) and 0 < hr["wall_s"] <= 110
         and isn(hr.get("peak_rss_mb")) and 0 < hr["peak_rss_mb"] <= 1000 and hr.get("guard") in GUARDS and hr.get("identity") == "gateway_instance_role")
ls = b.get("listener") or {}
listener_ok = ls.get("bound_host") == "127.0.0.1" and ls.get("off_by_default") is True and ls.get("armings") == 0 and ls.get("lease_parameter_written") is False
tests = b.get("tests") or {}
tests_ok = isn(tests.get("named_passed")) and tests["named_passed"] >= 1 and tests.get("named_failed") == 0 and isn(tests.get("window_set_passed")) and tests["window_set_passed"] >= 1 and tests.get("window_set_failed") == 0
bignums = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40,64}"', '""', raw))
pw = b.get("process_wide_state")
pw_ok = isinstance(pw, str) and len(pw.strip()) >= 20
ok = same and rl_ok and hr_ok and listener_ok and tests_ok and pw_ok and not bignums
print("host runs on release_sha %s" % ("equal" if same else "NOT equal"))
print("process-wide state this change touches, as recorded in Phase A (CVO verdict 35844): %s" % ("named" if pw_ok else "ABSENT or too short"))
print("route leg on the host (fresh process, hard guard): admin routes %s before, %s after; /gateway/families present %s; no identity %s (want 401), a verified non-owner %s (want 403), the whoami control %s (want 401), a missing-route control %s (want 404), read() called on a refusal %s (want False): %s" % (
      rl.get("routes_before"), rl.get("routes_after"), rl.get("families_route_present_after"), rl.get("unauth_status"), rl.get("nonowner_status"), rl.get("whoami_control_unauth_status"), rl.get("missing_route_control_status"), rl.get("read_called_on_refusal"), "ok" if rl_ok else "NOT OK"))
print("family_depth read on the host as the gateway instance role: families %s of denominator %s; values %s, measured %s, claim-less %s (want 0); wall %s s; peak rss %s MB: %s" % (
      hr.get("families"), hr.get("denominator"), hr.get("values_total"), hr.get("measured_values"), hr.get("claim_less_values"), hr.get("wall_s"), hr.get("peak_rss_mb"), "ok" if hr_ok else "NOT OK"))
print("listener: bound %s, off by default %s, armings %s (want 0), lease parameter written %s (want False): %s; tests: named passed %s failed %s, window set passed %s failed %s: %s; digit runs of 9 or more %d (want 0)" % (
      ls.get("bound_host"), ls.get("off_by_default"), ls.get("armings"), ls.get("lease_parameter_written"), "ok" if listener_ok else "NOT OK", tests.get("named_passed"), tests.get("named_failed"), tests.get("window_set_passed"), tests.get("window_set_failed"), "ok" if tests_ok else "NOT OK", len(bignums)))
print("OK" if ok else "NO")
PYEOF
)
rec=$(printf '%s' "$rec" | tr -d '\r')
halves=$(python -I - "$(native "$ASK")" <<'PYEOF'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
print("yes" if all(re.search(r"(?mi)^#+ .*%s" % h, t) for h in ("CTO", "COO", "CVO")) and re.search(r"(?i)process-wide state this change touches\s*:\s*\S", t) else "no")
PYEOF
)
halves=$(printf '%s' "$halves" | tr -d '\r')
echo "SSRF audit (OG-sec-3, outbound HTTP code unchanged by this release) verdict and controllable count: $secv (want CLEAN 0)"
echo "base ${base:0:10} is the live ref read on the host: $([ "$base" = "$live" ] && [ -n "$live" ] && echo yes || echo no); dell1 harvest release ${DELL:0:10} is an ancestor of base: $dellanc; release ${rel:0:10}; trunk ${trunk:0:10}"
hcar=0; hn=0; for h in harvest_research harvest_figures harvest_identity harvest_keys; do hn=$((hn+1)); a=$(git rev-parse "$base:$GW/app/$h.py" 2>/dev/null | tr -d '\r'); b2=$(git rev-parse "$rel:$GW/app/$h.py" 2>/dev/null | tr -d '\r'); [ -n "$a" ] && [ "$a" = "$b2" ] && hcar=$((hcar+1)); done
echo "dell1's four harvest files byte-equal between the live base and the release: $hcar of $hn (want 4 of 4)"
echo "files differing $n; outside the take list $outside (want 0); take-list files missing $missing (want 0); not byte-equal to trunk's $neq (want 0); client, typed_scope, flow, tools, destructive_ops, listener, deploy script, unit, manifest, catalog or Terraform files in the diff $barred (want 0)"
printf '%s\n' "$rec" | sed '$d'
echo "ask has the three halves and the process-wide state line $halves"
[ "$secv" = "CLEAN 0" ] && [ "$hcar" = 4 ] && [ "$dellanc" = yes ] && [ -n "$live" ] && [ "$base" = "$live" ] && [ "$n" = 2 ] && [ "$outside" = 0 ] && [ "$missing" = 0 ] && [ "$neq" = 0 ] && [ "$barred" = 0 ] && [ "$halves" = yes ] && [ "$(printf '%s\n' "$rec" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
