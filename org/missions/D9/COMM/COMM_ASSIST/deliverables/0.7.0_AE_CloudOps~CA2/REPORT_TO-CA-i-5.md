# COMM_ASSIST.TO-CA-i-5 -- final report (0.7.0_AE_CloudOps~CA2, dell2, 2026-10-13 22:0x local / 2026-10-14 02:0xZ)

Result: CAi5-AC1, AC2 and AC3 all PASS; the proof instance validates VALID. One surprise row: COMM_ASSIST-D2-S1 (the order names COMM_ASSIST-CA2-S<k>, which the row grammar refuses).

## Steps
1. Precondition, run before anything was installed: `I5-PRE ok=True device=dell2 rows=7 object_id=7 seq_key=7 forwarder=True mailbox=True identity=True reason=none`. The checkout already held the pin; no sync run.
2. Variables set from the live handler (`aws lambda get-function-configuration`, read-only), never typed. Names set:
   `MUSE_MAILBOX_URL` (from `LDO_MAILBOX_URL`) and `MUSE_LDO_ID` (from `LDO_ID`), both at User scope. Each read back equal to the function's value.
3. By-hand run: `MUSE-FORWARD sent=0 rejected=0 failed=0`, exit 0. It created NO folder (row COMM_ASSIST-D2-S1: `forwarder.py` returns when `answers\` is absent).
   The empty `answers\` was created by hand, a named write in the order; a second run then created `answers\done\` and `answers\rejected\`.
4. Task `MuseAnswerForward` registered (command below) and started once: last result 0, repetition PT2M with no duration, next run queued.
5. Install read-back: `I5-INSTALL ok=True task=found last_result=0 env_url=True env_ldo=True folders=True reason=none`.
6. End-to-end refusal test, run ONCE, started ~30 seconds after a task fire so the task could not pick the file up first:
   `I5-E2E ok=True forwarded=1 refused=bad-signature waited_s=0 reason=none`. The 22:04:33 fire then exited 0 and sent nothing (one marker in `done\`, `rejected\` empty).

## The three output lines
- `I5-PRE ok=True device=dell2 rows=7 object_id=7 seq_key=7 forwarder=True mailbox=True identity=True reason=none`
- `I5-INSTALL ok=True task=found last_result=0 env_url=True env_ldo=True folders=True reason=none`
- `I5-E2E ok=True forwarded=1 refused=bad-signature waited_s=0 reason=none`

## Scheduled-task registration command (PowerShell, as run)
```
$repo = 'C:\dev\ajb_workspace'
$cmd = '$env:MUSE_MAILBOX_URL=[Environment]::GetEnvironmentVariable(''MUSE_MAILBOX_URL'',''User''); $env:MUSE_LDO_ID=[Environment]::GetEnvironmentVariable(''MUSE_LDO_ID'',''User''); python data\transcripts\scripts\muse_reader\forwarder.py --root $env:USERPROFILE\muse-reader'
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument ('-NoProfile -Command "' + $cmd + '"') -WorkingDirectory $repo
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 2)
$principal = New-ScheduledTaskPrincipal -UserId "$env:COMPUTERNAME\$env:USERNAME" -LogonType S4U -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 10)
Register-ScheduledTask -TaskName MuseAnswerForward -Action $action -Trigger $trigger -Principal $principal -Settings $settings
Start-ScheduledTask -TaskName MuseAnswerForward
```
User `Test`, S4U, the same principal as `MuseReaderRefresh`. The two variables were set with
`[Environment]::SetEnvironmentVariable('<name>', <value read from the live function>, 'User')`.

## Where the test record sits
The test answer `answers\e2e-20261014T020311Z.json` stays in `answers\` (the forwarder never moves a file's bytes); its marker
`answers\done\b6cff723213c47bdd7bffa812d5987c0b865c3bf30a4bb0d723cdfadbcb74f98.json` is in `answers\done\`. The order text says the file stays in `done\`.
Because the file stays in `answers\`, every 2-minute fire skips it (the same bytes act once); it is not resent.

## Rollback (on the issuer's word)
```
Unregister-ScheduledTask -TaskName MuseAnswerForward -Confirm:$false
[Environment]::SetEnvironmentVariable('MUSE_MAILBOX_URL', $null, 'User')
[Environment]::SetEnvironmentVariable('MUSE_LDO_ID', $null, 'User')
```
The `answers\` folder may stay; it holds only the test record.

## Not done, by design
No key installed, no policy, IAM, firewall or sshd change. AWS use: reads, plus the one `sqs send-message` the forwarder made for the
throwaway-key test answer. Muse was asked to sign nothing, and no real answer was sent or acted on.
