#!/usr/bin/env bash
# OPLGTW OG-en-30 AC1 (round 42): the client tools' served notes make no completeness claim the source cannot back (the CVO's row Z-S385; CLAUDE.md "a value must carry its claim").
# In the docstrings of the client_* functions in app/tools.py: (1) none of the phrases "true zero", "report zero", "zero fees" appears; (2) the no_fee_rows_in_window note names the SOURCE ("source"), says the account has no fee row there,
# says it does not establish a zero total ("total"), and carries no bare "zero" claim; (3) tools.py keeps its line count (1896; the data catalog cites it by line).
# Override (dry-run controls only): EN30_TOOLS_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
TOOLS="${EN30_TOOLS_OVERRIDE:-$GW/app/tools.py}"
[ -f "$TOOLS" ] || { echo "tools.py absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python -I - "$(native "$TOOLS")" <<'PYEOF'
import ast, sys
src = open(sys.argv[1], encoding="utf-8").read()
t = ast.parse(src)
docs = {}
for n in ast.walk(t):
    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("client_"):
        docs[n.name] = ast.get_docstring(n) or ""
alldoc = "\n".join(docs.values()).lower()
banned = [p for p in ("true zero", "report zero", "zero fees") if p in alldoc]
# the note: the sentence that begins with the code word, up to the next code-like word or the end
fee = docs.get("client_get_fees", "")
i = fee.find("no_fee_rows_in_window")
seg = fee[i:i + 600].lower() if i >= 0 else ""
for stop in ("window_read_busy", "window_required", "window_too_long", "firm_not_", "no_partition_at_as_of", "account_not_in_partition"):
    j = seg.find(stop, 25)
    if j > 0:
        seg = seg[:j]
note_ok = bool(seg) and "source" in seg and "no fee row" in seg and "total" in seg and "zero" not in seg
lines = src.count("\n")
ok = not banned and note_ok and lines == 1896
print("banned completeness phrases in the client_* docstrings: %s (want none); the no_fee_rows_in_window note names the source, says no fee row there, does not claim a total and has no bare 'zero': %s; tools.py newline count %d (want 1896)" % (banned or "none", "yes" if note_ok else "NO", lines))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
