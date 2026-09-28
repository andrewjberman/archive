#!/usr/bin/env bash
# OA-f-4 AC1 (built, CTO ruling msg 26260): at opal_ai ${OA_NESTED_REF:-HEAD}, verify-boundary.ps1 uses NO WinRM
# remoting (0 Invoke-Command, 0 -ComputerName), runs its arms with Start-Process carrying -Credential, -Wait and
# -WorkingDirectory (>=2 such calls), still PARSES (0 errors), and against the cut fd8ab8a57f only that one file changed.
. "$(dirname "$0")/_root.sh"
REF="${OA_NESTED_REF:-HEAD}"
F="opal/runtime/provision/verify-boundary.ps1"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f4ac1_$$")"; mkdir -p "$T"
git -C opal_ai show "$REF:$F" > "$T/v.ps1" 2>/dev/null
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"
ic=$(grep -ciE 'Invoke-Command|-ComputerName' "$T/v.ps1")
sp=$(python - "$T/v.ps1" <<'EOF'
import re, sys
t = open(sys.argv[1], encoding="utf-8", errors="replace").read()
# join PowerShell backtick continuations so one Start-Process call reads as one statement
t = re.sub(r"`\r?\n\s*", " ", t)
n = 0
for m in re.finditer(r"Start-Process\b[^\n]*", t):
    s = m.group(0)
    if "-Credential" in s and "-Wait" in s and "-WorkingDirectory" in s:
        n += 1
print(n)
EOF
)
perr=$(timeout 40 powershell -NoProfile -Command "\$e=\$null; [void][System.Management.Automation.Language.Parser]::ParseFile('$WT\\v.ps1',[ref]\$null,[ref]\$e); \$e.Count" 2>&1 | tr -d '\r' | tail -1)
others=$(git -C opal_ai diff --name-only "$OA_NESTED_PIN" "$REF" 2>/dev/null | grep -v -x -F "$F" | grep -c .)
rm -rf "$T"
echo "opal_ai $REF: Invoke-Command/ComputerName=$ic; Start-Process with -Credential -Wait -WorkingDirectory=$sp; parse errors=${perr:-none}; other files changed vs $OA_NESTED_PIN=$others"
if [ "$ic" = 0 ] && [ "${sp:-0}" -ge 2 ] && [ "$perr" = 0 ] && [ "$others" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
