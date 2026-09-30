#!/usr/bin/env bash
# MS-a-3 AC1 (the account plane, read live): the local account Opal_MSP exists and is enabled, and it is a member of
# neither Administrators nor CodexSandboxUsers; Opal_Agent's existence is unchanged by the act (read beside it).
. "$(dirname "$0")/_root.sh"
out=$(timeout 60 powershell.exe -NoProfile -Command "\$u = Get-LocalUser -Name 'Opal_MSP' -ErrorAction SilentlyContinue; \$a = [bool](Get-LocalUser -Name 'Opal_Agent' -ErrorAction SilentlyContinue); \$adm = @(Get-LocalGroupMember -Group 'Administrators' -ErrorAction SilentlyContinue | Where-Object { \$_.Name -like '*\\Opal_MSP' }).Count; \$cx = @(Get-LocalGroupMember -Group 'CodexSandboxUsers' -ErrorAction SilentlyContinue | Where-Object { \$_.Name -like '*\\Opal_MSP' }).Count; Write-Output ('exists=' + [bool]\$u + ' enabled=' + [bool](\$u -and \$u.Enabled) + ' admin=' + \$adm + ' codex=' + \$cx + ' opal_agent_exists=' + \$a)" 2>&1 | tr -d '\r' | tail -1)
echo "$out"
if printf '%s' "$out" | grep -q 'exists=True enabled=True admin=0 codex=0'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
