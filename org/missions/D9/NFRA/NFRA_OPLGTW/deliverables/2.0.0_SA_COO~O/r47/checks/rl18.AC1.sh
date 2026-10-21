#!/usr/bin/env bash
# OPLGTW OG-rl-18 AC1 (round 47, the gateway release `batch17`; PHASE A): the take list of OG-rt-1 (the master-wide Schwab scope), whole from trunk, on the live ref read on the host.
#  - W/rl18_release.json {base_sha, release_sha, trunk_sha, live_ref_host}; base_sha IS the live ref read on the host; dell1's harvest release 6575999df5 is an ancestor of base;
#    base..release differs ONLY in the twelve files below (the four of OG-rt-1, the five of OG-ed-1, the two of OG-mp-1 and the served catalog app/refs/DATA_CATALOG.yaml, MCPINDEX candidate e, md5 03d2dbbae1f0) (each byte-equal to its blob at trunk_sha) and in ONE KEY of EC2_MANIFEST.json (the opal-gateway mcportal_commit pin, 21ad40432cae to a577f99afc81df4a42c1740c78cf58270c8991e5); every other file (the batch16 files included, whether or not batch16 is live), the unit file, deploy-to-ec2.sh and every .tf is byte-equal between base and release;
#    dell1's four harvest files are byte-equal between base and release.
#  - W/PHASE_A_OG-rl-18.json (every host run under a HARD GUARD): tests {named_passed, named_failed 0, window_set_passed, window_set_failed 0, suite_difference_named true}, probes {rt1_ac1_ok 11, rt1_ac2_ok 11, ed1_ac1_ok 7, mp1_ac1_ok 4} (the 11, 11, 7 and 4 labelled lines of rt1.AC1, rt1.AC2, ed1.AC1 and mp1.AC1 run
#    against the candidate tree), explicit_unchanged true (a scope with explicit account lists parses, filters and resolves as the live ref does), sentinel_grants_in_store 0 (a read-only scan of the policy records: no stored grant names ["*"] before the code is live),
#    process_wide_state (a sentence naming what the change touches).
#  - W/NEVER_WIDEN_ASK_OG-rl-18.md has the three halves AND a line "process-wide state this change touches:" naming the list, AND states the release-order condition (this code live before any grant names the sentinel).
# Overrides (dry-run controls only): RL18_REC_OVERRIDE, RL18_PA_OVERRIDE, RL18_ASK_OVERRIDE, RL18_LIVE_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
GW=infra/aws/ec2/opal-gateway
W=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1
REC="${RL18_REC_OVERRIDE:-$W/rl18_release.json}"; PA="${RL18_PA_OVERRIDE:-$W/PHASE_A_OG-rl-18.json}"; ASK="${RL18_ASK_OVERRIDE:-$W/NEVER_WIDEN_ASK_OG-rl-18.md}"
[ -f "$REC" ] && [ -f "$PA" ] && [ -f "$ASK" ] || { echo "rl18_release.json, PHASE_A_OG-rl-18.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel trunk hostlive <<<"$(python3 -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''),d.get('trunk_sha',''),d.get('live_ref_host',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" && git cat-file -e "${base}^{commit}" && git cat-file -e "${trunk}^{commit}" || { echo "base, release or trunk sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
live=${RL18_LIVE_OVERRIDE:-$hostlive}
DELL=6575999df5d22c0123abfc0c88cd1c6f1efe8c96
git merge-base --is-ancestor "$DELL" "$base" && dellanc=yes || dellanc=no
TAKE="app/data_entitlement.py app/account_ref.py app/integrations/schwab/integration.py tests/test_og_rt1.py app/server.py app/token_broker.py tests/test_og_ed1.py tests/test_scoped_consent_r253.py tests/test_login_admit_r24.py app/admin_api.py tests/test_og_mp1.py app/refs/DATA_CATALOG.yaml"
MANI=infra/aws/ec2/EC2_MANIFEST.json
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
allow_re="^($(for p in $TAKE; do printf '%s|' "$GW/$p" | sed 's/\./\\./g'; done)$MANI)$"
outside=$(printf '%s\n' "$files" | grep -vE "$allow_re" | grep -c .)
missing=0; for p in $TAKE; do printf '%s\n' "$files" | grep -qx "$GW/$p" || missing=$((missing+1)); done
neq=0; for p in $files; do [ "$p" = "$MANI" ] && continue; a=$(git rev-parse "$rel:$p" 2>/dev/null | tr -d '\r'); b=$(git rev-parse "$trunk:$p" 2>/dev/null | tr -d '\r'); [ -n "$a" ] && [ "$a" = "$b" ] || neq=$((neq+1)); done
barred=$(printf '%s\n' "$files" | grep -cE "$GW/deploy-to-ec2\.sh|$GW/deploy/|\.tf$")
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
want = sorted(k for k in changed if k.endswith("/opal-gateway/mcportal_commit"))
ok = changed == want and len(want) == 1
before = fa.get(want[0]) if want else None
after = fb.get(want[0]) if want else None
print("manifest keys changed %s; only the opal-gateway mcportal_commit pin: %s; pin %s -> %s" % (len(changed), "yes" if ok else "NO", (before or "")[:12], (after or "")[:12]))
print("OK" if ok and before == "21ad40432cae0d09c5ab9d806307944baaf45cb9" and after == "a577f99afc81df4a42c1740c78cf58270c8991e5" else "NO")
PYEOF
)
mani=$(printf '%s' "$mani" | tr -d '\r')
cat_md5=$(git show "$rel:$GW/app/refs/DATA_CATALOG.yaml" 2>/dev/null | md5sum | cut -d' ' -f1 | tr -d '\r')
cat_ok=no; [ "$cat_md5" = 03d2dbbae1f07b8d4fa5f0eaa73355d6 ] && cat_ok=yes
rec=$(python3 -I - "$(native "$PA")" "$rel" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
same = b.get("release_sha") == sys.argv[2]
t = b.get("tests") or {}
tests_ok = (isn(t.get("named_passed")) and t["named_passed"] >= 1 and t.get("named_failed") == 0 and isn(t.get("window_set_passed")) and t["window_set_passed"] >= 1
            and t.get("window_set_failed") == 0 and t.get("suite_difference_named") is True)
p = b.get("probes") or {}
p_ok = p.get("rt1_ac1_ok") == 11 and p.get("rt1_ac2_ok") == 11 and p.get("ed1_ac1_ok") == 7 and p.get("mp1_ac1_ok") == 4
ex_ok = b.get("explicit_unchanged") is True
sg_ok = b.get("sentinel_grants_in_store") == 0
pw = b.get("process_wide_state")
pw_ok = isinstance(pw, str) and len(pw.strip()) >= 20
bignums = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40,64}"', '""', raw))
ok = same and tests_ok and p_ok and ex_ok and sg_ok and pw_ok and not bignums
print("host runs on release_sha %s; tests: named passed %s failed %s, window set passed %s failed %s, suite difference named %s: %s" % (
      "equal" if same else "NOT equal", t.get("named_passed"), t.get("named_failed"), t.get("window_set_passed"), t.get("window_set_failed"), t.get("suite_difference_named"), "ok" if tests_ok else "NOT OK"))
print("probes on the candidate tree: rt1.AC1 lines ok %s of 11, rt1.AC2 lines ok %s of 11, ed1.AC1 lines ok %s of 7, mp1.AC1 lines ok %s of 4: %s; explicit-list scope unchanged %s; stored grants naming the sentinel %s (want 0): %s" % (
      p.get("rt1_ac1_ok"), p.get("rt1_ac2_ok"), p.get("ed1_ac1_ok"), p.get("mp1_ac1_ok"), "ok" if p_ok else "NOT OK", b.get("explicit_unchanged"), b.get("sentinel_grants_in_store"), "ok" if (ex_ok and sg_ok) else "NOT OK"))
print("process-wide state this change touches, as recorded in Phase A (CVO verdict 35844): %s; digit runs of 9 or more %d (want 0)" % ("named" if pw_ok else "ABSENT or too short", len(bignums)))
print("OK" if ok else "NO")
PYEOF
)
rec=$(printf '%s' "$rec" | tr -d '\r')
halves=$(python3 -I - "$(native "$ASK")" <<'PYEOF'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
print("yes" if all(re.search(r"(?mi)^#+ .*%s" % h, t) for h in ("CTO", "COO", "CVO")) and re.search(r"(?i)process-wide state this change touches\s*:\s*\S", t) and re.search(r"(?i)before any grant names", t) and re.search(r"(?i)non-admin with a deny record still gets 403", t) and re.search(r"(?i)live at once", t) and re.search(r"(?i)routes are owner-gated", t) and re.search(r"(?i)gateway writes nothing itself", t) and re.search(r"owner_gate\.owner_only", t) and re.search(r"(?i)over R3c.s hybrid", t) and re.search(r"(?i)R3c hunk survives", t) and re.search(r"a577f99afc81df4a42c1740c78cf58270c8991e5", t) and re.search(r"03d2dbbae1f0", t) and re.search(r"(?i)catalog", t) and re.search(r"(?i)GET", t) and re.search(r"(?i)POST", t) else "no")
PYEOF
)
halves=$(printf '%s' "$halves" | tr -d '\r')
echo "base ${base:0:10} is the live ref read on the host: $([ "$base" = "$live" ] && [ -n "$live" ] && echo yes || echo no); dell1 harvest release ${DELL:0:10} is an ancestor of base: $dellanc; release ${rel:0:10}; trunk ${trunk:0:10}"
hcar=0; hn=0; for h in harvest_research harvest_figures harvest_identity harvest_keys; do hn=$((hn+1)); a=$(git rev-parse "$base:$GW/app/$h.py" 2>/dev/null | tr -d '\r'); b2=$(git rev-parse "$rel:$GW/app/$h.py" 2>/dev/null | tr -d '\r'); [ -n "$a" ] && [ "$a" = "$b2" ] && hcar=$((hcar+1)); done
echo "dell1's four harvest files byte-equal between the live base and the release: $hcar of $hn (want 4 of 4)"
echo "files differing $n (want 13: the twelve and the manifest); outside the take list and the manifest $outside (want 0); take-list files missing $missing (want 0); not byte-equal to trunk's $neq (want 0); deploy script, deploy folder or Terraform files in the diff $barred (want 0)"
printf '%s\n' "$mani" | sed '$d'
echo "served catalog in the release is MCPINDEX candidate e (md5 03d2dbbae1f0): $cat_ok"
printf '%s\n' "$rec" | sed '$d'
echo "ask has the three halves, the process-wide state line, the release-order condition and the exemption widening $halves"
[ "$hcar" = 4 ] && [ "$dellanc" = yes ] && [ -n "$live" ] && [ "$base" = "$live" ] && [ "$n" = 13 ] && [ "$cat_ok" = yes ] && [ "$(printf '%s\n' "$mani" | tail -1)" = OK ] && [ "$outside" = 0 ] && [ "$missing" = 0 ] && [ "$neq" = 0 ] && [ "$barred" = 0 ] && [ "$halves" = yes ] && [ "$(printf '%s\n' "$rec" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
