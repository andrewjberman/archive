#!/usr/bin/env bash
# MP-b-2 AC3 (R-4, the grants' shape, read from the committed Terraform): mcportal_grant_writer.tf at HEAD declares the
# table named mcportal-grant-changes-table; the statement Sid McportalGrantChangesPutOnly grants exactly
# ["dynamodb:PutItem"]; and the statement Sid GatewayReadsMcportalGrantChanges grants only read actions (GetItem, Query,
# Scan) -- no Put, Update, Delete or BatchWrite.
. "$(dirname "$0")/_root.sh"
TF="infra/aws/terraform/opal-gateway/mcportal_grant_writer.tf"
out=$(git show "HEAD:$TF" 2>/dev/null | timeout 30 python -c "
import re, sys
t = sys.stdin.buffer.read().decode('utf-8')
tbl = 'yes' if re.search(r'name\s*=\s*\"mcportal-grant-changes-table\"', t) else 'no'
def actions(sid):
    m = re.search(r'Sid\s*=\s*\"%s\"(.*?)\}' % sid, t, re.S)
    if not m:
        return None
    a = re.search(r'Action\s*=\s*\[(.*?)\]', m.group(1), re.S)
    return sorted(re.findall(r'\"([^\"]+)\"', a.group(1))) if a else None
w = actions('McportalGrantChangesPutOnly'); g = actions('GatewayReadsMcportalGrantChanges')
ro = {'dynamodb:GetItem', 'dynamodb:Query', 'dynamodb:Scan'}
print('table=%s writer=%s gateway=%s' % (tbl, w, g))
print('W_OK=%s' % ('yes' if w == ['dynamodb:PutItem'] else 'no'))
print('G_OK=%s' % ('yes' if g and set(g) <= ro else 'no'))
" 2>&1 | tr -d '\r')
printf '%s\n' "$out" | sed -n 1p
tb=$(printf '%s\n' "$out" | sed -n 's/^table=\([a-z]*\) .*/\1/p'); wo=$(printf '%s\n' "$out" | sed -n 's/^W_OK=//p'); go=$(printf '%s\n' "$out" | sed -n 's/^G_OK=//p')
echo "changes table declared=${tb:-no}; writer statement PutItem only=${wo:-no}; gateway statement read-only=${go:-no}"
if [ "$tb" = yes ] && [ "$wo" = yes ] && [ "$go" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
