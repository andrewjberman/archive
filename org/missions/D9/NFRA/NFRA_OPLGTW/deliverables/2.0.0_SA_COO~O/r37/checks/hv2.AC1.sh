#!/usr/bin/env bash
# OPLGTW OG-hv-2 AC1 (round-37 R4, PHASE A): the re-cut and the grant file.
#  - W/hv2_release.json base_sha is the live ref BEFORE this release: EC2_MANIFEST deployed_commit at HEAD, or, once this
#    release is the deployed one, its previous_deployed_commit;
#  - base..release differs only in OG-hv-1's seven gateway files, and app/harvest_read.py is byte-equal to box/sitez HEAD;
#  - infra/aws/terraform/opal-gateway/harvest_read_iam.tf: the GetObject object ARNs' prefixes equal SERVED_PREFIXES
#    (read from HEAD's app/harvest_read.py), the s3:prefix list condition covers the same 24, the builder's policy name is
#    present, and no action other than s3:GetObject / s3:ListBucket appears.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/hv2_release.json"
[ -f "$REC" ] || { echo "hv2_release.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" || { echo "release_sha ${rel:-EMPTY} is not a commit here"; echo "RESULT: FAIL"; exit 1; }
read -r dep prev <<<"$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'];print(s.get('deployed_commit','NONE'),s.get('previous_deployed_commit','NONE'))" | tr -d '\r')"
live=$dep; [ "$dep" = "$rel" ] && live=$prev
ALLOW="^$GW/(app/harvest_read\.py|app/tools\.py|app/data_entitlement\.py|app/destructive_ops\.py|tests/test_og_hv1\.py|tests/test_entitlement_admin\.py|tests/test_data_entitlement_family\.py)$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
eqh=no; [ "$(git rev-parse "$rel:$GW/app/harvest_read.py" 2>/dev/null)" = "$(git rev-parse "HEAD:$GW/app/harvest_read.py" 2>/dev/null)" ] && eqh=yes
tf=$(python - <<'EOF'
import ast, re
try:
    tree = ast.parse(open("infra/aws/ec2/opal-gateway/app/harvest_read.py", encoding="utf-8").read())
    want = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "SERVED_PREFIXES" for t in n.targets):
            want = set(ast.literal_eval(n.value))
    t = open("infra/aws/terraform/opal-gateway/harvest_read_iam.tf", encoding="utf-8").read()
except Exception:
    print("grant object prefixes equal SERVED_PREFIXES: 0 of 0, extra 0; list condition prefixes 0 of 0; non-read actions 0 (file absent)")
    print("NO"); raise SystemExit(0)
objs = set(re.findall(r"arn:aws:s3:::opal-data-harvest/([^\"*]+)\*", t))
conds = set(p.rstrip("*") for p in re.findall(r"\"([a-z0-9-]+/\*?)\"", t))
acts = set(re.findall(r"\"(s3:[A-Za-z*]+|kms:[A-Za-z*]+|[a-z0-9]+:[A-Za-z*]+)\"", t))
nonread = len(acts - {"s3:GetObject", "s3:ListBucket", "s3:prefix"})
named = "gateway-global-harvest-read-policy" in t or "harvest-read" in t
wide = len(re.findall(r"opal-data-harvest/\*", t))   # a bucket-wide object ARN rides beside the 24 unseen by objs
# A5: harvest_read.py reads through internal_role.s3_client() (the assumed gateway-global-internal-reader-role, no
# fallback), so the one policy attaches to aws_iam_role.int_reader and never to aws_iam_role.gw.
role_ok = "aws_iam_role.int_reader" in t and "aws_iam_role.gw" not in t
print("grant object prefixes equal SERVED_PREFIXES: %d of %d, extra %d; list condition prefixes %d of %d; non-read actions %d; bucket-wide object ARNs %d; builder name %s; attached to the internal reader role %s"
      % (len(objs & want), len(want), len(objs - want), len(conds & want), len(want), nonread, wide, "yes" if named else "no", "yes" if role_ok else "no"))
print("OK" if want and len(want) == 24 and objs == want and want <= conds and nonread == 0 and wide == 0 and named and role_ok else "NO")
EOF
)
tf=$(printf '%s' "$tf" | tr -d '\r')
echo "base ${base:0:10} is the live ref before this release: $([ "$base" = "$live" ] && echo yes || echo no) (manifest ${dep:0:10}/${prev:0:10}); release ${rel:0:10}"
echo "files differing $(printf '%s\n' "$files" | grep -c .); outside OG-hv-1's files $outside (want 0); harvest_read.py byte-equal to HEAD: $eqh"
printf '%s\n' "$tf" | head -1
[ "$base" = "$live" ] && [ "$outside" = 0 ] && [ "$eqh" = yes ] && [ "$(printf '%s\n' "$tf" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
