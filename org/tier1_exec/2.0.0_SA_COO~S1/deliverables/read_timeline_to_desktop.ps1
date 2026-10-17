# Read one Opal account's Microsoft 365 timeline through the globgrph door and write it to a file on this user's Desktop.
# Run in Windows PowerShell as a member of globgrph-trino-access-group (the IAM user Andrew_Berman):
#     powershell -ExecutionPolicy Bypass -File C:\Dev\ajb_workspace\org\tier1_exec\2.0.0_SA_COO~S1\deliverables\read_timeline_to_desktop.ps1
# It shows which AWS identity your CLI is using, finds the MFA device(s) of that identity (and lets you pick when there are several), asks for
# the account, the window and the 6-digit code, trades the code for a short session, calls the door's MEMBER alias, and saves the answer as
# timeline_<account>_<start>.txt on your Desktop. The session keys live in this process only. Nothing is sent anywhere else.
# SOC2_MSLOGS round-1 stopgap (issuer 2.0.0_SA_COO~S1) until the read client has its own Desktop option.

$ErrorActionPreference = "Stop"
$repo = "C:\Dev\ajb_workspace"
$member = "Andrew_Berman"

# This machine's DEFAULT AWS profile is the box's agent user (cloudops-dell1-agent-user), not you. The door admits Andrew_Berman only, so the script
# uses a NAMED profile that holds Andrew_Berman's own access key. Create it once, in this PowerShell window:   aws configure --profile andrew
# (the key id and secret are Andrew_Berman's; they come from where you already keep them, never from this repository or from chat).
Remove-Item Env:AWS_SESSION_TOKEN -ErrorAction SilentlyContinue
$prof = Read-Host "AWS CLI profile that holds the Andrew_Berman access key (Enter for: andrew)"
if (-not $prof) { $prof = "andrew" }
$env:AWS_PROFILE = $prof

# 1. Which identity is the CLI using?
$who = aws sts get-caller-identity --output json | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) { throw "aws sts get-caller-identity failed: the CLI has no usable AWS credentials in this window" }
$user = ($who.Arn -split "/")[-1]
Write-Host ("CLI identity: " + $who.Arn)
if ($user -ne $member) {
    Write-Host ("WARNING: the door admits the IAM user " + $member + " only (group globgrph-trino-access-group). This window is " + $user + ". Continue only if you know why.") -ForegroundColor Yellow
}

# 2. Which MFA device(s) does that identity have?
$serials = @()
$listed = aws iam list-mfa-devices --user-name $user --query "MFADevices[].SerialNumber" --output json 2>$null
if ($LASTEXITCODE -eq 0 -and $listed) { $serials = @($listed | ConvertFrom-Json) }
if ($serials.Count -eq 0) {
    throw ("No MFA device is registered for " + $user + " (or the CLI may not list them). Open AWS Console > IAM > Users > " + $user + " > Security credentials and read the MFA device ARN, then edit `$serials in this script.")
}
$serial = $serials[0]
if ($serials.Count -gt 1) {
    for ($i = 0; $i -lt $serials.Count; $i++) { Write-Host ("  [" + $i + "] " + $serials[$i]) }
    $pick = Read-Host "Which device does your authenticator entry belong to (number)"
    $serial = $serials[[int]$pick]
}
Write-Host ("MFA device: " + $serial + "   (in your authenticator app, use the entry for THIS device name)")

# 3. The questions
$account = Read-Host "Account address (for example andrew@opalinvest.com)"
if ($account -notmatch "^[^@\s]+@[^@\s]+$") { throw "that is not an email address: $account" }
$start = Read-Host "Window start, UTC (for example 2026-10-15T00:00:00Z)"
$end = Read-Host "Window end, UTC (for example 2026-10-16T00:00:00Z)"
foreach ($t in @($start, $end)) { if ($t -notmatch "^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$") { throw "not a UTC time like 2026-10-15T00:00:00Z: $t" } }
$code = Read-Host "MFA code (6 digits, fresh from the entry for the device above)"
if ($code -notmatch "^\d{6}$") { throw "the code is 6 digits" }

# 4. The session and the read
$raw = aws sts get-session-token --serial-number $serial --token-code $code --output json
if ($LASTEXITCODE -ne 0) { throw "aws sts get-session-token failed: the code or the device is wrong. Try the other authenticator entry, with a fresh code." }
$cred = ($raw | ConvertFrom-Json).Credentials
Remove-Item Env:AWS_PROFILE -ErrorAction SilentlyContinue   # the session keys below must win over the named profile
$env:AWS_ACCESS_KEY_ID = $cred.AccessKeyId
$env:AWS_SECRET_ACCESS_KEY = $cred.SecretAccessKey
$env:AWS_SESSION_TOKEN = $cred.SessionToken
$env:AWS_DEFAULT_REGION = "us-east-1"

$safe = ($account -replace "[^A-Za-z0-9@._-]", "_")
$stamp = ($start -replace "[^0-9]", "").Substring(0, 8)
$out = Join-Path ([Environment]::GetFolderPath("Desktop")) ("timeline_" + $safe + "_" + $stamp + ".txt")

Set-Location $repo
python data\m365_metadata\scripts\silver\read_timeline.py --account $account --start $start --end $end | Out-File -FilePath $out -Encoding utf8
if ($LASTEXITCODE -ne 0) { throw "read_timeline.py failed; see the message above" }
Write-Host ("Saved: " + $out)
Write-Host ("Lines: " + (Get-Content $out | Measure-Object -Line).Lines)
