#!/usr/bin/env bash
# MP-a-2 AC4 (R-9, row Z-W1-S5): the grant writer's note in infra/aws/lambda/ci/lambda-source-map.json no longer names
# the retired MCPORTAL_OWNER_OID variable and names the two variables MP-b-2 introduced, MCPORTAL_OWNER_KEY_CLAIM and
# MCPORTAL_OWNER_KEY. Read at HEAD (git show), never the working-tree path.
. "$(dirname "$0")/_root.sh"
F="infra/aws/lambda/ci/lambda-source-map.json"
res=$(git show "HEAD:$F" 2>&1 | python -c "
import re, sys
t = sys.stdin.read()
oid = t.count('MCPORTAL_OWNER_OID')
claim = t.count('MCPORTAL_OWNER_KEY_CLAIM')
key = len(re.findall(r'MCPORTAL_OWNER_KEY\b(?!_)', t))
print('bytes=%d MCPORTAL_OWNER_OID=%d MCPORTAL_OWNER_KEY_CLAIM=%d MCPORTAL_OWNER_KEY=%d' % (len(t), oid, claim, key))
" 2>&1 | tr -d '\r')
echo "$F at HEAD: $res"
if printf '%s' "$res" | grep -q 'MCPORTAL_OWNER_OID=0 ' && ! printf '%s' "$res" | grep -qE 'MCPORTAL_OWNER_KEY_CLAIM=0 |MCPORTAL_OWNER_KEY=0$|bytes=0 '; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
