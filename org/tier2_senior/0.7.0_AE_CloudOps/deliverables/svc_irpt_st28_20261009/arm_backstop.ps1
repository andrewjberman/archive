$ErrorActionPreference = 'Stop'
$taskName = 'Opal-TO28-svc-irpt-REMOVE-20261009'
$repo = 'C:\Users\AndrewBerman\Desktop\ajb_workspace'
$script = Join-Path $repo 'org/tier2_senior/0.7.0_AE_CloudOps/deliverables/svc_irpt_st28_20261009/remove_backstop.ps1'
$deadlineUtc = [DateTimeOffset]::Parse('2026-10-09T13:09:10.4758656Z')
$localAt = $deadlineUtc.LocalDateTime
$arguments = '-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "' + $script + '"'

$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $arguments -WorkingDirectory $repo
$trigger = New-ScheduledTaskTrigger -Once -At $localAt
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -ExecutionTimeLimit (New-TimeSpan -Minutes 15)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited

Register-ScheduledTask `
  -TaskName $taskName `
  -Action $action `
  -Trigger $trigger `
  -Settings $settings `
  -Principal $principal `
  -Description 'Authorized TO28 ADD+4h backstop: restore signed BEFORE policy if X1 has not already closed the ledger.' `
  -Force | Out-Null

$task = Get-ScheduledTask -TaskName $taskName
$info = Get-ScheduledTaskInfo -TaskName $taskName
$record = [ordered]@{
  task_name = $taskName
  state = [string]$task.State
  deadline_utc = $deadlineUtc.ToString('o')
  trigger_local = $localAt.ToString('o')
  next_run_time_local = $info.NextRunTime.ToString('o')
  start_when_available = $task.Settings.StartWhenAvailable
  wake_to_run = $task.Settings.WakeToRun
  execution_time_limit = [string]$task.Settings.ExecutionTimeLimit
  action_execute = $task.Actions.Execute
  action_arguments = $task.Actions.Arguments
  working_directory = $task.Actions.WorkingDirectory
}

$json = $record | ConvertTo-Json -Depth 10
$path = Join-Path $repo 'org/tier2_senior/0.7.0_AE_CloudOps/deliverables/svc_irpt_st28_20261009/backstop-schedule.json'
[System.IO.File]::WriteAllText($path, $json + [Environment]::NewLine, (New-Object System.Text.UTF8Encoding($false)))
$json
