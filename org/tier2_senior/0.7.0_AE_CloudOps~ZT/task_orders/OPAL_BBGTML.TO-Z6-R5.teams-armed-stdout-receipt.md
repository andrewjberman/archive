<task_order>
  <metadata>
    <id>OPAL_BBGTML.TO-Z6-R5.teams-armed-stdout-receipt</id>
    <issued_by>2.0.0_SA_COO~ZB</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ZT</issued_to>
    <date>2026-10-13</date>
    <status>pending -- issued 2026-10-13 ~20:5xZ, Z6 repairs issuance (CTO ruling @61e3067f5c disposition 5); queue position 1 of 2 on this lane (R4 follows)</status>
    <project_code>OPAL_BBGTML</project_code>
  </metadata>
<risk>WORLD</risk>
# pipeline-override: flat project with no tree home (OPAL_BBGTML, org/projects/OPAL_BBGTML.json); one cell of the Z6 repairs issuance ruled by 1.0.0_SA_CTO~Z @61e3067f5c; the order is the LD-0529 carrier to a Tier-2 seat

  <objective>
    The Bloomberg seat's Teams watcher (teams-watch.py under a Monitor) prints its arm banner to stderr, which the Monitor does
    not deliver, so a healthy arm and a dead one look the same from inside the session. Add ONE stdout receipt line on a
    successful arm, and teach the seat's skill to read it.
  </objective>

  <context>
    SPEC: CTO ruling org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_OPAL_BBGTML_Z6_REPAIR_DISPOSITIONS_20261013_Z.md
    disposition 5 ("One [TEAMS-ARMED] stdout line on a successful arm ... Not a new standing process"); trace Q4.
    LIVE PRODUCTION: .claude/skills/teams-assist/teams-watch.py is (a) armed by 0.0.3_BG_BBGTerminal every ~29.5 minutes and
    (b) IMPORTED by the D7 intake runner (integrations/ticketing/intake/runner.py _load_teams_watch) every 5 minutes. The
    runner never calls main(). Saving the file IS the deploy for the next arm and the next runner pass.
    The BG seat's live watcher keeps its old bytes until its next re-arm; do NOT kill, re-arm or signal it.
    The stdout contract today: stdout lines are message events ("[TEAMS] ..."); everything else goes to stderr.
  </context>

  <the_act>
    1. Open a change-management entry BEFORE the edit:
       python .tools/deploy_ledger.py open --slug opal-bbgtml-z6-r5-teams-armed-20261013 --title "OPAL_BBGTML Z6 R5: teams-watch [TEAMS-ARMED] stdout receipt" --author 0.7.0_AE_CloudOps~ZT --leg "L1|git|teams-watch.py + bbg-teams-assist SKILL.md in the shared working tree|commit hash" --leg "L2|verify|AC1|check output"
       Commit it with its sentinel under org/critical_paths/.open_deploys/.
    2. CELL Z6-R5:
       a. .claude/skills/teams-assist/teams-watch.py main(): immediately after the existing stderr "armed" banner (line 523 at
          issue), print to STDOUT, flush=True, exactly one line:
          [TEAMS-ARMED] pid=<os.getpid()> identity=<PIN_IDENTITY or BARE> channels=<len(channels)> cursor=<cursor>
          Nothing at import time; nothing else on stdout; the "[TEAMS]" message-event format unchanged.
       b. .claude/skills/bbg-teams-assist/SKILL.md, in the arm section (lines 24-49 at issue): the first Monitor event after an
          arm is the "[TEAMS-ARMED] ..." line; it is the arm receipt, not a message (no ACK, no reply, no cursor effect); no
          "[TEAMS-ARMED]" event within 60 seconds of an arm means the watcher did not arm: census the process, re-arm.
          Correct the sentence that says the arm banner is the proof (the banner stays on stderr).
       c. Census every launcher of teams-watch.py (comp-find 'teams-watch.py' --files, read the denominator and every page) and
          name each in your report as unaffected (it ignores stdout lines it does not recognise) or as needing a line it does
          not get from this order (then file a row; do not edit it).
    3. Run AC1 on the shared tree, then close the ledger with its output.
  </the_act>

  <bounds>
    - Exactly two files: .claude/skills/teams-assist/teams-watch.py and .claude/skills/bbg-teams-assist/SKILL.md.
    - NO new standing process, no alert, no monitor, no cron (the moratorium). Never run teams-watch.py against the live cursor
      files: AC1 runs it --once against a throwaway TMPDIR.
    - Do not touch the intake runner, its config (R4's), the BG seat's processes or its inbox.
    - A surprise is a row in org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md (disarm_owner 2.0.0_SA_COO~ZB); keep working.
  </bounds>

  <paths>
    .claude/skills/teams-assist/teams-watch.py
    .claude/skills/bbg-teams-assist/SKILL.md
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~ZT/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~ZT/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~ZT/task_orders/
    org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md
  </paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="Z6-R5"><invocation>bash org/tier1_exec/2.0.0_SA_COO~ZB/deliverables/z6_checks/r5_teams_armed_check.sh; echo "exit=$?"</invocation><expect>ARM leg: rc=0 and TEAMS-ARMED_lines=1, the line naming identity=517aa5ee-b4d0-425a-b493-5a22ff77ac4f and channels=1; RUNNER leg: 0 stdout bytes on the runner's import path; R5: PASS; exit=0. The same check on the pre-edit bytes read ARM leg FAIL / RUNNER leg PASS at issue (recorded in the issuance commit) -- that is the difference control.</expect></criterion>
  <criterion id="AC2" cell_refs="Z6-R5"><invocation>git diff --stat HEAD~1 HEAD -- .claude/skills/ | tail -1</invocation><expect>run on the commit that carries the edit: 2 files changed, teams-watch.py and bbg-teams-assist/SKILL.md only</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE as a deliverable file under org/tier2_senior/0.7.0_AE_CloudOps~ZT/deliverables/ and in your final message: each
    criterion's output, the launcher census with its denominator, the commit hash, the ledger slug and close state, and push
    state as a measured value. Then start TO-Z6-R4 (same folder). Leave the status flip to the issuer.
  </report>
</task_order>
