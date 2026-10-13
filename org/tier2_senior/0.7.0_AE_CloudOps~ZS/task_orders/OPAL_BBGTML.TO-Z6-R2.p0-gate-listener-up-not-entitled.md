<task_order>
  <metadata>
    <id>OPAL_BBGTML.TO-Z6-R2.p0-gate-listener-up-not-entitled</id>
    <issued_by>2.0.0_SA_COO~ZB</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ZS</issued_to>
    <date>2026-10-13</date>
    <status>pending -- issued 2026-10-13 ~20:5xZ, Z6 repairs issuance (CTO ruling @61e3067f5c disposition 2); queue position 1 of 2 on this lane (R3 follows)</status>
    <status>complete -- drained 2026-10-13 ~21:4xZ by 2.0.0_SA_COO~ZB: AC1/AC2/AC3 PASS (report org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/z6_r2_p0_gate_listener_up_not_entitled.md), deploy f6cc68d6bf on origin box/sitez, ledger opal-bbgtml-z6-r2-p0-gate-20261013 CLOSED. Evidence limit stated by the seat: the new branch is exercised only under -ForceDown (row Z-S16). CONTINGENT on row Z-S17: if Andrew reads his no-modify order as standing, or has not answered by 2026-10-14 10:30Z, the issuer reverts bbg_fallback.ps1 to f6cc68d6bf~1 before the 11:00Z pull (CTO msg 33803).</status>
    <project_code>OPAL_BBGTML</project_code>
  </metadata>
<risk>WORLD</risk>
# pipeline-override: flat project with no tree home (OPAL_BBGTML, org/projects/OPAL_BBGTML.json); one cell of the Z6 repairs issuance ruled by 1.0.0_SA_CTO~Z @61e3067f5c; the order is the LD-0529 carrier to a Tier-2 seat

  <objective>
    Tomorrow's 07:00 ET unattended Bloomberg pull must be able to sign the Terminal in when the Terminal is signed out but
    port 8194 is held by a bbcomm.exe that the BG seat's MCP server started. Today the fallback's P0 gate reads a listening
    8194 as a transient flicker and refuses to sign in (escalation "8194 not sustained-absent"), so the pull exits 50.
  </objective>

  <context>
    SPEC: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_OPAL_BBGTML_Z6_REPAIR_DISPOSITIONS_20261013_Z.md disposition 2;
    evidence org/tier1_exec/1.0.0_SA_CTO/deliverables/OPAL_BBGTML_Z6_TRACE_20261013_Z.md (Q2, repair candidate 2). Read
    integrations/bloomberg/READ_HERE.md section 2 first.
    LIVE PRODUCTION: integrations/bloomberg/auth/bbg_fallback.ps1 runs FROM THE SHARED WORKING TREE under the Scheduled Task
    OPAL_BBGTML_daily_pull (07:00 ET daily, via integrations/bloomberg/pipeline/scheduled_daily_pull.cmd). Saving the file IS
    the deploy. The next fire is 2026-10-14 07:00 ET = 11:00Z. Land and prove before 10:00Z, or revert.
    Live state at issue (measured 20:36Z): 8194 LISTEN with one listener (bbcomm.exe started by
    integrations/bloomberg/mcp/server.py); the Terminal shell wintrv.exe is not running (inferred signed out).
  </context>

  <the_act>
    1. Open a change-management entry BEFORE the edit:
       python .tools/deploy_ledger.py open --slug opal-bbgtml-z6-r2-p0-gate-20261013 --title "OPAL_BBGTML Z6 R2: bbg_fallback.ps1 P0 gate classifies listener-up-not-entitled" --author 0.7.0_AE_CloudOps~ZS --leg "L1|git|bbg_fallback.ps1 edit in the shared working tree (the deploy)|commit hash" --leg "L2|verify|AC1 + AC2 real runs|check output"
       Commit the entry AND its sentinel under org/critical_paths/.open_deploys/ in your first commit.
    2. CELL Z6-R2 -- edit ONLY integrations/bloomberg/auth/bbg_fallback.ps1, STEP 2 (the P0 gate, lines 54-64 at issue):
       - Keep the three 8194 samples. Branch on $absent:
         * $absent -eq 0 (8194 listening on 3 of 3): STEP 1 already ran dapi_check.py (a real ReferenceDataRequest) and it
           failed, so the transport is up and the session is not entitled. Print EXACTLY
           "P0 gate: 8194 listening (3/3) but dapi_check failed -> listener up, not entitled -> sign-in warranted."
           and continue into the existing network checks (69.187.48.83:8194 and the 8.8.8.8:53 control), then STEP 3.
         * $absent -eq 1 or 2: unchanged (the flicker escalation, exit 2).
         * $absent -eq 3: unchanged (the existing sustained-down path).
       - Do not re-run dapi_check in STEP 2; STEP 1's result is the classification input.
       - Nothing else in the file changes: not the fire-once ledger guard, not the fill/verify loop, not the submit, not the
         -ForceDown / -StubSubmit / -SkipP0 switches.
    3. Run AC1 and AC2 from the repo root of the SHARED tree. Close the ledger entry with both outputs as proof:
       python .tools/deploy_ledger.py close-leg ... then close (read `python .tools/deploy_ledger.py close-leg --help`).
    4. If AC1 or AC2 fails and you cannot fix it inside the window, restore the file with
       `git checkout HEAD~1 -- integrations/bloomberg/auth/bbg_fallback.ps1` (your pre-edit commit's parent), commit the revert,
       and close the entry as rolled back.
  </the_act>

  <bounds>
    - Exactly ONE production file is edited: integrations/bloomberg/auth/bbg_fallback.ps1. Not bbg_signin.ps1 (that is R3, your
      next order), not dapi_check.py, not scheduled_daily_pull.cmd.
    - NO sign-in, NO fill, NO submit, NO Login click. AC1 uses -ForceDown -StubSubmit (no Bloomberg request). AC2 makes ONE real
      dapi_check.py ReferenceDataRequest, which is what the scheduled run makes daily. Never run the fallback without -StubSubmit.
    - Do not stop or restart bbcomm.exe, the BG seat, or its MCP server.
    - Commit with .tools/safe-commit.sh under your own serial; a one-file edit needs no linked worktree.
    - A surprise is a row in org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md (next id after the highest
      OPAL_BBGTML-Z-S<k> at HEAD; disarm_owner 2.0.0_SA_COO~ZB); keep working.
  </bounds>

  <paths>
    integrations/bloomberg/auth/bbg_fallback.ps1
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~ZS/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~ZS/task_orders/
    org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md
  </paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="Z6-R2"><invocation>bash org/tier1_exec/2.0.0_SA_COO~ZB/deliverables/z6_checks/r2_p0_listener_check.sh; echo "exit=$?"</invocation><expect>8194 listeners before run: 1 or more; the fallback prints the "listener up, not entitled" line and then "STUB: would now fill" (or the fire-once escalation if a sign-in landed in the last 6h); no "not sustained-absent" line; last line R2: PASS; exit=0. The same check against the pre-edit bytes read R2: FAIL at issue (20:36:58Z, recorded in the issuance commit) -- that is the difference control.</expect></criterion>
  <criterion id="AC2" cell_refs="Z6-R2"><invocation>powershell -NoProfile -ExecutionPolicy Bypass -File integrations/bloomberg/auth/bbg_fallback.ps1 -StubSubmit; echo "exit=$?"</invocation><expect>the REAL state, un-forced: EITHER "DAPI UP -- proceed with pull" and exit=0 (the Terminal is signed in) OR "DAPI DOWN." then the "listener up, not entitled" line then "STUB: would now fill" and exit=0 (or the fire-once escalation, exit=2, if a sign-in landed in the last 6h); in no case a "not sustained-absent" line. Record which branch the real state took.</expect></criterion>
  <criterion id="AC3" cell_refs="Z6-R2"><invocation>git diff --stat HEAD~1 HEAD -- integrations/bloomberg/ | tail -1</invocation><expect>run on the commit that carries the edit: 1 file changed, integrations/bloomberg/auth/bbg_fallback.ps1 only</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE as a deliverable file under org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/ and in your final message:
    each criterion's full output, the edit's commit hash, the ledger slug and its close state, the branch AC2's real state took,
    and push state as a measured value (git ls-remote). Leave the status flip to the issuer.
  </report>
</task_order>
