#!/usr/bin/env bash
# OPLGTW OG-ap-39 AC1 (round 42, the seventh batched gateway release: the measured window page size, the db3 test that reads the worktree, the absent_reason codes documented; PHASE A):
#  - W/ap39_release.json {base_sha, release_sha, trunk_sha}; base_sha is the live ref BEFORE this release (EC2_MANIFEST deployed_commit at HEAD; previous_deployed_commit once this release is the deployed one);
#  - base..release differs only in the take list (app/client_adapter_bd49f.py, app/tools.py, tests/test_og_db3.py, tests/test_og_en29.py, and tests/test_og_*.py files OG-en-29 updated for the new size), every file byte-equal to its blob at trunk_sha, all four named files present;
#  - NOT in the diff: client_core.py, typed_scope.py, etfs_rivals_flow.py, destructive_ops.py, deploy-to-ec2.sh, the unit file, the manifest, the data catalog, Terraform;
#  - W/PHASE_A_OG-ap-39.json (every host run under a HARD GUARD): the page size in the release equals the sweep's chosen size, the 49F chain at that size answers within the pre-stated numbers and the same rows as the live code, the 27-tool read live against candidate.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
GW=infra/aws/ec2/opal-gateway
W=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1
REC="${AP39_REC_OVERRIDE:-$W/ap39_release.json}"
PA="${AP39_PA_OVERRIDE:-$W/PHASE_A_OG-ap-39.json}"
ASK="${AP39_ASK_OVERRIDE:-$W/NEVER_WIDEN_ASK_OG-ap-39.md}"
SWEEP="${AP39_SWEEP_OVERRIDE:-$W/PAGE_SWEEP.json}"
[ -f "$REC" ] && [ -f "$PA" ] && [ -f "$ASK" ] && [ -f "$SWEEP" ] || { echo "ap39_release.json, PHASE_A_OG-ap-39.json, PAGE_SWEEP.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel trunk <<<"$(python -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''),d.get('trunk_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" && git cat-file -e "${base}^{commit}" && git cat-file -e "${trunk}^{commit}" || { echo "base, release or trunk sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
read -r dep prev <<<"$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -I -c "import json,sys;s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'];print(s.get('deployed_commit','NONE'),s.get('previous_deployed_commit','NONE'))" | tr -d '\r')"
live=$dep; [ "$dep" = "$rel" ] && live=$prev
[ -n "$AP39_LIVE_OVERRIDE" ] && live=$AP39_LIVE_OVERRIDE
TAKE="$GW/app/client_adapter_bd49f.py $GW/app/tools.py $GW/tests/test_og_db3.py $GW/tests/test_og_en29.py"
ALLOW="^($GW/(app/client_adapter_bd49f\.py|app/tools\.py|tests/test_og_[a-z0-9]+\.py)|infra/logic/registry/[A-Za-z0-9_]+\.json)$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
missing=0; for p in $TAKE; do printf '%s\n' "$files" | grep -qx "$p" || missing=$((missing+1)); done
neq=0; for p in $files; do a=$(git rev-parse "$rel:$p" 2>/dev/null | tr -d '\r'); b=$(git rev-parse "$trunk:$p" 2>/dev/null | tr -d '\r'); [ -n "$a" ] && [ "$a" = "$b" ] || neq=$((neq+1)); done
barred=$(printf '%s\n' "$files" | grep -cE "$GW/app/(client_core|typed_scope|etfs_rivals_flow|destructive_ops)\.py|$GW/deploy-to-ec2\.sh|$GW/deploy/opal-gateway\.service|infra/aws/ec2/EC2_MANIFEST\.json|\.tf$|$GW/app/refs/")
chosen=$(python -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print((d.get('body',d)).get('chosen_partitions',''))" "$(native "$SWEEP")" | tr -d '\r')
relconst=$(git show "$rel:$GW/app/client_adapter_bd49f.py" | sed -n 's/^PAGE_PARTITIONS = \([0-9]*\).*/\1/p' | head -1 | tr -d '\r')
rec=$(python -I - "$(native "$PA")" "$rel" "$chosen" <<'PYEOF'
import json, re, statistics, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
GUARDS = ("oom_score_adj_1000_rlimit_as_1400mb", "oom_score_adj_1000_cgroup_memmax_1400mb")
same = b.get("release_sha") == sys.argv[2]
chosen = int(sys.argv[3]) if sys.argv[3].isdigit() else None
ch = b.get("chain") or {}
# the rule, fixed by the order before any run: FIVE fresh runs at the chosen size under the cgroup guard; the median of the five run medians 20 MB or less, no run median above 30 MB, the longest page of every run under 15 s,
# host peak under 75 in every run, and the combined rows of the newest 120 partitions equal (sha256) to the LIVE code's in every run
runs = ch.get("runs") or []
meds = [r.get("median_growth_mb") for r in runs]
meds_ok = len(runs) >= 5 and all(isn(m) for m in meds)
mom = statistics.median(meds) if meds_ok else None
mx = max(meds) if meds_ok else None
chain_ok = (meds_ok and ch.get("partitions_per_page") == chosen and chosen in (30, 60, 120) and mom <= 20 and mx <= 30
            and all(isn(r.get("max_page_wall_s")) and r["max_page_wall_s"] < 15 for r in runs)
            and all(isn(r.get("host_peak_pct")) and r["host_peak_pct"] < 75 for r in runs)
            and all(r.get("rows_hash_120_equal_live") is True for r in runs) and ch.get("guard") in GUARDS)
t27 = b.get("tool27") or {}
names = lambda k: t27.get(k) if isinstance(t27.get(k), list) else None
eq_n, both, better, bad_ref, bad_diff = t27.get("equal"), names("both_failed"), names("candidate_answered_live_failed"), names("live_answered_candidate_refused"), names("answers_differ")
t27_ok = (t27.get("tools") == 27 and isn(eq_n) and both is not None and better is not None and bad_ref == [] and bad_diff == []
          and eq_n + len(both) + len(better) == 27 and t27.get("guard") in GUARDS and t27.get("tools_list_names_equal") is True)
bignums = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40,64}"', '""', raw))
ok = same and chain_ok and t27_ok and not bignums
print("host runs on release_sha %s, every one under a hard guard" % ("equal" if same else "NOT equal"))
print("49F chain at %s partitions per page (the sweep chose %s): %d runs, median of the run medians %s MB (limit 20), highest run median %s MB (limit 30), longest page under 15 s and host peak under 75 and rows equal the live code's in every run: %s" % (
      ch.get("partitions_per_page"), chosen, len(runs), None if mom is None else round(mom, 1), mx, "ok" if chain_ok else "NOT OK"))
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
echo "files differing $n; outside the take list $outside (want 0); take-list files missing $missing (want 0); not byte-equal to trunk's $neq (want 0); client_core, typed_scope, etfs_rivals_flow, destructive_ops, deploy script, unit, manifest, catalog or Terraform files in the diff $barred (want 0)"
echo "PAGE_PARTITIONS in the release blob: ${relconst:-NONE}; the sweep chose: ${chosen:-NONE}"
printf '%s\n' "$rec" | sed '$d'
echo "ask has the three halves $halves"
[ "$base" = "$live" ] && [ "$n" -ge 4 ] && [ "$outside" = 0 ] && [ "$missing" = 0 ] && [ "$neq" = 0 ] && [ "$barred" = 0 ] && [ -n "$chosen" ] && [ "$relconst" = "$chosen" ] && [ "$halves" = yes ] && [ "$(printf '%s\n' "$rec" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
