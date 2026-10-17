# Read one Opal account's Microsoft 365 timeline through the globgrph door and write it to a file on this user's Desktop.
# Run in Windows PowerShell as a member of globgrph-trino-access-group (Andrew_Berman):
#     powershell -ExecutionPolicy Bypass -File C:\Dev\ajb_workspace\org\tier1_exec\2.0.0_SA_COO~S1\deliverables\read_timeline_to_desktop.ps1
# It asks for the account, the window and your 6-digit MFA code, trades the code for a short session, calls the door's MEMBER alias, and saves
# the answer as timeline_<account>_<start>.txt on your Desktop. The session keys live in this process only. Nothing is sent anywhere else.
# SOC2_MSLOGS round-1 stopgap (issuer 2.0.0_SA_COO~S1) until the read client has its own Desktop option.

$ErrorActionPreference = "Stop"
$repo = "C:\Dev\ajb_workspace"
$serial = "arn:aws:iam::313476888478:mfa/Andrew_Phone"

$account = Read-Host "Account address (for example andrew@opalinvest.com)"
$start = Read-Host "Window start, UTC (for example 2026-10-15T00:00:00Z)"
$end = Read-Host "Window end, UTC (for example 2026-10-16T00:00:00Z)"
$code = Read-Host "MFA code (6 digits, from your phone now)"

Remove-Item Env:AWS_PROFILE -ErrorAction SilentlyContinue
$raw = aws sts get-session-token --serial-number $serial --token-code $code --output json
if ($LASTEXITCODE -ne 0) { throw "aws sts get-session-token failed (check the 6-digit code; it changes every 30 seconds)" }
$cred = ($raw | ConvertFrom-Json).Credentials
$env:AWS_ACCESS_KEY_ID = $cred.AccessKeyId
$env:AWS_SECRET_ACCESS_KEY = $cred.SecretAccessKey
$env:AWS_SESSION_TOKEN = $cred.SessionToken
$env:AWS_DEFAULT_REGION = "us-east-1"

$safe = ($account -replace "[^A-Za-z0-9@._-]", "_")
$stamp = ($start -replace "[^0-9]", "").Substring(0, 8)
$out = Join-Path ([Environment]::GetFolderPath("Desktop")) ("timeline_" + $safe + "_" + $stamp + ".txt")

Set-Location $repo
python data\m365_metadata\scripts\silver\read_timeline.py --account $account --start $start --end $end | Out-File -FilePath $out -Encoding utf8
if ($LASTEXITCODE -ne 0) { throw "read_timeline.py failed; no file was kept if it printed nothing" }
Write-Host ("Saved: " + $out)
Write-Host ("Lines: " + (Get-Content $out | Measure-Object -Line).Lines)
