#!/usr/bin/env bash
# OPLGTW OG-cd-2 AC2 (round 46): the mount is the SMALLEST change. app/admin_api.py differs from its base blob (c1885ec0404f45714616addeec961923ff549ed0) by exactly TWO ADDED lines and no removed line:
# `from . import family_depth` and ONE Route line for "/gateway/families" (GET) whose endpoint is owner_only(family_depth.families) (the module's handler is not decorated; the gate is added here).
# Override (dry-run controls only): CD2_BASE_OVERRIDE, CD2_FILE_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
BASE="${CD2_BASE_OVERRIDE:-c1885ec0404f45714616addeec961923ff549ed0}"
F="${CD2_FILE_OVERRIDE:-$GW/app/admin_api.py}"
git cat-file -e "$BASE" 2>/dev/null || { echo "base blob $BASE not in this repository"; echo "RESULT: FAIL"; exit 1; }
git cat-file -p "$BASE" > "${TMPDIR:-/tmp}/cd2_base_admin_api.py"
res=$(python -I - "$(native "${TMPDIR:-/tmp}/cd2_base_admin_api.py")" "$(native "$F")" <<'PYEOF'
import difflib, re, sys
a = open(sys.argv[1], encoding="utf-8").read().splitlines()
b = open(sys.argv[2], encoding="utf-8").read().splitlines()
added, removed = [], []
for l in difflib.unified_diff(a, b, lineterm="", n=0):
    if l.startswith(("+++", "---", "@@")):
        continue
    (added if l.startswith("+") else removed).append(l[1:])
imp = [l for l in added if re.fullmatch(r"\s*from \. import family_depth\s*", l)]
rt = [l for l in added if re.fullmatch(r'\s*Route\("/gateway/families",\s*owner_only\(family_depth\.families\),\s*methods=\["GET"\]\),?\s*', l)]
ok = len(added) == 2 and len(removed) == 0 and len(imp) == 1 and len(rt) == 1
print("added lines %d (want 2), removed lines %d (want 0); import line %d (want 1); owner-gated Route line %d (want 1)" % (len(added), len(removed), len(imp), len(rt)))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
