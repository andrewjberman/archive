#!/usr/bin/env bash
# OPLGTW OG-pr-6 AC2 (round 45; round-44 analysis OG-pr-6 criterion 2): the audit lake's S3 client is built with an EXPLICIT botocore Config with bounded timeouts and a retry cap.
# Read from the AST of app/audit.py: a call `boto3.client(..., config=Config(...))` (the name `Config` imported from botocore.config) with keyword arguments
#   connect_timeout a number in (0, 5], read_timeout a number in (0, 10], retries a dict with max_attempts an integer in [1, 2].
# Why those bounds (OG-ev-11, round 44): 80 of 81 audit-write sites run on the event loop; botocore's default is 60 s connect, 60 s read and 5 attempts, so one stalled put could hold the loop for minutes.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="${PR6_AUDIT_OVERRIDE:-$GW/app/audit.py}"
res=$(python -I - "$(native "$F")" <<'PYEOF'
import ast, sys
t = ast.parse(open(sys.argv[1], encoding="utf-8").read())
imports_config = any(isinstance(n, ast.ImportFrom) and (n.module or "").startswith("botocore") and any(a.name == "Config" for a in n.names) for n in ast.walk(t))
found = None
for n in ast.walk(t):
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "client" and isinstance(n.func.value, ast.Name) and n.func.value.id == "boto3":
        kw = {k.arg: k.value for k in n.keywords if k.arg}
        c = kw.get("config")
        if isinstance(c, ast.Call) and isinstance(c.func, ast.Name) and c.func.id == "Config":
            found = {k.arg: k.value for k in c.keywords if k.arg}
def num(v):
    return v.value if isinstance(v, ast.Constant) and isinstance(v.value, (int, float)) and not isinstance(v.value, bool) else None
ct = num(found.get("connect_timeout")) if found else None
rt = num(found.get("read_timeout")) if found else None
ma = None
if found and isinstance(found.get("retries"), ast.Dict):
    d = found["retries"]
    for k, v in zip(d.keys, d.values):
        if isinstance(k, ast.Constant) and k.value == "max_attempts" and isinstance(v, ast.Constant) and isinstance(v.value, int) and not isinstance(v.value, bool):
            ma = v.value
ok = imports_config and found is not None and ct is not None and 0 < ct <= 5 and rt is not None and 0 < rt <= 10 and ma is not None and 1 <= ma <= 2
print("boto3.client call with an explicit botocore Config: %s; Config imported from botocore: %s; connect_timeout %s (want a number in (0, 5]); read_timeout %s (want a number in (0, 10]); retries max_attempts %s (want 1 or 2)" % (
      "yes" if found is not None else "NO", "yes" if imports_config else "NO", ct, rt, ma))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
