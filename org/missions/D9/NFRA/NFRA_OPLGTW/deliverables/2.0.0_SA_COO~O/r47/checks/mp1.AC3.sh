#!/usr/bin/env bash
# OPLGTW OG-mp-1 AC3 (a bound): the edit is the mount and nothing more. app/admin_api.py against the pinned blob 2fb26985d9: 1 to 4 lines changed in all, every added line names admin_people_access
# (the import and the `*admin_people_access.routes,` entry), no line removed except where the import block is re-ordered; app/admin_people_access.py is byte-equal to HEAD at the issuance
# (blob read below); tests/test_og_mp1.py exists with at least 3 test functions.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
G=infra/aws/ec2/opal-gateway
res=$(python3 -I - "$(native "$G")" <<'PYEOF'
import difflib, re, subprocess, sys
G = sys.argv[1]
ok = True
old = subprocess.run(["git", "show", "2fb26985d9b6982f2118c391fc3ad8a458a4a068"], capture_output=True).stdout.decode("utf-8").splitlines()
new = open(G + "/app/admin_api.py", encoding="utf-8").read().splitlines()
d = list(difflib.unified_diff(old, new, lineterm="", n=0))
r = [x[1:] for x in d if x.startswith("-") and not x.startswith("---")]
a = [x[1:] for x in d if x.startswith("+") and not x.startswith("+++")]
good = 1 <= len(a) <= 4 and len(r) == 0 and all("admin_people_access" in x for x in a) and any("import admin_people_access" in x for x in a) and any("*admin_people_access.routes" in x for x in a)
ok = ok and good
print("app/admin_api.py against the pin: %d removed, %d added (want 0 removed, 2 to 4 added, each naming admin_people_access, the import and the routes entry): %s" % (len(r), len(a), "ok" if good else "NO"))
mod = subprocess.run(["git", "rev-parse", "HEAD:infra/aws/ec2/opal-gateway/app/admin_people_access.py"], capture_output=True).stdout.decode().strip()
cur = subprocess.run(["git", "hash-object", G + "/app/admin_people_access.py"], capture_output=True).stdout.decode().strip()
good = bool(mod) and mod == cur
ok = ok and good
print("app/admin_people_access.py byte-equal to HEAD: %s" % ("ok" if good else "NO"))
try:
    n = len(re.findall(r"(?m)^def test_", open(G + "/tests/test_og_mp1.py", encoding="utf-8").read()))
except Exception:
    n = 0
good = n >= 3
ok = ok and good
print("tests/test_og_mp1.py: %d test functions (want 3 or more): %s" % (n, "ok" if good else "NO"))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
