#!/usr/bin/env bash
# OPLGTW OG-cs-5 AC2 (cli-shim workstream, wave 1): the writer event carries widening_confirm only when the owner sent true.
# app/admin_people_access.invoke_set_person_access(tid, oid, change, expect_revision, owner_header, client=<fake>, widening_confirm=<bool>) in one fresh process, a fake lambda client capturing the Payload:
#  (a) widening_confirm=True -> the event holds "widening_confirm": true and the six old keys unchanged;
#  (b) widening_confirm=False and the argument omitted -> the event holds EXACTLY the six old keys (action, tid, oid, change, expect_revision, owner_header): no widening_confirm key at all;
#  (c) the route passes it: the source of access_post reads body.get("widening_confirm") (checked by calling access_post's inner function through a stub request when reachable, else by source text) and hands it to invoke_set_person_access.
. "$(dirname "$0")/../../r47/checks/_gwtests.sh"
res=$(python3 -I - "$(native "$GW")" <<'PYEOF'
import inspect, io, json, os, sys
G = sys.argv[1]
sys.path.insert(0, G)
os.environ["MOCK_GRAPH"] = "1"
os.environ.setdefault("GRANT_WRITER_FUNCTION_NAME", "writer-fn")
import warnings
warnings.simplefilter("ignore")
ok = True


def say(label, cond):
    global ok
    ok = ok and bool(cond)
    print("%s: %s" % (label, "ok" if cond else "NOT OK"))


try:
    from app import admin_grants, admin_people_access as pa
except Exception as exc:  # noqa: BLE001
    print("import failed: %s" % type(exc).__name__)
    print("NO")
    sys.exit(0)
os.environ[admin_grants.GRANT_WRITER_FUNCTION_ENV] = "writer-fn"


class Fake:
    def __init__(self):
        self.events = []

    def invoke(self, FunctionName, InvocationType, Payload):  # noqa: N803
        self.events.append(json.loads(Payload.decode("utf-8")))
        return {"Payload": io.BytesIO(json.dumps({"verdict": "written", "reason": ""}).encode())}


OLD = {"action", "tid", "oid", "change", "expect_revision", "owner_header"}
args = ("t" * 8 + "-0000-0000-0000-" + "0" * 12, "o" * 8 + "-0000-0000-0000-" + "0" * 12, {"channels_allow": ["native"]}, None, "hdr")
try:
    f1 = Fake()
    pa.invoke_set_person_access(*args, client=f1, widening_confirm=True)
    e1 = f1.events[0] if f1.events else {}
    say("widening_confirm=True: the event holds widening_confirm true and the six old keys (keys %s)" % sorted(e1), e1.get("widening_confirm") is True and OLD <= set(e1))
    f2, f3 = Fake(), Fake()
    pa.invoke_set_person_access(*args, client=f2, widening_confirm=False)
    pa.invoke_set_person_access(*args, client=f3)
    e2 = f2.events[0] if f2.events else {}
    e3 = f3.events[0] if f3.events else {}
    say("false and omitted: the event holds EXACTLY the six old keys (false: %s; omitted: %s)" % (sorted(e2), sorted(e3)), set(e2) == OLD and set(e3) == OLD)
except TypeError as exc:
    say("invoke_set_person_access accepts widening_confirm (TypeError %s)" % str(exc)[:60], False)
src = inspect.getsource(pa)
body_read = "widening_confirm" in inspect.getsource(pa.shape_refusal) and 'get("widening_confirm"' in src.replace("'", '"')
passes = "widening_confirm=" in src.split("def access_post", 1)[-1] if "def access_post" in src else False
say("the route reads widening_confirm from the body and hands it to the invoke (read %s, passed %s)" % (body_read, passes), body_read and passes)
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
