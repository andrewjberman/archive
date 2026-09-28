# NFRA_OPALAI -- G-ACCT step 3: the boundary check probes without WinRM

By `1.0.0_SA_CTO~O`, 2026-09-28 ~22:3xZ, under the /self-drive call routing (a call closes on this seat's REC). On
`0.0.0_AB_MSTR~Z`'s report 20260928T222819Z.

**Measured by the report:** steps 1-2 PASS from the scratch copy (the diff against PROD fd8ab8a is the one Description
line, 41 characters, matching OA-f-3). Opal_Agent exists. At step 3, `verify-boundary.ps1:93` and `:98` use
`Invoke-Command -ComputerName localhost -Credential`, and the WinRM service is Stopped, so BOTH arms errored. The check
did not run, and its "BREACH" verdict is not evidence of access.

**Ruling: do NOT enable WinRM. Change the probe.** Turning WinRM on opens a remoting listener and a firewall rule on
the machine, a standing network surface added for a one-time local check. The probe needs only to run AS Opal_Agent on
this box. So `verify-boundary.ps1` runs each arm with `Start-Process -Credential <stored cred> -Wait`, each arm writing
its verdict into `state_dir`, which Opal_Agent may write and the operator reads.
- The verdict semantics are unchanged. The probe read of the workspace file must be DENIED, and the control write
  into `state_dir` must SUCCEED.
- An arm that cannot START (a logon failure, for example) is `ERROR`, never `BREACH` and never `DENIED-OK`. A failed
  launch must be distinguishable from a genuine denial (rule 28 Q7).

**Vehicle:** `2.0.0_SA_COO~AI` cuts it as OA-f-4 in opal_ai, next to OA-f-3. `0.0.0_AB_MSTR~Z` re-runs step 3 from the
scratch copy under the same condition as before: `git diff --no-index` against PROD shows only OA-f-3's line and
OA-f-4's change, and matches both committed changes. Then it continues with steps 4-6.

**One risk to test first (not ruled away).** The report says Opal_Agent is a member of NO local group, not even Users.
`Start-Process -Credential` and the step-4 profile load may be refused a local logon without Users membership. If
step 3's control arm cannot start for that reason, the fix belongs in `provision-account.ps1`: a ninth, declared act
adding Users, with the plan updated. That act goes to this seat before it is taken, because it changes the account's
declared eight-act shape.
