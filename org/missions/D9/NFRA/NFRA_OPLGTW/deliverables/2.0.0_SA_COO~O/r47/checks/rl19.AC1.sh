#!/usr/bin/env bash
# OPLGTW OG-rl-19 AC1 (round 47, the gateway release R3c: the Schwab 0840 DUAL READ; PHASE A). The release tree is exactly four files over the base, the hybrid integration.py is exactly base + the OG-sk-2 hunk, the plan is two in-place IAM policy changes, the ask is complete.
#  - W/rl19_release.json {base_sha, release_sha, trunk_sha, live_ref_host}; base_sha IS the live ref read on the host, OR (Phase A before batch16 is live) batch16's release 8e3eddf959 PREDICTED while the host still reads the pre-batch16 ref 13917ef993; either way Phase B re-reads the host and AC2 requires it to equal base_sha; dell1's harvest release 6575999df5 is an ancestor of base.
#  - base..release differs ONLY in these four files under infra/aws/ec2/opal-gateway/: app/integrations/schwab/catalog.py, deploy/NFRA_OPLGTW_CONTRACT.json, tests/test_og_sk2.py (each byte-equal to its blob at trunk_sha) and
#    app/integrations/schwab/integration.py = the BASE blob with the OG-sk-2 hunk applied (the diff of trunk between c0a0ee2e9c2 and the OG-sk-2 drain, applied onto the base blob): NOT trunk's blob, which carries OG-rt-1's hunks (batch17's).
#    No deploy script, no deploy/ file other than the contract, no EC2_MANIFEST.json, no .tf, no unit in the diff.
#  - W/PHASE_A_OG-rl-19.json {"body": {release_sha, tests {named_passed >= 1, named_failed 0, suite_difference_named true}, probes {sk2_ac1_ok 13}, old_form_unchanged true, terraform_plan {add 0, change 2, destroy 0, targets [the two policy addresses]}, process_wide_state "..."}}.
#  - W/NEVER_WIDEN_ASK_OG-rl-19.md has the CTO, COO and CVO headings, the line "process-wide state this change touches:", and states: the FIRST grant on opal-data-49financial, the dual read falls back on ABSENT only, and R3a (the bucket exemption) verified live before this release.
# Overrides (dry-run controls only): RL19_REC_OVERRIDE, RL19_PA_OVERRIDE, RL19_ASK_OVERRIDE, RL19_LIVE_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
GW=infra/aws/ec2/opal-gateway
W=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1
REC="${RL19_REC_OVERRIDE:-$W/rl19_release.json}"; PA="${RL19_PA_OVERRIDE:-$W/PHASE_A_OG-rl-19.json}"; ASK="${RL19_ASK_OVERRIDE:-$W/NEVER_WIDEN_ASK_OG-rl-19.md}"
[ -f "$REC" ] && [ -f "$PA" ] && [ -f "$ASK" ] || { echo "rl19_release.json, PHASE_A_OG-rl-19.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel trunk hostlive <<<"$(python3 -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''),d.get('trunk_sha',''),d.get('live_ref_host',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" && git cat-file -e "${base}^{commit}" && git cat-file -e "${trunk}^{commit}" || { echo "base, release or trunk sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
live=${RL19_LIVE_OVERRIDE:-$hostlive}
B16=8e3eddf95916e430e4e9bbf615ca4fd91f9e852f; P0=13917ef993207bee6b8df0124eec5444da4d62cd
if [ -n "$live" ] && [ "$base" = "$live" ]; then base_ok=yes; elif [ "$base" = "$B16" ] && [ "$live" = "$P0" ]; then base_ok=predicted; else base_ok=no; fi
DELL=6575999df5d22c0123abfc0c88cd1c6f1efe8c96
git merge-base --is-ancestor "$DELL" "$base" && dellanc=yes || dellanc=no
TRUNK_WHOLE="app/integrations/schwab/catalog.py deploy/NFRA_OPLGTW_CONTRACT.json tests/test_og_sk2.py"
HYB=app/integrations/schwab/integration.py
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
allow_re="^($(for p in $TRUNK_WHOLE $HYB; do printf '%s|' "$GW/$p" | sed 's/\./\\./g'; done | sed 's/|$//'))$"
outside=$(printf '%s\n' "$files" | grep -vE "$allow_re" | grep -c .)
missing=0; for p in $TRUNK_WHOLE $HYB; do printf '%s\n' "$files" | grep -qx "$GW/$p" || missing=$((missing+1)); done
neq=0; for p in $TRUNK_WHOLE; do a=$(git rev-parse "$rel:$GW/$p" 2>/dev/null | tr -d '\r'); b=$(git rev-parse "$trunk:$GW/$p" 2>/dev/null | tr -d '\r'); [ -n "$a" ] && [ "$a" = "$b" ] || neq=$((neq+1)); done
barred=$(printf '%s\n' "$files" | grep -cE "$GW/deploy-to-ec2\.sh|$GW/deploy/(deploy|unit|[a-z_-]+\.(sh|service|env))|infra/aws/ec2/EC2_MANIFEST\.json|\.tf$")
# the hybrid: the base blob + the OG-sk-2 hunk, compared with the release's integration.py by blob hash
TMP=$(mktemp -d 2>/dev/null) || TMP="${TMPDIR:-/tmp}/rl19_$$"; mkdir -p "$TMP/app/integrations/schwab"
git show "$base:$GW/$HYB" > "$TMP/$HYB"
git diff c0a0ee2e9c2 "$trunk" -- "$GW/$HYB" | sed "s#a/$GW/#a/#; s#b/$GW/#b/#" > "$TMP/sk2.patch"
hyb_ok=no
if [ -s "$TMP/sk2.patch" ] && (cd "$TMP" && git apply sk2.patch 2>/dev/null); then
  want=$(git hash-object "$TMP/$HYB" | tr -d '\r'); got=$(git rev-parse "$rel:$GW/$HYB" 2>/dev/null | tr -d '\r')
  [ -n "$want" ] && [ "$want" = "$got" ] && hyb_ok=yes
fi
rm -rf "$TMP"
rec=$(python3 -I - "$(native "$PA")" "$rel" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
def isn(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)
same = b.get("release_sha") == sys.argv[2]
t = b.get("tests") or {}
tests_ok = isn(t.get("named_passed")) and t["named_passed"] >= 1 and t.get("named_failed") == 0 and t.get("suite_difference_named") is True
p = b.get("probes") or {}
p_ok = p.get("sk2_ac1_ok") == 13
tp = b.get("terraform_plan") or {}
plan_ok = tp.get("add") == 0 and tp.get("change") == 2 and tp.get("destroy") == 0 and sorted(tp.get("targets") or []) == ["aws_iam_role_policy.schwab_catalog_read_policy", "aws_iam_role_policy.schwab_data_read_policy"]
old_ok = b.get("old_form_unchanged") is True
pw = b.get("process_wide_state")
pw_ok = isinstance(pw, str) and len(pw.strip()) >= 20
big = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40,64}"', '""', raw))
ok = same and tests_ok and p_ok and plan_ok and old_ok and pw_ok and not big
print("record release_sha %s the release; tests: named passed %s failed %s, suite difference named %s: %s" % ("equals" if same else "DIFFERS FROM", t.get("named_passed"), t.get("named_failed"), t.get("suite_difference_named"), "ok" if tests_ok else "NOT OK"))
print("probes on the candidate tree: sk2.AC1 lines ok %s of 13: %s; old-form reads unchanged %s; terraform plan add %s change %s destroy %s on the two role policies: %s; process-wide state named %s; digit runs of 9 or more %d (want 0)" % (
      p.get("sk2_ac1_ok"), "ok" if p_ok else "NOT OK", b.get("old_form_unchanged"), tp.get("add"), tp.get("change"), tp.get("destroy"), "ok" if plan_ok else "NOT OK", "yes" if pw_ok else "NO", len(big)))
print("OK" if ok else "NO")
PYEOF
)
rec=$(printf '%s' "$rec" | tr -d '\r')
halves=$(python3 -I - "$(native "$ASK")" <<'PYEOF'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
need = (all(re.search(r"(?mi)^#+ .*%s" % h, t) for h in ("CTO", "COO", "CVO")) and re.search(r"(?i)process-wide state this change touches\s*:\s*\S", t)
        and re.search(r"(?i)first grant on opal-data-49financial", t) and re.search(r"(?i)falls back on ABSENT only", t) and re.search(r"(?i)R3a", t))
print("yes" if need else "no")
PYEOF
)
halves=$(printf '%s' "$halves" | tr -d '\r')
echo "base ${base:0:10} is the live ref read on the host, or batch16's release predicted while the host still reads the pre-batch16 ref: $base_ok; dell1 harvest release ${DELL:0:10} is an ancestor of base: $dellanc; release ${rel:0:10}; trunk ${trunk:0:10}"
echo "files differing $n (want 4); outside the four 0 expected: $outside; the four missing $missing (want 0); the three trunk-whole files not byte-equal to trunk's $neq (want 0); barred files (deploy script, unit, manifest, .tf) $barred (want 0)"
echo "integration.py is the BASE blob plus the OG-sk-2 hunk only (not trunk's blob): $hyb_ok"
printf '%s\n' "$rec" | sed '$d'
echo "ask has the three halves, the process-wide state line, the first grant on opal-data-49financial, the ABSENT-only fallback and R3a $halves"
[ "$dellanc" = yes ] && [ "$base_ok" != no ] && [ "$n" = 4 ] && [ "$outside" = 0 ] && [ "$missing" = 0 ] && [ "$neq" = 0 ] && [ "$barred" = 0 ] && [ "$hyb_ok" = yes ] && [ "$halves" = yes ] && [ "$(printf '%s\n' "$rec" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
