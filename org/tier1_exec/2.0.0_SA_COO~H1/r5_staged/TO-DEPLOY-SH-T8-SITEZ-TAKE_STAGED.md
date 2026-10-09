<task_order>
  <metadata>
    <id>MDPF_SECHIST.TO-DEPLOY-SH-T8.sitez-pull-take</id>
    <issued_by>2.0.0_SA_COO~H1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~Z</issued_to>
    <date>2026-10-09</date>
    <status>staged</status>
    <project_code>MDPF_SECHIST</project_code>
  </metadata>
<direct_act>true</direct_act>
<!-- STAGED, not issued: cut into task-orders/ when 1.0.0_SA_CTO~Z signs the site-Z producer half. Round-less by design: a deploy
act under a never-widen pair, not a cell (decomposition R5 row 2). -->
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECHIST/decompositions/MDPF_SECHIST_DECOMP_R5.md</decomp_doc> (round 5), row 2: SH-t-8 (as repaired by
SH-t-19) taken at site Z.
<owned_cells>SH-t-8</owned_cells>
</decomp_ref>

  <objective>
    Site Z's working tree takes ONE file, `integrations/bloomberg/pipeline/etf_daily_pull.py`, at blob
    `75342a695857a86e3a4f0c651d5febc6d66b98db` (box/dell1 @09b6a7d580, on origin), replacing blob `73735f44d6`. Do it OUTSIDE
    10:30Z-12:00Z, under a change-management ledger entry you open first and close last. Nothing else under
    `integrations/bloomberg/pipeline/` moves (Andrew's no-modify order binds every other file).
  </objective>

  <steps>
    1. Open the ledger entry (`.tools/deploy_ledger.py open`), legs: L1 take, L2 blob read, L3 first scheduled run.
    2. L1: `git fetch origin box/dell1`; `git show 09b6a7d580:integrations/bloomberg/pipeline/etf_daily_pull.py` into the working-tree file.
    3. L2: `git hash-object` on the working-tree file reads `75342a6958...`; any other value is a STOP and a restore to `73735f44d6`.
    4. L3 (the next scheduled fire, 07:00 ET): manifest `run_class` scheduled, exit 0, `history_gap_fill` and
       `history_backfill_exhausted` present, and the run log carries `history backfill exhausted count:`. Commit the evidence file.
  </steps>

  <rollback>
    Restore blob `73735f44d6` in the working tree; remove `history_gap_fill` / `history_backfill_exhausted` from manifests written
    since; drop gap-fill rows outside each run's production window; `bbg_budget` lines stay.
  </rollback>

  <context>
    Pair: COO half `org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECHIST_H1/NEVER_WIDEN_HALF_REQUEST_SECHIST_SH_T8_SITEZ_DEPLOY_20261009.md`
    (re-signed @c07670fbcf); CTO half `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_SECHIST_SH_T8_SITEZ_TAKE_20261009.md` (msg 2848);
    site-Z producer half: PENDING.
  </context>
</task_order>
