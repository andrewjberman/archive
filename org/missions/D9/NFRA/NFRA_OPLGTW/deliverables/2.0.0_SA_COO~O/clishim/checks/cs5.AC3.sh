#!/usr/bin/env bash
# OPLGTW OG-cs-5 AC3 (a bound and the neighbours): the edit is the carry and nothing more, and the tests around it still pass.
# (a) app/admin_people_access.py against the pinned blob 65f9faa4a9 (HEAD at the cut): at most 14 lines added and 6 removed in all, no other file under app/ differs from HEAD (git diff --name-only against the commit that added the order file names only admin_people_access.py under app/);
# (b) the NEW tests/test_cs5_widening_confirm.py has at least 4 test functions and passes 100 percent, and its neighbours tests/test_admin_people_access.py and tests/test_og_mp1.py pass (gwtests; the one carried red test_ogz1_ac08 allowed).
. "$(dirname "$0")/../../r47/checks/_gwtests.sh"
res=$(python3 -I - "$(native "$GW")" <<'PYEOF'
import difflib, re, subprocess, sys
G = sys.argv[1]
ok = True
old = subprocess.run(["git", "show", "65f9faa4a988910d61edb4aabeab4a605560afd4"], capture_output=True).stdout.decode("utf-8").splitlines()
try:
    new = open(G + "/app/admin_people_access.py", encoding="utf-8").read().splitlines()
except OSError:
    new = []
d = list(difflib.unified_diff(old, new, lineterm="", n=0))
r = [x for x in d if x.startswith("-") and not x.startswith("---")]
a = [x for x in d if x.startswith("+") and not x.startswith("+++")]
good = bool(new) and len(a) <= 14 and len(r) <= 6 and len(a) >= 3
ok = ok and good
print("app/admin_people_access.py against the pin: %d added, %d removed (want 3 to 14 added, at most 6 removed): %s" % (len(a), len(r), "ok" if good else "NO"))
BASE = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H", "-1", "--", "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-cs-5.cli-shim-the-access-post-carries-widening-confirm.md"], capture_output=True).stdout.decode().strip()
names = subprocess.run(["git", "diff", "--name-only", BASE, "--", G + "/app/"], capture_output=True).stdout.decode().split() if BASE else []
st = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", "--", G + "/app/"], capture_output=True).stdout.decode().split()
touched = sorted(set(n.split("/")[-1] for n in names + st))
good = touched == ["admin_people_access.py"]
ok = ok and good
print("files under app/ that differ from HEAD: %s (want admin_people_access.py alone): %s" % (touched, "ok" if good else "NO"))
try:
    n = len(re.findall(r"(?m)^def test_", open(G + "/tests/test_cs5_widening_confirm.py", encoding="utf-8").read()))
except OSError:
    n = 0
good = n >= 4
ok = ok and good
print("tests/test_cs5_widening_confirm.py: %d test functions (want 4 or more): %s" % (n, "ok" if good else "NO"))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
t=$(gwtests tests/test_cs5_widening_confirm.py tests/test_admin_people_access.py tests/test_og_mp1.py 2>&1 | tr -d '\r'); printf '%s\n' "$t" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && [ "$(printf '%s\n' "$t" | tail -1)" = "RESULT: PASS" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
