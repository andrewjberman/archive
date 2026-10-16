#!/usr/bin/env bash
# OPLGTW OG-ap-31 AC1 (round 39, the second batched gateway release, PHASE A): the re-cut carries exactly the round-39 code, nothing else.
#  - W/ap31_release.json {base_sha, release_sha, trunk_sha}; base_sha is the live ref BEFORE this release (EC2_MANIFEST deployed_commit at HEAD, or previous_deployed_commit once this release is the deployed one);
#  - base..release differs only in the allowed set (client_adapter_bd49f.py, data_entitlement.py, server.py, opal_discover/integration.py, the tests, the naming-gate registry files if the prelude is needed);
#  - no Terraform; tools.py and destructive_ops.py untouched; deploy-to-ec2.sh and EC2_MANIFEST.json UNCHANGED; no data copy committed;
#  - every registry file in the diff is byte-equal to its blob at trunk_sha; the ask has the three half headings.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
GW=infra/aws/ec2/opal-gateway
REC="${AP31_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/ap31_release.json}"
ASK="${AP31_ASK_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-31.md}"
[ -f "$REC" ] && [ -f "$ASK" ] || { echo "ap31_release.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel trunk <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''),d.get('trunk_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" && git cat-file -e "${base}^{commit}" && git cat-file -e "${trunk}^{commit}" || { echo "base, release or trunk sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
read -r dep prev <<<"$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'];print(s.get('deployed_commit','NONE'),s.get('previous_deployed_commit','NONE'))" | tr -d '\r')"
live=$dep; [ "$dep" = "$rel" ] && live=$prev
ALLOW="^($GW/(app/(client_adapter_bd49f|data_entitlement|server)\.py|app/integrations/opal_discover/integration\.py|tests/[A-Za-z0-9_./-]+)|infra/logic/registry/[A-Za-z0-9_]+\.json)$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
tf=$(printf '%s\n' "$files" | grep -c '\.tf$')
tools_touched=$(printf '%s\n' "$files" | grep -cE "$GW/app/(tools|destructive_ops)\.py")
deploy_changed=$(printf '%s\n' "$files" | grep -cE "$GW/deploy-to-ec2\.sh|infra/aws/ec2/EC2_MANIFEST\.json")
cm=$(git diff --name-only "$base" "$rel" -- "$GW/app/refs/partner_roster.json" "$GW/app/refs/scopes.json" | grep -c .)
regdiff=0; regbad=0
for p in $(printf '%s\n' "$files" | grep -E '^infra/logic/registry/'); do
  regdiff=$((regdiff+1)); a=$(git rev-parse "$rel:$p" 2>/dev/null | tr -d '\r'); b=$(git rev-parse "$trunk:$p" 2>/dev/null | tr -d '\r')
  [ -n "$a" ] && [ "$a" = "$b" ] || regbad=$((regbad+1))
done
halves=$(python - "$(native "$ASK")" <<'PYEOF'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
print("yes" if all(re.search(r"(?mi)^#+ .*%s" % h, t) for h in ("CTO", "COO", "CVO")) else "no")
PYEOF
)
halves=$(printf '%s' "$halves" | tr -d '\r')
echo "base ${base:0:10} is the live ref before this release: $([ "$base" = "$live" ] && echo yes || echo no) (manifest ${dep:0:10}/${prev:0:10}); release ${rel:0:10}; trunk ${trunk:0:10}"
echo "files differing $n; outside the batch set $outside (want 0); terraform files differing $tf (want 0); tools.py or destructive_ops.py touched $tools_touched (want 0)"
echo "deploy script or manifest changed $deploy_changed (want 0); data copies committed $cm (want 0); registry files in the diff $regdiff, not byte-equal to trunk's $regbad (want 0); ask has the three halves $halves"
[ "$base" = "$live" ] && [ "$n" -ge 1 ] && [ "$outside" = 0 ] && [ "$tf" = 0 ] && [ "$tools_touched" = 0 ] && [ "$deploy_changed" = 0 ] && [ "$cm" = 0 ] && [ "$regbad" = 0 ] && [ "$halves" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
