#!/usr/bin/env bash
# OPLGTW OG-en-34 AC1 (round 44; candidates item 12, the CVO's finding on OG-ap-44): app/probe_listener.py says "The probe still writes no access line of its own." Row Z-S397 measured the opposite: with the service's handlers restored, uvicorn logs the
# listener's requests too (h11_impl.py:57 and httptools_impl.py:61 gate on access_logger.hasHandlers()). The comment is corrected and NOTHING ELSE changes.
# Base blob (the file at the issuance, git rev-parse HEAD:<path>): 85ce5027cc8bd84dc93aa00bc71130e2c09c0795.
#  - the file differs from the base blob in at most 3 lines, every changed line (either side) is a comment line (starts with # after trimming);
#  - the AST of the file equals the AST of the base blob (no code or docstring change);
#  - the stale sentence is gone ("writes no access line") and the new comment names hasHandlers.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="$GW/app/probe_listener.py"
BASE="${EN34_BASE_OVERRIDE:-85ce5027cc8bd84dc93aa00bc71130e2c09c0795}"
git cat-file -e "$BASE" 2>/dev/null || { echo "base blob $BASE not in this repository"; echo "RESULT: FAIL"; exit 1; }
git cat-file -p "$BASE" > "${TMPDIR:-/tmp}/en34_base_probe_listener.py"
res=$(python -I - "$(native "${TMPDIR:-/tmp}/en34_base_probe_listener.py")" "$(native "$F")" <<'PYEOF'
import ast, difflib, sys
a = open(sys.argv[1], encoding="utf-8").read(); b = open(sys.argv[2], encoding="utf-8").read()
al = a.splitlines(); bl = b.splitlines()
changed = [l[2:] for l in difflib.ndiff(al, bl) if l[:2] in ("- ", "+ ")]
comment_only = all(x.strip().startswith("#") for x in changed)
ast_eq = ast.dump(ast.parse(a)) == ast.dump(ast.parse(b))
stale_gone = "writes no access line" not in b
names_has = "hasHandlers" in b
ok = 0 < len(changed) <= 3 + 3 and comment_only and ast_eq and stale_gone and names_has
print("changed lines (either side) %d (want 1 to 6, i.e. at most 3 replaced); every changed line is a comment %s; AST equal to the base blob %s; the stale sentence gone %s; the new comment names hasHandlers %s" % (
      len(changed), "yes" if comment_only else "NO", "yes" if ast_eq else "NO", "yes" if stale_gone else "NO", "yes" if names_has else "NO"))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
