#!/usr/bin/env bash
# OPLGTW cli-shim footprint check (shared by every cli-shim code cell). The cell's footprint and the tests around it.
#   cs_foot.sh <order-file> <files> <new-test-file> <min-tests> <neighbour>...
#   <files> is a comma list of paths RELATIVE to infra/aws/ec2/opal-gateway/ that the cell may write (the cell's whole footprint, tests included).
# (a) the files that differ from the commit that added <order-file> (committed, uncommitted and untracked, restricted to the gateway folder) are exactly <files>;
# (b) <new-test-file> has at least <min-tests> test functions and passes 100 percent, and every <neighbour> test file passes (gwtests; the one carried red test_ogz1_ac08 allowed).
. "$(dirname "$0")/../../r47/checks/_gwtests.sh"
ORDER="$1"; FILES="$2"; NEWT="$3"; MINT="$4"; shift 4
res=$(python3 -I - "$(native "$GW")" "$ORDER" "$FILES" "$NEWT" "$MINT" <<'PYEOF'
import re, subprocess, sys
G, ORDER, FILES, NEWT, MINT = sys.argv[1:6]
ok = True
BASE = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H", "-1", "--", ORDER], capture_output=True).stdout.decode().strip()
names = subprocess.run(["git", "diff", "--name-only", BASE, "--", G], capture_output=True).stdout.decode().split() if BASE else []
new = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", "--", G], capture_output=True).stdout.decode().split()
touched = sorted(set(n.split("infra/aws/ec2/opal-gateway/")[-1] for n in names + new))
want = sorted(FILES.split(","))
good = bool(BASE) and touched == want
ok = ok and good
print("files that differ from HEAD under the gateway folder: %s (want exactly %s): %s" % (touched, want, "ok" if good else "NO"))
try:
    n = len(re.findall(r"(?m)^def test_", open(G + "/" + NEWT, encoding="utf-8").read()))
except OSError:
    n = 0
good = n >= int(MINT)
ok = ok and good
print("%s: %d test functions (want %s or more): %s" % (NEWT, n, MINT, "ok" if good else "NO"))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
t=$(gwtests "$NEWT" "$@" 2>&1 | tr -d '\r'); printf '%s\n' "$t" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && [ "$(printf '%s\n' "$t" | tail -1)" = "RESULT: PASS" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
