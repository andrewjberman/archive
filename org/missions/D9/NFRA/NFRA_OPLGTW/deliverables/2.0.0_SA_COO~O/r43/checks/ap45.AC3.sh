#!/usr/bin/env bash
# OPLGTW OG-ap-45 AC3 (round 42; the CTO's criterion, msg 35632): after the landing, the gateway app/ is AST-equal to the LIVE release plus trunk's own changes, and those changes are LISTED.
# For every .py under infra/aws/ec2/opal-gateway/app/ in the live release (4257a2aa42 unless the record names another `live_sha`) and in the merge: equal; equal once docstrings are blanked (doc-only difference); or CODE-different.
# Every CODE-different file must be named in the record's `trunk_own_changes` (a list of {"path", "why"}); tools.py is never allowed there (it is code-equal to live by the release's own proof).
# Override (dry-run controls only): AP45_REC_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${AP45_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/ap45_landing.json}"
[ -f "$REC" ] || { echo "ap45_landing.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python -I - "$(native "$REC")" <<'PYEOF'
import ast, json, subprocess, sys
GW = "infra/aws/ec2/opal-gateway/app/"
rec = json.load(open(sys.argv[1], encoding="utf-8"))
merge = rec.get("merge_sha", "")
live = rec.get("live_sha") or "eff517546eeea48811cf13f3de38926c5944c6df"
def files(rev):
    out = subprocess.run(["git", "ls-tree", "-r", "--name-only", rev, GW], capture_output=True).stdout.decode("utf-8", "replace")
    return sorted(p for p in out.splitlines() if p.endswith(".py"))
def blob(rev, p):
    r = subprocess.run(["git", "show", "%s:%s" % (rev, p)], capture_output=True)
    return r.stdout if r.returncode == 0 else None
def stripped(b):
    t = ast.parse(b.decode("utf-8", "replace"))
    for n in ast.walk(t):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)) and n.body and isinstance(n.body[0], ast.Expr) and isinstance(getattr(n.body[0], "value", None), ast.Constant) and isinstance(n.body[0].value.value, str):
            n.body[0].value.value = ""
    return ast.dump(t)
fl, fm = files(live), files(merge)
allp = sorted(set(fl) | set(fm))
equal = doc_only = 0
code_diff, only_one = [], []
for p in allp:
    a, b = blob(live, p), blob(merge, p)
    if a is None or b is None:
        only_one.append(p); continue
    if a == b:
        equal += 1
    else:
        try:
            if stripped(a) == stripped(b):
                doc_only += 1
            else:
                code_diff.append(p)
        except SyntaxError:
            code_diff.append(p)
listed = {c.get("path") for c in (rec.get("trunk_own_changes") or []) if isinstance(c, dict) and c.get("path") and c.get("why")}
named = set(code_diff) | set(only_one)
unlisted = sorted(named - listed)
tools_bad = (GW + "tools.py") in named
print("app/ python files compared live %s against the merge: %d; equal %d; docstring-only differences %d; code-different %d; present on one side only %d" % (live[:10], len(allp), equal, doc_only, len(code_diff), len(only_one)))
print("trunk's own changes listed in the record: %d of %d code-different or one-sided files unlisted %d (want 0); tools.py code-equal to live: %s" % (len(named & listed), len(named), len(unlisted), "no" if tools_bad else "yes"))
print("the files that are code-different or one-sided: %s" % (", ".join(sorted(p.replace(GW, "") for p in named)) or "none"))
print("OK" if (not unlisted and not tools_bad and len(allp) > 50) else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
