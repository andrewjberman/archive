#!/usr/bin/env bash
# MP-pd-7 AC2 (F2 live; the served read, independent of the deploy's rc): over SSM on the gateway host, from /opt/opal-gateway
# with the host's .venv, as ec2-user, the probe begins with `import app.server` (row Z-S48) and reads that
#   - app.admin_people_access is importable and the app routes include POST and GET /people/{tid}/{oid}/access;
#   - app.admin_people._compute() has every row carry a `principal` key, and at least one non-null;
# and from this box, the grant-writer Lambda: its CodeSha256 equals the sha the close report states (field GW_LAMBDA_SHA256
# in the MP-pd-7 close report) and invoking it with NO owner header on action set_person_access answers REFUSED NO-OWNER-HEADER.
. "$(dirname "$0")/_root.sh"
CR="$PDD/0.7.0_AE_CloudOps~MQ/MP-pd-7_CLOSE_REPORT.md"
[ -f "$CR" ] || { echo "$CR absent"; echo "RESULT: FAIL"; exit 1; }
want=$(grep -oE 'GW_LAMBDA_SHA256=[A-Za-z0-9+/=]+' "$CR" | head -1 | cut -d= -f2-)
fn=$("$AWS" lambda list-functions --query "Functions[?contains(FunctionName,'mcportal-grant-writer')].FunctionName | [0]" --output text 2>/dev/null | tr -d '\r')
got=$("$AWS" lambda get-function-configuration --function-name "$fn" --query CodeSha256 --output text 2>/dev/null | tr -d '\r')
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
printf '%s' '{"action":"set_person_access","tid":"00000000-0000-0000-0000-000000000000","oid":"00000000-0000-0000-0000-000000000000","change":{"stopped":false},"expect_revision":null}' > "$T/ev.json"
inv=$("$AWS" lambda invoke --function-name "$fn" --payload "fileb://$(cygpath -w "$T/ev.json")" "$T/out.json" --query StatusCode --output text 2>/dev/null | tr -d '\r')
reason=$(python -c "import json,sys;d=json.load(open(sys.argv[1]));print(d.get('verdict'),d.get('reason'))" "$T/out.json" 2>&1 | tr -d '\r')
cat > "$T/probe.py" <<'PY'
import json, sys
sys.path.insert(0, "/opt/opal-gateway")
import app.server  # registers the served integrations (row Z-S48)
from app import admin_api, admin_people
paths = {(r.path, tuple(sorted(r.methods or []))) for r in admin_api.routes if hasattr(r, "path")}
ok_routes = any(p == "/people/{tid}/{oid}/access" and "POST" in m for p, m in paths) and any(p == "/people/{tid}/{oid}/access" and "GET" in m for p, m in paths)
body = admin_people._compute()
rows = body.get("people", [])
print(json.dumps({"routes": ok_routes, "rows": len(rows), "all_have_key": all("principal" in r for r in rows), "non_null": sum(1 for r in rows if r.get("principal"))}))
PY
python - "$T/probe.py" "$T/params.json" <<'PY'
import json, sys
src = open(sys.argv[1]).read()
cmds = ["cd /opt/opal-gateway && ./.venv/bin/python - <<'EOF'\n" + src + "\nEOF"]
json.dump({"commands": cmds, "executionTimeout": ["90"]}, open(sys.argv[2], "w"))
PY
ssm_run "$T/params.json"
echo "ssm status=$SSM_ST cmd=$SSM_CID out=$SSM_OUT"
echo "lambda=$fn sha_got=${got:-none} sha_want=${want:-none}; invoke status=${inv:-none} verdict_reason=[$reason]"
okssm=$(printf '%s' "$SSM_OUT" | python -c "import json,sys;d=json.loads(sys.stdin.read().strip().splitlines()[-1]);print('yes' if d['routes'] and d['rows']>=1 and d['all_have_key'] and d['non_null']>=1 else 'no')" 2>/dev/null)
if [ "$SSM_ST" = Success ] && [ "$okssm" = yes ] && [ -n "$want" ] && [ "$got" = "$want" ] && [ "$inv" = 200 ] && printf '%s' "$reason" | grep -q 'REFUSED NO-OWNER-HEADER'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
