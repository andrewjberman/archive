#!/usr/bin/env bash
# MP-pd-7 AC2 (Act A only, AMENDMENT A2; the deployed bytes, independent of the apply's rc): from this box, the grant-writer Lambda:
#   - its CodeSha256 equals the sha the close report states (field GW_LAMBDA_SHA256 in the MP-pd-7 close report);
#   - the code zip it serves (the presigned URL get-function returns) holds a lambda_function.py that contains WIDEN-NO-CONFIRM and widening_signoff;
#   - invoking it with NO owner header on action set_person_access answers REFUSED NO-OWNER-HEADER.
. "$(dirname "$0")/_root.sh"
CR="$PDD/0.7.0_AE_CloudOps~NFRA1/MP-pd-7_CLOSE_REPORT.md"
[ -f "$CR" ] || { echo "$CR absent"; echo "RESULT: FAIL"; exit 1; }
want=$(grep -oE 'GW_LAMBDA_SHA256=[A-Za-z0-9+/=]+' "$CR" | head -1 | cut -d= -f2-)
# list-functions auto-paginates and --query runs once per page (a page with no match prints "None"), so the name is picked by grep, not by [0]
fn=$("$AWS" lambda list-functions --query "Functions[?contains(FunctionName,'mcportal-grant-writer')].FunctionName" --output text | tr -d '\r' | tr '\t' '\n' | grep -m1 'mcportal-grant-writer')
got=$("$AWS" lambda get-function-configuration --function-name "$fn" --query CodeSha256 --output text | tr -d '\r')
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
printf '%s' '{"action":"set_person_access","tid":"00000000-0000-0000-0000-000000000000","oid":"00000000-0000-0000-0000-000000000000","change":{"stopped":false},"expect_revision":null}' > "$T/ev.json"
inv=$("$AWS" lambda invoke --function-name "$fn" --payload "fileb://$(cygpath -w "$T/ev.json")" "$(cygpath -w "$T/out.json")" --query StatusCode --output text | tr -d '\r')
reason=$(python -c "import json,sys;d=json.load(open(sys.argv[1]));print(d.get('verdict'),d.get('reason'))" "$(cygpath -w "$T/out.json")" 2>&1 | tr -d '\r')
url=$("$AWS" lambda get-function --function-name "$fn" --query Code.Location --output text | tr -d '\r')
curl -s -o "$T/code.zip" "$url"
tokens=$(python -c "
import sys, zipfile
z = zipfile.ZipFile(sys.argv[1])
src = z.read('lambda_function.py').decode('utf-8')
print('WIDEN-NO-CONFIRM' in src and 'widening_signoff' in src)
" "$(cygpath -w "$T/code.zip")" 2>&1 | tr -d '\r' | tail -1)
echo "lambda=$fn sha_got=${got:-none} sha_want=${want:-none}; invoke status=${inv:-none} verdict_reason=[$reason]; deployed lambda_function.py holds both widening tokens: $tokens"
if [ -n "$want" ] && [ "$got" = "$want" ] && [ "$inv" = 200 ] && printf '%s' "$reason" | grep -q 'REFUSED NO-OWNER-HEADER' && [ "$tokens" = True ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
