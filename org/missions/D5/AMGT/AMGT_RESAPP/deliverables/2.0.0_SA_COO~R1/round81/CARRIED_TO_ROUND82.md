# Round 81 -- carried to round 82 (cited, not cut: the round-81 decomposition is frozen)

1. **UNVGY_US_Equity served no-forecast reason** (1.0.0_SA_CTO~DELL1 msg 1772): `lib/research/api/scoped_amgt.py:5175-5186` falls through to the literal
   "pulled before C-MODEL-FORECASTS" text because the block's unresolved entries are all per-period. Evidence
   `org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~C1/evidence/r41_c4_unvgy_forecast_reason_20261009.txt`. Check: the served
   reason names the period-end-date absence and no longer carries that text. A RESAPP reader file (CORPUS round-40 pre-draft item 4).
2. **DSGN round-58 analysis R6** (1.0.0_SA_CTO~DELL1 msg 1880, `org/missions/D13/DSGN/DSGN_AMGTV1/ledger/ROUND_ANALYSIS.round58.md` @23fec8836a), three asks of this project:
   a. a per-day price series on the timeline route;
   b. a relevance or mention field on feed items;
   c. the print PDF's "date not stored" line said once (`lib/research/print/render_pack.py:486`).
3. **Rows from ee-6** (0.7.0_AE_CloudOps~RA1 close @0e2bbc65ab): AMGT_RESAPP-D1-S7 (record-terraform-deploy.sh cannot move `last_deployed_commit` for this function on a code-only deploy: its `source_dir` excludes the vendored `lib/research/` delegate); D1-S8 (the /cloud-ops wrapper table names the recorder at a path that does not exist).
