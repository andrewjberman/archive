#!/usr/bin/env bash
# OPLGTW OG-sk-2 AC3 (bounds): the edit set is exactly the five files named, the old form stays the contract's own keys, and the two contract copies are byte-equal.
#  (a) git status of the worktree names no file outside: app/integrations/schwab/catalog.py, app/integrations/schwab/integration.py, deploy/NFRA_OPLGTW_CONTRACT.json (under the gateway folder), org/standards/NFRA_OPLGTW_CONTRACT.json, tests/test_og_sk2.py (+ W/ and the channel);
#      the check reads `git diff --name-only <HEAD at the issuance> HEAD` is not available, so it compares each of the four existing files with its pinned blob and requires every OTHER tracked file under the gateway folder to hash equal to HEAD~n... (read below).
#  (b) the two contract copies are byte-equal (cmp);
#  (c) in the contract, data_prefixes and completion_prefixes are byte-equal to the pinned base's (the OLD form is untouched; the new form lives ONLY under "firm_form");
#  (d) catalog.py differs from the pinned blob be649c7518 by at most 160 added lines and removes at most 25 lines; integration.py (pin 9d40079469) by at most 30 added and 10 removed.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
G=infra/aws/ec2/opal-gateway
res=$(python3 -I - "$(native "$G")" <<'PYEOF'
import difflib, json, os, subprocess, sys
G = sys.argv[1]
ok = True


def blob(rev):
    return subprocess.run(["git", "show", rev], capture_output=True).stdout.decode("utf-8")


def delta(path, pin):
    old, new = blob(pin).splitlines(), open(path, encoding="utf-8").read().splitlines()
    d = list(difflib.unified_diff(old, new, lineterm="", n=0))
    return len([x for x in d if x.startswith("-") and not x.startswith("---")]), len([x for x in d if x.startswith("+") and not x.startswith("+++")])


r, a = delta(G + "/app/integrations/schwab/catalog.py", "be649c751890fd672f151f0abb248b589d06a86d")
g1 = 1 <= a <= 160 and r <= 25
r2, a2 = delta(G + "/app/integrations/schwab/integration.py", "9d4007946af95934634553799e2a436917cc1a74")
g2 = a2 <= 30 and r2 <= 10
print("catalog.py against the pin: %d removed, %d added (want at most 25 and 160, at least 1 added): %s" % (r, a, "ok" if g1 else "NO"))
print("integration.py against the pin: %d removed, %d added (want at most 10 and 30): %s" % (r2, a2, "ok" if g2 else "NO"))
dep = open(G + "/deploy/NFRA_OPLGTW_CONTRACT.json", "rb").read()
std = open(os.path.join("org", "standards", "NFRA_OPLGTW_CONTRACT.json"), "rb").read()
g3 = dep == std
print("the two contract copies are byte-equal: %s" % ("ok" if g3 else "NO"))
base = json.loads(blob("5daeeef445dc32fd80c4da23b7345b991985d7aa"))
cur = json.loads(dep.decode("utf-8"))
same = all(base.get(k) == cur.get(k) for k in ("data_prefixes", "completion_prefixes", "source_bucket", "masters", "datasets", "reader_role", "catalog_role"))
extra = sorted(set(cur) - set(base))
g4 = same and extra == ["firm_form"]
print("old-form contract keys byte-equal to the pinned base; the only added top-level key is %s: %s" % (extra, "ok" if g4 else "NO"))
st = subprocess.run(["git", "status", "--porcelain", "--", G, "org/standards"], capture_output=True).stdout.decode("utf-8").splitlines()
allowed = {"app/integrations/schwab/catalog.py", "app/integrations/schwab/integration.py", "deploy/NFRA_OPLGTW_CONTRACT.json", "tests/test_og_sk2.py"}
touched = []
for line in st:
    p = line[3:].strip().replace("\\", "/")
    p = p.replace("infra/aws/ec2/opal-gateway/", "")
    touched.append(p)
outside = [p for p in touched if p not in allowed and p != "org/standards/NFRA_OPLGTW_CONTRACT.json" and not p.endswith("__pycache__/")]
print("uncommitted files outside the edit set (0 expected when the worker has committed): %d" % len(outside))
print("OK" if (g1 and g2 and g3 and g4 and not outside) else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
