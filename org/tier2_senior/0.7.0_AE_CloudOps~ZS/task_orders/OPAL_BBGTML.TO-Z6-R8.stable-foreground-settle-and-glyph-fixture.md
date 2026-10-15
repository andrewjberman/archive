<task_order>
  <metadata>
    <id>OPAL_BBGTML.TO-Z6-R8.stable-foreground-settle-and-glyph-fixture</id>
    <issued_by>2.0.0_SA_COO~ZB</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ZS</issued_to>
    <date>2026-10-15</date>
    <status>pending -- issued 2026-10-15 ~20:2xZ on CTO ruling @079108405c (org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_OPAL_BBGTML_R8_STABLE_FOREGROUND_FIX_20261015_Z.md), itself on Andrew-direct Teams 2026-10-15T18:00:40Z "send this log to CTO and have them fix it". Build and prove tonight on a branch; LAND only after market close (now clear) and BEFORE 2026-10-16 09:00Z; never land inside 10:30Z-12:30Z. Not proven by 09:00Z = do not land, report.</status>
    <project_code>OPAL_BBGTML</project_code>
  </metadata>
<risk>WORLD</risk>
# pipeline-override: flat project with no tree home (OPAL_BBGTML, org/projects/OPAL_BBGTML.json); one repair cell ruled by 1.0.0_SA_CTO~Z @079108405c; the order is the LD-0529 carrier to a Tier-2 seat

  <objective>
    The unattended 07:00 ET sign-in has failed on 5 of 5 mornings since wintrv.exe was replaced on 2026-10-06 04:04Z. Signature B (10-11, 10-13, 10-15) is still live: the fill verifies, then 3 fixed foreground re-asserts all fail and the script aborts at zero attempts, because something transiently takes the foreground in the fill-to-submit gap. Make the submit WAIT THE TRANSIENT OUT: submit only after the login window has held the foreground steadily, so the 2026-10-16 07:00 ET fire signs in whichever window takes focus. Also address signature A (glyph calibration) without widening the band.
  </objective>

  <context>
    SPEC: the CTO ruling above, items 1-5. EVIDENCE: org/tier0_utility/0.0.3_BG_BBGTerminal/logs/2026-10-15/investigation_cron_signin_failure_two_signatures_one_binary_update.md; surprise rows OPAL_BBGTML-Z-S22, Z-S23, Z-S24 in org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md; the failing logs C:\Users\Opal Bloomberg\opal_bbg_logs\bbg_tplus1_20261011_070002.log, _20261013_070001.log, _20261015_070001.log. Landed code you edit: R3 @3dad54c56f and R7 @3aaf87a486 (R7's Get-FgTrace line stays).
    Read integrations/bloomberg/READ_HERE.md section 2 first. THE TERMINAL IS SIGNED IN AND SERVING RIGHT NOW. Nothing in this order may touch it: no -Fresh, no fill, no submit, no kill of wintrv, blpsmarthost, blpwtk2_subprocess or bbcomm, no real Login window. All tonight's proof runs against a FAKE login window that your own harness creates and destroys.
    Interpreter note (your 34464): the pull and fallback pin cma/Python311, not PATH python; this order does not change that.
  </context>

  <the_act>
    0. Own linked worktree from the shared tree's HEAD: git worktree add -b zs-bbgtml-z6-r8 C:/tmp/zs-z6-r8 HEAD
    1. CELL Z6-R8a, bbg_signin.ps1 submit phase, in the worktree. Replace the fixed 3-try foreground re-assert loop (the one that ends in "ABORT: focus lost before submit.") with a bounded SETTLE loop:
       - poll the foreground window every 250 ms for at most 90 s;
       - on every poll where the foreground is not the login window, re-assert it (SetForegroundWindow) and restart the stable clock;
       - the clock is real elapsed time (a Stopwatch), not a poll count: proceed only once the login window ('BLOOMBERG: Login', the bplus64 process, as Find-LoginWindow already identifies it) has been the foreground continuously for 2000 ms;
       - print one line per state change ("settle: lost fg to <proc>(<pid>), re-asserting", "settle: login window foreground, stable clock 2000/2000 ms after <n> ms") so the log reads the story;
       - if it never settles in 90 s: print "ABORT: focus lost before submit.", then R7's Get-FgTrace line, and exit 4 at ZERO attempts, exactly as today;
       - KEEP the last foreground check immediately before the ledger write and the click, with no sleep, no screenshot and no call between that check, the ledger write and the Click (the existing comment block states why). The settle loop is BEFORE it, never instead of it.
    2. CELL Z6-R8b, signature A (glyph calibration), bbg_verify.ps1: re-derive the reference rendering against the CURRENT build and DO NOT WIDEN the band [len-1, len]. Evidence first: collect every retained render of the correct username on the current build (the glyph-run counts the logs print: 10 on 10-06 and 10-08, 11 on 10-11, 10-13 and 10-15; plus any retained screenshots under C:\opal-elev, the BG seat logs and the logs dir) and run the existing glyph counter over them. Then state, with the numbers, whether a legitimate 10-run render can be told apart from the original border-artifact mutant (which also measures 10 and must keep failing, see the comment above $uLo). If it can, re-derive the fixture and the expected count in place and re-run the mutant battery so the mutant still fails. If it CANNOT be separated by run count alone, change nothing in bbg_verify.ps1 and report that finding with the evidence; the settle loop lands regardless. Never widen the band, never loosen the password-dot check.
    3. THE PROOF (AC1, AC2), tonight, from the WORKTREE copy, with a harness you write under org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/ (r8_thief_harness.ps1 or similar):
       - the harness first asserts Find-LoginWindow finds NO window (if one exists, it is a real Login window: exit without touching anything);
       - it creates a FAKE top-level window titled 'BLOOMBERG: Login' owned by the harness process, and a THIEF (a second window of the harness) that takes the foreground on a schedule;
       - arm RELEASE: the thief steals the foreground for about 3 s then stops; bbg_signin.ps1 -Phase submit -DryRun must settle and print "DRY-RUN: focus held at the click point";
       - arm HOLD: the thief keeps the foreground for the whole run; the same invocation must abort at about 90 s with R7's TRACE line, exit 4, and no click;
       - the harness destroys both windows at exit and leaves no process behind. Never use -Fresh, never run a fill, never touch wintrv or any Bloomberg process.
    4. LANDING, only on AC1 + AC2 PASS, only after 2026-10-15 20:00Z market close (clear) and only before 2026-10-16 09:00Z: open the NEVER-2 ledger entry FIRST
       python .tools/deploy_ledger.py open --slug opal-bbgtml-z6-r8-stable-fg-20261015 --title "OPAL_BBGTML Z6 R8: settle until the login window holds foreground, then submit" --author 0.7.0_AE_CloudOps~ZS --leg "L1|git|bbg_signin.ps1 (+ bbg_verify.ps1 only if cell R8b changed it) in the shared working tree (the deploy)|merge hash" --leg "L2|verify|AC3 on the shared tree|check output"
       commit it with its sentinel, merge with `bash .tools/safe-merge.sh zs-bbgtml-z6-r8 -m "..."`, run AC3 on the shared tree, close the entry, remove the worktree and branch. AC3 FAIL = revert the merge in the shared tree the same hour, and in any case before 10:30Z. If AC1 or AC2 does not pass by 09:00Z, DO NOT LAND: leave the branch, close nothing falsely, report which arm failed and why.
  </the_act>

  <bounds>
    - Production files: integrations/bloomberg/auth/bbg_signin.ps1 and, ONLY if cell R8b changes it, integrations/bloomberg/auth/bbg_verify.ps1. bbg_fallback.ps1, the fire-once ledger guard, the P0 gate, the sign-in ledger and its budget, the 07:30 backstop, R3's bounded re-fill and R7's trace are UNCHANGED.
    - NEVER click Login on the real Terminal, NEVER write the sign-in ledger (%USERPROFILE%\.bbg_signin_attempts.json): every submit in this order runs with -DryRun, against the harness's fake window only. NEVER touch the signed-in Terminal or any Bloomberg process. Never print, log or commit a credential, the login name or a screenshot.
    - On this box an edit to these files IS a deploy the moment it touches the shared tree (the scheduled task runs the working tree), which is why nothing lands in the shared tree before AC1 and AC2 pass on the branch.
    - Do not overwrite Positioning-pipeline or ETFS-view operations (Andrew 2026-10-14).
    - A surprise is a row in org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md (disarm_owner 2.0.0_SA_COO~ZB); keep working.
  </bounds>

  <paths>
    integrations/bloomberg/auth/bbg_signin.ps1
    integrations/bloomberg/auth/bbg_verify.ps1
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~ZS/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~ZS/task_orders/
    org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md
  </paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="Z6-R8a"><invocation>powershell -NoProfile -ExecutionPolicy Bypass -File org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/r8_thief_harness.ps1 -Arm release -Script C:/tmp/zs-z6-r8/integrations/bloomberg/auth/bbg_signin.ps1 2>&amp;1 | tee org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/z6_r8_arm_release.log; echo "exit=${PIPESTATUS[0]}"</invocation><expect>exit=0; the log shows at least one "settle: lost fg" line, then "settle: login window foreground, stable clock 2000/2000 ms", then "DRY-RUN: focus held at the click point"; the sign-in attempts count is EQUAL before and after (record both) and wintrv's process start time is EQUAL before and after (record both)</expect></criterion>
  <criterion id="AC2" cell_refs="Z6-R8a"><invocation>powershell -NoProfile -ExecutionPolicy Bypass -File org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/r8_thief_harness.ps1 -Arm hold -Script C:/tmp/zs-z6-r8/integrations/bloomberg/auth/bbg_signin.ps1 2>&amp;1 | tee org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/z6_r8_arm_hold.log; echo "exit=${PIPESTATUS[0]}"</invocation><expect>exit=4 after 85 to 95 seconds; the log shows "ABORT: focus lost before submit." followed by one TRACE line, and never "DRY-RUN:"; the sign-in attempts count is EQUAL before and after (record both) and wintrv's process start time is EQUAL before and after (record both)</expect></criterion>
  <criterion id="AC3" cell_refs="Z6-R8a"><invocation>bash org/tier1_exec/2.0.0_SA_COO~ZB/deliverables/z6_checks/r2_p0_listener_check.sh; echo "exit=$?"</invocation><expect>run on the SHARED tree after the merge: R2: PASS and exit=0 (the landed bytes still parse and R2's P0 classification still holds; no GUI)</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE as a deliverable file under org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/ and in your final message: each criterion's output (AC1 and AC2 as the log path plus the key lines and the four before/after numbers), the cell R8b evidence table (every retained render and its run count, and the explicit separable / not separable verdict), the branch, the merge hash, the ledger slug and close state, the clock time you landed, and push state as a measured value. If you did not land, say which arm failed and why. Leave the status flip to the issuer. The real-run read (the 2026-10-16 07:00 ET fire: a clean unattended sign-in, or an abort whose TRACE line names the window) is graded by the issuer, not by this order.
  </report>
</task_order>
