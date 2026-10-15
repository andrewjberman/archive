# HVST-cb-2 step 6: the five reads (R1-R5) plus the account stop rule check. Read only. Usage: cb2_reads.ps1 <label e.g. +3min> <T0 e.g. 2026-10-15T20:23:04Z>
param([string]$Label, [string]$T0)
Set-Location 'C:\dev\ajb_workspace'
$D = 'org\missions\D5\AMGT\AMGT_HARVST\deliverables\0.7.0_AE_CloudOps~SC1\round87'
$out = "$D\cb2_reads.out"
$state = 'C:\dev\ajb_workspace\.runtime\harvest-cycle\state'
$log = "$state\cycle_runner.log"
$task = 'Opal Data Harvest - Continuous Cycle'
function W($s) { Add-Content -Path $out -Value $s -Encoding ascii }
$now = (Get-Date).ToUniversalTime()
W ""
W "===== READ $Label  taken $($now.ToString('yyyy-MM-ddTHH:mm:ssZ'))  (T0 $T0) ====="

# R1: log freshness (+ a NEW line at +15)
$age = ($now - (Get-Item $log).LastWriteTime.ToUniversalTime()).TotalMinutes
$ctlAge = ($now - (Get-Item 'C:\Windows\System32\drivers\etc\hosts').LastWriteTime.ToUniversalTime()).TotalMinutes
$lines = @(Get-Content $log).Count
W ("R1 log last write age_min={0:N2}  lines={1}  control(hosts file age_min={2:N0}, must read stale)" -f $age, $lines, $ctlAge)
$cnt3 = "$D\cb2_r1_lines_plus3.txt"
if ($Label -like '*3*' -and $Label -notlike '*15*') { Set-Content $cnt3 -Value $lines -Encoding ascii; W "R1 plus3 line count recorded: $lines (R1 at +3 TRUE iff age_min < 5: $($age -lt 5))" }
else { $l3 = [int](Get-Content $cnt3); W "R1 plus15 lines=$lines vs plus3 lines=$l3 new_lines=$($lines - $l3)  (R1 at +15 TRUE iff new_lines > 0: $($lines -gt $l3))" }

# R2: the task XML
$xmlText = (schtasks /query /xml /tn $task) -join "`n"
$xmlName = if ($Label -like '*15*') { 'cb2_task_plus15.xml' } else { 'cb2_task.xml' }
Set-Content -Path "$D\$xmlName" -Value $xmlText -Encoding ascii
$xml = [xml]$xmlText
$ex = $xml.Task.Actions.Exec
$cmdOk = ($ex.Command -match 'pythonw\.exe"?$'); $argOk = ($ex.Arguments -match '--refresh-once')
$ctl = ('C:\x\python.exe' -match 'pythonw\.exe"?$')
W "R2 Command=$($ex.Command)  ends_pythonw=$cmdOk  Arguments_contain_refresh_once=$argOk  (control: python.exe vs the pythonw pattern -> $ctl, must be False)  saved=$xmlName"

# R3: no console window for the runner
$procs = @(Get-CimInstance Win32_Process -Filter "Name='pythonw.exe'" | Where-Object { $_.CommandLine -match 'lib\.opal_data_harvest\.cycle_runner' })
W "R3 runner rows=$($procs.Count)"
foreach ($p in $procs) {
  $mwh = (Get-Process -Id $p.ProcessId).MainWindowHandle
  $kids = @(Get-CimInstance Win32_Process -Filter "ParentProcessId=$($p.ProcessId)" | Where-Object { $_.Name -eq 'conhost.exe' })
  $kidTxt = if ($kids.Count -eq 0) { 'NONE' } else { ($kids.ProcessId -join ',') }
  W "R3 pid=$($p.ProcessId) MainWindowHandle=$mwh CONHOST_CHILD=$kidTxt"
}
$ch = @(Get-CimInstance Win32_Process -Filter "Name='conhost.exe'")
$ctlDone = $false
foreach ($c in $ch) {
  $par = Get-CimInstance Win32_Process -Filter "ProcessId=$($c.ParentProcessId)" -ErrorAction SilentlyContinue
  if ($par -and $par.Name -match '^(python|powershell|cmd|bash)\.exe$') {
    $k = @(Get-CimInstance Win32_Process -Filter "ParentProcessId=$($par.ProcessId)" | Where-Object { $_.Name -eq 'conhost.exe' })
    W "R3 control: live console process $($par.Name) pid=$($par.ProcessId) has conhost child(ren) $($k.ProcessId -join ',')  (must be non-empty)"; $ctlDone = $true; break
  }
}
if (-not $ctlDone) { W "R3 control: NO live console process with a conhost child was found among $($ch.Count) conhost.exe rows (control not exercised)" }

# R4: checkpoint done length, and error lines since T0
$doneTotal = 0; $detail = @()
foreach ($pub in 'wsj', 'barrons') {
  $f = Get-ChildItem "$state\cycles\$pub" -Filter '*.checkpoint.json' -ErrorAction SilentlyContinue | Where-Object { $_.Name -notmatch 'run_summary' } | Sort-Object Name | Select-Object -Last 1
  if ($f) { $j = Get-Content $f.FullName -Raw | ConvertFrom-Json; $n = @($j.done).Count; $doneTotal += $n; $detail += "$pub $($f.Name) done=$n" } else { $detail += "$pub no checkpoint" }
}
W "R4 checkpoint done total=$doneTotal  ($($detail -join '; '))"
$d3 = "$D\cb2_r4_done_plus3.txt"
if ($Label -like '*3*' -and $Label -notlike '*15*') { Set-Content $d3 -Value $doneTotal -Encoding ascii; W "R4 plus3 done total recorded: $doneTotal" }
else { $b = [int](Get-Content $d3); W "R4 plus15 done=$doneTotal vs plus3 done=$b growth=$($doneTotal - $b)  (R4 at +15 TRUE iff growth >= 3: $(($doneTotal - $b) -ge 3))" }
$since = @(Get-Content $log | Where-Object { $_ -ge $T0 })
$errs = @($since | Where-Object { $_ -match 'AttributeError|OSError|WinError' }).Count
$jobs = @($since | Where-Object { $_ -match ' JOB ' }).Count
W "R4 error lines since T0 (AttributeError|OSError|WinError)=$errs ; control: JOB lines since T0 matched by the same method=$jobs (the file is readable and the filter reaches its lines)"

# R5: windows
$o = python -I "$D\cb2_windows_read.py" read "$D\cb2_windows_baseline.json" "R5 $Label"
$o | ForEach-Object { W $_ }
$o | Add-Content -Path "$D\cb2_windows.out" -Encoding ascii

# account stop rule
$failed = @($since | Where-Object { $_ -match 'REFRESH .*FAILED' })
W "STOP RULE: REFRESH FAILED lines since T0 = $($failed.Count)"
foreach ($pub in 'wsj', 'barrons') {
  $r = @($since | Where-Object { $_ -match "REFUSAL $pub " }).Count
  $rf = @($since | Where-Object { $_ -match "REFRESH ${pub}: done" }).Count
  W "STOP RULE: $pub REFRESH done=$rf REFUSAL lines=$r"
}
W "runner alive: $((Get-ScheduledTask -TaskName $task).State)  pythonw rows=$($procs.Count)"
