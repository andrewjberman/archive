<task_order>
  <metadata>
    <id>OPAL_BBGTML.TO-GUARD-3.checker-series-compare-and-tripwire-recency</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~RV</issued_to>
    <date>2026-10-07</date>
    <status>complete -- merged @80bcd69f78 at 09:54Z; REPORT 1 (@2e50c18d45) and REPORT 2 (@a00f5c1b83) read; issuer's own runs: GUARD-3A PASS and GUARD-3B PASS from the merged tree, and the FIRST LIVE READ on 2026-10-07: the 07:00 ET vehicle's log reads "all 13 custom CIX series reach the as-of 2026-10-06" with LastTaskResult 0, and the 07:30 ET checker LastTaskResult 0; NEVER-2 entry closed @d75142de44; the hand-run send path (row OPAL_BBGTML-Z-S12) continues under TO-GUARD-4</status>
    <project_code>OPAL_BBGTML</project_code>
  </metadata>
<risk>WORLD</risk>
# pipeline-override: outside the canonical pipeline -- a seat act on a closed project (OPAL_BBGTML) on 1.0.0_SA_CTO~Z's fix route, ADDENDUM 6 @22a0c6aebc, on Andrew's word @1981fd223d; ONE issuance of two cells (GUARD-3a the checker, GUARD-3b the tripwire); the order is the LD-0529 carrier, not a round

  <objective>
    Close the two Bloomberg detection gaps Andrew approved. Andrew, verbatim, ~05:55Z on 2026-10-07 at the 3.0.0_SA_CVO~Z
    terminal: "Yeah we can close gap 1 with the checker compare you described, go with your recs on that matter and gap 2".
    Gap 1: the 07:30 ET checker passes while a benchmark series is days behind. Gap 2: the pull's tripwire passes while a
    custom CIX series is frozen (row OPAL_BBGTML-Z-S5).
  </objective>

  <context>
    THE SPEC is ADDENDUM 6 of org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_INDEX_BENCHMARK_FIX_ROUTE_20261006.md
    (@22a0c6aebc). Read it in full first; where this order and the addendum differ, the addendum wins. Andrew's record:
    org/tier1_exec/3.0.0_SA_CVO/deliverables/ANDREW_DIRECT_20261007_055xZ_BBG_CHECKER_SERIES_DATE_COMPARE_AND_TRIPWIRE_RECENCY_APPROVED.md.
    His lift of the integrations/bloomberg/ no-modify order covers THESE TWO EDITS ONLY.
    Read integrations/bloomberg/READ_HERE.md first (the law for any Bloomberg work). This order makes NO Bloomberg call, no
    Terminal sign-in and no pull: both proofs read objects that already exist.
    SITE-Z SCHEDULED TASKS RUN THE WORKING TREE: an edit to either file in the shared tree is live the moment it touches disk.
    So you build and prove in a linked worktree, and the merge into the shared tree is the deploy.
  </context>

  <the_act>
    Work in your OWN linked worktree cut from the shared tree's HEAD (a sparse cone is fine; it must carry .tools, lib,
    integrations/bloomberg, org/tier2_senior, org/critical_paths). Edit nothing in the shared tree before the merge.

    CELL GUARD-3a, THE CHECKER -- integrations/bloomberg/pipeline/freshness_check.py.
    1. After its existing data_as_of check, it reads each model's benchmark_last_date.index and benchmark_last_date.etf from
       the SAME served body it already read (s3://opal-data-portal-v2/json/benchmarks/model_portfolio_benchmarks.json) and
       compares each to data_as_of.
    2. A series whose date is before data_as_of raises the checker's EXISTING summons (the summon() function it already has),
       with a detail naming each model, the side (index or etf) and the two dates. No new alert, schedule, channel, file or
       recipient. A new Kind word for this summons is allowed; entry_step() must answer it.
    3. A served body in which a model carries no benchmark_last_date reads as a DISTINCT not-measured result: its own log
       word and its own exit path. It is never a PASS and never the series-behind result.
    4. The existing behaviour stays: the date check, the schedule-gap self-check, the three test flags, exit 0/2/3. State in
       your report which exit code each new result uses and why it collides with nothing.
    5. Give the series compare a pure function (body in, result out) so it is proved without S3 or a summons.

    CELL GUARD-3b, THE TRIPWIRE -- integrations/bloomberg/pipeline/tplus1/tools/bbg_pkl_tripwire.py (the copy the scheduled
    vehicle runs: scheduled_daily_pull.cmd line 39 names tplus1).
    1. For EVERY custom CIX series in the data PKL, the last non-null date equals the as-of date the tripwire already resolves
       (lib/trading_calendar). A series behind FAILS the tripwire through its existing _fail path, naming the series and its
       last date.
    2. How a custom CIX series is recognised is read from the PKL and the pull's own definitions, never typed as a list of
       names. Print the denominator: N custom CIX series graded.
    3. The control: SPX (not a custom series) is unaffected.
    The tzero copy (integrations/bloomberg/pipeline/tzero/tools/bbg_pkl_tripwire.py) DIFFERS from the tplus1 copy today and
    is NOT in this order. Do not touch it. Say in your report whether anything scheduled runs it.

    THE PROOFS, on real objects (write the proof scripts under your deliverables folder; they import the edited modules
    from your worktree and write nothing to S3):
    - 3a: both versions of the served key. VersionId Qbef40yVOC1A7F31_vikeqMQSDK198.e (2026-10-06 16:16:52Z): the
      series-behind result naming 9 series (index 2026-09-29 on 5 models, etf 2026-09-29 on 4). VersionId
      fxNfvcQ8KZE2iB5YYF64oMVyXZZcuRDe (2026-10-07 01:28:18Z): no summons, all 10 current. A planted body with the field
      removed from one model: the not-measured result. (Both VersionIds read live by the issuer at 06:2xZ.)
    - 3b: the two pulls of the 2026-10-05 data PKL the addendum names. The 2026-10-06 12:29Z pull is
      s3://opal-data-portal-v2/benchmarks/data_20261005_v1.pkl VersionId fPWS_TCLSvx2dW9SZGDl3hcQL735m5XJ (read by the
      issuer): FAIL, naming the 7 series at 2026-09-29. The 2026-10-07 01:26Z re-pull: PASS. The issuer's listing of that key
      shows ONE version, so the re-pull is NOT at that key: locate it by its time (the project output folder, or the key the
      re-pull wrote) and name where you read it. If it cannot be found, that proof arm is NOT RUN: say so and file a row; do
      not substitute a planted file for it. SPX reads PASS on both.
    - Run the existing battery (integrations/bloomberg/pipeline/freshness_check_battery.py) from your worktree and report
      its last line; it must not regress.

    THE LANDING:
    1. Commit the two edits in your worktree (one commit per cell).
    2. Open ONE NEVER-2 entry. Its legs: the merge; the first live read.
    3. Merge into the shared tree with .tools/safe-merge.sh in ONE gap, and NOT between 10:30Z and 12:00Z (the 07:00 ET
       vehicle and the 07:30 ET check). Before the merge, read that neither scheduled task is running.
    4. After the merge, from the shared tree: run the checker's --verdict-only arm and the 3a and 3b proofs once more
       against the merged bytes.
    5. The FIRST LIVE READ is the next 07:00 ET vehicle's tripwire result and the next 07:30 ET checker result, both PASS on
       current data. Read both from their logs and report them. A FAIL on CURRENT data means revert the merge the same hour
       (one revert commit of the two edits) and report. A FAIL because the data really is behind is the build working: report
       it, do not revert.
  </the_act>

  <bounds>
    - No other file under integrations/bloomberg/ is touched: not publish_to_portal.py, not the sign-in files, not
      register_daily_task.ps1, not the tzero copy, not the battery. Rows OPAL_BBGTML-Z-S1..Z-S4 stay under Andrew's order.
    - NO Bloomberg call, no Terminal sign-in, no pull, no publish, no S3 write, no schedule change.
    - No new alert, alarm, monitor, notification or recipient: the summons is the checker's existing one (the moratorium).
    - A surprise is a row in org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md (id OPAL_BBGTML-Z-S<k>, disarm_owner
      2.0.0_SA_COO~Z); keep working.
  </bounds>

  <paths>
    integrations/bloomberg/pipeline/freshness_check.py
    integrations/bloomberg/pipeline/tplus1/tools/bbg_pkl_tripwire.py
    org/tier2_senior/0.7.0_AE_CloudOps~RV/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~RV/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md
  </paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="GUARD-3a"><invocation>python org/tier2_senior/0.7.0_AE_CloudOps~RV/deliverables/guard3a_checker_proof.py; echo "exit=$?"</invocation><expect>three arms on real bodies: VersionId Qbef40yV... reads the series-behind result naming 9 series; VersionId fxNfvcQ8... reads no summons with 10 of 10 current; the planted body reads the distinct not-measured result; a last line GUARD-3A: PASS; and exit=0</expect></criterion>
  <criterion id="AC2" cell_refs="GUARD-3b"><invocation>python org/tier2_senior/0.7.0_AE_CloudOps~RV/deliverables/guard3b_tripwire_proof.py; echo "exit=$?"</invocation><expect>the 2026-10-06 12:29Z pull reads FAIL naming 7 series at 2026-09-29 with the denominator of custom CIX series printed; the 2026-10-07 01:26Z re-pull reads PASS (or NOT RUN with its reason and a row); SPX PASS on each; a last line GUARD-3B: PASS; and exit=0</expect></criterion>
  <criterion id="AC3" cell_refs="GUARD-3a GUARD-3b"><invocation>git diff --stat HEAD~2 HEAD -- integrations/bloomberg/ | tail -1</invocation><expect>run on the two cell commits in the worktree before the merge: exactly 2 files changed under integrations/bloomberg/, the two this order names</expect></criterion>
</proof_of_spec>

  <report>
    Report to 2.0.0_SA_COO~Z TWICE: once when the merge has landed and the post-merge proofs have run (each criterion's
    output, the exit codes of the new results, the merge commit, the NEVER-2 entry path, the time of the merge against the
    10:30Z-12:00Z window, the measured push state), and once after the first live read (the two log lines, and CLOSED or
    REVERTED). Leave the status flip to the issuer.
  </report>
</task_order>
