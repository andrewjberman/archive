#!/usr/bin/env bash
# OPLGTW OG-rl-17 AC1 (round 47, the batched gateway release `batch16`; PHASE A): the take list of round 47's seven build cells, whole from trunk, on the live ref read on the host.
#  - W/rl17_release.json {base_sha, release_sha, trunk_sha, live_ref_host}; base_sha IS the live ref read on the host (live_ref_host); dell1's harvest release 6575999df5 is an ancestor of base;
#    base..release differs ONLY in the take list below (each file byte-equal to its blob at trunk_sha, except EC2_MANIFEST.json whose diff is EXACTLY the two keys named); every other file, the OG-rt-1 files
#    (data_entitlement.py, account_ref.py, integrations/schwab/integration.py), destructive_ops.py, refs/, the unit file, deploy-to-ec2.sh and every .tf, is byte-equal between base and release;
#    dell1's four harvest files are byte-equal between base and release.
#  - W/PHASE_A_OG-rl-17.json (every host run under a HARD GUARD): tests {named_passed, named_failed 0, window_set_passed, window_set_failed 0, suite_difference_named true}, guard_burst {limit 2, ran 2, refused >= 1, code "gateway_busy"},
#    fences {orion, eclipse, commonwealth: each segment count >= 1 on the deployed catalog}, contract {copies_equal true, target_memory_mib 8192}, process_wide_state (a sentence naming what the change touches).
#  - W/NEVER_WIDEN_ASK_OG-rl-17.md has the three halves AND a line "process-wide state this change touches:" naming the list.
# Overrides (dry-run controls only): RL17_REC_OVERRIDE, RL17_PA_OVERRIDE, RL17_ASK_OVERRIDE, RL17_LIVE_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
GW=infra/aws/ec2/opal-gateway
W=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1
REC="${RL17_REC_OVERRIDE:-$W/rl17_release.json}"; PA="${RL17_PA_OVERRIDE:-$W/PHASE_A_OG-rl-17.json}"; ASK="${RL17_ASK_OVERRIDE:-$W/NEVER_WIDEN_ASK_OG-rl-17.md}"
[ -f "$REC" ] && [ -f "$PA" ] && [ -f "$ASK" ] || { echo "rl17_release.json, PHASE_A_OG-rl-17.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel trunk hostlive <<<"$(python3 -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''),d.get('trunk_sha',''),d.get('live_ref_host',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" && git cat-file -e "${base}^{commit}" && git cat-file -e "${trunk}^{commit}" || { echo "base, release or trunk sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
live=${RL17_LIVE_OVERRIDE:-$hostlive}
DELL=6575999df5d22c0123abfc0c88cd1c6f1efe8c96
git merge-base --is-ancestor "$DELL" "$base" && dellanc=yes || dellanc=no
TAKE="app/client_core.py app/client_adapter_bdcottonwood.py app/family_depth.py app/integrations/ycharts/integration.py app/integrations/opal_portal/integration.py app/harvest_typed.py app/integrations/portal_index/integration.py app/integrations/opal_discover/integration.py app/inflight_guard.py app/tools.py app/admin_gateway_breakdown.py app/news_typed.py app/admin_people_access.py deploy/NFRA_OPLGTW_CONTRACT.json tests/test_og_fc1.py tests/test_og_sx1.py tests/test_og_sz1.py tests/test_og_mg3.py tests/test_og_tp1.py tests/test_og_ix1.py tests/test_og_nf1.py tests/test_og_gt0.py tests/test_og_gt5.py tests/test_og_rv2.py tests/test_admin_people_access.py"
MANI=infra/aws/ec2/EC2_MANIFEST.json
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
allow_re="^($(for p in $TAKE; do printf '%s|' "$GW/$p" | sed 's/\./\\./g'; done)$MANI)$"
outside=$(printf '%s\n' "$files" | grep -vE "$allow_re" | grep -c .)
missing=0; for p in $TAKE; do printf '%s\n' "$files" | grep -qx "$GW/$p" || missing=$((missing+1)); done
neq=0; for p in $files; do [ "$p" = "$MANI" ] && continue; a=$(git rev-parse "$rel:$p" 2>/dev/null | tr -d '\r'); b=$(git rev-parse "$trunk:$p" 2>/dev/null | tr -d '\r'); [ -n "$a" ] && [ "$a" = "$b" ] || neq=$((neq+1)); done
barred=$(printf '%s\n' "$files" | grep -cE "$GW/app/(data_entitlement|account_ref|destructive_ops|server|graph|probe_listener|audit|owner_gate|typed_scope|client_adapter_(bd49f|eclipse|orion|commonwealth|smartx|schwab)|integrations/schwab/integration)\.py|$GW/app/refs/|$GW/deploy-to-ec2\.sh|$GW/deploy/opal-gateway\.service|\.tf$")
mani=$(python3 -I - "$base" "$rel" <<'PYEOF'
import json, subprocess, sys
def load(ref):
    out = subprocess.run(["git", "show", "%s:infra/aws/ec2/EC2_MANIFEST.json" % ref], capture_output=True)
    return json.loads(out.stdout.decode("utf-8"))
a, b = load(sys.argv[1]), load(sys.argv[2])
def flat(o, p=""):
    if isinstance(o, dict):
        r = {}
        for k, v in o.items():
            r.update(flat(v, p + "/" + k))
        return r
    return {p: o}
fa, fb = flat(a), flat(b)
changed = sorted(k for k in set(fa) | set(fb) if fa.get(k) != fb.get(k))
want = sorted(k for k in changed if k.endswith("/opal-gateway/mcportal_commit") or (k.endswith("/machine_type") and "opal-gateway" in k))
ok = changed == want and any(k.endswith("/mcportal_commit") for k in want)
pin = [fb[k] for k in want if k.endswith("/mcportal_commit")]
print("manifest keys changed %s; only the mcportal_commit pin and the gateway machine_type: %s; pin %s" % (len(changed), "yes" if ok else "NO", (pin[0][:12] if pin else None)))
print("OK" if ok and pin and pin[0] == "21ad40432cae0d09c5ab9d806307944baaf45cb9" else "NO")
PYEOF
)
mani=$(printf '%s' "$mani" | tr -d '\r')
rec=$(python3 -I - "$(native "$PA")" "$rel" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
same = b.get("release_sha") == sys.argv[2]
t = b.get("tests") or {}
tests_ok = (isn(t.get("named_passed")) and t["named_passed"] >= 1 and t.get("named_failed") == 0 and isn(t.get("window_set_passed")) and t["window_set_passed"] >= 1
            and t.get("window_set_failed") == 0 and t.get("suite_difference_named") is True)
g = b.get("guard_burst") or {}
g_ok = g.get("limit") == 2 and g.get("ran") == 2 and isn(g.get("refused")) and g["refused"] >= 1 and g.get("code") == "gateway_busy"
f = b.get("fences") or {}
f_ok = all(isn(f.get(k)) and f[k] >= 1 for k in ("orion", "eclipse", "commonwealth"))
c = b.get("contract") or {}
c_ok = c.get("copies_equal") is True and c.get("target_memory_mib") == 8192
pw = b.get("process_wide_state")
pw_ok = isinstance(pw, str) and len(pw.strip()) >= 20
bignums = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40,64}"', '""', raw))
ok = same and tests_ok and g_ok and f_ok and c_ok and pw_ok and not bignums
print("host runs on release_sha %s; tests: named passed %s failed %s, window set passed %s failed %s, suite difference named %s: %s" % (
      "equal" if same else "NOT equal", t.get("named_passed"), t.get("named_failed"), t.get("window_set_passed"), t.get("window_set_failed"), t.get("suite_difference_named"), "ok" if tests_ok else "NOT OK"))
print("guard burst (scratch limit 2): ran %s, refused %s, code %s: %s; fences on the deployed catalog: orion %s, eclipse %s, commonwealth %s segment(s): %s; contract copies equal %s, target_memory_mib %s: %s" % (
      g.get("ran"), g.get("refused"), g.get("code"), "ok" if g_ok else "NOT OK", f.get("orion"), f.get("eclipse"), f.get("commonwealth"), "ok" if f_ok else "NOT OK", c.get("copies_equal"), c.get("target_memory_mib"), "ok" if c_ok else "NOT OK"))
print("process-wide state this change touches, as recorded in Phase A (CVO verdict 35844): %s; digit runs of 9 or more %d (want 0)" % ("named" if pw_ok else "ABSENT or too short", len(bignums)))
print("OK" if ok else "NO")
PYEOF
)
rec=$(printf '%s' "$rec" | tr -d '\r')
halves=$(python3 -I - "$(native "$ASK")" <<'PYEOF'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
print("yes" if all(re.search(r"(?mi)^#+ .*%s" % h, t) for h in ("CTO", "COO", "CVO")) and re.search(r"(?i)process-wide state this change touches\s*:\s*\S", t) else "no")
PYEOF
)
halves=$(printf '%s' "$halves" | tr -d '\r')
echo "base ${base:0:10} is the live ref read on the host: $([ "$base" = "$live" ] && [ -n "$live" ] && echo yes || echo no); dell1 harvest release ${DELL:0:10} is an ancestor of base: $dellanc; release ${rel:0:10}; trunk ${trunk:0:10}"
hcar=0; hn=0; for h in harvest_research harvest_figures harvest_identity harvest_keys; do hn=$((hn+1)); a=$(git rev-parse "$base:$GW/app/$h.py" 2>/dev/null | tr -d '\r'); b2=$(git rev-parse "$rel:$GW/app/$h.py" 2>/dev/null | tr -d '\r'); [ -n "$a" ] && [ "$a" = "$b2" ] && hcar=$((hcar+1)); done
echo "dell1's four harvest files byte-equal between the live base and the release: $hcar of $hn (want 4 of 4)"
echo "files differing $n; outside the take list $outside (want 0); take-list files missing $missing (want 0); not byte-equal to trunk's $neq (want 0); OG-rt-1 files, destructive_ops, refs, unit, deploy script or Terraform files in the diff $barred (want 0)"
printf '%s\n' "$mani" | sed '$d'
printf '%s\n' "$rec" | sed '$d'
echo "ask has the three halves and the process-wide state line $halves"
[ "$hcar" = 4 ] && [ "$dellanc" = yes ] && [ -n "$live" ] && [ "$base" = "$live" ] && [ "$outside" = 0 ] && [ "$missing" = 0 ] && [ "$neq" = 0 ] && [ "$barred" = 0 ] && [ "$halves" = yes ] && [ "$(printf '%s\n' "$mani" | tail -1)" = OK ] && [ "$(printf '%s\n' "$rec" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
