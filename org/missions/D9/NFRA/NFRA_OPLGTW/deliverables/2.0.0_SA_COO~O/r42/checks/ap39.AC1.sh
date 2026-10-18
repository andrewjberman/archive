#!/usr/bin/env bash
# OPLGTW OG-ap-39 AC1 (round 42, the seventh batched gateway release: the db3 test that reads the worktree and the absent_reason codes documented in the client tools' notes; PHASE A).
# AMENDED A3 (the sweep OG-ev-6 chose 30, so OG-en-29 is superseded: no page-size change):
#  - W/ap39_release.json {base_sha, release_sha, trunk_sha}; base_sha is the live ref BEFORE this release (EC2_MANIFEST deployed_commit at HEAD; previous_deployed_commit once this release is the deployed one);
#  - base..release differs only in the take list (app/tools.py, tests/test_og_db3.py), every file byte-equal to its blob at trunk_sha, both present;
#  - NOT in the diff: client_adapter_bd49f.py, client_core.py, typed_scope.py, etfs_rivals_flow.py, destructive_ops.py, deploy-to-ec2.sh, the unit file, the manifest, the data catalog, Terraform;
#  - harvest_research.py is carried unchanged from the live ref and equals the CTO-verified blob 574959b682d4a13a0a429c45fa00b77b6caa2ab5 (msg 35603, live ref 4257a2aa42);
#  - W/PHASE_A_OG-ap-39.json (every host run under a HARD GUARD): the 27-tool read, live code against candidate, every answer equal (the notes change descriptions, never answers).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
GW=infra/aws/ec2/opal-gateway
W=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1
REC="${AP39_REC_OVERRIDE:-$W/ap39_release.json}"
PA="${AP39_PA_OVERRIDE:-$W/PHASE_A_OG-ap-39.json}"
ASK="${AP39_ASK_OVERRIDE:-$W/NEVER_WIDEN_ASK_OG-ap-39.md}"
[ -f "$REC" ] && [ -f "$PA" ] && [ -f "$ASK" ] || { echo "ap39_release.json, PHASE_A_OG-ap-39.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel trunk <<<"$(python -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''),d.get('trunk_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" && git cat-file -e "${base}^{commit}" && git cat-file -e "${trunk}^{commit}" || { echo "base, release or trunk sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
read -r dep prev <<<"$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -I -c "import json,sys;s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'];print(s.get('deployed_commit','NONE'),s.get('previous_deployed_commit','NONE'))" | tr -d '\r')"
live=$dep; [ "$dep" = "$rel" ] && live=$prev
[ -n "$AP39_LIVE_OVERRIDE" ] && live=$AP39_LIVE_OVERRIDE
TAKE="$GW/app/tools.py $GW/tests/test_og_db3.py"
ALLOW="^($GW/(app/tools\.py|tests/test_og_db3\.py)|infra/logic/registry/[A-Za-z0-9_]+\.json)$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
missing=0; for p in $TAKE; do printf '%s\n' "$files" | grep -qx "$p" || missing=$((missing+1)); done
neq=0; for p in $files; do a=$(git rev-parse "$rel:$p" 2>/dev/null | tr -d '\r'); b=$(git rev-parse "$trunk:$p" 2>/dev/null | tr -d '\r'); [ -n "$a" ] && [ "$a" = "$b" ] || neq=$((neq+1)); done
barred=$(printf '%s\n' "$files" | grep -cE "$GW/app/(client_[a-z0-9_]+|typed_scope|etfs_rivals_flow|destructive_ops)\.py|$GW/deploy-to-ec2\.sh|$GW/deploy/opal-gateway\.service|infra/aws/ec2/EC2_MANIFEST\.json|\.tf$|$GW/app/refs/")
hrb=$(git rev-parse "$base:$GW/app/harvest_research.py" 2>/dev/null | tr -d '\r'); hrr=$(git rev-parse "$rel:$GW/app/harvest_research.py" 2>/dev/null | tr -d '\r')
PIN=574959b682d4a13a0a429c45fa00b77b6caa2ab5
rec=$(python -I - "$(native "$PA")" "$rel" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
GUARDS = ("oom_score_adj_1000_rlimit_as_1400mb", "oom_score_adj_1000_cgroup_memmax_1400mb")
same = b.get("release_sha") == sys.argv[2]
t27 = b.get("tool27") or {}
names = lambda k: t27.get(k) if isinstance(t27.get(k), list) else None
eq_n, both, better, bad_ref, bad_diff = t27.get("equal"), names("both_failed"), names("candidate_answered_live_failed"), names("live_answered_candidate_refused"), names("answers_differ")
t27_ok = (t27.get("tools") == 27 and isn(eq_n) and both is not None and better is not None and bad_ref == [] and bad_diff == []
          and eq_n + len(both) + len(better) == 27 and t27.get("guard") in GUARDS and t27.get("tools_list_names_equal") is True)
bignums = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40,64}"', '""', raw))
ok = same and t27_ok and not bignums
print("host runs on release_sha %s, every one under a hard guard" % ("equal" if same else "NOT equal"))
print("the 27-tool read, live code against candidate under the guard: %s of %s equal; failed on both %s; candidate answered where live failed %s; answered on live and refused on the candidate %s; answers that differ %s; tools/list names equal %s: %s" % (
      eq_n, t27.get("tools"), None if both is None else len(both), None if better is None else len(better), None if bad_ref is None else len(bad_ref), None if bad_diff is None else len(bad_diff), t27.get("tools_list_names_equal"), "ok" if t27_ok else "NOT OK"))
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
echo "base ${base:0:10} is the live ref before this release: $([ "$base" = "$live" ] && echo yes || echo no) (manifest ${dep:0:10}/${prev:0:10}); release ${rel:0:10}; trunk ${trunk:0:10}"
echo "harvest_research.py blob carried unchanged from the live ref (CT4): base ${hrb:0:10}, release ${hrr:0:10}: $([ -n "$hrb" ] && [ "$hrb" = "$hrr" ] && echo equal || echo DIFFERENT); the CTO-verified blob of the live ref 4257a2aa42 (msg 35603) is ${PIN:0:10}: $([ "$hrr" = "$PIN" ] && echo carried || echo NOT-CARRIED)"
echo "files differing $n; outside the take list $outside (want 0); take-list files missing $missing (want 0); not byte-equal to trunk's $neq (want 0); adapter, client_core, typed_scope, etfs_rivals_flow, destructive_ops, deploy script, unit, manifest, catalog or Terraform files in the diff $barred (want 0)"
printf '%s\n' "$rec" | sed '$d'
echo "ask has the three halves $halves"
[ -n "$hrb" ] && [ "$hrb" = "$hrr" ] && [ "$hrr" = "$PIN" ] && [ "$base" = "$live" ] && [ "$n" -ge 2 ] && [ "$outside" = 0 ] && [ "$missing" = 0 ] && [ "$neq" = 0 ] && [ "$barred" = 0 ] && [ "$halves" = yes ] && [ "$(printf '%s\n' "$rec" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
