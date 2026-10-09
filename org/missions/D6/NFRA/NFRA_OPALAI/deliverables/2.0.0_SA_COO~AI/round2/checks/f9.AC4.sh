#!/usr/bin/env bash
# OA-f-9 AC4 (amendment A2, row Z-S63): launcher.ps1 at ${OA_F9A2_REF:-HEAD} starts the Analyst WITH a first prompt, so
# prompt.md's "On launch" steps (identity gate, Teams engine arm) run unattended instead of the window idling at input.
# Behaviour arm: the launcher's own `$analystCmd = ...` line is evaluated with stub values, and the built command must end
#   --add-dir '<refs>' '<prompt>'  with the prompt naming "On launch" and carrying no double quote (the outer -Command "...").
# Bounds: the file parses; the ARGLEN guard and Process.Start launch stay; only launcher.ps1 differs from de5ce25fa3.
. "$(dirname "$0")/_root.sh"
REF="${OA_F9A2_REF:-HEAD}"; BASE="de5ce25fa3"
L="opal/runtime/launcher.ps1"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f9ac4_$$")"; mkdir -p "$T"
git -C opal_ai show "$REF:$L" > "$T/l.ps1" 2>/dev/null || { echo "launcher.ps1 absent at $REF"; rm -rf "$T"; echo "RESULT: FAIL"; exit 1; }
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"
grep -E '^\$analystCmd = ' "$T/l.ps1" | head -1 > "$T/line.ps1"
cat > "$T/eval.ps1" <<'PS'
param([string]$LineFile)
$q = [string][char]39
$Config = 'C:\cfg\runtime.config.json'; $claudeExe = 'C:\bin\claude.exe'; $refsDir = 'C:\rt\opal\agent\refs'
. ([scriptblock]::Create((Get-Content -Raw -LiteralPath $LineFile)))
$tail = ' --add-dir ' + $q + $refsDir + $q
$i = $analystCmd.IndexOf($tail)
if ($i -lt 0) { 'BUILT: no-add-dir'; exit 0 }
$rest = $analystCmd.Substring($i + $tail.Length)
if ($rest -match "^ '([^']+)'$") { $p = $Matches[1]; 'BUILT: prompt=' + ($(if ($p -match 'On launch') {'on-launch'} else {'other'})) + ' dq=' + ([int]$p.Contains('"')) } else { 'BUILT: no-prompt' }
PS
built=$(timeout 60 powershell -NoProfile -ExecutionPolicy Bypass -File "$WT\\eval.ps1" -LineFile "$WT\\line.ps1" 2>&1 | tr -d '\r' | grep '^BUILT:' | tail -1)
perr=$(timeout 60 powershell -NoProfile -Command "\$e=\$null; [void][System.Management.Automation.Language.Parser]::ParseFile('$WT\\l.ps1',[ref]\$null,[ref]\$e); \$e.Count" 2>&1 | tr -d '\r' | tail -1)
argl=$(grep -c 'LAUNCHER: REFUSE ARGLEN' "$T/l.ps1"); pst=$(grep -c 'Diagnostics.Process\]::Start' "$T/l.ps1")
other=$(git -C opal_ai diff --name-only "$BASE" "$REF" 2>/dev/null | grep -v -x "$L" | grep -c .)
rm -rf "$T"
echo "opal_ai $REF: ${built:-BUILT: unreadable}; parse errors=${perr:-?}; ARGLEN guard=$argl; Process.Start=$pst; other files changed vs $BASE=$other"
if [ "$built" = "BUILT: prompt=on-launch dq=0" ] && [ "$perr" = 0 ] && [ "$argl" -ge 1 ] && [ "$pst" -ge 2 ] && [ "$other" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
