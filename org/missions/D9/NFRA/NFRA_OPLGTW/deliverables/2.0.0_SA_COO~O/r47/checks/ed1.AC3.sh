#!/usr/bin/env bash
# OPLGTW OG-ed-1 AC3 (a bound): the edit is the exemption and its two call sites, nothing more. Against the pinned blobs
#  data_entitlement.py aff1cf560f (at most 12 lines changed in all, every added line in the email-deny region: names CONSENT/consent/INTERNAL_PAGE/route_class/master admin, or is a comment),
#  server.py 9d740ed043 (exactly the one call `_email_denied(email` gains route_class and the docstring/comment naming it: at most 4 lines changed, each naming route_class or consent),
#  token_broker.py e5df633a37 (the one `email_denial(` call gains route_class: at most 4 lines changed, each naming route_class or consent).
# tests/test_og_ed1.py exists with at least 4 test functions; no other file under app/ differs from HEAD at the issuance (git status of the worktree is read by the invoker).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
G=infra/aws/ec2/opal-gateway
res=$(python3 -I - "$(native "$G")" <<'PYEOF'
import difflib, re, subprocess, sys
G = sys.argv[1]
ok = True


def delta(rel, pin):
    old = subprocess.run(["git", "show", pin], capture_output=True).stdout.decode("utf-8").splitlines()
    new = open(G + "/" + rel, encoding="utf-8").read().splitlines()
    d = list(difflib.unified_diff(old, new, lineterm="", n=0))
    return [x[1:] for x in d if x.startswith("-") and not x.startswith("---")], [x[1:] for x in d if x.startswith("+") and not x.startswith("+++")]


def check(rel, pin, limit, pat):
    global ok
    r, a = delta(rel, pin)
    n = max(len(r), len(a))
    good = 1 <= n <= limit and all(re.search(pat, x) for x in a)
    ok = ok and good
    print("%s against the pin: %d removed, %d added (want 1 to %d lines, every added line matching the exemption): %s" % (rel, len(r), len(a), limit, "ok" if good else "NO"))


PAT = r"(?i)consent|route_class|INTERNAL_PAGE|master.admin|^\s*#|^\s*$|OG-ed-1"
check("app/data_entitlement.py", "aff1cf560fba31bc231445a7ad91d1ac1229b50f", 12, PAT)
check("app/server.py", "9d740ed043e3fc7e11259657481121fa40e60e11", 4, PAT)
check("app/token_broker.py", "e5df633a372adc92adda3cbd4a74733d4d2bae0c", 4, PAT)
try:
    t = open(G + "/tests/test_og_ed1.py", encoding="utf-8").read()
    n = len(re.findall(r"(?m)^def test_", t))
except Exception:
    n = 0
good = n >= 4
ok = ok and good
print("tests/test_og_ed1.py: %d test functions (want 4 or more): %s" % (n, "ok" if good else "NO"))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
