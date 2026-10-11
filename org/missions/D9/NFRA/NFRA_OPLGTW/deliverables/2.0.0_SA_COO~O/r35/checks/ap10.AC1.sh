#!/usr/bin/env bash
# OPLGTW OG-ap-10 AC1 (round-35 E2, the .pptx release re-cut, Phase B1): the release in W/ap10_release.json sits on the live
# ref 28ba9532b6 and carries ONLY OG-ab-2's and OG-mu-1's gateway hunks:
#  - only these 6 files differ from the base: site_to_s3.py, tools.py, destructive_ops.py, deploy-to-ec2.sh,
#    tests/test_og_ab2_pairs.py, tests/test_og_mu1.py;
#  - site_to_s3.py and the two test files are byte-equal to box/sitez HEAD (only ab-2 and mu-1 touched them since live);
#  - tools.py and destructive_ops.py: the release diff has the patch-id of ab-2's own hunk (5c2f6e9324);
#  - deploy-to-ec2.sh: the diff with the .env printf line set aside has the patch-id of ab-2's own hunk set aside the
#    same way, and the printf differs from the base's only by ADVI_MARKET_UPDATE_S3_ROOT=%s\n and its one argument.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/ap10_release.json"
LIVE=28ba9532b648061cecafe426836d3e96af4529cd; AB2=5c2f6e9324; G=infra/aws/ec2/opal-gateway
[ -f "$REC" ] || { echo "ap10_release.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" || { echo "release_sha ${rel:-EMPTY} is not a commit here"; echo "RESULT: FAIL"; exit 1; }
ALLOW="^$G/(app/integrations/advi_billing/site_to_s3\.py|app/tools\.py|app/destructive_ops\.py|deploy-to-ec2\.sh|tests/test_og_ab2_pairs\.py|tests/test_og_mu1\.py)$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
eqh=0; for f in app/integrations/advi_billing/site_to_s3.py tests/test_og_ab2_pairs.py tests/test_og_mu1.py; do
  [ "$(git rev-parse "$rel:$G/$f" 2>/dev/null)" = "$(git rev-parse "HEAD:$G/$f" 2>/dev/null)" ] && eqh=$((eqh+1)); done
pid() { git diff "$1" "$2" -- "$3" | grep -vE "^[-+]printf 'MOCK_GRAPH=0" | git patch-id --stable | awk '{print $1}'; }
pe=0; for f in app/tools.py app/destructive_ops.py deploy-to-ec2.sh; do
  a=$(pid "$AB2~1" "$AB2" "$G/$f"); b=$(pid "$base" "$rel" "$G/$f"); [ -n "$a" ] && [ "$a" = "$b" ] && pe=$((pe+1)); done
pf=$(python - "$base" "$rel" <<'EOF'
import subprocess, sys
def pl(ref):
    t = subprocess.run(["git", "show", ref + ":infra/aws/ec2/opal-gateway/deploy-to-ec2.sh"], capture_output=True).stdout.decode("utf-8")
    return [l for l in t.split("\n") if l.startswith("printf 'MOCK_GRAPH=0")]
b, r = pl(sys.argv[1]), pl(sys.argv[2])
K = "ADVI_MARKET_UPDATE_S3_ROOT=%s\\n"; A = '"${ADVI_MARKET_UPDATE_S3_ROOT}" '
ok = len(b) == 1 and len(r) == 1 and r[0].count(K) == 1 and r[0].count(A) == 1 and r[0].replace(K, "", 1).replace(A, "", 1) == b[0]
print("yes" if ok else "no")
EOF
)
pf=$(printf '%s' "$pf" | tr -d '\r')
echo "base ${base:0:10} is the live ref 28ba9532b6: $([ "$base" = "$LIVE" ] && echo yes || echo no); release ${rel:0:10}"
echo "files differing $(printf '%s\n' "$files" | grep -c .); outside the .pptx pair's files $outside (want 0)"
echo "byte-equal to HEAD: $eqh of 3; ab-2 hunk patch-id equal: $pe of 3; printf differs only by the market_update key and argument: $pf"
[ "$base" = "$LIVE" ] && [ "$outside" = 0 ] && [ "$eqh" = 3 ] && [ "$pe" = 3 ] && [ "$pf" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
