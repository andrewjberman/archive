#!/usr/bin/env bash
# OPLGTW OG-ap-40 AC1 (round 42, the eighth batched gateway release: the loopback probe listener OG-pr-1, under its own never-widen; PHASE A):
#  - the SSRF audit OG-sec-1 reads CLEAN (the CTO's precondition, msg 35584: any controllable target is a STOP);
#  - W/ap40_release.json {base_sha, release_sha, trunk_sha}; base_sha is the live ref BEFORE this release; base..release differs only in app/probe_listener.py, app/server.py (the lifespan hookup) and tests/test_og_*.py,
#    every file byte-equal to its blob at trunk_sha; NOT in the diff: client_*.py, typed_scope.py, etfs_rivals_flow.py, tools.py, destructive_ops.py, deploy-to-ec2.sh, the unit file, the manifest, the catalog, Terraform;
#  - W/PHASE_A_OG-ap-40.json (every host run under a HARD GUARD): the listener binds 127.0.0.1 only (not in the ALB target group), is OFF by default, arms by an SSM lease of 60 minutes or less and expires closed,
#    serves exactly etfs_compare_peers and client_get_transactions for the fixed probe principal and the test account, refuses any other tool and any other account, labels every call probe:<order>, and the service heap read works.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
GW=infra/aws/ec2/opal-gateway
W=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1
SEC="${AP40_SEC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~145/SSRF_AUDIT.json}"
REC="${AP40_REC_OVERRIDE:-$W/ap40_release.json}"
PA="${AP40_PA_OVERRIDE:-$W/PHASE_A_OG-ap-40.json}"
ASK="${AP40_ASK_OVERRIDE:-$W/NEVER_WIDEN_ASK_OG-ap-40.md}"
[ -f "$SEC" ] && [ -f "$REC" ] && [ -f "$PA" ] && [ -f "$ASK" ] || { echo "SSRF_AUDIT.json, ap40_release.json, PHASE_A_OG-ap-40.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
secv=$(python -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));b=d.get('body',d);print(b.get('verdict',''),b.get('controllable_yes',''))" "$(native "$SEC")" | tr -d '\r')
read -r base rel trunk <<<"$(python -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''),d.get('trunk_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" && git cat-file -e "${base}^{commit}" && git cat-file -e "${trunk}^{commit}" || { echo "base, release or trunk sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
read -r dep prev <<<"$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -I -c "import json,sys;s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'];print(s.get('deployed_commit','NONE'),s.get('previous_deployed_commit','NONE'))" | tr -d '\r')"
live=$dep; [ "$dep" = "$rel" ] && live=$prev
[ -n "$AP40_LIVE_OVERRIDE" ] && live=$AP40_LIVE_OVERRIDE
TAKE="$GW/app/probe_listener.py $GW/app/server.py $GW/tests/test_og_pr1.py"
ALLOW="^($GW/(app/probe_listener\.py|app/server\.py|tests/test_og_[a-z0-9]+\.py)|infra/logic/registry/[A-Za-z0-9_]+\.json)$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
missing=0; for p in $TAKE; do printf '%s\n' "$files" | grep -qx "$p" || missing=$((missing+1)); done
neq=0; for p in $files; do a=$(git rev-parse "$rel:$p" 2>/dev/null | tr -d '\r'); b=$(git rev-parse "$trunk:$p" 2>/dev/null | tr -d '\r'); [ -n "$a" ] && [ "$a" = "$b" ] || neq=$((neq+1)); done
barred=$(printf '%s\n' "$files" | grep -cE "$GW/app/(client_[a-z0-9_]+|typed_scope|etfs_rivals_flow|tools|destructive_ops)\.py|$GW/deploy-to-ec2\.sh|$GW/deploy/opal-gateway\.service|infra/aws/ec2/EC2_MANIFEST\.json|\.tf$|$GW/app/refs/")
rec=$(python -I - "$(native "$PA")" "$rel" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
GUARDS = ("oom_score_adj_1000_rlimit_as_1400mb", "oom_score_adj_1000_cgroup_memmax_1400mb")
same = b.get("release_sha") == sys.argv[2]
ls = b.get("listener") or {}
listener_ok = (ls.get("bound_host") == "127.0.0.1" and ls.get("reachable_from_outside") is False and ls.get("in_alb_target_group") is False and ls.get("off_by_default") is True
               and isn(ls.get("lease_minutes")) and 0 < ls["lease_minutes"] <= 60 and ls.get("expires_closed") is True
               and sorted(ls.get("tools_served") or []) == ["client_get_transactions", "etfs_compare_peers"]
               and ls.get("other_tool_refused") is True and ls.get("other_account_refused") is True and ls.get("audit_label_on_every_call") is True
               and ls.get("guard") in GUARDS)
hp = b.get("heap_read") or {}
heap_ok = hp.get("method") in ("tracemalloc_signal", "py_spy_dump", "proc_status_signal") and isn(hp.get("before_mb")) and isn(hp.get("after_mb")) and hp.get("service_pid_stable") is True
tests = b.get("tests") or {}
tests_ok = tests.get("arm_call_expiry_passed") is True and isn(tests.get("window_set_passed")) and tests["window_set_passed"] >= 1 and tests.get("window_set_failed") == 0
bignums = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40,64}"', '""', raw))
ok = same and listener_ok and heap_ok and tests_ok and not bignums
print("host runs on release_sha %s" % ("equal" if same else "NOT equal"))
print("listener: bound %s, reachable from outside %s, in the ALB target group %s, off by default %s, lease %s minutes, expires closed %s, tools %s, other tool refused %s, other account refused %s, audit label on every call %s: %s" % (
      ls.get("bound_host"), ls.get("reachable_from_outside"), ls.get("in_alb_target_group"), ls.get("off_by_default"), ls.get("lease_minutes"), ls.get("expires_closed"), ls.get("tools_served"), ls.get("other_tool_refused"), ls.get("other_account_refused"), ls.get("audit_label_on_every_call"), "ok" if listener_ok else "NOT OK"))
print("heap read of the service PID: method %s, before %s MB, after %s MB, pid stable %s: %s; tests: arm/call/expiry %s, window set passed %s failed %s: %s; digit runs of 9 or more %d (want 0)" % (
      hp.get("method"), hp.get("before_mb"), hp.get("after_mb"), hp.get("service_pid_stable"), "ok" if heap_ok else "NOT OK", tests.get("arm_call_expiry_passed"), tests.get("window_set_passed"), tests.get("window_set_failed"), "ok" if tests_ok else "NOT OK", len(bignums)))
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
echo "SSRF audit (OG-sec-1) verdict and controllable count: $secv (want CLEAN 0)"
echo "base ${base:0:10} is the live ref before this release: $([ "$base" = "$live" ] && echo yes || echo no) (manifest ${dep:0:10}/${prev:0:10}); release ${rel:0:10}; trunk ${trunk:0:10}"
hrb=$(git rev-parse "$base:$GW/app/harvest_research.py" 2>/dev/null | tr -d ''); hrr=$(git rev-parse "$rel:$GW/app/harvest_research.py" 2>/dev/null | tr -d '')
echo "harvest_research.py blob carried unchanged from the live ref (CT4): base ${hrb:0:10}, release ${hrr:0:10}: $([ -n "$hrb" ] && [ "$hrb" = "$hrr" ] && echo equal || echo DIFFERENT); the CTO-verified blob of the live ref 4257a2aa42 (msg 35603) is 574959b682: $([ "$hrr" = 574959b682d4a13a0a429c45fa00b77b6caa2ab5 ] && echo carried || echo NOT-CARRIED)"
echo "files differing $n; outside the take list $outside (want 0); take-list files missing $missing (want 0); not byte-equal to trunk's $neq (want 0); client, typed_scope, flow, tools, destructive_ops, deploy script, unit, manifest, catalog or Terraform files in the diff $barred (want 0)"
printf '%s\n' "$rec" | sed '$d'
echo "ask has the three halves $halves"
[ "$secv" = "CLEAN 0" ] && [ -n "$hrb" ] && [ "$hrb" = "$hrr" ] && [ "$hrr" = 574959b682d4a13a0a429c45fa00b77b6caa2ab5 ] && [ "$base" = "$live" ] && [ "$n" -ge 3 ] && [ "$outside" = 0 ] && [ "$missing" = 0 ] && [ "$neq" = 0 ] && [ "$barred" = 0 ] && [ "$halves" = yes ] && [ "$(printf '%s\n' "$rec" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
