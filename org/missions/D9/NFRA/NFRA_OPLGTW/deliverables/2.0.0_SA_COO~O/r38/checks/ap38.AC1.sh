#!/usr/bin/env bash
# OPLGTW OG-ap-38 AC1 (round 41, the sixth batched gateway release: the repair of the ARMED hazard Z-S375, PHASE A):
#  - W/ap38_release.json {base_sha, release_sha, trunk_sha}; base_sha is the live ref BEFORE this release (EC2_MANIFEST deployed_commit at HEAD; previous_deployed_commit once this release is the deployed one);
#  - base..release differs only in the take list (app/typed_scope.py, app/etfs_rivals_flow.py, deploy/opal-gateway.service, tests/test_og_en25.py, tests/test_og_un1.py, and only if the naming gate needs it a registry file),
#    every file byte-equal to its blob at trunk_sha, all five present;
#  - NOT in the diff: tools.py, client_*.py, destructive_ops.py, deploy-to-ec2.sh, the manifest, the catalog, Terraform;
#  - W/PHASE_A_OG-ap-38.json (every host run under a HARD GUARD, never unguarded): the call that ran away (etfs_compare_peers with an unrecognised period and axis) answers in bounded memory and time, a valid pair answers,
#    the 49F chain is unchanged, the unit's limits are acceptable to systemd on the host.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
GW=infra/aws/ec2/opal-gateway
W=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1
REC="${AP38_REC_OVERRIDE:-$W/ap38_release.json}"
PA="${AP38_PA_OVERRIDE:-$W/PHASE_A_OG-ap-38.json}"
ASK="${AP38_ASK_OVERRIDE:-$W/NEVER_WIDEN_ASK_OG-ap-38.md}"
[ -f "$REC" ] && [ -f "$PA" ] && [ -f "$ASK" ] || { echo "ap38_release.json, PHASE_A_OG-ap-38.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel trunk <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''),d.get('trunk_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" && git cat-file -e "${base}^{commit}" && git cat-file -e "${trunk}^{commit}" || { echo "base, release or trunk sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
read -r dep prev <<<"$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'];print(s.get('deployed_commit','NONE'),s.get('previous_deployed_commit','NONE'))" | tr -d '\r')"
live=$dep; [ "$dep" = "$rel" ] && live=$prev
[ -n "$AP38_LIVE_OVERRIDE" ] && live=$AP38_LIVE_OVERRIDE
TAKE="$GW/app/typed_scope.py $GW/app/etfs_rivals_flow.py $GW/deploy/opal-gateway.service $GW/tests/test_og_en25.py $GW/tests/test_og_un1.py"
ALLOW="^($GW/(app/typed_scope\.py|app/etfs_rivals_flow\.py|deploy/opal-gateway\.service|tests/test_og_(en25|un1)\.py)|infra/logic/registry/[A-Za-z0-9_]+\.json)$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
missing=0; for p in $TAKE; do printf '%s\n' "$files" | grep -qx "$p" || missing=$((missing+1)); done
neq=0; for p in $files; do a=$(git rev-parse "$rel:$p" 2>/dev/null | tr -d '\r'); b=$(git rev-parse "$trunk:$p" 2>/dev/null | tr -d '\r'); [ -n "$a" ] && [ "$a" = "$b" ] || neq=$((neq+1)); done
barred=$(printf '%s\n' "$files" | grep -cE "$GW/app/(tools|destructive_ops|client_[a-z0-9_]+)\.py|$GW/deploy-to-ec2\.sh|infra/aws/ec2/EC2_MANIFEST\.json|\.tf$|$GW/app/refs/")
rec=$(python - "$(native "$PA")" "$rel" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
GUARDS = ("oom_score_adj_1000_rlimit_as_1400mb", "oom_score_adj_1000_cgroup_memmax_1400mb")
same = b.get("release_sha") == sys.argv[2]
pe = b.get("peers") or {}
peers_ok = (pe.get("candidate_outcome") in ("empty_section", "refusal") and isn(pe.get("candidate_peak_rss_mb")) and pe["candidate_peak_rss_mb"] <= 700
            and isn(pe.get("candidate_wall_s")) and pe["candidate_wall_s"] <= 30 and pe.get("live_outcome") in ("MemoryError", "killed_by_guard")
            and pe.get("guard") in GUARDS)
vp = b.get("valid_pair") or {}
valid_ok = vp.get("answered") is True and isn(vp.get("peak_rss_mb")) and vp["peak_rss_mb"] <= 700 and isn(vp.get("rows_matched"))
ch = b.get("chain") or {}
chain_ok = (isn(ch.get("pages")) and ch["pages"] >= 4 and isn(ch.get("median_growth_mb")) and ch["median_growth_mb"] <= 20
            and isn(ch.get("first_page_wall_s")) and ch["first_page_wall_s"] <= 45 and isn(ch.get("host_peak_pct")) and ch["host_peak_pct"] < 75
            and ch.get("pages_equal_live") is True)
un = b.get("unit") or {}
unit_ok = un.get("cgroup_v2") is True and un.get("memory_controller") is True and un.get("verify_rc") == 0 and un.get("scratch_removed") is True
runs = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40}"', '""', raw))
ok = same and peers_ok and valid_ok and chain_ok and unit_ok and not runs
print("host runs on release_sha %s, every one under a hard guard (oom_score_adj 1000, and an address-space or cgroup memory limit of 1400 MB)" % ("equal" if same else "NOT equal"))
print("the call that ran away: candidate %s, peak RSS %s MB (limit 700), %s s (limit 30); the live code under the same guard: %s: %s" % (
    pe.get("candidate_outcome"), pe.get("candidate_peak_rss_mb"), pe.get("candidate_wall_s"), pe.get("live_outcome"), "ok" if peers_ok else "NOT OK"))
print("a valid period and axis: answered %s, rows matched %s, peak RSS %s MB (limit 700): %s; 49F chain: %s pages, median growth %s MB (limit 20), first page %s s (limit 45), host peak %s, pages equal the live code's %s: %s; unit: cgroup v2 %s, memory controller %s, systemd-analyze verify rc %s: %s" % (
    vp.get("answered"), vp.get("rows_matched"), vp.get("peak_rss_mb"), "ok" if valid_ok else "NOT OK", ch.get("pages"), ch.get("median_growth_mb"), ch.get("first_page_wall_s"), ch.get("host_peak_pct"), ch.get("pages_equal_live"), "ok" if chain_ok else "NOT OK",
    un.get("cgroup_v2"), un.get("memory_controller"), un.get("verify_rc"), "ok" if unit_ok else "NOT OK"))
print("OK" if ok else "NO")
PYEOF
)
rec=$(printf '%s' "$rec" | tr -d '\r')
halves=$(python - "$(native "$ASK")" <<'PYEOF'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
print("yes" if all(re.search(r"(?mi)^#+ .*%s" % h, t) for h in ("CTO", "COO", "CVO")) else "no")
PYEOF
)
halves=$(printf '%s' "$halves" | tr -d '\r')
echo "base ${base:0:10} is the live ref before this release: $([ "$base" = "$live" ] && echo yes || echo no) (manifest ${dep:0:10}/${prev:0:10}); release ${rel:0:10}; trunk ${trunk:0:10}"
echo "files differing $n; outside the take list $outside (want 0); take-list files missing $missing (want 0); not byte-equal to trunk's $neq (want 0); tools, client, destructive_ops, deploy script, manifest, catalog or Terraform files in the diff $barred (want 0)"
printf '%s\n' "$rec" | sed '$d'
echo "ask has the three halves $halves"
[ "$base" = "$live" ] && [ "$n" -ge 5 ] && [ "$outside" = 0 ] && [ "$missing" = 0 ] && [ "$neq" = 0 ] && [ "$barred" = 0 ] && [ "$halves" = yes ] && [ "$(printf '%s\n' "$rec" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
