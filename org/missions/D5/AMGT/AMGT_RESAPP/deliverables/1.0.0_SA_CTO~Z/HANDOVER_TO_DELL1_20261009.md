# AMGT_RESAPP -- HAND-OVER to DELL1 (`1.0.0_SA_CTO~Z` to `1.0.0_SA_CTO~DELL1`), 2026-10-09 ~01:2xZ

**Order:** Andrew-direct ~22:5xZ 2026-10-08, record
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261008_225xZ_AMGT_DSGN_RIVALS_TO_DELL1_AFTER_ROUND_CLOSE_AND_BBG_CENSUS.md`
@b7361ceb2a. **Census:** `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_DELL1_MOVE_BBG_AND_LOCAL_DEPENDENCY_CENSUS_20261008.md`
@6a308cd424. Written to `1.0.0_SA_CTO~DELL1`'s term (1).

## State at hand-over

| item | value |
|---|---|
| tree row | `org/missions/D5/AMGT/AMGT_RESAPP/project.json`: `active`, `EXECUTING`, `fabric: site-z`, `coo_lane: 2.0.0_SA_COO~Z`; CVO `3.0.0_SA_CVO~Z`. DELL1 re-places it at L3 and sets `fabric: dell1` |
| PRD | `prd/AMGT_RESAPP_PRD.md` v0.41 @b5f90bbf8d: ADMITTED; ratified-text half SIGNED by `3.0.0_SA_CVO~Z`, current |
| last round | **79 CLOSED**: 8 of 8 terminal; cc-8 AC3 PASS (slug 32207, `ADJUDICATION_v97.md` @5d75eaf8fd); analysis `ledger/ROUND_ANALYSIS.round79.md` with round 80's enrichment list |
| open orders | `to-check --all --project AMGT_RESAPP` reads **175 ACTIVE**. With every round's orders terminal per the issuer (msg 32134), this is the stale-first-tag reading. **DELL1's COO reconciles it first**, from each order's LAST `<status>` |
| open deploy ledgers | none (read 01:1xZ). cc-7's pair is closed and its ledger CLOSED @42700562a4 |
| site-Z CTO halves in force | none unspent |
| site-Z-only file | **`C:/tmp/cc7-r79-63f0605039.zip` (42 MB)**, the kept build zip and the next build's `AMGT_DEPLOYED_ZIP` (msg 32149). DELL1 rebuilds it from the pinned commit; it is not carried as a file |

## Site-Z producers (census; they stay on site Z)

- The **price leg** (`price_axis_pull.py` + `price_series_persist.py`) writes Lead Panel prices to DynamoDB `opal-harvest-security-metrics`.
  It is a leg of the 11:00Z daily Bloomberg pull (`integrations/bloomberg/pipeline/scheduled_daily_pull.cmd:352-387`) and runs
  only while the Terminal is up; on 2026-10-08 it was skipped (rc 50, Terminal signed out).
- **`pull_consumer.py`**, the page-refresh queue consumer, stays on the box (PRD `:1390-1392`).
- **Hand-run Bloomberg pulls** (`model_block_pull`, `research_pulls`, `price_history_pull`, `pull_baba_daily_px`, the management
  fallback, `scores/robustness.py`, `filings/battery.py`). A DELL1 seat asks a site-Z seat to run them.
- The **`bloomberg` MCP health check** and the **pull log** `%USERPROFILE%\opal_bbg_logs` are site Z only. DELL1 graders read the
  S3/DynamoDB outputs or a relay.
- **A DELL1 change to any producer path is a site-Z deploy** under a never-widen pair, with `1.0.0_SA_CTO~Z`'s half signed before
  the merge (`1.0.0_SA_CTO~DELL1` msg 1267). The daily pull runs site Z's working tree, which box-sync moves.
- **`opal-amgt-scoped-api`** deploys from site Z's tree by `0.7.0_AE_CloudOps~Z`. Its next deploy populates its source-map record
  (analysis R5).

## The walker (analysis R4)

The UI walker account is one identity across boxes. A DELL1 walk starts only after `ui_walker_account.py status` reads disarmed,
and it files BLOCKING and stops if another holder arms it.

## Acts only Andrew can do (cited)

- Lifting his 2026-09-15 hold on the news collection's mechanism and cadence (FWD-16).

-- 1.0.0_SA_CTO~Z
