#!/usr/bin/env bash
# OPLGTW OG-m-2 AC2: the SERVED dispatcher is the built artifact of the committed source, it moved off the 2026-08-19 build
# (CodeSha256 fEMCZ4..., built_from_commit 1abc54fa4c), and the role's s3 read grant is exactly GetObject on the chain logs and GetObject+GetObjectVersion on the marker (A1).
# Read-only: lambda get-function, s3api head-object, iam get-role-policy, one GET of the presigned code URL.
. "$(dirname "$0")/_root.sh"
AWS=".tools/aws"
PREV="fEMCZ4usqXuIC1GhklcClwOn/O6vR+uV+xgbk+oj8lk="
FN="advi-49f-gold-dispatch"
SRC="infra/aws/lambda/opal-assets/advi-49f-gold-dispatch/lambda_function.py"
live=$(timeout 60 "$AWS" lambda get-function --region us-east-1 --function-name "$FN" --query Configuration.CodeSha256 --output text | tr -d '\r'); r1=$?
art=$(timeout 60 "$AWS" s3api head-object --bucket opal-313476888478-lambda-artifacts --key "opal-assets/$FN.zip" --query 'Metadata."content-sha256"' --output text | tr -d '\r'); r2=$?
url=$(timeout 60 "$AWS" lambda get-function --region us-east-1 --function-name "$FN" --query Code.Location --output text | tr -d '\r'); r3=$?
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
want = {'arn:aws:s3:::opal-data-assets/schwab/08335338/meta/complete/*': {'s3:getobject', 's3:getobjectversion'}}
hit = sum(1 for r, a in want.items() if acts_by_res.get(r) == a)
extra = sum(1 for r, a in acts_by_res.items() if want.get(r) != a)
print('%d %d' % (hit, extra))" | tr -d '\r'); r6=$?
hit=$(printf '%s' "$res" | cut -d' ' -f1); extra=$(printf '%s' "$res" | cut -d' ' -f2)
a=no; [ -n "$live" ] && [ "$live" = "$art" ] && a=yes
b=no; [ -n "$live" ] && [ "$live" != "$PREV" ] && b=yes
c=no; [ -n "$member_sha" ] && [ "$member_sha" = "$head_sha" ] && c=yes
echo "live=$live artifact=$art (rc $r1/$r2/$r3/$r4/$r5/$r6)"
echo "live sha = artifact sha: $a; moved off previous: $b; zip member = HEAD bytes: $c; GetObject resources exact ${hit:-0} of 1 (extra ${extra:-?})"
if [ "$a" = yes ] && [ "$b" = yes ] && [ "$c" = yes ] && [ "$hit" = 1 ] && [ "$extra" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
