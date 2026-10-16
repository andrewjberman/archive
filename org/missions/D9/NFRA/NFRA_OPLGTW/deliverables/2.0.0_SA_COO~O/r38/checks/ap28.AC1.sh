#!/usr/bin/env bash
# OPLGTW OG-ap-28 AC1 (round 38, the batched gateway release, PHASE A): the re-cut carries exactly the round-38 code, the catalog edit and the one deploy hunk, no Terraform.
#  - W/ap28_release.json {base_sha, release_sha, trunk_sha, mcportal_sha}; base_sha is the live ref BEFORE this release (EC2_MANIFEST deployed_commit at HEAD, or previous_deployed_commit once this release is the deployed one);
#  - base..release differs only in the allowed set (the round-38 app files, the catalog, the deploy script, the tests, the manifest); no Terraform;
#  - app/tools.py and app/destructive_ops.py are NOT in the diff (no tool is added or removed);
#  - the deploy script's diff adds the env key BLACKDIAMOND49FLIVE_READER_ROLE_ARN in its own printf slot with its own arg (every other slot unmoved), resolves the role by _vr_arn, removes no line but the env printf, and passes bash -n (r38/checks/_dsh_check.py);
#  - the manifest's mcportal_commit equals mcportal_sha, descends from the live pin, and is the only manifest field changed;
#  - the release does NOT commit app/refs/partner_roster.json or app/refs/scopes.json; the ask for three halves exists.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${AP28_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/ap28_release.json}"
ASK="${AP28_ASK_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-28.md}"
[ -f "$REC" ] && [ -f "$ASK" ] || { echo "ap28_release.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel trunk mcp <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''),d.get('trunk_sha',''),d.get('mcportal_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" && git cat-file -e "${base}^{commit}" && git cat-file -e "${trunk}^{commit}" || { echo "base, release or trunk sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
read -r dep prev <<<"$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'];print(s.get('deployed_commit','NONE'),s.get('previous_deployed_commit','NONE'))" | tr -d '\r')"
live=$dep; [ "$dep" = "$rel" ] && live=$prev
ALLOW="^($GW/(app/(client_core|client_role|client_adapter_(bd49f|bdcottonwood|commonwealth|orion|schwab|smartx)|news_typed|harvest_press|data_entitlement|config|query_v0|ratelimit|server|audit)\.py|app/graphql_plumbing/catalog_gate\.py|app/refs/DATA_CATALOG\.yaml|deploy-to-ec2\.sh|tests/[A-Za-z0-9_./-]+)|infra/aws/ec2/EC2_MANIFEST\.json)$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
tf=$(printf '%s\n' "$files" | grep -c '\.tf$')
tools_touched=$(printf '%s\n' "$files" | grep -cE "$GW/app/(tools|destructive_ops)\.py")
dsh=$(python "$(native "$(dirname "$0")/_dsh_check.py")" "$base" "$rel" | tr -d '\r')
dget() { printf '%s' "$dsh" | tr ' ' '\n' | grep "^$1=" | cut -d= -f2; }
cm=$(git ls-tree -r --name-only "$rel" -- "$GW/app/refs/partner_roster.json" "$GW/app/refs/scopes.json" | grep -c .)
cmbase=$(git ls-tree -r --name-only "$base" -- "$GW/app/refs/partner_roster.json" "$GW/app/refs/scopes.json" | grep -c .)
mcp_ok=$(python - "$base" "$rel" "$mcp" <<'PYEOF'
import json, subprocess, sys
base, rel, mcp = sys.argv[1:4]
def man(ref):
    raw = subprocess.run(["git", "show", "%s:infra/aws/ec2/EC2_MANIFEST.json" % ref], capture_output=True).stdout.decode("utf-8", "replace")
    return json.loads(raw)["services"]["opal-gateway"]
b, r = man(base), man(rel)
same = {k: v for k, v in b.items() if k != "mcportal_commit"} == {k: v for k, v in r.items() if k != "mcportal_commit"}
desc = False
if mcp and r.get("mcportal_commit") == mcp:
    desc = subprocess.run(["git", "-C", "mcportal", "merge-base", "--is-ancestor", b.get("mcportal_commit", ""), mcp], capture_output=True).returncode == 0
print("yes" if (r.get("mcportal_commit") == mcp and same and desc) else "no")
PYEOF
)
mcp_ok=$(printf '%s' "$mcp_ok" | tr -d '\r')
halves=$(python - "$(native "$ASK")" <<'PYEOF'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
print("yes" if all(re.search(r"(?mi)^#+ .*%s" % h, t) for h in ("CTO", "COO", "CVO")) else "no")
PYEOF
)
halves=$(printf '%s' "$halves" | tr -d '\r')
echo "base ${base:0:10} is the live ref before this release: $([ "$base" = "$live" ] && echo yes || echo no) (manifest ${dep:0:10}/${prev:0:10}); release ${rel:0:10}; trunk ${trunk:0:10}"
echo "files differing $n; outside the batch set $outside (want 0); terraform files differing $tf (want 0); tools.py or destructive_ops.py touched $tools_touched (want 0)"
echo "deploy script: env key added $(dget key_added) (want 1); every %s has its arg $(dget pct_equals_args); slot aligned, other slots unmoved $(dget aligned); role resolved by _vr_arn $(dget role_assigned) (want 1); removed lines other than the env printf $(dget removed_other) (want 0); added lines other than the printf and the role $(dget added_other) (informational); bash -n $(dget syntax)"
echo "mcportal pin: manifest mcportal_commit equals the GO's, descends from the live pin, only that manifest field changed $mcp_ok; data copies committed in the release $cm (base had $cmbase; want equal); ask has the three halves $halves"
[ "$base" = "$live" ] && [ "$n" -ge 1 ] && [ "$outside" = 0 ] && [ "$tf" = 0 ] && [ "$tools_touched" = 0 ] && [ "$(dget key_added)" = 1 ] && [ "$(dget pct_equals_args)" = yes ] && [ "$(dget aligned)" = yes ] && [ "$(dget role_assigned)" = 1 ] && [ "$(dget removed_other)" = 0 ] && [ "$(dget syntax)" = yes ] && [ "$mcp_ok" = yes ] && [ "$cm" = "$cmbase" ] && [ "$halves" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
