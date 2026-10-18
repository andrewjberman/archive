#!/usr/bin/env bash
# OPLGTW OG-en-28 AC1 (round 42): the absent_reason codes a caller can receive are documented, one line each, in the docstrings of the client_* tools in app/tools.py (what the code means and what a caller does next);
# and the edit changes no line COUNT in tools.py (the data catalog cites tools.py by line number).
# Record W/ABSENT_CODES.json = {"codes": [{"code": "...", "where": "file:line", "means": "...", "caller_does": "..."}]} (the worker's enumeration; prefix codes are written in full, e.g. no_model_assignment_49f).
# Overrides (dry-run controls only): EN28_REC_OVERRIDE, EN28_TOOLS_OVERRIDE, EN28_NUMSTAT_OVERRIDE (a "added deleted" pair).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${EN28_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~143/ABSENT_CODES.json}"
TOOLS="${EN28_TOOLS_OVERRIDE:-$GW/app/tools.py}"
[ -f "$REC" ] || { echo "ABSENT_CODES.json absent"; echo "RESULT: FAIL"; exit 1; }
ns="${EN28_NUMSTAT_OVERRIDE:-$(git log --author='0.9.0_WK_NFRA_OPLGTW~143 <' --format= --numstat -- "$TOOLS" | awk '{a+=$1; d+=$2} END {print a+0, d+0}')}"
res=$(python -I - "$(native "$REC")" "$(native "$TOOLS")" "$(native "$GW/app/client_adapter_bd49f.py")" "$(native "$GW/app/client_core.py")" "$ns" <<'PYEOF'
import ast, json, re, sys
rec, tools, adapter, core, ns = sys.argv[1:6]
d = json.load(open(rec, encoding="utf-8")); d = d.get("body", d)
codes = d.get("codes") or []
names = [c.get("code") for c in codes if isinstance(c, dict)]
# the adapter's literal codes, derived from its source (a code the worker did not list is a miss)
t = ast.parse(open(adapter, encoding="utf-8").read())
fixed = set()
for n in ast.walk(t):
    if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "_absent" and len(n.args) > 1 and isinstance(n.args[1], ast.Constant) and isinstance(n.args[1].value, str):
        fixed.add(n.args[1].value)
    if isinstance(n, ast.Dict):
        for k, v in zip(n.keys, n.values):
            if isinstance(k, ast.Constant) and k.value == "absent_reason":
                for sub in ast.walk(v):
                    if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                        fixed.add(sub.value)
fixed.add("window_read_busy")
fixed = {("no_model_assignment_49f" if c == "no_model_assignment_" else c) for c in fixed}
missing_from_rec = sorted(c for c in fixed if c not in names)
ct = ast.parse(open(core, encoding="utf-8").read())
refusals = set()
for n in ast.walk(ct):
    if isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id == "REFUSALS" for x in n.targets) and isinstance(n.value, ast.Dict):
        refusals = {k.value for k in n.value.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)}
universe = fixed | refusals
invented = sorted(c for c in names if c and c not in universe)
ts = open(tools, encoding="utf-8").read()
tt = ast.parse(ts)
docs = []
for n in ast.walk(tt):
    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("client_"):
        docs.append(ast.get_docstring(n) or "")
alldoc = "\n".join(docs)
def documented(c):
    for ln in alldoc.split("\n"):
        if c in ln and len(ln.split(c, 1)[1].strip(" :-,.;")) >= 20:
            return True
    return False
undoc = sorted(c for c in names if c and not documented(c))
a, dl = (ns.split() + ["x", "x"])[:2]
same_lines = a.isdigit() and dl.isdigit() and a == dl and int(a) > 0
ok = len(set(names)) >= 8 and not missing_from_rec and not invented and not undoc and same_lines
print("codes listed %d distinct (want 8 or more) of the %d the adapter and the core's REFUSALS table can set; adapter codes missing from the record %d (want 0); codes outside both sets %d (want 0); listed codes with no documenting line in a client_* docstring %d (want 0); tools.py lines added %s, deleted %s (want equal, above 0)" % (len(set(names)), len(universe), len(missing_from_rec), len(invented), len(undoc), a, dl))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
