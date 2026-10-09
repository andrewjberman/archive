#!/usr/bin/env bash
# OA-f-9 AC5 (amendment A3, row Z-S64): the Analyst's first prompt reaches claude as a PROMPT, not as an --add-dir value.
# claude 2.1.295's --add-dir is variadic (<directories...>), so a prompt placed right after it is swallowed as a second
# directory; AC4 graded that defective shape. AC5 supersedes AC4.
# String arm: the launcher's own `$analystCmd = ...` line, evaluated with stub values, must END
#   --add-dir '<refs>' -- '<prompt>'   (prompt names "On launch", no double quote: it rides inside -Command "...").
# CLI arm (the installed claude, same version as the Analyst's): control `-p --add-dir <d> <prompt>` must refuse
#   ("Input must be provided"), fix `-p --add-dir <d> -- <prompt>` must answer PONG. Two small API calls.
# Bounds: the file parses; the ARGLEN guard and both Process.Start launches stay; only launcher.ps1 differs from 8cdc7b9.
. "$(dirname "$0")/_root.sh"
REF="${OA_F9A3_REF:-HEAD}"; BASE="8cdc7b9735"
L="opal/runtime/launcher.ps1"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f9ac5_$$")"; mkdir -p "$T"
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
if ($rest -match "^ -- '([^']+)'$") { $p = $Matches[1]; 'BUILT: separator=yes prompt=' + ($(if ($p -match 'On launch') {'on-launch'} else {'other'})) + ' dq=' + ([int]$p.Contains('"')) }
elseif ($rest -match "^ '([^']+)'$") { 'BUILT: separator=no' } else { 'BUILT: no-prompt' }
PS
built=$(timeout 60 powershell -NoProfile -ExecutionPolicy Bypass -File "$WT\\eval.ps1" -LineFile "$WT\\line.ps1" 2>&1 | tr -d '\r' | grep '^BUILT:' | tail -1)
perr=$(timeout 60 powershell -NoProfile -Command "\$e=\$null; [void][System.Management.Automation.Language.Parser]::ParseFile('$WT\\l.ps1',[ref]\$null,[ref]\$e); \$e.Count" 2>&1 | tr -d '\r' | tail -1)
argl=$(grep -c 'LAUNCHER: REFUSE ARGLEN' "$T/l.ps1"); pst=$(grep -c 'Diagnostics.Process\]::Start' "$T/l.ps1")
other=$(git -C opal_ai diff --name-only "$BASE" "$REF" 2>/dev/null | grep -v -x "$L" | grep -c .)
mkdir -p "$T/d"; PR="Reply with exactly the word PONG and nothing else."
ctl=$(cd "$T" && timeout 120 claude -p --add-dir "$T/d" "$PR" < /dev/null 2>&1 | tr -d '\r')
fix=$(cd "$T" && timeout 120 claude -p --add-dir "$T/d" -- "$PR" < /dev/null 2>&1 | tr -d '\r')
cv=$(claude --version 2>&1 | head -1 | tr -d '\r')
cr=no; printf '%s' "$ctl" | grep -q 'Input must be provided' && cr=yes
fp=no; printf '%s' "$fix" | grep -q -x 'PONG' && fp=yes
rm -rf "$T"
echo "opal_ai $REF: ${built:-BUILT: unreadable}; parse errors=${perr:-?}; ARGLEN guard=$argl; Process.Start=$pst; other files changed vs $BASE=$other; cli ($cv): control refused=$cr, separator answered PONG=$fp"
if [ "$built" = "BUILT: separator=yes prompt=on-launch dq=0" ] && [ "$perr" = 0 ] && [ "$argl" -ge 1 ] && [ "$pst" -ge 2 ] && [ "$other" = 0 ] && [ "$cr" = yes ] && [ "$fp" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
