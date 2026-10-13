# COMM_ASSIST.TO-CA-h-2 -- final report (0.7.0_AE_CloudOps~CA2, dell2, 2026-10-13)

Result: CAh2-AC1, AC2 and AC3 all PASS; the proof instance validates VALID.

## Steps
1. Pin: `git merge-base --is-ancestor bfaa09da63 HEAD` -> ancestor on `box/dell2` (HEAD e061f31fa9). No sync run.
2. Identity, run before anything else: `H2-IDENTITY ok=True user=cloudops-dell2-agent-user in_group=True reason=none`.
3. Tools: Python 3.14.7; aws-cli/2.37.9 Python/3.14.6 Windows/11 exe/AMD64; OpenSSH_10.5p1, OpenSSL 3.5.7 9 Jun 2026.
   `ssh-keygen -V` is not a version flag (it takes a validity interval and exits 1 with usage), so the OpenSSH version is `ssh -V`.
   ssh-keygen itself is present. Nothing was installed.
4. Folder `C:\Users\Test\muse-reader` created by the manual run: `MUSE-REFRESH ok=4 absent=0 unreadable=0`. Task registered and started.
5. SSH read: `H2-SSH ok=True listening=True keys=3 ...` (fingerprints below).
6. No surprise rows filed.

## Scheduled-task registration command (PowerShell, as run)
```
$py = 'C:\Users\Test\AppData\Local\Programs\Python\Python314\python.exe'
$repo = 'C:\dev\ajb_workspace'
$root = Join-Path $env:USERPROFILE 'muse-reader'
$action = New-ScheduledTaskAction -Execute $py -Argument "data\transcripts\scripts\muse_reader\refresh.py --root `"$root`"" -WorkingDirectory $repo
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 15)
$principal = New-ScheduledTaskPrincipal -UserId "$env:COMPUTERNAME\$env:USERNAME" -LogonType S4U -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 10)
Register-ScheduledTask -TaskName MuseReaderRefresh -Action $action -Trigger $trigger -Principal $principal -Settings $settings
Start-ScheduledTask -TaskName MuseReaderRefresh
```
User `Test`, S4U logon (runs whether or not logged on, stores no password). Repetition PT15M with no duration, so no end date.
Read back: NextRunTime 17:41:23 local after the 17:26 fire.

## The three output lines
- `H2-IDENTITY ok=True user=cloudops-dell2-agent-user in_group=True reason=none`
- `H2-SCHEDULED ok=True task=found last_result=0 age_min=1.7 ok=4 absent=0 unreadable=0 reason=none`
- `H2-SSH ok=True listening=True keys=3 fingerprints=SHA256:Ysgq86UGf/r7GargduCa/3yzyl6wb0wgKbzUpsc9kMg,SHA256:oq0WqfmN1I15uxqNGuoN64t+SubEBfmPINUyLgqFBRQ,SHA256:oq0WqfmN1I15uxqNGuoN64t+SubEBfmPINUyLgqFBRQ reason=none`

## For the issuer (row COMM_ASSIST-S3)
AC3 lists 3 key lines but only 2 DISTINCT fingerprints; the second and third lines are the same key
(`SHA256:oq0WqfmN1I15uxqNGuoN64t+SubEBfmPINUyLgqFBRQ`). The other is `SHA256:Ysgq86UGf/r7GargduCa/3yzyl6wb0wgKbzUpsc9kMg`.
Compare these with muse's key. This seat did not decide whether muse's key is among them and added no key.

## Rollback (on the issuer's word)
```
Unregister-ScheduledTask -TaskName MuseReaderRefresh -Confirm:$false
Remove-Item -Recurse -Force "$env:USERPROFILE\muse-reader"
```
The folder is a regenerable copy; nothing else was touched.

## Not done, by design
No `answers/` folder, forwarder or SQS send (FWD-7, round 17). No policy, key, sshd or firewall change. AWS use was read-only,
under `cloudops-dell2-agent-user`. The 17:41 fire was queued but had not run when this was written.
