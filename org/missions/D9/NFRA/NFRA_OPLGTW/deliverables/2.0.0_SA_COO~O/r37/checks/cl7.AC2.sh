#!/usr/bin/env bash
# OPLGTW OG-cl-7 AC2 (round-37 G2-BUILD): the naming gate in ENFORCE over every client module added WHOLE prints no REFUSE, and no module holds a hand-kept firm-name literal outside a lookup(...) call.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
D=$(mktemp -d); : > "$D/all.diff"
files=$(ls "$GW"/app/client_*.py 2>/dev/null)
[ -n "$files" ] || { echo "no client modules"; echo "RESULT: FAIL"; exit 1; }
for f in $files; do git diff --no-index --no-color /dev/null "$f" >> "$D/all.diff" 2>/dev/null; done
printf 'org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/x.json\n' > "$D/paths.txt"
for f in $files; do printf '%s\n' "$f" >> "$D/paths.txt"; done
timeout 115 python .tools/naming-gate.py --diff "$D/all.diff" --staged-paths "$D/paths.txt" --enforce > "$D/gate.out" 2>&1; grc=$?
refuse=$(grep -c "NAMING REFUSE" "$D/gate.out")
lits=$(python - $files <<'PYEOF'
import ast, sys
FIRMS = ("49financial", "cottonwood", "inflection")
bad = 0
for f in sys.argv[1:]:
    t = ast.parse(open(f, encoding="utf-8").read())
    inside = set()
    for n in ast.walk(t):
        if isinstance(n, ast.Call) and getattr(n.func, "id", getattr(n.func, "attr", "")) == "lookup":
            for a in ast.walk(n):
                inside.add(id(a))
    for n in ast.walk(t):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value in FIRMS and id(n) not in inside:
            bad += 1
print(bad)
PYEOF
)
lits=$(printf '%s' "$lits" | tr -d '\r')
echo "naming gate over the client modules in ENFORCE: rc=$grc; REFUSE verdicts $refuse (want 0); hand-kept firm literals $lits (want 0)"
rm -rf "$D"
[ "$grc" = 0 ] && [ "$refuse" = 0 ] && [ "$lits" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
