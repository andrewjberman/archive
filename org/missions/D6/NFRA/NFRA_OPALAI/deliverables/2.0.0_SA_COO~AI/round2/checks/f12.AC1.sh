#!/usr/bin/env bash
# OA-f-12 AC1 (built): opal_ai/opal/runtime/resolve-claude.ps1 at ${OA_F12_REF:-HEAD} resolves a configured claude_exe the
# NON-ELEVATED operator cannot see into (Opal_Agent's own profile) instead of throwing. Arms, run non-elevated:
#   seam   claude_exe = the REAL configured path (read from C:\opal_runtime\runtime.config.json; this token gets
#          'Access is denied' on it) -> 'CLAUDE_EXE: <that path>', exit 0, and no 'Access is denied' text in the output
#   miss   claude_exe = a missing path in a READABLE scratch dir, PATH without claude -> 'LAUNCHER: REFUSE CLAUDE-NOT-FOUND', exit 5
#   found  claude_exe = an existing readable scratch file -> 'CLAUDE_EXE: <that file>', exit 0
#   bound  parses; vs r2-dev 0fb3fcb694 the only file changed is resolve-claude.ps1
. "$(dirname "$0")/_root.sh"
REF="${OA_F12_REF:-HEAD}"; BASE="0fb3fcb694"; F="opal/runtime/resolve-claude.ps1"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f12ac1_$$")"; mkdir -p "$T"
git -C opal_ai show "$REF:$F" > "$T/r.ps1" 2>/dev/null || { echo "resolve-claude.ps1 absent at $REF"; rm -rf "$T"; echo "RESULT: FAIL"; exit 1; }
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"
real=$(timeout 30 powershell -NoProfile -Command "(Get-Content 'C:\\opal_runtime\\runtime.config.json' -Raw | ConvertFrom-Json).claude_exe" 2>&1 | tr -d '\r' | tail -1)
printf 'stub\n' > "$T/fake-claude.exe"
python - "$T" "$WT" "$real" <<'PY'
import json, sys, os
t, wt, real = sys.argv[1:4]
base = {"checkout_dir": "X", "state_dir": "X", "workspace_probe_file": "X", "prod_ref": "PROD"}
json.dump(dict(base, claude_exe=real), open(os.path.join(t, "cs.json"), "w"))
json.dump(dict(base, claude_exe=wt + "\\no-such-claude.exe"), open(os.path.join(t, "cm.json"), "w"))
json.dump(dict(base, claude_exe=wt + "\\fake-claude.exe"), open(os.path.join(t, "cf.json"), "w"))
PY
run() { timeout 40 powershell -NoProfile -ExecutionPolicy Bypass -Command "\$env:PATH='C:\\Windows\\System32'; & '$WT\\r.ps1' -Config '$WT\\$1'; exit \$LASTEXITCODE" 2>&1 | tr -d '\r'; }
rc() { timeout 40 powershell -NoProfile -ExecutionPolicy Bypass -Command "\$env:PATH='C:\\Windows\\System32'; & '$WT\\r.ps1' -Config '$WT\\$1' | Out-Null; exit \$LASTEXITCODE" >/dev/null 2>&1; echo $?; }
os=$(run cs.json); cs=$(rc cs.json); om=$(run cm.json); cm=$(rc cm.json); of=$(run cf.json); cf=$(rc cf.json)
sline=$(printf '%s\n' "$os" | grep -m1 '^CLAUDE_EXE:'); denied=$(printf '%s\n' "$os" | grep -ci 'access is denied')
pe=$(timeout 40 powershell -NoProfile -Command "\$e=\$null; [void][System.Management.Automation.Language.Parser]::ParseFile('$WT\\r.ps1',[ref]\$null,[ref]\$e); \$e.Count" 2>&1 | tr -d '\r' | tail -1)
others=$(git -C opal_ai diff --name-only "$BASE" "$REF" 2>/dev/null | grep -v -x -F -e "$F" | grep -c .)
rm -rf "$T"
echo "opal_ai $REF: seam '${sline:-none}' rc=$cs access-denied text=$denied; miss '$(printf '%s\n' "$om" | grep -m1 'LAUNCHER: REFUSE' || echo none)' rc=$cm; found '$(printf '%s\n' "$of" | grep -m1 '^CLAUDE_EXE:' || echo none)' rc=$cf; parse errors=$pe; other files changed vs $BASE=$others"
if printf '%s' "$sline" | grep -qiF "$real" && [ "$cs" = 0 ] && [ "$denied" = 0 ] \
   && printf '%s' "$om" | grep -q 'LAUNCHER: REFUSE CLAUDE-NOT-FOUND' && [ "$cm" = 5 ] \
   && printf '%s' "$of" | grep -q 'fake-claude.exe' && [ "$cf" = 0 ] && [ "$pe" = 0 ] && [ "$others" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
