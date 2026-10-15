<task_order>
  <metadata>
    <id>OPAL_BBGTML.TO-Z6-R7.focus-abort-foreground-trace</id>
    <issued_by>2.0.0_SA_COO~ZB</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ZS</issued_to>
    <date>2026-10-15</date>
    <status>pending -- issued 2026-10-15 ~11:4xZ on CTO ruling @701a4c705a (org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_OPAL_BBGTML_FOCUS_DEFECT_OWNER_20261015_Z.md) after the 11:00Z fire ran R3's code and aborted again. Build and exercise on a branch now; LAND only outside 10:30Z-12:30Z (so not before 12:30Z today).</status>
    <project_code>OPAL_BBGTML</project_code>
  </metadata>
<risk>WORLD</risk>
# pipeline-override: flat project with no tree home (OPAL_BBGTML, org/projects/OPAL_BBGTML.json); one repair cell ruled by 1.0.0_SA_CTO~Z @701a4c705a; the order is the LD-0529 carrier to a Tier-2 seat

  <objective>
    The unattended sign-in has produced 0 successes since 2026-08-18. R2 and R3 (two blind changes to window focus) did not hold: at the
    11:00Z fire on 2026-10-15 the focus re-assert took 0 of 3, the one bounded re-fill failed the same check ("ABORT: focus did not take
    (fg=32116010 != 266432)"), and the pull ended rc=50. Stop guessing. Make every focus-related abort RECORD what holds the foreground and what
    state the session is in, so the fix is cut from evidence.
  </objective>

  <context>
    SPEC: the CTO ruling above, item 2: "The cell records what has the foreground at each abort: the foreground window's title and process, and
    whether the session is locked, disconnected or console. The fallback logs that at the moment of failure, through the existing escalation line
    only, with no new standing process." Zero Bloomberg attempts stays a hard constraint.
    EVIDENCE: C:\Users\Opal Bloomberg\opal_bbg_logs\bbg_tplus1_20261015_070001.log lines 15, 27-36; C:\opal-elev\bbg_fallback_ESCALATION.txt (13 entries
    since 08-17); surprise row OPAL_BBGTML-Z-S22. Landed code: R3 @3dad54c56f (the 3-try re-assert and one bounded re-fill stay as they are).
    Read integrations/bloomberg/READ_HERE.md section 2 first. The Terminal is signed out now and Andrew's sign-in is listed as a site Z open-call
    act (sitez-20261015T112146Z-f6f4); his sign-in may happen at any moment, so this order touches no Terminal window and no Login window.
  </context>

  <the_act>
    0. Own linked worktree from the shared tree's HEAD: git worktree add -b zs-bbgtml-z6-r7 C:/tmp/zs-z6-r7 HEAD
    1. CELL Z6-R7, in the worktree:
       a. integrations/bloomberg/auth/bbg_signin.ps1: add a function that builds ONE ASCII line
          "TRACE fgproc=<process name>(<pid>) fgtitle='<foreground window title, at most 60 chars, non-ASCII dropped, single quotes removed>'
           loginhwnd=<login window handle or none> sess=<this process's session id> console=<active console session id>
           state=<Active|Disconnected|other, from the session's connection state> locked=<y|n>"
          and print it at EVERY focus-related abort ("ABORT: focus lost before submit", "ABORT: focus did not take", and the re-assert exhaustion),
          immediately before the abort's exit. Hints, not binding: GetForegroundWindow + GetWindowThreadProcessId + Get-Process;
          WTSGetActiveConsoleSessionId; `quser`/`query session` or WTSQuerySessionInformation for the state; locked = a LogonUI.exe process in
          the session. If a field cannot be read, print it as "unreadable", never omit it.
       b. integrations/bloomberg/auth/bbg_fallback.ps1: capture the last "TRACE " line from the bbg_signin.ps1 output it already pipes through Say,
          and append it to the message of the existing Escalate(...) call on the rc=4 and fill-not-verified paths. NO new file, NO new process,
          NO new scheduled task: the trace rides the existing escalation line only. Add a TEST-ONLY switch -TraceTest: it runs the trace function
          once against the CURRENT foreground, calls Escalate with a "TRACE-TEST" prefix, and exits 0 without touching the Terminal, any Login
          window, the sign-in ledger or bbg_signin.ps1's fill/submit. Add a TEST-ONLY env var BBG_ESCALATION_PATH that, when set, redirects
          Escalate's file write (default unchanged: C:\opal-elev\bbg_fallback_ESCALATION.txt), so the test never adds a fake entry to the real file.
       c. Nothing else changes in either file.
    2. THE EXERCISE (AC1, AC2), from the WORKTREE copy, any time (it touches no Terminal): no precondition on dapi_check.
    3. LANDING, only on AC1 + AC2 PASS and only when the clock is NOT between 10:30Z and 12:30Z: open the ledger entry
       python .tools/deploy_ledger.py open --slug opal-bbgtml-z6-r7-focus-trace-20261015 --title "OPAL_BBGTML Z6 R7: foreground trace at each focus abort" --author 0.7.0_AE_CloudOps~ZS --leg "L1|git|bbg_signin.ps1 + bbg_fallback.ps1 in the shared working tree (the deploy)|merge hash" --leg "L2|verify|AC3 on the shared tree|check output"
       commit it with its sentinel, merge with `bash .tools/safe-merge.sh zs-bbgtml-z6-r7 -m "..."`, run AC3 on the shared tree, close the entry,
       remove the worktree and branch. AC3 FAIL = revert the merge in the shared tree the same hour.
  </the_act>

  <bounds>
    - Exactly two production files: integrations/bloomberg/auth/bbg_signin.ps1 and integrations/bloomberg/auth/bbg_fallback.ps1.
    - NEVER click Login, NEVER write the sign-in ledger (%USERPROFILE%\.bbg_signin_attempts.json), NEVER run a fill or submit, NEVER touch a Terminal
      or Login window or bbcomm.exe. The trace reads the foreground only. Never print, log or commit a credential, the login name or a screenshot.
    - No change to the fire-once ledger guard, the P0 gate, the verify logic, R3's re-assert or re-fill logic, or the scheduled task.
    - Do not overwrite Positioning-pipeline or ETFS-view operations (Andrew 2026-10-14).
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
  <criterion id="AC1" cell_refs="Z6-R7"><invocation>BBG_ESCALATION_PATH=C:/tmp/zs-z6-r7/trace_test_escalation.txt powershell -NoProfile -ExecutionPolicy Bypass -File C:/tmp/zs-z6-r7/integrations/bloomberg/auth/bbg_fallback.ps1 -TraceTest; echo "exit=$?"; grep -c -E "TRACE fgproc=[^ ]+\([0-9]+\) fgtitle='[^']{0,60}' loginhwnd=[^ ]+ sess=[0-9]+ console=[0-9]+ state=[^ ]+ locked=(y|n)" C:/tmp/zs-z6-r7/trace_test_escalation.txt</invocation><expect>exit=0 and the grep count is exactly 1</expect></criterion>
  <criterion id="AC2" cell_refs="Z6-R7"><invocation>powershell -NoProfile -Command "(Get-Content $env:USERPROFILE\.bbg_signin_attempts.json -Raw | ConvertFrom-Json).attempts.Count"</invocation><expect>run once immediately before AC1 and once immediately after: the two counts are EQUAL, and the file C:\opal-elev\bbg_fallback_ESCALATION.txt has the same line count before and after (the test spent no attempt and added no fake entry). Record all four numbers.</expect></criterion>
  <criterion id="AC3" cell_refs="Z6-R7"><invocation>bash org/tier1_exec/2.0.0_SA_COO~ZB/deliverables/z6_checks/r2_p0_listener_check.sh; echo "exit=$?"</invocation><expect>run on the SHARED tree after the merge: R2: PASS and exit=0 (the landed bytes still parse and R2's P0 classification still holds; no GUI)</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE as a deliverable file under org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/ and in your final message: each criterion's output
    (AC1 with the matched trace line, which holds no credential), the branch, the merge hash, the ledger slug and close state, and push state as a
    measured value. If you built and exercised but could not land inside the window, say so and when you will land. Leave the status flip to the issuer.
    The real-run read (the TRACE text on the next failed fire's escalation line, or a clean sign-in) is graded by the issuer, not by this order.
  </report>
</task_order>
