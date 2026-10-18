#!/usr/bin/env bash
# OPLGTW OG-en-27 AC1 (round 42): tests/test_og_db3.py::test_ogdb3_ac03 reads the WORKTREE, not git history, so it passes in a release tree.
# The oracle: the test file and deploy-to-ec2.sh are copied into a folder that is NOT inside any git repository and the three tests run there (the old ac03 shells out to git and fails there);
# and the body of test_ogdb3_ac03 holds no `git` token. EN27_TEST_OVERRIDE points at an alternative test file (dry-run controls only).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
T="${EN27_TEST_OVERRIDE:-$GW/tests/test_og_db3.py}"; S="$GW/deploy-to-ec2.sh"
[ -f "$T" ] && [ -f "$S" ] || { echo "test file or deploy script absent"; echo "RESULT: FAIL"; exit 1; }
tmp=$(mktemp -d); mkdir -p "$tmp/opal-gateway/tests"; cp "$T" "$tmp/opal-gateway/tests/test_og_db3.py"; cp "$S" "$tmp/opal-gateway/deploy-to-ec2.sh"
ingit=no; git -C "$tmp" rev-parse --show-toplevel >/dev/null 2>&1 && ingit=yes
out=$(cd "$tmp/opal-gateway" && timeout 110 python -m pytest tests/test_og_db3.py -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_ogdb3_ac01 test_ogdb3_ac02 test_ogdb3_ac03; do printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
gitbody=$(python -I - "$(native "$T")" <<'PYEOF'
import ast, sys
src = open(sys.argv[1], encoding="utf-8").read()
fn = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == "test_ogdb3_ac03"]
print("absent" if not fn else ("git-token-in-body" if "git" in (ast.get_source_segment(src, fn[0]) or "").lower() else "none"))
PYEOF
)
gitbody=$(printf '%s' "$gitbody" | tr -d '\r')
echo "copy outside any git repository: in a repo $ingit (want no); pytest rc=$rc; the three db3 tests passed $p of 3; git tokens in the body of test_ogdb3_ac03: $gitbody (want none)"
[ "$ingit" = no ] && [ "$rc" = 0 ] && [ "$p" = 3 ] && [ "$gitbody" = none ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
