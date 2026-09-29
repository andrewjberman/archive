#!/usr/bin/env bash
# OA-f-8 AC1 (built): opal_ai/opal/runtime/resolve-claude.ps1 at ${OA_F8_REF:-HEAD} resolves the Claude Code executable
# the launcher starts as Opal_Agent, in this order: (1) the config key `claude_exe` when it names an existing file;
# (2) `claude.exe` on PATH; else (3) a LOUD refusal line `LAUNCHER: REFUSE CLAUDE-NOT-FOUND ...` with exit 5. It prints
# exactly one line `CLAUDE_EXE: <path>` (exit 0) on success. Three arms, run against scratch configs:
#   arm1 claude_exe = an existing scratch file            -> CLAUDE_EXE: <that file>, exit 0
#   arm2 claude_exe = a missing path, PATH without claude -> LAUNCHER: REFUSE CLAUDE-NOT-FOUND, exit 5
#   arm3 no claude_exe key, PATH without claude           -> LAUNCHER: REFUSE CLAUDE-NOT-FOUND, exit 5
# (G-ACCT step 4 measured Claude Code at C:\Users\Opal_Agent\.local\bin\claude.exe, NOT on Opal_Agent's PATH, so the
# launcher's bare 'claude.exe' would fail at step 6.)
. "$(dirname "$0")/_root.sh"
REF="${OA_F8_REF:-HEAD}"
F="opal/runtime/resolve-claude.ps1"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f8ac1_$$")"; mkdir -p "$T"
if ! git -C opal_ai show "$REF:$F" > "$T/r.ps1" 2>/dev/null; then echo "resolve-claude.ps1 absent at $REF"; rm -rf "$T"; echo "RESULT: FAIL"; exit 1; fi
printf 'stub\n' > "$T/fake-claude.exe"
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"
mk() { python -c "import json,sys;d={'checkout_dir':'X','state_dir':'X','workspace_probe_file':'X','prod_ref':'PROD'};
import sys
if sys.argv[2]!='-': d['claude_exe']=sys.argv[2]
json.dump(d,open(sys.argv[1],'w'))" "$1" "$2"; }
mk "$T/c1.json" "$WT\\fake-claude.exe"; mk "$T/c2.json" "$WT\\no-such-claude.exe"; mk "$T/c3.json" -
run() { # a PATH with only System32, so a claude on the real PATH cannot satisfy arms 2-3
  timeout 40 powershell -NoProfile -ExecutionPolicy Bypass -Command "\$env:PATH='C:\\Windows\\System32'; & '$WT\\r.ps1' -Config '$WT\\$1'; exit \$LASTEXITCODE" 2>&1 | tr -d '\r' | grep -m1 -E '^(CLAUDE_EXE:|LAUNCHER: REFUSE)'; }
o1=$(run c1.json); r1=$?; o2=$(run c2.json); o3=$(run c3.json)
e1=$(timeout 40 powershell -NoProfile -ExecutionPolicy Bypass -Command "\$env:PATH='C:\\Windows\\System32'; & '$WT\\r.ps1' -Config '$WT\\c1.json' | Out-Null; exit \$LASTEXITCODE" >/dev/null 2>&1; echo $?)
e2=$(timeout 40 powershell -NoProfile -ExecutionPolicy Bypass -Command "\$env:PATH='C:\\Windows\\System32'; & '$WT\\r.ps1' -Config '$WT\\c2.json' | Out-Null; exit \$LASTEXITCODE" >/dev/null 2>&1; echo $?)
rm -rf "$T"
echo "opal_ai $REF: arm1='${o1:-none}' rc=$e1; arm2='${o2:-none}' rc=$e2; arm3='${o3:-none}'"
if printf '%s' "$o1" | grep -q 'fake-claude.exe' && [ "$e1" = 0 ] \
   && printf '%s' "$o2" | grep -q 'LAUNCHER: REFUSE CLAUDE-NOT-FOUND' && [ "$e2" = 5 ] \
   && printf '%s' "$o3" | grep -q 'LAUNCHER: REFUSE CLAUDE-NOT-FOUND'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
