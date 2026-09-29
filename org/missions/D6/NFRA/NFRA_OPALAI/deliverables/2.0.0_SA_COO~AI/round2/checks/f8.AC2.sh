#!/usr/bin/env bash
# OA-f-8 AC2 (wiring + bound): launcher.ps1 at ${OA_F8_REF:-HEAD} starts Claude Code from the RESOLVED path (it calls
# resolve-claude.ps1 and passes the result to Start-Process), with NO bare 'claude.exe' literal left in any Start-Process;
# the example config names the optional key `claude_exe`; both scripts PARSE; and against the local round-2 DEV
# dcececf53c the only files changed are launcher.ps1, resolve-claude.ps1 and provision/runtime.config.example.json.
. "$(dirname "$0")/_root.sh"
REF="${OA_F8_REF:-HEAD}"; BASE="dcececf53c"
L="opal/runtime/launcher.ps1"; R="opal/runtime/resolve-claude.ps1"; X="opal/runtime/provision/runtime.config.example.json"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f8ac2_$$")"; mkdir -p "$T"
git -C opal_ai show "$REF:$L" > "$T/l.ps1" 2>/dev/null; git -C opal_ai show "$REF:$R" > "$T/r.ps1" 2>/dev/null
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"
calls=$(grep -c 'resolve-claude' "$T/l.ps1")
bare=$(python - "$T/l.ps1" <<'EOF'
import re, sys
t = re.sub(r"`\r?\n\s*", " ", open(sys.argv[1], encoding="utf-8", errors="replace").read())
print(sum(1 for m in re.finditer(r"Start-Process\b[^\n]*", t) if re.search(r"['\"]claude\.exe['\"]", m.group(0))))
EOF
)
key=$(git -C opal_ai show "$REF:$X" 2>/dev/null | grep -c '"claude_exe"')
p=0; for f in l r; do e=$(timeout 40 powershell -NoProfile -Command "\$e=\$null; [void][System.Management.Automation.Language.Parser]::ParseFile('$WT\\$f.ps1',[ref]\$null,[ref]\$e); \$e.Count" 2>&1 | tr -d '\r' | tail -1); [ "$e" = 0 ] && [ -s "$T/$f.ps1" ] && p=$((p+1)); done
others=$(git -C opal_ai diff --name-only "$BASE" "$REF" 2>/dev/null | grep -v -x -F -e "$L" -e "$R" -e "$X" | grep -c .)
rm -rf "$T"
echo "opal_ai $REF: launcher calls resolve-claude=$calls; bare 'claude.exe' in Start-Process=$bare; example names claude_exe=$key; parse-clean scripts=$p of 2; other files changed vs $BASE=$others"
if [ "$calls" -ge 1 ] && [ "$bare" = 0 ] && [ "$key" -ge 1 ] && [ "$p" = 2 ] && [ "$others" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
