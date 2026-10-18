#!/usr/bin/env bash
# OPLGTW OG-ap-42 AC1 (round 43, the ninth batched gateway release: the probe-lease firm pin OG-pr-4, the Graph host pin OG-sec-2 and the reset-discriminating test OG-en-31; PHASE A):
#  - the completed SSRF audit OG-sec-3 reads CLEAN (the CTO's precondition: any controllable target is a STOP);
#  - W/ap42_release.json {base_sha, release_sha, trunk_sha, live_ref_host, harvest_blobs}; base_sha IS the live ref read on the host (live_ref_host, the file /opt/opal-gateway/.deployed_commit) and 6575999df5 (dell1's harvest release) is an ancestor of it;
#    base..release differs only in app/probe_listener.py, app/graph.py and tests/test_og_*.py, every file byte-equal to its blob at trunk_sha; the four harvest files (harvest_research, harvest_figures, harvest_identity, harvest_keys) are byte-equal to base's (CARRIED UNCHANGED);
#    NOT in the diff: server.py, client_*.py, typed_scope.py, etfs_rivals_flow.py, tools.py, destructive_ops.py, deploy-to-ec2.sh, the unit file, the manifest, the catalog, Terraform;
#  - W/PHASE_A_OG-ap-42.json (every host run under a HARD GUARD): the firm pin refuses a mismatched firm with 403 probe_firm_refused BEFORE the tool runs, a lease without firm is refused as malformed, the Graph host pin refuses a forged host before any request,
#    NO ARMING happened (armings 0: no SSM lease was written), and the named test set passes on the host.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
GW=infra/aws/ec2/opal-gateway
W=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1
SEC="${AP42_SEC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~153/SSRF_AUDIT_R43.json}"
REC="${AP42_REC_OVERRIDE:-$W/ap42_release.json}"
PA="${AP42_PA_OVERRIDE:-$W/PHASE_A_OG-ap-42.json}"
ASK="${AP42_ASK_OVERRIDE:-$W/NEVER_WIDEN_ASK_OG-ap-42.md}"
[ -f "$SEC" ] && [ -f "$REC" ] && [ -f "$PA" ] && [ -f "$ASK" ] || { echo "SSRF_AUDIT.json, ap42_release.json, PHASE_A_OG-ap-42.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
secv=$(python -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));b=d.get('body',d);print(b.get('verdict',''),b.get('controllable_yes',''))" "$(native "$SEC")" | tr -d '\r')
read -r base rel trunk hostlive <<<"$(python -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''),d.get('trunk_sha',''),d.get('live_ref_host',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" && git cat-file -e "${base}^{commit}" && git cat-file -e "${trunk}^{commit}" || { echo "base, release or trunk sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
live=$hostlive
[ -n "$AP42_LIVE_OVERRIDE" ] && live=$AP42_LIVE_OVERRIDE
DELL=6575999df5d22c0123abfc0c88cd1c6f1efe8c96
git merge-base --is-ancestor "$DELL" "$base" && dellanc=yes || dellanc=no
TAKE="$GW/app/probe_listener.py $GW/app/graph.py $GW/tests/test_og_pr1.py $GW/tests/test_og_sec2.py"
ALLOW="^($GW/(app/probe_listener\.py|app/graph\.py|tests/test_og_[a-z0-9]+\.py)|infra/logic/registry/[A-Za-z0-9_]+\.json)$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
missing=0; for p in $TAKE; do printf '%s\n' "$files" | grep -qx "$p" || missing=$((missing+1)); done
neq=0; for p in $files; do a=$(git rev-parse "$rel:$p" 2>/dev/null | tr -d '\r'); b=$(git rev-parse "$trunk:$p" 2>/dev/null | tr -d '\r'); [ -n "$a" ] && [ "$a" = "$b" ] || neq=$((neq+1)); done
barred=$(printf '%s\n' "$files" | grep -cE "$GW/app/(client_[a-z0-9_]+|typed_scope|etfs_rivals_flow|tools|destructive_ops|server)\.py|$GW/deploy-to-ec2\.sh|$GW/deploy/opal-gateway\.service|infra/aws/ec2/EC2_MANIFEST\.json|\.tf$|$GW/app/refs/")
rec=$(python -I - "$(native "$PA")" "$rel" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
GUARDS = ("oom_score_adj_1000_rlimit_as_1400mb", "oom_score_adj_1000_cgroup_memmax_1400mb")
same = b.get("release_sha") == sys.argv[2]
fp = b.get("firm_pin") or {}
fp_ok = (fp.get("mismatched_firm_status") == 403 and fp.get("mismatched_firm_error") == "probe_firm_refused" and fp.get("tool_ran_on_mismatch") is False
         and fp.get("matched_firm_answered") is True and fp.get("lease_without_firm_refused") is True and fp.get("guard") in GUARDS)
gp = b.get("graph_pin") or {}
gp_ok = gp.get("forged_host_refused") is True and gp.get("request_sent_to_forged_host") is False and gp.get("graph_host_allowed") is True
ls = b.get("listener") or {}
listener_ok = ls.get("bound_host") == "127.0.0.1" and ls.get("off_by_default") is True and ls.get("armings") == 0 and ls.get("lease_parameter_written") is False
tests = b.get("tests") or {}
tests_ok = isn(tests.get("named_passed")) and tests["named_passed"] >= 1 and tests.get("named_failed") == 0 and isn(tests.get("window_set_passed")) and tests["window_set_passed"] >= 1 and tests.get("window_set_failed") == 0
bignums = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40,64}"', '""', raw))
ok = same and fp_ok and gp_ok and listener_ok and tests_ok and not bignums
print("host runs on release_sha %s" % ("equal" if same else "NOT equal"))
print("firm pin on the host: mismatched firm %s %s, the tool ran on the mismatch %s, a matched firm answered %s, a lease without firm refused %s: %s; graph host pin: forged host refused %s, a request was sent to it %s, graph.microsoft.com allowed %s: %s" % (
      fp.get("mismatched_firm_status"), fp.get("mismatched_firm_error"), fp.get("tool_ran_on_mismatch"), fp.get("matched_firm_answered"), fp.get("lease_without_firm_refused"), "ok" if fp_ok else "NOT OK",
      gp.get("forged_host_refused"), gp.get("request_sent_to_forged_host"), gp.get("graph_host_allowed"), "ok" if gp_ok else "NOT OK"))
print("listener: bound %s, off by default %s, armings %s (want 0), lease parameter written %s (want False): %s; tests: named passed %s failed %s, window set passed %s failed %s: %s; digit runs of 9 or more %d (want 0)" % (
      ls.get("bound_host"), ls.get("off_by_default"), ls.get("armings"), ls.get("lease_parameter_written"), "ok" if listener_ok else "NOT OK", tests.get("named_passed"), tests.get("named_failed"), tests.get("window_set_passed"), tests.get("window_set_failed"), "ok" if tests_ok else "NOT OK", len(bignums)))
print("OK" if ok else "NO")
PYEOF
)
rec=$(printf '%s' "$rec" | tr -d '\r')
halves=$(python -I - "$(native "$ASK")" <<'PYEOF'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
print("yes" if all(re.search(r"(?mi)^#+ .*%s" % h, t) for h in ("CTO", "COO", "CVO")) else "no")
PYEOF
)
halves=$(printf '%s' "$halves" | tr -d '\r')
echo "SSRF audit (OG-sec-3) verdict and controllable count: $secv (want CLEAN 0)"
echo "base ${base:0:10} is the live ref read on the host: $([ "$base" = "$live" ] && [ -n "$live" ] && echo yes || echo no); dell1 harvest release ${DELL:0:10} is an ancestor of base: $dellanc; release ${rel:0:10}; trunk ${trunk:0:10}"
hcar=0; hn=0; for h in harvest_research harvest_figures harvest_identity harvest_keys; do hn=$((hn+1)); a=$(git rev-parse "$base:$GW/app/$h.py" 2>/dev/null | tr -d '\r'); b2=$(git rev-parse "$rel:$GW/app/$h.py" 2>/dev/null | tr -d '\r'); [ -n "$a" ] && [ "$a" = "$b2" ] && hcar=$((hcar+1)); done
echo "dell1's four harvest files byte-equal between the live base and the release: $hcar of $hn (want 4 of 4)"
echo "files differing $n; outside the take list $outside (want 0); take-list files missing $missing (want 0); not byte-equal to trunk's $neq (want 0); client, typed_scope, flow, tools, destructive_ops, deploy script, unit, manifest, catalog or Terraform files in the diff $barred (want 0)"
printf '%s\n' "$rec" | sed '$d'
echo "ask has the three halves $halves"
[ "$secv" = "CLEAN 0" ] && [ "$hcar" = 4 ] && [ "$dellanc" = yes ] && [ -n "$live" ] && [ "$base" = "$live" ] && [ "$n" -ge 4 ] && [ "$outside" = 0 ] && [ "$missing" = 0 ] && [ "$neq" = 0 ] && [ "$barred" = 0 ] && [ "$halves" = yes ] && [ "$(printf '%s\n' "$rec" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
