# HVST-cc-5 step 6: R1-R6 plus R7 (the bar) and the account stop rule. Read only. Usage: cc5_reads.ps1 <label> <T0 e.g. 2026-10-16T00:31:23Z> <plus3|plus15>
param([string]$Label, [string]$T0, [string]$Mark)
Set-Location 'C:\dev\ajb_workspace'
$D = 'org\missions\D5\AMGT\AMGT_HARVST\deliverables\0.7.0_AE_CloudOps~SC1\round88'
$out = "$D\cc5_reads.out"
$state = 'C:\dev\ajb_workspace\.runtime\harvest-cycle\state'
$runtime = 'C:\dev\ajb_workspace\.runtime\harvest-cycle\runtime'
$log = "$state\cycle_runner.log"
$task = 'Opal Data Harvest - Continuous Cycle'
function W($s) { Add-Content -Path $out -Value $s -Encoding ascii }
$now = (Get-Date).ToUniversalTime()
W ""
W "===== READ $Label  taken $($now.ToString('yyyy-MM-ddTHH:mm:ssZ'))  (T0 $T0) ====="

# R1
$age = ($now - (Get-Item $log).LastWriteTime.ToUniversalTime()).TotalMinutes
$ctlAge = ($now - (Get-Item 'C:\Windows\System32\drivers\etc\hosts').LastWriteTime.ToUniversalTime()).TotalMinutes
$lines = @(Get-Content $log).Count
W ("R1 log last write age_min={0:N2}  lines={1}  control(hosts file age_min={2:N0}, must read stale)" -f $age, $lines, $ctlAge)
$cnt3 = "$D\cc5_r1_lines_plus3.txt"
if ($Mark -eq 'plus3') { Set-Content $cnt3 -Value $lines -Encoding ascii; W "R1 plus3 line count recorded: $lines (R1 at +3 TRUE iff age_min < 5: $($age -lt 5))" }
else { $l3 = [int](Get-Content $cnt3); W "R1 plus15 lines=$lines vs plus3 lines=$l3 new_lines=$($lines - $l3)  (R1 at +15 TRUE iff new_lines > 0: $($lines -gt $l3))" }

# R2
$xmlText = (schtasks /query /xml /tn $task) -join "`n"
$xmlName = if ($Mark -eq 'plus15') { 'cc5_task_plus15.xml' } else { 'cc5_task.xml' }
Set-Content -Path "$D\$xmlName" -Value $xmlText -Encoding ascii
$xml = [xml]$xmlText
$ex = $xml.Task.Actions.Exec
$cmdOk = ($ex.Command -match 'pythonw\.exe"?$'); $argOk = ($ex.Arguments -match '--refresh-once'); $pubOk = ($ex.Arguments -match '--publishers wsj barrons sa --refresh-once')
$ctl = ('C:\x\python.exe' -match 'pythonw\.exe"?$')
W "R2 Command=$($ex.Command)  ends_pythonw=$cmdOk  Arguments_contain_refresh_once=$argOk  publishers_exactly_wsj_barrons_sa=$pubOk  WorkingDirectory=$($ex.WorkingDirectory)  (control: python.exe vs the pythonw pattern -> $ctl, must be False)  saved=$xmlName"

# R3
$procs = @(Get-CimInstance Win32_Process -Filter "Name='pythonw.exe'" | Where-Object { $_.CommandLine -match 'lib\.opal_data_harvest\.cycle_runner' })
W "R3 runner rows=$($procs.Count)"
foreach ($p in $procs) {
  $mwh = (Get-Process -Id $p.ProcessId).MainWindowHandle
  $kids = @(Get-CimInstance Win32_Process -Filter "ParentProcessId=$($p.ProcessId)" | Where-Object { $_.Name -eq 'conhost.exe' })
  $kidTxt = if ($kids.Count -eq 0) { 'NONE' } else { ($kids.ProcessId -join ',') }
  W "R3 pid=$($p.ProcessId) MainWindowHandle=$mwh CONHOST_CHILD=$kidTxt"
}
$ctlDone = $false
foreach ($c in @(Get-CimInstance Win32_Process -Filter "Name='conhost.exe'")) {
  $par = Get-CimInstance Win32_Process -Filter "ProcessId=$($c.ParentProcessId)" -ErrorAction SilentlyContinue
  if ($par -and $par.Name -match '^(python|powershell|cmd|bash)\.exe$') {
    $k = @(Get-CimInstance Win32_Process -Filter "ParentProcessId=$($par.ProcessId)" | Where-Object { $_.Name -eq 'conhost.exe' })
    W "R3 control: live console process $($par.Name) pid=$($par.ProcessId) has conhost child(ren) $($k.ProcessId -join ',')  (must be non-empty)"; $ctlDone = $true; break
  }
}
if (-not $ctlDone) { W "R3 control: NO live console process with a conhost child was found (control not exercised)" }

# R4
$doneTotal = 0; $detail = @()
foreach ($pub in 'wsj', 'barrons', 'sa') {
  $f = Get-ChildItem "$state\cycles\$pub" -Filter '*.checkpoint.json' -ErrorAction SilentlyContinue | Where-Object { $_.Name -notmatch 'run_summary' -and $_.Name -ge ($T0.Substring(0,4) + $T0.Substring(5,2) + $T0.Substring(8,2) + 'T' + $T0.Substring(11,2) + $T0.Substring(14,2) + $T0.Substring(17,2) + 'Z.checkpoint.json') } | Sort-Object Name | Select-Object -Last 1
  if ($f) { $j = Get-Content $f.FullName -Raw | ConvertFrom-Json; $n = @($j.done).Count; $doneTotal += $n; $detail += "$pub $($f.Name) done=$n" } else { $detail += "$pub no checkpoint at or after T0" }
}
W "R4 checkpoint done total (cycles started at or after T0)=$doneTotal  ($($detail -join '; '))"
$d3 = "$D\cc5_r4_done_plus3.txt"
if ($Mark -eq 'plus3') { Set-Content $d3 -Value $doneTotal -Encoding ascii; W "R4 plus3 done total recorded: $doneTotal" }
else { $b = [int](Get-Content $d3); W "R4 plus15 done=$doneTotal vs plus3 done=$b growth=$($doneTotal - $b)  (R4 at +15 TRUE iff growth >= 3: $(($doneTotal - $b) -ge 3))" }
$since = @(Get-Content $log | Where-Object { $_ -ge $T0 })
$errs = @($since | Where-Object { $_ -match 'AttributeError|OSError|WinError' }).Count
$jobs = @($since | Where-Object { $_ -match ' JOB ' }).Count
W "R4 error lines since T0 (AttributeError|OSError|WinError)=$errs ; control: JOB lines since T0 matched by the same method=$jobs"

# R5
$o = python -I "C:\dev\ajb_workspace\org\missions\D5\AMGT\AMGT_HARVST\deliverables\0.7.0_AE_CloudOps~SC1\round87\cb2_windows_read.py" read "$D\cc5_windows_baseline.json" "R5 $Label"
$o | ForEach-Object { W $_ }
$o | Add-Content -Path "$D\cc5_windows.out" -Encoding ascii

# R6
foreach ($pub in 'wsj', 'barrons', 'sa') {
  $jb = @($since | Where-Object { $_ -match " JOB $pub " }).Count
  $st = @($since | Where-Object { $_ -match " STOP ${pub}:" })
  W "R6 $pub JOB lines since T0=$jb ; STOP $pub lines=$($st.Count) $(if ($st.Count) { '(' + (($st | ForEach-Object { $_.Substring(0, [Math]::Min(120, $_.Length)) }) -join ' | ') + ')' })"
}
$statuses = @($since | Where-Object { $_ -match ' JOB ' } | ForEach-Object { ($_ -split 'status=')[1].Split(' ')[0] } | Group-Object | ForEach-Object { "$($_.Name)=$($_.Count)" })
W "R6 JOB statuses since T0: $($statuses -join ', ')"

# R7: the bar, from the s3 get ledger
$led = "$runtime\s3_get_ledger.jsonl"
$rows = @(Get-Content $led | Where-Object { $_.Trim() } | ForEach-Object { $_ | ConvertFrom-Json } | Where-Object { $_.ended_at -gt $T0 })
W "R7 ledger lines with ended_at after T0: $($rows.Count) (file lines $(@(Get-Content $led).Count))"
$avg = @{}; $cnt = @{}
foreach ($cmd in 'run', 'upload-harvest') {
  $g = @($rows | Where-Object { $_.command -eq $cmd })
  $c = ($g | Measure-Object get_count -Sum).Sum; $b = ($g | Measure-Object get_bytes -Sum).Sum
  if (-not $c) { $c = 0 }; if (-not $b) { $b = 0 }
  $a = if ($g.Count) { $b / $g.Count } else { 0 }
  $avg[$cmd] = $a; $cnt[$cmd] = $g.Count
  W ("R7 command={0} lines={1} sum_get_count={2} sum_get_bytes={3} avg_bytes_per_line={4:N0}" -f $cmd, $g.Count, $c, $b, $a)
}
$jobsN = $cnt['run']; $upN = $cnt['upload-harvest']
$upPerJob = if ($jobsN) { $upN / $jobsN } else { 0 }
$projBytes = ($avg['run'] + $avg['upload-harvest'] * $upPerJob) * 242
W ("R7 uploads_per_job={0:N4}  projection of a 242-pair cycle = (avg run bytes {1:N0} + avg upload bytes {2:N0} x {0:N4}) x 242 = {3:N0} bytes = {4:N4} GiB  (bar 5 GiB; over bar: {5})" -f $upPerJob, $avg['run'], $avg['upload-harvest'], $projBytes, ($projBytes / 1GB), ($projBytes / 1GB -gt 5))
$cj = @(Get-ChildItem "$state\cycles" -Recurse -Filter '*.cycle.json' | Where-Object { $_.Name -ge ($T0.Substring(0,4) + $T0.Substring(5,2) + $T0.Substring(8,2) + 'T' + $T0.Substring(11,2) + $T0.Substring(14,2) + $T0.Substring(17,2) + 'Z.cycle.json') })
W "R7 cycle.json files at or after T0: $($cj.Count)"
foreach ($f in $cj) { $j = Get-Content $f.FullName -Raw | ConvertFrom-Json; W "R7 $($f.Name) s3_jobs_lines=$($j.s3_jobs_lines) s3_get_count_jobs=$($j.s3_get_count_jobs) s3_get_bytes_jobs=$($j.s3_get_bytes_jobs) s3_get_count=$($j.s3_get_count) s3_get_bytes=$($j.s3_get_bytes)" }

# account stop rule
$failed = @($since | Where-Object { $_ -match 'REFRESH .*FAILED' })
W "STOP RULE: REFRESH FAILED lines since T0 = $($failed.Count)"
foreach ($pub in 'wsj', 'barrons', 'sa') {
  $r = @($since | Where-Object { $_ -match "REFUSAL $pub " }).Count
  $rf = @($since | Where-Object { $_ -match "REFRESH ${pub}: done" }).Count
  W "STOP RULE: $pub REFRESH done=$rf REFUSAL lines=$r"
}
W "runner alive: $((Get-ScheduledTask -TaskName $task).State)  pythonw rows=$($procs.Count)  STOP present: $(Test-Path 'C:\dev\ajb_workspace\.runtime\harvest-cycle\STOP')"

