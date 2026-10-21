#!/usr/bin/env bash
# OPLGTW OG-cs-9 AC1 (cli-shim workstream, wave 5, the gateway release `batch18`; PHASE A): the take list of the cli-shim cells, whole from trunk, on the live ref read on the host, and the folder reader's IAM plan.
#  - W/cs9_release.json {base_sha, release_sha, trunk_sha, live_ref_host}; base_sha IS the live ref read on the host; dell1's harvest release 6575999df5 is an ancestor of base;
#    base..release differs ONLY in the 18 required take-list files below (and may add the two optional pin tests), each byte-equal to its blob at trunk_sha EXCEPT deploy-to-ec2.sh, whose whole diff is ONE line: ENABLED_INTEGRATIONS gains the token `folders` (and nothing else changes in it);
#    EC2_MANIFEST.json, the served catalog, the unit file and every .tf are byte-equal between base and release; dell1's four harvest files are byte-equal between base and release.
#  - W/PHASE_A_OG-cs-9.json (every host run under a HARD GUARD): tests {named_passed, named_failed 0, window_set_passed, window_set_failed 0, suite_difference_named true}, probes (each issuer probe run from a worktree at release_sha, the probe files taken from trunk) {cs1_ac1, cs1_ac2, cs2_ac1, cs2_ac2, cs2_ac3, cs3_ac1, cs3_ac2, cs5_ac1, cs5_ac2, cs7_ac1, cs10_ac1, cs10_ac2} each "PASS",
#    iam_plan {to_add 6, to_change 0, to_destroy 0} (the plan of infra/aws/terraform/opal-gateway/folder_reader_iam.tf printed by the safe-apply tool, NOT applied), process_wide_state (a sentence).
#  - W/NEVER_WIDEN_ASK_OG-cs-9.md has the three halves AND a line "process-wide state this change touches:", and states: the three tools go live (tools/list 103 to 106), the new reader role over the three served buckets with the bronze and raw denies, ENABLED_INTEGRATIONS gains folders, "a person with no folder string reads nothing", and names gateway-folder-read-role.
# Overrides (dry-run controls only): CS9_REC_OVERRIDE, CS9_PA_OVERRIDE, CS9_ASK_OVERRIDE, CS9_LIVE_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
GW=infra/aws/ec2/opal-gateway
W=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1
REC="${CS9_REC_OVERRIDE:-$W/cs9_release.json}"; PA="${CS9_PA_OVERRIDE:-$W/PHASE_A_OG-cs-9.json}"; ASK="${CS9_ASK_OVERRIDE:-$W/NEVER_WIDEN_ASK_OG-cs-9.md}"
[ -f "$REC" ] && [ -f "$PA" ] && [ -f "$ASK" ] || { echo "cs9_release.json, PHASE_A_OG-cs-9.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel trunk hostlive <<<"$(python3 -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''),d.get('trunk_sha',''),d.get('live_ref_host',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" && git cat-file -e "${base}^{commit}" && git cat-file -e "${trunk}^{commit}" || { echo "base, release or trunk sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
live=${CS9_LIVE_OVERRIDE:-$hostlive}
DELL=6575999df5d22c0123abfc0c88cd1c6f1efe8c96
git merge-base --is-ancestor "$DELL" "$base" && dellanc=yes || dellanc=no
TAKE="app/folder_grant.py app/folder_engine.py app/folder_tools.py app/client_grant.py app/integrations/folders/__init__.py app/integrations/folders/integration.py app/integrations/registry.py app/data_entitlement.py app/admin_people_access.py deploy/NFRA_OPLGTW_CONTRACT.json tests/test_cs1_folder_grant.py tests/test_cs2_folder_tools.py tests/test_cs3_folder_engine.py tests/test_cs5_widening_confirm.py tests/test_cs7_client_grant.py tests/test_cs8_contract_supersession.py tests/test_cs10_folders_mount.py"
OPT="tests/test_entitlement_admin.py tests/test_tool_classification_composition.py"
DEPLOY=deploy-to-ec2.sh
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
allow_re="^($(for p in $TAKE $OPT $DEPLOY; do printf '%s|' "$GW/$p" | sed 's/\./\\./g'; done | sed 's/|$//'))$"
outside=$(printf '%s\n' "$files" | grep -vE "$allow_re" | grep -c .)
missing=0; for p in $TAKE $DEPLOY; do printf '%s\n' "$files" | grep -qx "$GW/$p" || missing=$((missing+1)); done
neq=0; for p in $files; do [ "$p" = "$GW/$DEPLOY" ] && continue; a=$(git rev-parse "$rel:$p" 2>/dev/null | tr -d '\r'); b=$(git rev-parse "$trunk:$p" 2>/dev/null | tr -d '\r'); [ -n "$a" ] && [ "$a" = "$b" ] || neq=$((neq+1)); done
barred=$(printf '%s\n' "$files" | grep -cE "\.tf$|EC2_MANIFEST\.json|DATA_CATALOG\.yaml|\.service$")
dep=$(python3 -I - "$base" "$rel" "$GW/$DEPLOY" <<'PYEOF'
import re, subprocess, sys
base, rel, path = sys.argv[1:4]
def show(ref):
    return subprocess.run(["git", "show", "%s:%s" % (ref, path)], capture_output=True).stdout.decode("utf-8").replace("\r", "").split("\n")
a, b = show(base), show(rel)
diffs = [(x, y) for x, y in zip(a, b) if x != y]
same_len = len(a) == len(b)
ok = same_len and len(diffs) == 1
detail = "differing lines %d, same length %s" % (len(diffs), same_len)
if ok:
    x, y = diffs[0]
    mx, my = re.search(r'ENABLED_INTEGRATIONS="([^"]*)"', x), re.search(r'ENABLED_INTEGRATIONS="([^"]*)"', y)
    ok = bool(mx and my) and (mx.group(1).split() + ["folders"]) == my.group(1).split() and x.replace(mx.group(0), "") == y.replace(my.group(0), "")
    detail += "; ENABLED_INTEGRATIONS %s -> %s" % (mx.group(1) if mx else None, my.group(1) if my else None)
print("deploy-to-ec2.sh: %s: %s" % (detail, "only the folders token added" if ok else "NOT only the folders token"))
print("OK" if ok else "NO")
PYEOF
)
dep=$(printf '%s' "$dep" | tr -d '\r')
rec=$(python3 -I - "$(native "$PA")" "$rel" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
same = b.get("release_sha") == sys.argv[2]
t = b.get("tests") or {}
tests_ok = (isn(t.get("named_passed")) and t["named_passed"] >= 1 and t.get("named_failed") == 0 and isn(t.get("window_set_passed")) and t["window_set_passed"] >= 1
            and t.get("window_set_failed") == 0 and t.get("suite_difference_named") is True)
want = ("cs1_ac1", "cs1_ac2", "cs2_ac1", "cs2_ac2", "cs2_ac3", "cs3_ac1", "cs3_ac2", "cs5_ac1", "cs5_ac2", "cs7_ac1", "cs10_ac1", "cs10_ac2")
p = b.get("probes") or {}
p_ok = all(p.get(k) == "PASS" for k in want)
ip = b.get("iam_plan") or {}
ip_ok = ip.get("to_add") == 6 and ip.get("to_change") == 0 and ip.get("to_destroy") == 0
pw = b.get("process_wide_state")
pw_ok = isinstance(pw, str) and len(pw.strip()) >= 20
bignums = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40,64}"', '""', raw))
ok = same and tests_ok and p_ok and ip_ok and pw_ok and not bignums
print("host runs on release_sha %s; tests: named passed %s failed %s, window set passed %s failed %s, suite difference named %s: %s" % (
      "equal" if same else "NOT equal", t.get("named_passed"), t.get("named_failed"), t.get("window_set_passed"), t.get("window_set_failed"), t.get("suite_difference_named"), "ok" if tests_ok else "NOT OK"))
print("probes on the candidate tree: %d of %d read PASS: %s; reader IAM plan to add %s, change %s, destroy %s (want 6, 0, 0): %s" % (
      sum(1 for k in want if p.get(k) == "PASS"), len(want), "ok" if p_ok else "NOT OK", ip.get("to_add"), ip.get("to_change"), ip.get("to_destroy"), "ok" if ip_ok else "NOT OK"))
print("process-wide state this change touches, as recorded in Phase A: %s; digit runs of 9 or more %d (want 0)" % ("named" if pw_ok else "ABSENT or too short", len(bignums)))
print("OK" if ok else "NO")
PYEOF
)
rec=$(printf '%s' "$rec" | tr -d '\r')
halves=$(python3 -I - "$(native "$ASK")" <<'PYEOF'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
need = [r"(?i)process-wide state this change touches\s*:\s*\S", r"(?i)a person with no folder string reads nothing", r"gateway-folder-read-role", r"ENABLED_INTEGRATIONS", r"\b106\b", r"folder_list", r"folder_describe", r"folder_query", r"(?i)bronze", r"(?i)\braw\b", r"(?i)before the host is touched|apply.{0,40}before the deploy"]
print("yes" if all(re.search(r"(?mi)^#+ .*%s" % h, t) for h in ("CTO", "COO", "CVO")) and all(re.search(x, t) for x in need) else "no")
PYEOF
)
halves=$(printf '%s' "$halves" | tr -d '\r')
mani_same=no; git diff --quiet "$base" "$rel" -- infra/aws/ec2/EC2_MANIFEST.json && mani_same=yes
echo "base ${base:0:10} is the live ref read on the host: $([ "$base" = "$live" ] && [ -n "$live" ] && echo yes || echo no); dell1 harvest release ${DELL:0:10} is an ancestor of base: $dellanc; release ${rel:0:10}; trunk ${trunk:0:10}"
hcar=0; hn=0; for h in harvest_research harvest_figures harvest_identity harvest_keys; do hn=$((hn+1)); a=$(git rev-parse "$base:$GW/app/$h.py" 2>/dev/null | tr -d '\r'); b2=$(git rev-parse "$rel:$GW/app/$h.py" 2>/dev/null | tr -d '\r'); [ -n "$a" ] && [ "$a" = "$b2" ] && hcar=$((hcar+1)); done
echo "dell1's four harvest files byte-equal between the live base and the release: $hcar of $hn (want 4 of 4)"
echo "files differing $n (want 19 to 21: the 18 required with the deploy script, plus at most the two optional pin tests); outside the take list $outside (want 0); required files missing $missing (want 0); not byte-equal to trunk's $neq (want 0); Terraform, manifest, catalog or unit files in the diff $barred (want 0); manifest unchanged $mani_same"
printf '%s\n' "$dep" | sed '$d'
printf '%s\n' "$rec" | sed '$d'
echo "ask has the three halves, the process-wide state line, the tools-live, IAM and enablement widening $halves"
[ "$hcar" = 4 ] && [ "$dellanc" = yes ] && [ -n "$live" ] && [ "$base" = "$live" ] && [ "$n" -ge 19 ] && [ "$n" -le 21 ] && [ "$outside" = 0 ] && [ "$missing" = 0 ] && [ "$neq" = 0 ] && [ "$barred" = 0 ] && [ "$mani_same" = yes ] && [ "$(printf '%s\n' "$dep" | tail -1)" = OK ] && [ "$halves" = yes ] && [ "$(printf '%s\n' "$rec" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
