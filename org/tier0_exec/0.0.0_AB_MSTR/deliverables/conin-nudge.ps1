# conin-nudge.ps1 -- focus-free wake of an IDLE seat (1.0.0_SA_CTO~Z ruling, msg 35848).
# Writes the fixed line "check your inbox" + Enter into the target process's console input buffer
# (AttachConsole + WriteConsoleInput). No window focus, no keystroke injection into the desktop.
#
# BOUNDS (ruling 35848): a real stuck-seat case only; only while the seat is IDLE at its input with
# no turn running; the payload is FIXED (no parameter changes it); each use is logged. Any other
# payload needs the CTO's word again.
#
# Usage: conin-nudge.ps1 -Serial <full serial> -TargetPid <claude.exe pid> -Reason <text>
#        (pid for a serial: the last SPAWN row naming it in org/mcp/agent-spawn-audit.log, pid=N;
#         the script refuses unless that pid is alive and is claude.exe.)
# -SelfTest: skip the claude.exe name check and log to the .selftest log. Used on a throwaway console only.
param(
  [Parameter(Mandatory=$true)][string]$Serial,
  [Parameter(Mandatory=$true)][int]$TargetPid,
  [Parameter(Mandatory=$true)][string]$Reason,
  [switch]$SelfTest
)
$Payload = 'check your inbox'
$root = (& git rev-parse --show-toplevel).Trim()
$log = Join-Path $root ('org/tier0_exec/0.0.0_AB_MSTR/logs/conin-nudge-uses' + $(if ($SelfTest) { '.selftest' } else { '' }) + '.log')
New-Item -ItemType Directory -Force (Split-Path $log) | Out-Null
function Log([string]$result) {
  $line = '{0} serial={1} pid={2} payload="{3}" reason="{4}" result={5}' -f (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'), $Serial, $TargetPid, $Payload, $Reason, $result
  Add-Content -Path $log -Value $line -Encoding ascii
  Write-Output $line
}
if ($Serial -notmatch '^[0-9]+\.[0-9]+\.[0-9]+_[A-Za-z]+_[A-Za-z0-9]+(~[A-Za-z0-9]+)?$') { Write-Output "ERROR: '$Serial' is not an agent serial"; exit 4 }
$proc = Get-Process -Id $TargetPid -ErrorAction SilentlyContinue
if (-not $proc) { Log 'REFUSED:pid-not-alive'; exit 3 }
if (-not $SelfTest -and $proc.ProcessName -ne 'claude') { Log ('REFUSED:process-is-' + $proc.ProcessName + '-not-claude'); exit 3 }

Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class ConIn {
  [StructLayout(LayoutKind.Explicit, CharSet=CharSet.Unicode)]
  public struct INPUT_RECORD {
    [FieldOffset(0)] public ushort EventType;
    [FieldOffset(4)] public int bKeyDown;
    [FieldOffset(8)] public ushort wRepeatCount;
    [FieldOffset(10)] public ushort wVirtualKeyCode;
    [FieldOffset(12)] public ushort wVirtualScanCode;
    [FieldOffset(14)] public char UnicodeChar;
    [FieldOffset(16)] public uint dwControlKeyState;
  }
  [DllImport("kernel32.dll", SetLastError=true)] public static extern bool FreeConsole();
  [DllImport("kernel32.dll", SetLastError=true)] public static extern bool AttachConsole(uint pid);
  [DllImport("kernel32.dll", SetLastError=true)] public static extern IntPtr CreateFile(string n, uint a, uint s, IntPtr sa, uint d, uint f, IntPtr t);
  [DllImport("kernel32.dll", SetLastError=true)] public static extern bool WriteConsoleInput(IntPtr h, INPUT_RECORD[] b, uint n, out uint w);
  [DllImport("kernel32.dll")] public static extern bool CloseHandle(IntPtr h);
}
'@
$null = [ConIn]::FreeConsole()
if (-not [ConIn]::AttachConsole([uint32]$TargetPid)) { Log ('FAILED:attach-err-' + [Runtime.InteropServices.Marshal]::GetLastWin32Error()); exit 3 }
$h = [ConIn]::CreateFile('CONIN$', [uint32]3221225472, [uint32]3, [IntPtr]::Zero, [uint32]3, [uint32]0, [IntPtr]::Zero)
if ($h -eq [IntPtr](-1)) { Log ('FAILED:conin-open-err-' + [Runtime.InteropServices.Marshal]::GetLastWin32Error()); exit 4 }
$recs = New-Object System.Collections.Generic.List[ConIn+INPUT_RECORD]
foreach ($ch in ($Payload + "`r").ToCharArray()) {
  foreach ($down in 1,0) {
    $r = New-Object ConIn+INPUT_RECORD
    $r.EventType = 1; $r.bKeyDown = $down; $r.wRepeatCount = 1; $r.UnicodeChar = $ch
    if ($ch -eq "`r") { $r.wVirtualKeyCode = 13; $r.wVirtualScanCode = 28 }
    $recs.Add($r)
  }
}
[uint32]$w = 0
$ok = [ConIn]::WriteConsoleInput($h, $recs.ToArray(), [uint32]$recs.Count, [ref]$w)
$null = [ConIn]::CloseHandle($h)
# WROTE only says the buffer accepted the records. Whether the seat MOVED is read from its inbox ack / log, never from here.
Log ('WROTE-' + $w + '-of-' + $recs.Count + '-ok-' + $ok + ' (seat movement NOT measured here; read its ack)')
