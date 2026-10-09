param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$repo = 'C:\Users\AndrewBerman\Desktop\ajb_workspace'
$taskName = 'Opal-TO28-svc-irpt-REMOVE-20261009'
$deadlineUtc = [DateTimeOffset]::Parse('2026-10-09T13:09:10.4758656Z')
$outRel = 'org/tier2_senior/0.7.0_AE_CloudOps/deliverables/svc_irpt_st28_20261009'
$outDir = Join-Path $repo $outRel
$secretId = 'irpt/svc-irpt-analysis/password'
$resourceArn = 'arn:aws:secretsmanager:us-east-1:313476888478:secret:irpt/svc-irpt-analysis/password-rfHf9l'
$ownerArn = 'arn:aws:iam::313476888478:root'
$addRel = 'org/tier1_exec/2.0.0_SA_COO/deliverables/SVC_IRPT_READER_POLICY_ADD_dell2_window_20261008.json'
$beforeRel = 'org/tier1_exec/2.0.0_SA_COO/deliverables/SVC_IRPT_READER_POLICY_BEFORE_restore_20261008.json'
$sentinelRel = 'org/critical_paths/.open_deploys/svc-irpt-st28-window-laptop-20261009.json'
$ledgerRel = 'org/critical_paths/change_management/20261009T0905Z_svc-irpt-st28-window-laptop-20261009_deploy_completion.md'
$proofRel = 'org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_CTLPLN.TO-APPLY-28.svc-irpt-reader-dell2-window-st28-ledger-laptop.proof_of_spec.json'
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Write-NoBom([string]$Path, [string]$Text) {
  [System.IO.File]::WriteAllText($Path, $Text.TrimEnd() + [Environment]::NewLine, $utf8NoBom)
}

function Send-SeatMessage([string]$To, [string]$Subject, [string]$Body) {
  $env:OPAL_AGENT_SERIAL = '0.7.0_AE_CloudOps'
  & (Join-Path $repo 'org/mcp/codex-send.ps1') -To $To -Subject $Subject -Body $Body | Out-File -FilePath (Join-Path $outDir 'backstop-messages.log') -Append -Encoding utf8
}

function Read-LivePolicy([string]$OutputPath) {
  $text = & aws secretsmanager get-resource-policy --secret-id $secretId --query ResourcePolicy --output text
  if ($LASTEXITCODE -ne 0) { throw 'get-resource-policy failed' }
  Write-NoBom $OutputPath ($text | Out-String)
}

function Compare-Policy([string]$LivePath, [string]$ExpectedRel, [string]$OutputPath, [string]$Label) {
  & python (Join-Path $outDir 'policy_set_rule.py') $LivePath (Join-Path $repo $ExpectedRel) $OutputPath --label $Label
  if ($LASTEXITCODE -ne 0) { throw "set-rule mismatch: $Label" }
}

function Simulate-Policy([string]$PolicyPath, [array]$Checks, [string]$OutputPath) {
  $policyUri = 'file://' + $PolicyPath.Replace([char]92, '/')
  $results = @()
  foreach ($check in $Checks) {
    $raw = & aws iam simulate-principal-policy --policy-source-arn $check.principal --action-names secretsmanager:GetSecretValue --resource-arns $resourceArn --resource-policy $policyUri --resource-owner $ownerArn --output json
    if ($LASTEXITCODE -ne 0) { throw "simulation failed for $($check.principal)" }
    $parsed = $raw | ConvertFrom-Json
    $decision = $parsed.EvaluationResults[0].EvalDecision
    $results += [ordered]@{
      principal = $check.principal
      expected = $check.expected
      decision = $decision
      result = $parsed.EvaluationResults[0]
    }
    if ($decision -ne $check.expected) {
      throw "unexpected decision $decision for $($check.principal), expected $($check.expected)"
    }
  }
  Write-NoBom $OutputPath ($results | ConvertTo-Json -Depth 30)
  return $results
}

function Remove-ScheduledBackstop {
  & schtasks.exe /Delete /TN $taskName /F | Out-Null
}

Set-Location $repo
$sentinel = Join-Path $repo $sentinelRel

if (-not (Test-Path -LiteralPath $sentinel -PathType Leaf)) {
  if (-not $DryRun) { Remove-ScheduledBackstop }
  exit 0
}

if ($DryRun) {
  foreach ($required in @($addRel, $beforeRel, $sentinelRel, $ledgerRel, "$outRel/policy_set_rule.py")) {
    if (-not (Test-Path -LiteralPath (Join-Path $repo $required) -PathType Leaf)) {
      throw "missing required path: $required"
    }
  }
  "DRY_RUN_OK deadline_utc=$($deadlineUtc.ToString('o')) sentinel_present=True"
  exit 0
}

try {
  $remaining = $deadlineUtc - [DateTimeOffset]::UtcNow
  if ($remaining.TotalSeconds -gt 60) {
    throw "backstop invoked more than 60 seconds early: $([math]::Round($remaining.TotalSeconds, 3)) seconds"
  }
  if ($remaining.TotalSeconds -gt 0) {
    Start-Sleep -Seconds ([math]::Ceiling($remaining.TotalSeconds))
  }
  if (-not (Test-Path -LiteralPath $sentinel -PathType Leaf)) {
    Remove-ScheduledBackstop
    exit 0
  }

  $startPath = Join-Path $outDir 'remove-start.json'
  Read-LivePolicy $startPath
  Compare-Policy $startPath $addRel (Join-Path $outDir 'remove-start-verdict.json') 'remove-start-live-vs-signed-add'

  $putStart = [DateTimeOffset]::UtcNow
  $putRaw = & aws secretsmanager put-resource-policy --secret-id $secretId --resource-policy "file://$beforeRel" --block-public-policy --output json
  if ($LASTEXITCODE -ne 0) { throw 'put-resource-policy BEFORE failed' }
  $putEnd = [DateTimeOffset]::UtcNow
  Write-NoBom (Join-Path $outDir 'remove-put.json') ($putRaw | Out-String)
  Write-NoBom (Join-Path $outDir 'remove-put-timing.json') ([ordered]@{
      put_start_utc = $putStart.ToString('o')
      put_end_utc = $putEnd.ToString('o')
      trigger = 'ADD+4h backstop'
      deadline_utc = $deadlineUtc.ToString('o')
      resource_arn = $resourceArn
      policy = 'signed BEFORE'
      block_public_policy = $true
    } | ConvertTo-Json)

  $afterPath = Join-Path $outDir 'remove-after.json'
  Read-LivePolicy $afterPath
  Compare-Policy $afterPath $beforeRel (Join-Path $outDir 'remove-put-verdict.json') 'remove-live-vs-signed-before'

  $checks = @(
    [ordered]@{ principal='arn:aws:iam::313476888478:user/cloudops-dell2-agent-user'; expected='explicitDeny' },
    [ordered]@{ principal='arn:aws:iam::313476888478:user/cloudops-dell1-agent-user'; expected='explicitDeny' },
    [ordered]@{ principal='arn:aws:iam::313476888478:user/Andrew_Berman'; expected='allowed' }
  )
  $results = Simulate-Policy $afterPath $checks (Join-Path $outDir 'remove-live-simulations.json')

  & python .tools/deploy_ledger.py close-leg --slug svc-irpt-st28-window-laptop-20261009 --leg-id REMOVE --proof "ADD+4h backstop; live ADD setequal; signed BEFORE put $($putStart.ToString('HH:mm:ss'))-$($putEnd.ToString('HH:mm:ss'))Z with block-public-policy; live BEFORE setequal; dell2 explicitDeny, dell1 explicitDeny, walker allowed; no GetSecretValue"
  if ($LASTEXITCODE -ne 0) { throw 'deploy ledger REMOVE close-leg failed' }
  & python .tools/deploy_ledger.py close --slug svc-irpt-st28-window-laptop-20261009
  if ($LASTEXITCODE -ne 0) { throw 'deploy ledger close failed' }

  $removeReportRel = "$outRel/REMOVE.md"
  Write-NoBom (Join-Path $repo $removeReportRel) @"
# TO28 REMOVE

The ADD+4h backstop restored the signed BEFORE resource policy from $($putStart.ToString('o')) through $($putEnd.ToString('o')). The start matched signed ADD and the readback matched signed BEFORE under the required set rule. Simulations returned Dell2 `explicitDeny`, Dell1 `explicitDeny`, and Andrew_Berman `allowed`. No `GetSecretValue` call was made and no secret value was read.
"@

  $proof = [ordered]@{
    schema_version = '1.0'
    genre = 'DEPLOY'
    to_id = 'NFRA_CTLPLN.TO-APPLY-28.svc-irpt-reader-dell2-window-st28-ledger-laptop'
    phase = 'NON-BUILD-OTHER'
    firm = 'FABRIC'
    spec_ref = [ordered]@{
      doc = 'org/tier2_senior/0.7.0_AE_CloudOps/task_orders/NFRA_CTLPLN.TO-APPLY-28.svc-irpt-reader-dell2-window-st28-ledger-laptop.md'
      group = 'OTHER'
      vintage_commit = '7968f19e65'
    }
    decomp_ref = [ordered]@{
      doc = 'org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md'
      vintage_commit = '7dd661eb9f5f42815d2541ac729747c3d8a25cbc'
      to_ref = 'org/tier2_senior/0.7.0_AE_CloudOps/task_orders/NFRA_CTLPLN.TO-APPLY-28.svc-irpt-reader-dell2-window-st28-ledger-laptop.md'
    }
    assignee = '0.7.0_AE_CloudOps'
    artifacts_produced = @([ordered]@{
      path_or_key = "$outRel/remove-after.json"
      kind = 'doc'
      commit_or_etag = 'PENDING-THIS-COMMIT'
      deployed_state = 'DEPLOYED-VERIFIED'
      deploy_evidence = "ADD+4h backstop; live ADD setequal; signed BEFORE restored by $($putEnd.ToString('o')); live BEFORE setequal; dell2 explicitDeny, dell1 explicitDeny, walker allowed; no secret value read"
      artifact_covered_by = @('AC1')
    })
    acceptance = @([ordered]@{
      criterion_id = 'AC1'
      criterion_verbatim = 'aws secretsmanager get-resource-policy returns WalkerReadsByExplicitArn after REMOVE'
      method = 'live_read'
      invocation = 'aws secretsmanager get-resource-policy --secret-id irpt/svc-irpt-analysis/password --query ResourcePolicy --output text'
      expect = 'WalkerReadsByExplicitArn'
      output_evidence = 'remove-after.json and remove-put-verdict.json: live policy contains WalkerReadsByExplicitArn and equals signed BEFORE under the set rule'
      denominator = 'one resource policy and 3 principals after REMOVE'
      status = 'PASS'
      status_reason = 'Live readback equals signed BEFORE; simulations show both Dells explicitDeny and Andrew_Berman allowed.'
    })
    controls = [ordered]@{
      reader_window = [ordered]@{
        description = 'Dell2 access is removed while the original walker remains allowed'
        expected_landed = 'dell2 explicitDeny and walker allowed'
        expected_not_landed = 'dell2 allowed or walker denied'
        observed = 'dell2 explicitDeny; walker allowed'
        status = 'PASS'
      }
    }
    never_widen_pair = [ordered]@{
      coo_half = 'org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_SVC_IRPT_READER_DELL2_WINDOW_20261008.md@0e800098a7'
      cto_half = 'org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_SVC_IRPT_READER_DELL2_WINDOW_20261008.md@7aab22d727 + consent msg 107850'
    }
    risk_class = 'WORLD'
    rollback = 'The signed BEFORE document is the closed state. If drift appears, put that exact document on the one secret with block-public-policy and re-run set equality plus the three simulations.'
    scope = 'ADD and REMOVE are complete for the st28 window; the resource policy is restored to signed BEFORE.'
    declared_exclusions = @()
    surprises = @()
    session_log = $removeReportRel
    compiler_tools = @([ordered]@{
      tool = 'aws iam simulate-principal-policy'
      invocation = 'one exact secret ARN per principal with the signed live resource policy'
      result = 'After REMOVE: dell2 explicitDeny; dell1 explicitDeny; Andrew_Berman allowed; no GetSecretValue call'
    })
  }
  Write-NoBom (Join-Path $repo $proofRel) ($proof | ConvertTo-Json -Depth 30)

  $commitPaths = @(
    $sentinelRel,
    $ledgerRel,
    "$outRel/remove-start.json",
    "$outRel/remove-start-verdict.json",
    "$outRel/remove-put.json",
    "$outRel/remove-put-timing.json",
    "$outRel/remove-after.json",
    "$outRel/remove-put-verdict.json",
    "$outRel/remove-live-simulations.json",
    $removeReportRel,
    $proofRel
  )
  $commitArgs = @('.tools/safe-commit.sh', '--author', '0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>', '-m', 'ops: close TO28 svc-irpt st28 reader window', '--') + $commitPaths
  & bash @commitArgs
  if ($LASTEXITCODE -ne 0) { throw 'safe-commit for REMOVE failed' }
  $hash = (& git rev-parse HEAD).Trim()
  Send-SeatMessage '2.0.0_SA_COO~C' "TO28 REMOVE $($putEnd.ToString('yyyy-MM-ddTHH:mm:ssZ')) — CLOSED" "ADD+4h backstop restored signed BEFORE. Dell2 explicitDeny; Dell1 explicitDeny; Andrew_Berman allowed. No GetSecretValue and no value read. Ledger closed. Commit $hash."
  Send-SeatMessage '0.0.0_AB_MSTR' "RELAY to 2.0.0_SA_COO~G2 — TO28 REMOVE $($putEnd.ToString('yyyy-MM-ddTHH:mm:ssZ'))" "Signed BEFORE restored at the ADD+4h backstop. Dell2 GetSecretValue simulation explicitDeny. Ledger closed. Commit $hash."
  Remove-ScheduledBackstop
} catch {
  $failure = [ordered]@{
    failed_utc = [DateTimeOffset]::UtcNow.ToString('o')
    error = $_.Exception.Message
    sentinel_present = [bool](Test-Path -LiteralPath $sentinel -PathType Leaf)
  } | ConvertTo-Json
  Write-NoBom (Join-Path $outDir 'backstop-failure.json') $failure
  Send-SeatMessage '2.0.0_SA_COO~C' 'TO28 REMOVE BACKSTOP FAILED — immediate intervention required' "The one-time REMOVE backstop failed: $($_.Exception.Message). No secret value was read. Check svc-irpt-st28-window-laptop-20261009 immediately."
  Send-SeatMessage '0.0.0_AB_MSTR' 'RELAY to 2.0.0_SA_COO~G2 — TO28 REMOVE BACKSTOP FAILED' "The REMOVE backstop failed: $($_.Exception.Message). Immediate intervention required. No secret value was read."
  exit 1
}
