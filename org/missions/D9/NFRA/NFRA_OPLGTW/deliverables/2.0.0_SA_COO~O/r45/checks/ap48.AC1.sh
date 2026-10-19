#!/usr/bin/env bash
# OPLGTW OG-ap-48 AC1 (round 45, the twelfth batched gateway release; PHASE A): the audit lake leg made bounded and audible (OG-pr-6: app/audit.py and tests/test_og_pr6.py).
#  - W/ap48_release.json {base_sha, release_sha, trunk_sha, live_ref_host}; base_sha IS the live ref read on the host (live_ref_host, the file /opt/opal-gateway/.deployed_commit; expected e09c30c3f0, the eleventh release, unless dell1 has deployed since);
#    base..release differs ONLY in app/audit.py and tests/test_og_pr6.py, each byte-equal to its blob at trunk_sha; every other file (dell1's harvest files included) is byte-equal between base and release;
#    NOT in the diff: server.py, graph.py, tools.py, client_*.py, typed_scope.py, etfs_rivals_flow.py, destructive_ops.py, probe_listener.py, deploy-to-ec2.sh, the unit file, the manifest, the catalog, Terraform.
#  - W/PHASE_A_OG-ap-48.json (every host run under a HARD GUARD): `audit_leg` = in a fresh process, the audit S3 client is built with an explicit botocore Config of bounded connect and read timeouts and a retry cap, a put to a black-hole endpoint raises within a bound,
#    the failure counter reads 1 and ONE stderr line was written, the local floor line is still written; `process_wide_state` names what the change touches (CVO verdict 35844): stderr volume (rate-bounded) and the boto3 client's botocore Config; NO ARMING.
#  - W/NEVER_WIDEN_ASK_OG-ap-48.md has the three halves AND a line "process-wide state this change touches:" naming the list, or "none, read".
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
GW=infra/aws/ec2/opal-gateway
W=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1
SEC="${AP48_SEC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~153/SSRF_AUDIT_R43.json}"   # outbound HTTP code unchanged by this release; still read
REC="${AP48_REC_OVERRIDE:-$W/ap48_release.json}"
PA="${AP48_PA_OVERRIDE:-$W/PHASE_A_OG-ap-48.json}"
ASK="${AP48_ASK_OVERRIDE:-$W/NEVER_WIDEN_ASK_OG-ap-48.md}"
[ -f "$SEC" ] && [ -f "$REC" ] && [ -f "$PA" ] && [ -f "$ASK" ] || { echo "SSRF_AUDIT.json, ap48_release.json, PHASE_A_OG-ap-48.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
secv=$(python -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));b=d.get('body',d);print(b.get('verdict',''),b.get('controllable_yes',''))" "$(native "$SEC")" | tr -d '\r')
read -r base rel trunk hostlive <<<"$(python -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''),d.get('trunk_sha',''),d.get('live_ref_host',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" && git cat-file -e "${base}^{commit}" && git cat-file -e "${trunk}^{commit}" || { echo "base, release or trunk sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
live=$hostlive
[ -n "$AP48_LIVE_OVERRIDE" ] && live=$AP48_LIVE_OVERRIDE
DELL=6575999df5d22c0123abfc0c88cd1c6f1efe8c96
git merge-base --is-ancestor "$DELL" "$base" && dellanc=yes || dellanc=no
TAKE="$GW/app/audit.py $GW/tests/test_og_pr6.py"
ALLOW="^($GW/(app/audit\.py|tests/test_og_pr6\.py)|infra/logic/registry/[A-Za-z0-9_]+\.json)$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
missing=0; for p in $TAKE; do printf '%s\n' "$files" | grep -qx "$p" || missing=$((missing+1)); done
neq=0; for p in $files; do a=$(git rev-parse "$rel:$p" 2>/dev/null | tr -d '\r'); b=$(git rev-parse "$trunk:$p" 2>/dev/null | tr -d '\r'); [ -n "$a" ] && [ "$a" = "$b" ] || neq=$((neq+1)); done
barred=$(printf '%s\n' "$files" | grep -cE "$GW/app/(client_[a-z0-9_]+|typed_scope|etfs_rivals_flow|tools|destructive_ops|server|graph|probe_listener)\.py|$GW/deploy-to-ec2\.sh|$GW/deploy/opal-gateway\.service|infra/aws/ec2/EC2_MANIFEST\.json|\.tf$")
rec=$(python -I - "$(native "$PA")" "$rel" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
GUARDS = ("oom_score_adj_1000_rlimit_as_1400mb", "oom_score_adj_1000_cgroup_memmax_1400mb")
same = b.get("release_sha") == sys.argv[2]
al = b.get("audit_leg") or {}
cfg = al.get("config") or {}
al_ok = (isn(cfg.get("connect_timeout")) and 0 < cfg["connect_timeout"] <= 5 and isn(cfg.get("read_timeout")) and 0 < cfg["read_timeout"] <= 10
         and isinstance(cfg.get("max_attempts"), int) and 1 <= cfg["max_attempts"] <= 2
         and isn(al.get("failed_put_wall_s")) and 0 < al["failed_put_wall_s"] <= 15 and al.get("counter_after_failure") == 1 and al.get("stderr_lines") == 1
         and al.get("floor_line_written") is True and al.get("guard") in GUARDS)
ls = b.get("listener") or {}
listener_ok = ls.get("bound_host") == "127.0.0.1" and ls.get("off_by_default") is True and ls.get("armings") == 0 and ls.get("lease_parameter_written") is False
tests = b.get("tests") or {}
tests_ok = isn(tests.get("named_passed")) and tests["named_passed"] >= 1 and tests.get("named_failed") == 0 and isn(tests.get("window_set_passed")) and tests["window_set_passed"] >= 1 and tests.get("window_set_failed") == 0
bignums = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40,64}"', '""', raw))
pw = b.get("process_wide_state")
pw_ok = isinstance(pw, str) and len(pw.strip()) >= 20
ok = same and al_ok and listener_ok and tests_ok and pw_ok and not bignums
print("host runs on release_sha %s" % ("equal" if same else "NOT equal"))
print("process-wide state this change touches, as recorded in Phase A (CVO verdict 35844): %s" % ("named" if pw_ok else "ABSENT or too short"))
print("audit lake leg on the host: client Config connect %s s, read %s s, attempts %s; a put to a black-hole endpoint raised in %s s; failure counter %s and stderr lines %s after one failure; the local floor line still written %s: %s" % (
      cfg.get("connect_timeout"), cfg.get("read_timeout"), cfg.get("max_attempts"), al.get("failed_put_wall_s"), al.get("counter_after_failure"), al.get("stderr_lines"), al.get("floor_line_written"), "ok" if al_ok else "NOT OK"))
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
