<task_order>
  <metadata>
    <id>MDPF_SECHIST.TO-VERIFY-SH-T8.sitez-pull-landing</id>
    <issued_by>2.0.0_SA_COO~H1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~Z</issued_to>
    <date>2026-10-09</date>
    <status>staged</status>
    <project_code>MDPF_SECHIST</project_code>
  </metadata>
<direct_act>true</direct_act>
<!-- STAGED, not issued. RECAST from the take order (@019edd782b) to a VERIFY on 1.0.0_SA_CTO~Z's producer half @5dfc4f27a2: blob
75342a6958 has been live in site Z's tree since box-sync 574fe5ce6b (17:09Z), row MDPF_SECHIST-Z-S2. The addressee is the site-Z lane
0.0.0_AB_MSTR~Z names (asked via 0.0.0_AB_MSTR~DELL1, msg 2992). If that lane already holds V1, this file is not issued. -->
<risk>WORLD</risk>
<proof_genre>VERIFY</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECHIST/decompositions/MDPF_SECHIST_DECOMP_R5.md</decomp_doc> (round 5), row 2: SH-t-8 (as repaired by
SH-t-19) at site Z.
<owned_cells>SH-t-8</owned_cells>
</decomp_ref>

  <objective>
    VERIFY, no file written (V1 of the site-Z half). Before the 2026-10-10 07:00 local (11:00Z) scheduled pull, open a NEVER-2 ledger entry
    that names box-sync `574fe5ce6b` as the landing of `integrations/bloomberg/pipeline/etf_daily_pull.py` at blob
    `75342a695857a86e3a4f0c651d5febc6d66b98db`. Close it on the first scheduled run's acceptance.
  </objective>

  <steps>
    1. Open the entry (`.tools/deploy_ledger.py open`) with legs L1 landing read and L2 first scheduled run.
    2. L1: record `git hash-object` on the working-tree file (must read `75342a6958...`), `git status` clean for that path, and
       `pytest integrations/bloomberg/pipeline/test_etf_daily_pull_history_plan.py` (13 passed).
    3. L2, after the 07:00 local fire: manifest `run_class` scheduled, exit 0, `history_gap_fill` and `history_backfill_exhausted` present,
       and the run log carries `history backfill exhausted count:`. Write the evidence file and close the entry.
    4. Any acceptance failure: roll back before the next 07:00 run (below) and report.
  </steps>

  <rollback>
    Restore blob `73735f44d6` with a new commit on `box/sitez` (never a rebase); remove the two new manifest fields and any gap rows
    outside each run's window; `bbg_budget` lines stay.
  </rollback>

  <rules>
    V2: nothing else under `integrations/bloomberg/pipeline/` moves (Andrew's no-modify order).
  </rules>
</task_order>
