# TO-DQ-t24: register only after CTO~Z signs and the deployment ledger is open.
$ErrorActionPreference = 'Stop'
$repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../../..'))
$python = 'C:/Users/Opal Bloomberg/AppData/Local/Programs/Python/Python311/python.exe'
Set-Location -LiteralPath $repo
$taskName = & $python -c "from lib.opal_naming import name; print(name('mdpf', None, 'demque-backfill', 'task', qualifier='20261010'))"
if ($LASTEXITCODE -ne 0 -or $taskName -ne 'mdpf-demque-backfill-20261010-task') { throw 'Task name derivation failed' }
$resultCode = 2
try {
    if ((Get-Date).ToString('yyyy-MM-dd') -ne '2026-10-10') { throw 'Authorized day has not arrived or has passed' }
    $manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'MDPF_DEMQUE_ZQ_T24_MANIFEST.json') -Raw | ConvertFrom-Json
    foreach ($entry in $manifest.PSObject.Properties) {
        $actual = (Get-FileHash -LiteralPath (Join-Path $repo $entry.Name) -Algorithm SHA256).Hash
        if ($actual -ne $entry.Value) { throw "Signed source/request drift: $($entry.Name)" }
    }
    & $python data/mdpf/scripts/demque/bbg_backfill.py --apply *> (Join-Path $PSScriptRoot 'MDPF_DEMQUE_ZQ_T24_DRAW.log')
    $drawCode = $LASTEXITCODE
    & $python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_DEMQUE_Q1/R7_CHECKS/dq_t24_draw.py *> (Join-Path $PSScriptRoot 'MDPF_DEMQUE_ZQ_T24_AC2.log')
    $checkCode = $LASTEXITCODE
    if ($drawCode -eq 0 -and $checkCode -eq 0) { $resultCode = 0 }
} catch {
    $_ | Out-String | Add-Content -LiteralPath (Join-Path $PSScriptRoot 'MDPF_DEMQUE_ZQ_T24_DRAW.log')
} finally {
    # Exactly this one-shot task; no other task or durable run marker is removed.
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction Stop
}
exit $resultCode
