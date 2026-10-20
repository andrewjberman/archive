#!/usr/bin/env bash
# MP-zo-5 AC2 (independent of the worker's file): the deployed grant writer imports at /var/task and carries its owner-key configuration.
# A no-header invoke of set_person_access answers REFUSED NO-OWNER-HEADER: handle() checks the writer's own owner config BEFORE the
# header (REFUSED OWNER-CONFIG-MISSING otherwise), so this answer shows the handler imported from its built package (row C-S8) and the owner key
# is set on the function (row W3-S2). Values are never read or printed.
. "$(dirname "$0")/../../pd/checks/_root.sh"
fn=$("$AWS" lambda list-functions --query "Functions[?contains(FunctionName,'mcportal-grant-writer')].FunctionName" --output text | tr -d '\r' | tr '\t' '\n' | grep -m1 'mcportal-grant-writer')
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
printf '%s' '{"action":"set_person_access","tid":"00000000-0000-0000-0000-000000000000","oid":"00000000-0000-0000-0000-000000000000","change":{"stopped":false},"expect_revision":null}' > "$T/ev.json"
inv=$("$AWS" lambda invoke --function-name "$fn" --payload "fileb://$(cygpath -w "$T/ev.json")" "$(cygpath -w "$T/out.json")" --query StatusCode --output text | tr -d '\r')
reason=$(python -c "import json,sys;d=json.load(open(sys.argv[1]));print(d.get('verdict'),d.get('reason'))" "$(cygpath -w "$T/out.json")" 2>&1 | tr -d '\r')
echo "lambda=$fn invoke status=${inv:-none} verdict_reason=[$reason]"
if [ "$inv" = 200 ] && printf '%s' "$reason" | grep -q 'REFUSED NO-OWNER-HEADER'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
