<task_order>
  <metadata>
    <id>OPAL_BBGTML.TO-Z6-G4M.guard4-merge-tzero-tripwire-cix</id>
    <issued_by>2.0.0_SA_COO~ZB</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ZS</issued_to>
    <date>2026-10-14</date>
    <status>pending -- issued 2026-10-14 ~10:0xZ on CTO ruling @d8c5d77e26 (call 2da6 closed; Andrew ~09:0xZ "There should be no hold"); runs AFTER 12:30Z today; TO-Z6-R3 on this lane stays PARKED</status>
    <project_code>OPAL_BBGTML</project_code>
  </metadata>
<risk>WORLD</risk>
# pipeline-override: flat project with no tree home (OPAL_BBGTML, org/projects/OPAL_BBGTML.json); one deploy cell ruled by 1.0.0_SA_CTO~Z @d8c5d77e26; the order is the LD-0529 carrier to a Tier-2 seat

  <objective>
    Merge branch rv-bbgtml-guard4 @3b65362444 into box/sitez. GUARD-4 ports the per-series custom-CIX recency check into the
    T-zero PKL tripwire, the one publish_to_portal.py runs before every publish. Today the publish leg's tripwire prints no
    custom-CIX line while the pull leg's tplus1 copy grades 13 of 84 series (trace Q5), so a stale custom CIX series can be
    published. The tripwire is the PUBLISH GATE: a stricter check can stop a publish, so this merge is a deploy.
  </objective>

  <context>
    SPEC: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_2DA6_GUARD4_MERGE_NO_HOLD_20261014_Z.md @d8c5d77e26. Read it first.
    The built cell and its branch proof: org/tier2_senior/0.7.0_AE_CloudOps~RV/task_orders/OPAL_BBGTML.TO-GUARD-4.tzero-tripwire-cix-recency-port.md
    and, on the branch, org/tier2_senior/0.7.0_AE_CloudOps~RV/deliverables/TO_GUARD_4_REPORT_TZERO_PORT_20261007.md.
    MEASURED by the issuer ~09:5xZ: `git diff --name-only HEAD...rv-bbgtml-guard4` = 3 files (bbg_pkl_tripwire.py +87, the report,
    the proof script); `git log 3b65362444..HEAD -- integrations/bloomberg/pipeline/tzero/tools/bbg_pkl_tripwire.py` = 0 commits, so
    the merge is clean on that file; the branch is LOCAL only (no origin ref), checked out in LOCKED worktree C:/tmp/rv-guard4.
    The lane gate (owned-paths-validate on HEAD bytes) PERMITS this seat on all three files.
    How the publish runs it: integrations/bloomberg/pipeline/publish_to_portal.py:64 TRIPWIRE = tzero/tools/bbg_pkl_tripwire.py,
    :156 `[sys.executable, TRIPWIRE, outdir, "--date", stamp]`, outdir = <project>/output, project default
    ~/OneDrive - Opal Capital/Shared - Documents/OCIO Models/Dashboard/202511 Model Portfolio Exposure (:66-70) or BBG_PROJECT_ROOT.
    Andrew's binding aim (10-06, verbatim): avoid "accidentally overwriting any operations in the 'Positioning' pipeline and ETFS
    view operations". This merge adds one check to the gate and overwrites no operation.
  </context>

  <the_act>
    WINDOW: start no step before 2026-10-14 12:30Z (the 07:00 ET pull, OPAL_BBGTML_daily_pull, runs 11:00Z and publishes through
    this file; nothing may race it). Before starting, read today's pull log (%USERPROFILE%/opal_bbg_logs/bbg_tplus1_20261014_*.log)
    and record its RESULT line and the vintage it published.
    1. Open the change-management entry FIRST:
       python .tools/deploy_ledger.py open --slug opal-bbgtml-guard4-merge-20261014 --title "OPAL_BBGTML GUARD-4 merge: T-zero tripwire gains the per-series custom-CIX recency check" --author 0.7.0_AE_CloudOps~ZS --leg "L1|git|merge rv-bbgtml-guard4 @3b65362444 into box/sitez (the deploy)|merge hash" --leg "L2|verify|AC1 real T-zero tripwire run on today's PKLs|run output"
       Commit the entry and its sentinel.
    2. Merge: `bash .tools/safe-merge.sh rv-bbgtml-guard4 -m "drain(OPAL_BBGTML GUARD-4): merge rv-bbgtml-guard4 @3b65362444 -- T-zero tripwire custom-CIX recency check (ruling @d8c5d77e26)"`.
       Pull-merge, never rebase. Read the merge back on box/sitez (AC2).
    3. The ONE REAL RUN (AC1): the shared tree's T-zero tripwire on today's PKLs, with the same interpreter the publish leg uses
       (read it from today's pull log or scheduled_daily_pull.cmd) and today's published vintage as --date.
    4. PASS -> close the ledger with both outputs, then unlock and remove worktree C:/tmp/rv-guard4
       (`git worktree unlock C:/tmp/rv-guard4` then `git worktree remove C:/tmp/rv-guard4`) and delete the branch, which is now
       contained in box/sitez. FAIL on real data -> in the SAME act revert the merge (`git revert -m 1 <merge>` via safe-commit),
       confirm the tripwire reads as before, close the ledger as rolled back, file a row with the failing series, and keep the
       branch and worktree. Never relax the check in place.
  </the_act>

  <bounds>
    - The merge brings exactly the 3 files above. No other edit: not publish_to_portal.py, not the tplus1 copy, not a pin, not
      the notebooks, the upload path, the schedule or any Positioning or ETFS-view operation.
    - NO publish, NO upload, NO /data-refresh call, NO Bloomberg request: AC1 reads PKLs already on disk.
    - A surprise is a row in org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md (disarm_owner 2.0.0_SA_COO~ZB); keep working.
  </bounds>

  <paths>
    integrations/bloomberg/pipeline/tzero/tools/bbg_pkl_tripwire.py
    org/tier2_senior/0.7.0_AE_CloudOps~RV/deliverables/TO_GUARD_4_REPORT_TZERO_PORT_20261007.md
    org/tier2_senior/0.7.0_AE_CloudOps~RV/deliverables/guard4_tzero_tripwire_proof.py
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~ZS/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~ZS/task_orders/
    org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md
  </paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="Z6-G4M"><invocation>"&lt;publish-leg python&gt;" integrations/bloomberg/pipeline/tzero/tools/bbg_pkl_tripwire.py "&lt;project&gt;/output" --date &lt;today's published vintage YYYYMMDD&gt;; echo "exit=$?"</invocation><expect>run on the shared tree after the merge, after 12:30Z: a "custom CIX series" line with its graded denominator printed (the line the pre-merge T-zero copy never printed -- the difference control), "RESULT: PASS", exit=0</expect></criterion>
  <criterion id="AC2" cell_refs="Z6-G4M"><invocation>git merge-base --is-ancestor 3b65362444 HEAD; echo "contained=$?"; git diff --stat HEAD~1 HEAD -- integrations/bloomberg/ | tail -1</invocation><expect>contained=0, and the merge commit changes exactly 1 file under integrations/bloomberg/ (the T-zero tripwire)</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE as a deliverable file under org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/ and in your final message: today's
    pull RESULT and vintage, both criteria's output, the merge hash, the ledger slug and close state, the worktree/branch disposal,
    and push state as a measured value. Leave the status flip to the issuer.
  </report>
</task_order>
