#!/usr/bin/env bash
# OA-e-7 AC1 (built, ruling I-3): the PARENT .claude/skills/teams-assist/teams-watch.py header (its first 60 lines, at
# HEAD) names its real consumers -- the D7 intake runner by path `integrations/ticketing/intake/runner.py` and the
# operator's `/teams-assist` -- and points at the Analyst's OWN watch `opal_ai/opal/agent/teams_watch/teams-watch.py`, so
# nobody reads this file as the Analyst's. BOUND (the file is LIVE PRODUCTION, imported by OPAL_D7_ticket_intake every
# 5 minutes): the module's code is UNCHANGED against the round-2 cut -- its AST with the module docstring removed is equal
# (comments are invisible to the AST), and HEAD's bytes py_compile.
. "$(dirname "$0")/_root.sh"
F=".claude/skills/teams-assist/teams-watch.py"
out=$(python - "$F" "$OA_R2_BASE" <<'EOF' 2>&1 | tr -d '\r'
import ast, subprocess, sys
f, base = sys.argv[1], sys.argv[2]
def show(ref):
    return subprocess.run(["git", "show", f"{ref}:{f}"], capture_output=True).stdout.decode("utf-8", "replace")
head, cut = show("HEAD"), show(base)
if not head or not cut:
    print("read failed: head=%d cut=%d bytes" % (len(head), len(cut))); sys.exit(0)
hdr = "\n".join(head.splitlines()[:60])
toks = ["integrations/ticketing/intake/runner.py", "/teams-assist", "opal_ai/opal/agent/teams_watch/teams-watch.py"]
named = sum(1 for t in toks if t in hdr)
def code(src):
    t = ast.parse(src)
    if t.body and isinstance(t.body[0], ast.Expr) and isinstance(getattr(t.body[0], "value", None), ast.Constant) and isinstance(t.body[0].value.value, str):
        t.body = t.body[1:]
    return ast.dump(t)
try:
    same = "yes" if code(head) == code(cut) else "no"
    compile(head, f, "exec"); comp = "yes"
except SyntaxError as e:
    same, comp = "n/a", "no (%s)" % e
print("header consumers named %d of 3; code AST equal to cut=%s; compiles=%s" % (named, same, comp))
EOF
)
echo "$out"
if printf '%s' "$out" | grep -q 'named 3 of 3; code AST equal to cut=yes; compiles=yes'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
