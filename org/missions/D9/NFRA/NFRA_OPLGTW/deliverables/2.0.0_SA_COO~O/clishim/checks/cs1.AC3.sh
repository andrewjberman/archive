#!/usr/bin/env bash
# OPLGTW OG-cs-1 AC3 (cli-shim workstream, wave 1): the cell's footprint and the tests around it.
# (a) the files that differ from HEAD under the gateway folder are exactly: app/data_entitlement.py, app/folder_grant.py (new), tests/test_cs1_folder_grant.py (new) (git diff --name-only against the commit that added the order file, plus untracked, restricted to infra/aws/ec2/opal-gateway/);
# (b) the NEW tests/test_cs1_folder_grant.py has at least 10 test functions and passes 100 percent; its neighbours tests/test_og_cp1.py, tests/test_og_rt1.py and tests/test_og_ed1.py pass (gwtests; the one carried red test_ogz1_ac08 allowed).
. "$(dirname "$0")/../../r47/checks/_gwtests.sh"
res=$(python3 -I - "$(native "$GW")" <<'PYEOF'
import re, subprocess, sys
G = sys.argv[1]
ok = True
BASE = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H", "-1", "--", "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-cs-1.cli-shim-folder-grant-and-the-folder-string-parser.md"], capture_output=True).stdout.decode().strip()
names = subprocess.run(["git", "diff", "--name-only", BASE, "--", G], capture_output=True).stdout.decode().split() if BASE else []
new = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", "--", G], capture_output=True).stdout.decode().split()
touched = sorted(set(n.split("infra/aws/ec2/opal-gateway/")[-1] for n in names + new))
want = ["app/data_entitlement.py", "app/folder_grant.py", "tests/test_cs1_folder_grant.py"]
good = touched == want
ok = ok and good
print("files that differ from HEAD under the gateway folder: %s (want exactly %s): %s" % (touched, want, "ok" if good else "NO"))
try:
    n = len(re.findall(r"(?m)^def test_", open(G + "/tests/test_cs1_folder_grant.py", encoding="utf-8").read()))
except OSError:
    n = 0
good = n >= 10
ok = ok and good
print("tests/test_cs1_folder_grant.py: %d test functions (want 10 or more): %s" % (n, "ok" if good else "NO"))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
t=$(gwtests tests/test_cs1_folder_grant.py tests/test_og_cp1.py tests/test_og_rt1.py tests/test_og_ed1.py 2>&1 | tr -d '\r'); printf '%s\n' "$t" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && [ "$(printf '%s\n' "$t" | tail -1)" = "RESULT: PASS" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
