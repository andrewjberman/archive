#!/usr/bin/env bash
# OA-f-5 AC1 (built): at opal_ai ${OA_NESTED_REF:-HEAD}, launcher.ps1's gate launch (the Start-Process that runs
# launch-gate.ps1 AS Opal_Agent) carries -WorkingDirectory, as its claude.exe launch already does -- without it the child
# inherits the operator's current directory, which Opal_Agent cannot enter ("The directory name is invalid", measured by
# the issuer 2026-09-28). Every Start-Process -Credential in the file carries -WorkingDirectory; the file PARSES; and
# against the cut fd8ab8a57f only launcher.ps1 changed.
. "$(dirname "$0")/_root.sh"
REF="${OA_NESTED_REF:-HEAD}"
F="opal/runtime/launcher.ps1"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f5ac1_$$")"; mkdir -p "$T"
git -C opal_ai show "$REF:$F" > "$T/l.ps1" 2>/dev/null
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"
counts=$(python - "$T/l.ps1" <<'EOF'
import re, sys
t = open(sys.argv[1], encoding="utf-8", errors="replace").read()
t = re.sub(r"`\r?\n\s*", " ", t)
calls = [m.group(0) for m in re.finditer(r"Start-Process\b[^\n]*", t) if "-Credential" in m.group(0)]
wd = sum(1 for c in calls if "-WorkingDirectory" in c)
gate = sum(1 for c in calls if "gatePath" in c and "-WorkingDirectory" in c)
print("%d %d %d" % (len(calls), wd, gate))
EOF
)
set -- $counts; n=${1:-0}; wd=${2:-0}; gate=${3:-0}
perr=$(timeout 40 powershell -NoProfile -Command "\$e=\$null; [void][System.Management.Automation.Language.Parser]::ParseFile('$WT\\l.ps1',[ref]\$null,[ref]\$e); \$e.Count" 2>&1 | tr -d '\r' | tail -1)
others=$(git -C opal_ai diff --name-only "$OA_NESTED_PIN" "$REF" 2>/dev/null | grep -v -x -F "$F" | grep -c .)
rm -rf "$T"
echo "opal_ai $REF: credentialed Start-Process=$n with -WorkingDirectory=$wd; gate launch with -WorkingDirectory=$gate; parse errors=${perr:-none}; other files changed vs $OA_NESTED_PIN=$others"
if [ "$n" -ge 2 ] && [ "$wd" = "$n" ] && [ "$gate" -ge 1 ] && [ "$perr" = 0 ] && [ "$others" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
