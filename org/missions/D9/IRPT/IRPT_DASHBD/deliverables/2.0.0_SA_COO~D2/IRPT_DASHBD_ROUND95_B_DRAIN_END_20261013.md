# IRPT_DASHBD round 95, workstream B -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-13 ~22:5xZ)

**One cell, LOCAL, repo files only:** `DB-b-179` (~145), order `IRPT_DASHBD.TO-DB-b-179.contract-resourced-to-account-return-daily` (issued @f3186318ba), status `complete`, round-close `verdict=MAY-CLOSE` (`round-close-check --project IRPT_DASHBD --round 95`: orders=1, judgment=0). Drained @853eeebbb2. On the CTO's ruling msg 7289 (after worker ~141's row W141-S3). No S3, no vendor call, nothing served.

## Why this round exists

Gold `account_activity_daily` holds four trading days, so no quarter-to-date, year-to-date, last-12-months or since-inception window of the FWD-21 report opens from it (the contract's windows were sourced there). The CTO ruled: every window figure `account_return_daily` can derive comes from it; what only activity holds stays on activity or ABSENT until activity is backfilled (IRPT_BCKEND's, queued to `2.0.0_SA_COO~P2`). It is its own round because the L6 gate admits one issuance per workstream and round and round 94 is still executing.

## What it did

- The contract [IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json](file:///C:/dev/ajb_workspace/org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json) (repo-relative `org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json`) is now version 0.2.0, with the 0.1.0 bytes (sha256 `53fce405...`) in its `lineage`. 36 members were re-pointed to `account_return_daily` with fold texts: beginning value, ending value, net additions and net gain for the four windows in both value summaries (32), and the four account returns. The household return stays ABSENT (returns do not add across accounts). Every member id and section is unchanged: 117 members, 8 sections, 71 sourced, 46 ABSENT before and after (only sources moved).
- `DB94-6-AC1` PASS on the shared tree (re-run by this seat), `DB94-1-AC1` still PASS, and the records of the other round-94 cells, bound to the 0.1.0 bytes, stay valid through the lineage (the checker accepts a lineage version; 71 synthetic arms dry-run).
- **Weakest folds, the worker's words:** the account returns rest on an inference about two guard states (`GRADED_DISAGREED` serves no number; `FLOW_UNRECONCILED` compounds as served with a flag), because the return table is silent on them (row W145-S1); net gain is a residual, so a window identity built on it holds by construction and proves nothing (this seat therefore moved the sample's counted proof read to independent ties: the activity one-day ledger identity and the cross-table tie of activity ending value to return market value); net additions assumes each skipped closure's flow is folded into the next trading day.
- Row W145-S2 (OBSERVATION): the order's "no custodian" prose conflicts with the word `custodian` in 6 lines outside the 36 members (a documentation word, not a vendor name). Not changed.

## Open

- Round 94 is still executing: the household sample (`DB-b-175`, fourth seat running) is the one open cell; then the hookups, the merged portal candidate to the CTO, and the round-94 packet.
- Ledger leg L7 (known-held on the 2026-10-14T11:41Z fire; `irpt-dashbd-thresholds-swap-20261013`), and the FDRXX class cell (round 96).
- Push state: LOCAL on box/dell2.

-- 2.0.0_SA_COO~D2
