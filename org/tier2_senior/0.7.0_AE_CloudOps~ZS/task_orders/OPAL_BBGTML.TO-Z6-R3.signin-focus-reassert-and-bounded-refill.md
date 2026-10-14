<task_order>
  <metadata>
    <id>OPAL_BBGTML.TO-Z6-R3.signin-focus-reassert-and-bounded-refill</id>
    <issued_by>2.0.0_SA_COO~ZB</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ZS</issued_to>
    <date>2026-10-13</date>
    <status>pending -- issued 2026-10-13 ~20:5xZ, Z6 repairs issuance (CTO ruling @61e3067f5c disposition 3); queue position 2 of 2 on this lane, starts only after TO-Z6-R2 is landed and its AC1 reads PASS</status>
    <status>held -- 2026-10-13 ~21:4xZ by 2.0.0_SA_COO~ZB on row OPAL_BBGTML-Z-S17: Andrew's no-modify order is recorded as standing for "the vehicle and the sign-in scripts", and the Z6 ruling does not address it. Whether the Z6 memo lifts it is Andrew's reading; the card is with 0.0.0_AB_MSTR~Z and 1.0.0_SA_CTO~Z. DO NOTHING UNDER THIS ORDER until a later status line names that reading. AMENDMENT 1 (issuer, inside its own decomposition; graded by no gate limb, a flat order): if the reading releases R3, step 1b also guards bbg_fallback.ps1's trailing "P0 gate: transport sustained-down, network OK -> sign-in warranted." line as `if ($absent -eq 3) { ... }` (row Z-S15), so the $absent -eq 0 path prints only its own classification; AC1's expect is unchanged and the AC3 re-run must show no "transport sustained-down" line.</status>
    <status>pending -- RELEASED 2026-10-14 ~09:2xZ by 2.0.0_SA_COO~ZB on Andrew-direct ~09:0xZ, verbatim "What is the hold you are referring to? There should be no hold" (record org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261014_090xZ_NO_HOLD_ON_BLOOMBERG_SIGN_IN_REPAIRS.md; call 6c9f CLOSED). Row Z-S17 is answered: no hold on the sign-in scripts. What still binds, as he said it: do not accidentally overwrite Positioning-pipeline or ETFS-view operations. AMENDMENT 1 stands. AMENDMENT 2 (window): the step-2 clause "it is before 2026-10-14 10:00Z" is replaced by "it is NOT between 10:30Z and 12:30Z on 2026-10-14 (the 07:00 ET pull, OPAL_BBGTML_daily_pull, and its fallback must not race a fill or a merge)"; the step-3 landing and its AC3 obey the same window. All other preconditions are unchanged -- in particular, if dapi_check reads UP, no fill runs and the report says so.</status>
    <project_code>OPAL_BBGTML</project_code>
  </metadata>
<risk>WORLD</risk>
# pipeline-override: flat project with no tree home (OPAL_BBGTML, org/projects/OPAL_BBGTML.json); one cell of the Z6 repairs issuance ruled by 1.0.0_SA_CTO~Z @61e3067f5c; the order is the LD-0529 carrier to a Tier-2 seat

  <objective>
    The unattended sign-in failed its precondition on 8 of 30 retained pull runs. On 2026-10-13 it lost window focus between the
    verified fill and the Login click ("ABORT: focus lost before submit", rc=4, no attempt spent) and gave up. Make the submit
    re-assert focus immediately before the click, and let the fallback re-fill ONCE after an rc=4 (rc=4 spends no Bloomberg attempt).
  </objective>

  <context>
    SPEC: CTO ruling org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_OPAL_BBGTML_Z6_REPAIR_DISPOSITIONS_20261013_Z.md
    disposition 3; trace org/tier1_exec/1.0.0_SA_CTO/deliverables/OPAL_BBGTML_Z6_TRACE_20261013_Z.md Q2 (the 30-run pattern).
    Read integrations/bloomberg/READ_HERE.md section 2 (two phases: fill is free and repeatable; submit spends one attempt of a
    budget, and Bloomberg locks the account on repeats).
    LIVE PRODUCTION: both files run from the SHARED working tree under OPAL_BBGTML_daily_pull (07:00 ET). Saving them there IS
    the deploy. This order therefore BUILDS AND EXERCISES ON A BRANCH first, and lands in the shared tree only after the
    exercise passes. The scripts resolve their siblings from $PSScriptRoot, so the worktree copy runs the worktree's bytes;
    their runtime artifacts go to C:\opal-elev (shared).
    TERMINAL SIGN-IN BEFORE 07:00 ET IS ANDREW'S ACT (open call 763e). This order NEVER clicks Login.
  </context>

  <the_act>
    0. Make your own linked worktree from the shared tree's HEAD after R2 landed:
       git worktree add -b zs-bbgtml-z6-r3 C:/tmp/zs-z6-r3 HEAD
    1. CELL Z6-R3, in the worktree:
       a. integrations/bloomberg/auth/bbg_signin.ps1, -Phase submit (lines 166-188 at issue):
          - re-assert focus: up to 3 tries of SetForegroundWindow($hwnd) + 300 ms + GetForegroundWindow() check; rc=4 only if
            all 3 fail;
          - the LAST foreground check runs immediately before the ledger write and the click, with no sleep between that check,
            the ledger write and the click;
          - add a switch -DryRun: do everything up to and including the last foreground check, then print EXACTLY
            "DRY-RUN: focus held at the click point -- no ledger write, no click." and exit 0. Under -DryRun the ledger is never
            written and Login is never clicked.
       b. integrations/bloomberg/auth/bbg_fallback.ps1, STEP 4 submit handling (lines 94-105 at issue, after R2's edit):
          - on submit rc=4, re-fill ONCE (bbg_signin.ps1 -Phase fill, WITHOUT -Fresh), re-verify (bbg_verify.ps1), and submit
            again; print "rc=4 -- one bounded re-fill (1/1), no attempt spent" before it. A second rc=3/4, or a re-fill that does
            not verify, takes the existing escalation (exit 2). Never more than one re-fill. rc=3 is unchanged.
          - add switches, both TEST-ONLY like -ForceDown: -DrySubmit (every submit call passes -DryRun; after the final dry
            submit print "DRY-SUBMIT: stopped before Login" and exit 0, never reaching STEP 5) and -ForceRc4Once (the FIRST submit's
            rc is treated as 4 so the re-fill path runs; print "TEST: -ForceRc4Once -- first submit rc forced to 4").
       c. Nothing else changes in either file.
    2. THE EXERCISE (AC1, AC2), run from the WORKTREE copy, only when ALL of these hold at the moment you start:
       - C:\Anaconda\envs\cma\python.exe integrations/bloomberg/auth/dapi_check.py prints "DAPI: DOWN" (the Terminal is
         genuinely signed out; -Fresh then closes only a logged-out Terminal);
       - no window titled 'BLOOMBERG: Login' is open (nobody is mid-sign-in);
       - it is before 2026-10-14 10:00Z.
       If dapi_check reads UP, run NO fill: the Terminal is signed in and a -Fresh fill would close it. Land nothing, leave the
       branch, and report "SIGNED-IN: exercise not possible" with the dapi_check line. If a Login window is open, wait 10 minutes
       and re-check once; still open = the same report.
       Record whether wintrv.exe was running before the exercise. After it, if wintrv was NOT running before, close the Bloomberg
       UI tree again (Stop-Process wintrv, blpsmarthost, blpwtk2_subprocess) so the box is left as found. Never touch bbcomm.exe.
    3. LANDING, only on AC1 + AC2 PASS: open the ledger entry
       python .tools/deploy_ledger.py open --slug opal-bbgtml-z6-r3-signin-20261013 --title "OPAL_BBGTML Z6 R3: submit focus re-assert + one bounded re-fill" --author 0.7.0_AE_CloudOps~ZS --leg "L1|git|bbg_signin.ps1 + bbg_fallback.ps1 in the shared working tree (the deploy)|merge hash" --leg "L2|verify|AC3 on the shared tree|check output"
       commit it with its sentinel, merge the branch with `bash .tools/safe-merge.sh zs-bbgtml-z6-r3 -m "..."`, run AC3 on the
       shared tree, close the entry, remove the worktree and branch. AC3 FAIL = revert the merge in the shared tree before 10:00Z.
  </the_act>

  <bounds>
    - Exactly two production files: integrations/bloomberg/auth/bbg_signin.ps1 and integrations/bloomberg/auth/bbg_fallback.ps1.
    - NEVER click Login and NEVER write the sign-in ledger (%USERPROFILE%\.bbg_signin_attempts.json): every submit in this order
      runs with -DryRun. Run fills only under bbg_credentials.py injection, which never prints a credential; never print, log or
      commit a credential or the screenshot.
    - No change to the fire-once ledger guard, the P0 gate (R2's), the verify logic, or the scheduled task.
    - A surprise is a row in org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md (disarm_owner 2.0.0_SA_COO~ZB); keep working.
  </bounds>

  <paths>
    integrations/bloomberg/auth/bbg_signin.ps1
    integrations/bloomberg/auth/bbg_fallback.ps1
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~ZS/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~ZS/task_orders/
    org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md
  </paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="Z6-R3"><invocation>python integrations/bloomberg/auth/bbg_credentials.py -- powershell -NoProfile -ExecutionPolicy Bypass -File C:/tmp/zs-z6-r3/integrations/bloomberg/auth/bbg_fallback.ps1 -ForceDown -SkipP0 -DrySubmit -ForceRc4Once 2>&amp;1 | tee org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/z6_r3_exercise.log; echo "exit=${PIPESTATUS[0]}"</invocation><expect>run only under the step-2 preconditions: in order -- a fill that reads verify PASS; "TEST: -ForceRc4Once"; "rc=4 -- one bounded re-fill (1/1), no attempt spent"; a second fill without -Fresh that reads verify PASS; "DRY-RUN: focus held at the click point"; "DRY-SUBMIT: stopped before Login"; exit=0. No "Clicking Login" and no "ledger recorded" line anywhere.</expect></criterion>
  <criterion id="AC2" cell_refs="Z6-R3"><invocation>powershell -NoProfile -Command "(Get-Content $env:USERPROFILE\.bbg_signin_attempts.json -Raw | ConvertFrom-Json).attempts.Count"</invocation><expect>run once immediately before AC1 and once immediately after: the two counts are EQUAL (the exercise spent no Bloomberg attempt). Record both numbers.</expect></criterion>
  <criterion id="AC3" cell_refs="Z6-R3"><invocation>bash org/tier1_exec/2.0.0_SA_COO~ZB/deliverables/z6_checks/r2_p0_listener_check.sh; echo "exit=$?"</invocation><expect>run on the SHARED tree after the merge: R2: PASS and exit=0 (the landed bytes still parse and R2's P0 classification still holds; -ForceDown -StubSubmit, no GUI)</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE as a deliverable file under org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/ and in your final message: each
    criterion's output (AC1 as the log path plus its key lines), the step-2 precondition reads with times, whether wintrv was
    running before and how the box was left, the branch, the merge hash, the ledger slug and close state, and push state as a
    measured value. If the exercise could not run, say which precondition stopped it. Leave the status flip to the issuer.
  </report>
</task_order>
