# =============================================================================
# r8_thief_harness.ps1 -- TO-Z6-R8 proof harness (OPAL_BBGTML, 0.7.0_AE_CloudOps~ZS).
#
# Proves bbg_signin.ps1's SETTLE loop (submit phase) against a FAKE login window, never the real Terminal.
#   * It first asserts that NO visible window titled 'BLOOMBERG: Login' exists (same test as Find-LoginWindow). If one does, it is a
#     real Login window: exit 7 without creating or touching anything.
#   * It creates a FAKE top-level window titled 'BLOOMBERG: Login' and a THIEF window, both owned by THIS process, then runs
#       bbg_signin.ps1 -Phase submit -DryRun        (-DryRun: no ledger write, no click -- ever)
#     as a hidden child and relays its output with elapsed-time stamps.
#   * -Arm release : the thief re-grabs the foreground every 80 ms from launch until 3 s after the child's first 'settle:' line,
#                    then STOPS (it stays an inert window). The child must settle and print the DRY-RUN line. Expected exit 0.
#   * -Arm hold    : the thief re-grabs the foreground every 80 ms for the whole run. The child must abort at ~90 s with
#                    'ABORT: focus lost before submit.' and R7's TRACE line, no DRY-RUN. Expected exit 4.
#   * Never uses -Fresh, never runs a fill, never touches wintrv or any Bloomberg process, never writes the sign-in ledger.
#     It READS the attempts count and wintrv's start times before and after and prints both.
#   * It destroys both windows and kills the child (if alive) on every exit path. Its exit code is the child's exit code.
#     Harness refusals/errors: 7 (real Login window present), 9 (harness error / child did not finish in time).
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File r8_thief_harness.ps1 -Arm release|hold -Script <path to bbg_signin.ps1>
# =============================================================================
param(
  [Parameter(Mandatory=$true)][ValidateSet('release','hold')][string]$Arm,
  [Parameter(Mandatory=$true)][string]$Script
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Text;
using System.Runtime.InteropServices;
public class H {
  public delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr l);
  [DllImport("user32.dll")] public static extern int GetWindowTextLength(IntPtr h);
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint a, uint b, bool attach);
  [DllImport("kernel32.dll")] public static extern uint GetCurrentThreadId();
}
"@

function Say($m) { Write-Output ("HARNESS {0}" -f $m) }

# Same test as bbg_signin.ps1's Find-LoginWindow: a VISIBLE window whose title is exactly 'BLOOMBERG: Login'.
function Find-Login {
  $script:__found = [IntPtr]::Zero
  $cb = [H+EnumProc]{ param($h, $l)
    if ([H]::IsWindowVisible($h)) {
      $len = [H]::GetWindowTextLength($h)
      if ($len -gt 0) {
        $sb = New-Object System.Text.StringBuilder ($len + 1)
        [void][H]::GetWindowText($h, $sb, $sb.Capacity)
        if ($sb.ToString() -eq 'BLOOMBERG: Login') { $script:__found = $h; return $false }
      }
    }
    return $true
  }
  [void][H]::EnumWindows($cb, [IntPtr]::Zero)
  return $script:__found
}

function Read-Counts {
  $att = 'unreadable'
  try { $att = [string](Get-Content (Join-Path $env:USERPROFILE '.bbg_signin_attempts.json') -Raw | ConvertFrom-Json).attempts.Count } catch {}
  $wt = 'none'
  try { $w = @(Get-Process wintrv -ErrorAction SilentlyContinue); if ($w.Count -gt 0) { $wt = (($w | ForEach-Object { 'pid {0} start {1}' -f $_.Id, $_.StartTime.ToUniversalTime().ToString('o') }) -join '; ') } } catch { $wt = 'unreadable' }
  return @($att, $wt)
}

# Take the foreground for $f. Both windows belong to this process; AttachThreadInput lets it win against whoever holds it now.
function Grab($f) {
  $fg = [H]::GetForegroundWindow()
  if ($fg -eq $f.Handle) { return }
  [uint32]$fpid = 0
  $ft = [H]::GetWindowThreadProcessId($fg, [ref]$fpid)
  $me = [H]::GetCurrentThreadId()
  $att = $false
  if ($ft -ne 0 -and $ft -ne $me) { $att = [H]::AttachThreadInput($me, $ft, $true) }
  [void][H]::SetForegroundWindow($f.Handle)
  if ($att) { [void][H]::AttachThreadInput($me, $ft, $false) }
}

if (-not (Test-Path $Script)) { Say "REFUSED: script not found: $Script"; exit 9 }
$pre = Find-Login
if ($pre -ne [IntPtr]::Zero) { Say ("REFUSED: a visible 'BLOOMBERG: Login' window already exists (hwnd={0}); it is a real Login window. Nothing was created or touched." -f $pre.ToInt64()); exit 7 }

$before = Read-Counts
Say ("before: sign-in attempts={0} ; wintrv: {1}" -f $before[0], $before[1])
Say ("arm={0} script={1}" -f $Arm, $Script)

$login = $null; $thief = $null; $p = $null; $out = $null; $childExit = 9; $sr = $null
try {
  [System.Windows.Forms.Application]::EnableVisualStyles()
  $login = New-Object System.Windows.Forms.Form
  $login.Text = 'BLOOMBERG: Login'; $login.StartPosition = 'Manual'; $login.Location = New-Object System.Drawing.Point(40, 40)
  $login.Size = New-Object System.Drawing.Size(260, 90); $login.ShowInTaskbar = $false; $login.FormBorderStyle = 'FixedToolWindow'
  $thief = New-Object System.Windows.Forms.Form
  $thief.Text = 'r8-harness-thief'; $thief.StartPosition = 'Manual'; $thief.Location = New-Object System.Drawing.Point(340, 40)
  $thief.Size = New-Object System.Drawing.Size(260, 90); $thief.ShowInTaskbar = $false; $thief.FormBorderStyle = 'FixedToolWindow'
  $login.Show(); $thief.Show()
  for ($i = 0; $i -lt 10; $i++) { [System.Windows.Forms.Application]::DoEvents(); Start-Sleep -Milliseconds 20 }
  $fake = Find-Login
  if ($fake -ne $login.Handle) { Say ("ERROR: the fake login window is not what Find-Login finds (found {0}, expected {1})" -f $fake.ToInt64(), $login.Handle.ToInt64()); exit 9 }
  Say ("fake login window hwnd={0} pid={1}; thief hwnd={2}" -f $login.Handle.ToInt64(), $PID, $thief.Handle.ToInt64())

  Grab $login
  for ($i = 0; $i -lt 10; $i++) { [System.Windows.Forms.Application]::DoEvents(); Start-Sleep -Milliseconds 20 }

  $out = Join-Path $env:TEMP ("r8_child_{0}.out" -f $PID)
  Remove-Item $out, ($out + '.err') -ErrorAction SilentlyContinue
  $clock = [System.Diagnostics.Stopwatch]::StartNew()
  $p = Start-Process -FilePath 'powershell.exe' -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ('"{0}"' -f $Script), '-Phase', 'submit', '-DryRun') `
        -WindowStyle Hidden -RedirectStandardOutput $out -RedirectStandardError ($out + '.err') -PassThru
  $null = $p.Handle
  Say ("child launched pid={0}" -f $p.Id)

  $fs = [System.IO.File]::Open($out, 'Open', 'Read', 'ReadWrite')
  $sr = New-Object System.IO.StreamReader($fs)
  $grab = [System.Diagnostics.Stopwatch]::StartNew()
  $thiefOn = $true; $grabs = 0; $settleSeenAt = -1.0; $released = $false
  $cap = if ($Arm -eq 'hold') { 115.0 } else { 60.0 }
  while ($true) {
    [System.Windows.Forms.Application]::DoEvents()
    while (($line = $sr.ReadLine()) -ne $null) {
      Write-Output ("[child +{0,6:N1}s] {1}" -f $clock.Elapsed.TotalSeconds, $line)
      if ($settleSeenAt -lt 0 -and $line -match '^\s*settle:') { $settleSeenAt = $clock.Elapsed.TotalSeconds }
    }
    if ($thiefOn -and $grab.ElapsedMilliseconds -ge 80) { Grab $thief; $grabs++; $grab.Restart() }
    if ($Arm -eq 'release' -and $thiefOn -and $settleSeenAt -ge 0 -and ($clock.Elapsed.TotalSeconds - $settleSeenAt) -ge 3.0) {
      $thiefOn = $false; $released = $true
      Say ("thief released at +{0:N1}s (3 s after the child's first settle line); it stays an inert window" -f $clock.Elapsed.TotalSeconds)
    }
    if ($p.HasExited) { break }
    if ($clock.Elapsed.TotalSeconds -gt $cap) { Say ("ERROR: child still running after {0} s; killing it" -f $cap); try { $p.Kill() } catch {}; break }
    Start-Sleep -Milliseconds 20
  }
  for ($i = 0; $i -lt 10; $i++) { Start-Sleep -Milliseconds 50; while (($line = $sr.ReadLine()) -ne $null) { Write-Output ("[child +{0,6:N1}s] {1}" -f $clock.Elapsed.TotalSeconds, $line) } }
  if ($p.HasExited) { $childExit = $p.ExitCode } else { $childExit = 9 }
  Say ("child exit={0} elapsed={1:N1}s thief_grabs={2} thief_released={3}" -f $childExit, $clock.Elapsed.TotalSeconds, $grabs, $released)
  if (Test-Path ($out + '.err')) { $e = (Get-Content ($out + '.err') -Raw); if ($e -and $e.Trim()) { Say ("child stderr (first 300 chars): " + $e.Trim().Substring(0, [Math]::Min(300, $e.Trim().Length))) } }
}
finally {
  if ($sr) { $sr.Dispose() }
  if ($p -and -not $p.HasExited) { try { $p.Kill() } catch {} }
  foreach ($f in @($thief, $login)) { if ($f) { try { $f.Close(); $f.Dispose() } catch {} } }
  if ($out) { Remove-Item $out, ($out + '.err') -ErrorAction SilentlyContinue }
  $after = Read-Counts
  Say ("after: sign-in attempts={0} ; wintrv: {1}" -f $after[0], $after[1])
  Say ("attempts equal: {0} ; wintrv start equal: {1}" -f ($before[0] -eq $after[0]), ($before[1] -eq $after[1]))
  $left = @(Get-Process -Id $PID -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -match 'BLOOMBERG|r8-harness' }).Count
  Say ("fake windows left open by this process: {0}" -f $left)
}
exit $childExit
