#!/usr/bin/env bash
# F6-AC4 -- THE REFUSAL NAMES THE SERVED SOURCE, AND THE TOOL RUNS WITH NO STORE ANYWHERE.
#
# comp_debt.py is READ ONLY here -- it is out of this order's grant (slot ~2 holds
# it concurrently under TO-CG-F-11). This probe prints its remaining refusal text
# and runs it; it edits nothing.
#
# The refusal test is done TWICE with two different instruments, because a grep
# over a file is text-local and could match a comment three functions away:
#   (1) the SOURCE LINES 133-137 printed verbatim with line numbers, and
#   (2) an AST read of the SystemExit argument inside _stitch/served refusal --
#       the actual string the tool would raise, assembled from its parts.
#
# The RUN is the C-S33 control that did not happen: with the local stitch store
# deleted, comp-debt either returns 0 or crashes. rc is printed, never inferred.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~7
TOOL=infra/aws/globgrph/comp_debt.py
W=C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph
PY=${PYTHON:-python}

echo "=== f6_refusal_and_run.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo "TOOL=$TOOL (READ ONLY -- out of this order's grant; F-11 holds it)"
echo

echo "--- INSTRUMENT 1: THE SOURCE LINES 133-137, VERBATIM, WITH LINE NUMBERS ---"
cat -n "$TOOL" | sed -n '132,142p'
echo

echo "--- INSTRUMENT 2: THE RAISED STRING, ASSEMBLED BY AN AST READ (not a grep) ---"
NAMED=$("$PY" - "$TOOL" <<'PYEOF'
import ast, sys
src = open(sys.argv[1], encoding="utf-8").read()
tree = ast.parse(src)
found = []
for node in ast.walk(tree):
    if not isinstance(node, ast.Raise):
        continue
    exc = node.exc
    if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name) and exc.func.id == "SystemExit":
        if not exc.args:
            continue
        a = exc.args[0]
        # a BinOp %-format or a bare joined string constant
        while isinstance(a, ast.BinOp):
            a = a.left
        if isinstance(a, ast.Constant) and isinstance(a.value, str):
            found.append((node.lineno, a.value))
hit = False
for line, text in found:
    if "REFUSE" in text and "served" in text:
        print("REFUSAL AT LINE %d, AS THE TOOL WOULD RAISE IT:" % line)
        for ln in text.rstrip("\n").split("\n"):
            print("    | %s" % ln)
        low = text.lower()
        names_stitch = ("stitch" in low)
        names_served = ("served" in low)
        names_no_local = ("no local database" in low)
        print("    names 'served'=%s  names 'stitch'=%s  names 'no local database'=%s"
              % (names_served, names_stitch, names_no_local))
        if names_served and names_stitch:
            hit = True
print("REFUSALS_FOUND=%d" % len(found))
print("REFUSAL_NAMES_SERVED_STITCH=%s" % ("true" if hit else "false"))
PYEOF
)
echo "$NAMED"
echo

echo "--- NEGATIVE CONTROL: the same AST reader on a refusal that names NO source ---"
"$PY" - <<'PYEOF'
import ast
mutant = (
    'def f():\n'
    '    try:\n'
    '        h = health()\n'
    '    except Exception as ex:\n'
    '        raise SystemExit("REFUSE: the graph is unreachable (%s)." % ex) from ex\n')
tree = ast.parse(mutant)
found = []
for node in ast.walk(tree):
    if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call):
        a = node.exc.args[0]
        while isinstance(a, ast.BinOp):
            a = a.left
        if isinstance(a, ast.Constant):
            found.append(a.value)
hit = any("REFUSE" in t and "served" in t and "stitch" in t.lower() for t in found)
print("  mutant refusal text: %r" % (found[0] if found else None))
print("  REFUSAL_PROBE_CONTROL=%s" % ("FIRED (the unnamed refusal was NOT scored true)"
                                      if not hit else "DEAD (the unnamed refusal scored true)"))
PYEOF
echo

echo "--- NO STORE ANYWHERE (the precondition of the run below) ---"
for p in "$W/kuzu_stitch_db" "$W/kuzu_stitch_db._build_manifest.json" "$W/stitch_graph.json" \
         infra/aws/globgrph/kuzu_stitch_db; do
  if ls -d "$p"; then echo "  -> PRESENT $p"; else echo "  -> ABSENT $p"; fi
done
echo

echo "--- THE RUN: comp-debt FROM THIS WORKTREE, NO LOCAL STORE (there is no .tools/comp-debt shim -- S88) ---"
"$PY" "$TOOL"
RC=$?
echo
echo "--- F6-AC4 VERDICT LINES ---"
echo "$NAMED" | grep '^REFUSAL_NAMES_SERVED_STITCH='
echo "COMP_DEBT_RC_WITHOUT_STORE=$RC"
echo "=== f6_refusal_and_run.sh END ==="
