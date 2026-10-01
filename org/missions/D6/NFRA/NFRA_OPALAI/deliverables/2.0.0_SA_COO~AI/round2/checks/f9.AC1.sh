#!/usr/bin/env bash
# OA-f-9 AC1 (built): launcher.ps1 at ${OA_F9_REF:-HEAD} starts the gate and the Analyst with .NET Process.Start, never
# Start-Process -Credential (row Z-S50: its window takes no keyboard input at High or Medium integrity); reads the gate on
# a pipe, not a temp file; refuses an elevated parent first; gives the Analyst --add-dir on the DERIVED agent\refs path
# and OPAL_RUNTIME_CONFIG; types no drive-letter path; parses; and changes only the cell's files vs r2-dev 0a5c7c2.
# Behaviour arm: run with a missing config. This token elevated -> 'LAUNCHER: REFUSE ELEVATED' rc=6; not elevated ->
# 'ERROR: config not found' rc=2. Either way nothing is fetched or started.
. "$(dirname "$0")/_root.sh"
REF="${OA_F9_REF:-HEAD}"; BASE="0a5c7c2"
L="opal/runtime/launcher.ps1"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f9ac1_$$")"; mkdir -p "$T"
git -C opal_ai show "$REF:$L" > "$T/l.ps1" 2>/dev/null || { echo "launcher.ps1 absent at $REF"; rm -rf "$T"; echo "RESULT: FAIL"; exit 1; }
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"
read -r cred pstart tmpf redir adddir refs orc elev envv drive <<EOF
$(python - "$T/l.ps1" <<'PY'
import re, sys
raw = open(sys.argv[1], encoding="utf-8", errors="replace").read()
code = "\n".join(l for l in raw.splitlines() if not l.lstrip().startswith("#"))
code = re.sub(r"<#.*?#>", "", code, flags=re.S)
j = re.sub(r"`\r?\n\s*", " ", code)
cred = sum(1 for m in re.finditer(r"Start-Process\b[^\n]*", j) if "-Credential" in m.group(0))
print(cred,
      len(re.findall(r"Diagnostics\.Process\]::Start", j)),
      len(re.findall(r"GetTempFileName", j)),
      len(re.findall(r"RedirectStandardOutput\s*=\s*\$true", j)),
      len(re.findall(r"--add-dir", j)),
      len(re.findall(r"agent[\\/]+refs", j)),
      len(re.findall(r"OPAL_RUNTIME_CONFIG", j)),
      len(re.findall(r"REFUSE ELEVATED", j)),
      len(re.findall(r"\.EnvironmentVariables", j)),
      len(re.findall(r"['\"][A-Za-z]:\\\\", j)))
PY
)
EOF
pe=$(timeout 40 powershell -NoProfile -Command "\$e=\$null; [void][System.Management.Automation.Language.Parser]::ParseFile('$WT\\l.ps1',[ref]\$null,[ref]\$e); \$e.Count" 2>&1 | tr -d '\r' | tail -1)
el=$(timeout 40 powershell -NoProfile -Command "([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)" 2>&1 | tr -d '\r' | tail -1)
bo=$(timeout 60 powershell -NoProfile -ExecutionPolicy Bypass -File "$WT\\l.ps1" -Config "$WT\\no-such-config.json" 2>&1 | tr -d '\r' | grep -m1 -E '^(LAUNCHER: REFUSE|ERROR:)')
br=$(timeout 60 powershell -NoProfile -ExecutionPolicy Bypass -File "$WT\\l.ps1" -Config "$WT\\no-such-config.json" >/dev/null 2>&1; echo $?)
others=$(git -C opal_ai diff --name-only "$BASE" "$REF" 2>/dev/null | grep -v -x -F \
  -e "$L" -e opal/runtime/provision/provision-account.ps1 -e opal/runtime/provision/runtime.config.example.json \
  -e opal/agent/hooks/concierge-gate.sh -e opal/agent/hooks/test_concierge_gate.sh | grep -c .)
rm -rf "$T"
echo "opal_ai $REF: Start-Process -Credential=$cred; Process.Start=$pstart; temp-file=$tmpf; stdout-pipe=$redir; --add-dir=$adddir; agent\\refs=$refs; OPAL_RUNTIME_CONFIG=$orc; REFUSE ELEVATED=$elev; .EnvironmentVariables=$envv; drive-letter literals=$drive; parse errors=$pe; elevated=$el; behaviour='${bo:-none}' rc=$br; other files changed vs $BASE=$others"
ok=1
for v in "$cred" "$tmpf" "$envv" "$drive" "$pe" "$others"; do [ "$v" = 0 ] || ok=0; done
[ "${pstart:-0}" -ge 2 ] && [ "${redir:-0}" -ge 1 ] && [ "${adddir:-0}" -ge 1 ] && [ "${refs:-0}" -ge 1 ] \
  && [ "${orc:-0}" -ge 1 ] && [ "${elev:-0}" -ge 1 ] || ok=0
if [ "$el" = "True" ]; then
  printf '%s' "$bo" | grep -q 'LAUNCHER: REFUSE ELEVATED' && [ "$br" = 6 ] || ok=0
else
  printf '%s' "$bo" | grep -q 'ERROR: config not found' && [ "$br" = 2 ] || ok=0
fi
[ "$ok" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
