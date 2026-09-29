#!/usr/bin/env bash
# OPLGTW OG-m-3 AC2: the SERVED dispatcher is the built artifact of the committed source and moved off the OG-m-2a build
# (CodeSha256 KqlIoAJs..., deployed 2026-09-29T02:05:33Z); the role's s3 read grant is EXACTLY {chain-log prefix:
# GetObject} and {marker prefix: GetObject+GetObjectVersion}; the function env carries CHAIN_LOG_PREFIX and
# CHAIN_LOG_BUCKET equal to the Terraform locals at HEAD (advi_49f_chain_log_prefix, advi_49f_bucket).
# Read-only: lambda get-function, s3api head-object, iam get-role-policy, one GET of the presigned code URL.
. "$(dirname "$0")/_root.sh"
AWS=".tools/aws"
PREV="KqlIoAJs98dXE1RoL9g0xBG0yQw9Mo3JiSFUaJO17qg="
FN="advi-49f-gold-dispatch"
SRC="infra/aws/lambda/opal-assets/advi-49f-gold-dispatch/lambda_function.py"
TF="infra/aws/terraform/opal-assets/advi_49f_floor.tf"
want_prefix=$(MSYS_NO_PATHCONV=1 git show "HEAD:$TF" | sed -n 's/^ *advi_49f_chain_log_prefix *= *"\([^"]*\)".*/\1/p' | head -1)
want_bucket=$(MSYS_NO_PATHCONV=1 git show "HEAD:$TF" | sed -n 's/^ *advi_49f_bucket *= *"\([^"]*\)".*/\1/p' | head -1)
live=$(timeout 60 "$AWS" lambda get-function --region us-east-1 --function-name "$FN" --query Configuration.CodeSha256 --output text | tr -d '\r'); r1=$?
art=$(timeout 60 "$AWS" s3api head-object --bucket opal-313476888478-lambda-artifacts --key "opal-assets/$FN.zip" --query 'Metadata."content-sha256"' --output text | tr -d '\r'); r2=$?
url=$(timeout 60 "$AWS" lambda get-function --region us-east-1 --function-name "$FN" --query Code.Location --output text | tr -d '\r'); r3=$?
envp=$(timeout 60 "$AWS" lambda get-function-configuration --region us-east-1 --function-name "$FN" --query 'Environment.Variables.CHAIN_LOG_PREFIX' --output text | tr -d '\r')
envb=$(timeout 60 "$AWS" lambda get-function-configuration --region us-east-1 --function-name "$FN" --query 'Environment.Variables.CHAIN_LOG_BUCKET' --output text | tr -d '\r')
head_sha=$(MSYS_NO_PATHCONV=1 git show "HEAD:$SRC" | sha256sum | cut -c1-64)
member_sha=$(timeout 60 python -c "
import hashlib, io, sys, urllib.request, zipfile
z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(sys.argv[1]).read()))
print(hashlib.sha256(z.read('lambda_function.py')).hexdigest())" "$url" | tr -d '\r'); r4=$?
pol=$(timeout 60 "$AWS" iam get-role-policy --role-name "$FN-role" --policy-name "$FN-scoped" --query PolicyDocument --output json | tr -d '\r'); r5=$?
res=$(printf '%s' "$pol" | python -c "
import json, sys, urllib.parse
raw = sys.stdin.read().strip()
d = json.loads(raw)
if isinstance(d, str):
    d = json.loads(urllib.parse.unquote(d))
acts_by_res = {}
for s in d.get('Statement', []):
    acts = s.get('Action', []); acts = [acts] if isinstance(acts, str) else acts
    s3a = [a.lower() for a in acts if a.lower().startswith('s3:')]
    if s3a:
        rs = s.get('Resource', []); rs = [rs] if isinstance(rs, str) else rs
        for r in rs:
            acts_by_res.setdefault(r, set()).update(s3a)
chain = 'arn:aws:s3:::' + sys.argv[1] + '/' + sys.argv[2] + '*'
want = {chain: {'s3:getobject'}, 'arn:aws:s3:::opal-data-assets/schwab/08335338/meta/complete/*': {'s3:getobject', 's3:getobjectversion'}}
hit = sum(1 for r, a in want.items() if acts_by_res.get(r) == a)
extra = sum(1 for r, a in acts_by_res.items() if want.get(r) != a)
print('%d %d' % (hit, extra))" "${want_bucket:-NONE}" "${want_prefix:-NONE}" | tr -d '\r'); r6=$?
hit=$(printf '%s' "$res" | cut -d' ' -f1); extra=$(printf '%s' "$res" | cut -d' ' -f2)
a=no; [ -n "$live" ] && [ "$live" = "$art" ] && a=yes
b=no; [ -n "$live" ] && [ "$live" != "$PREV" ] && b=yes
c=no; [ -n "$member_sha" ] && [ "$member_sha" = "$head_sha" ] && c=yes
e=no; [ -n "$want_prefix" ] && [ "$envp" = "$want_prefix" ] && [ -n "$want_bucket" ] && [ "$envb" = "$want_bucket" ] && e=yes
echo "live=$live artifact=$art local prefix=${want_prefix:-ABSENT} env prefix=$envp env bucket=$envb (rc $r1/$r2/$r3/$r4/$r5/$r6)"
echo "live sha = artifact sha: $a; moved off previous: $b; zip member = HEAD bytes: $c; s3 read grants exact ${hit:-0} of 2 (extra ${extra:-?}); env = locals: $e"
if [ "$a" = yes ] && [ "$b" = yes ] && [ "$c" = yes ] && [ "$hit" = 2 ] && [ "$extra" = 0 ] && [ "$e" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
