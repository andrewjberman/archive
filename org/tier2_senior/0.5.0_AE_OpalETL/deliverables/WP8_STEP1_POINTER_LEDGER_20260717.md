# WP8-DECOM step 1 -- the LIVE POINTER LEDGER (2026-07-17 ~18:1xZ)

**Filed by:** 0.5.0_AE_OpalETL, leading WP8-DECOM per Andrew-direct ~17:55Z ("Approve, start
now", record @ 6024e85ed). Denominator: comp-grep full-repo sweep (22,361 files scanned) +
the live IAM census (209 roles + 30 policies) + the live scheduler/rule listing + the D0
census (07-16). Every row has an owner and a close-mechanism.

## A. LIVE INFRASTRUCTURE POINTERS

| # | Pointer | State | Owner | Closes via |
|---|---|---|---|---|
| A1 | SI2 chain (canonical-schwab-si2-download 08:35/20:35Z; -08335338-pull 09:45/21:45Z; -08242234-pull 10:15/22:15Z) writing the staging trees | **ACTIVE WRITER, by design** | 0.6.2 (SERIAL DEAD -- COO routes to MSTR spawn-w/-first-tasking) | D1 (two clean cycles of the L5b repoint @ eac5476c1: cycle 1 = 07-18 ~09:46Z, cycle 2 = 07-19 -- CTO ruling 180551Z: this morning's fire = NOT-A-CYCLE, pre-repoint) + the chain's own re-home (0.6.2 cell) |
| A2 | IAM: 6 grant carriers (censused 07-17, incl. the fan-in deny fence + 2 ruling-pending-prefix roles) | measured | me (execution) / CTO (gate) | D5 removal battery |
| A3 | Event notifications | **NONE** (measured 07-16) | -- | already clean |
| A4 | comp-freshness | **NO live config row** -- help-example only; fixed to monolith fact_rps path this commit | me | **CLOSED THIS COMMIT** (the redirect-map row was authored against a config that turned out not to exist) |

## B. LIVE-CODE POINTERS (repo, non-doc)

| # | Pointer | State | Owner | Closes via |
|---|---|---|---|---|
| B1 | conv-seven converters (acc/rps/trn/lots->uln/ult/rld) | **REPOINTED to monolith 0824 TODAY** @ eac5476c1, parity-proven 6 tables | DS~A (done) / CTO (D1 gate) | D1 two clean cycles |
| B2 | /49-schwab-conv manual-bridge family: sync_schwab_onedrive_to_s3.py, rps_ingestion.py, convert_schwab_uln_to_silver.py (legacy, superseded by lots_to_silver) -- live literals, NO scheduler, DORMANT | dormant | CTO/DS (the standing trn_nna disposition) | skill + scripts retire on the trn_nna ruling; D5 doc-sweep tombstones |
| B3 | trn_nna consumer path (03_silver/TRN_NNA -> C_01.canonical_nna gold; enrich_transactions diagnostic) | the ONE uncovered feed (07-16 retirement AC) | CTO/DS ruling -- ask routed via COO (DS-base dead; DS~A mid-P2-landing, sequence behind) | trn_nna disposition -> then B2 retires whole |
| B4 | Dormant one-shots: diagnostics/_schwab_*, archive/process_schwab_uln_batch, analysis/w4_0824_column_census, test_crs_reader | dormant, no schedulers | me | D5 doc-sweep (tombstone or retarget headers) |

## C. DOC/RECORD POINTERS

| # | Pointer | Count | Closes via |
|---|---|---|---|
| C1 | .md references workspace-wide | 133 hits | D5 doc-sweep (post-D6 they become historical-correctly) |
| C2 | TAXSMA PRD/doc rows (~A, off-fabric sovereign delegate) | per D0 map | via COO to Andrew's board (COO mechanics 180218Z) -- doc-class, not execution-blocking |

## D. WHAT CHANGED vs THE 07-16 REDIRECT MAP

1. The conv-seven repoint (map rows 1-2, the L5b vehicle) LANDED today @ eac5476c1 -- D1 clock
   starts tomorrow (CTO: a clean-cycle count including a pre-change fire is the injected-column
   class).
2. The comp-freshness row (my cell) was a phantom -- help-example only, fixed in this commit.
3. 0.6.2's SI2-code-home cell + DS's B_02 cell: OWNERS CURRENTLY DEAD/BUSY -- asks routed via
   COO on SEND per his 180218Z mechanics, not burned against empty inboxes.
4. Everything else in the D0 map holds unchanged.

## E. THE CRITICAL PATH TO D6 (as of tonight)

trn_nna disposition (CTO/DS) + SI2 chain re-home (0.6.2 revival) are the two long poles;
prefix rulings land ~20:30Z tonight (CTO); D1 completes 07-19; D4 closes 07-24 17:21Z;
D5 07-24/25; D6 package to Andrew ~07-25.

## F. RESOLUTIONS (2026-07-17 ~18:2x-18:4xZ) -- both long poles now have landing paths

**ASK B / trn_nna -- RULED (CTO 182433Z via COO 183152Z): OPTION (b) RETIRE.** C_01 re-derives
NNA from monolith fact_trn; 03_silver/TRN_NNA is a legacy Rule-17 violation retired, never
replicated into the monolith. Builder = DS~A behind their A4 wave. Two ACs: AC1 parity (gold
NNA re-derived == legacy, to the cell, over a window, BEFORE the legacy converter retires); AC2
field-sufficiency (missing classifier input = a silver passthrough add to fact_trn, never a
computation move; CTO backstops). **The /49-schwab-conv retirement + B2 dormant-family retire on
AC1 parity-pass.** MY INDEPENDENT RETIRE-SAFETY GROUNDING (source-confirmed, converges): the
dying-bucket 03_silver/TRN_NNA has NO live production reader -- sole consumer
`enrich_transactions_with_schwab_diagnostic.py` is explicitly retired (do-NOT-run, Path-A
decision 2026-04-21); froze at date=20260420. Retire breaks nothing live.

**03_silver PREFIX -- WHOLLY DEAD (grounding for CTO's ~20:30Z batch).** Sub-prefixes TRN /
TRN_NNA / account_xref / scripts, all orphaned: account_xref frozen 20260421, live consumers
ALREADY repointed 2026-06-29 to opal-data-bd/schwab/silver/account_xref (build_dim_account.py:51,
build_dim_advisor_fee.py:47); TRN_NNA retire (above); TRN superseded by monolith fact_trn.
Disposition = RETIRE whole; the diagnostic-header "account_xref is an approved standalone silver
dimension" note is STALE (superseded by the 06-29 repoint).

**D1 CALENDAR RESOLVED (NEVER#1, CTO Amendment B).** Producer is NOT "09:46Z" (that was a
predecessor COORDINATION read appointment) -- it is opal-assets-silver-schwab-sweep-daily,
cron(15 12 UTC) DAILY. Trading calendar: 07-18 Sat + 07-19 Sun NON-trading; monolith bronze
carries ONLY trading-day partitions (empirical: every weekend + the Jul-3 holiday skipped;
latest 20260716) -> a weekend sweep = legitimate no-op, no cycle slot. Repoint landed 13:44Z
AFTER today's 12:15 sweep -> today = pre-repoint. **Cycles ~= 07-18 (processes date=2026-07-17)
+ ~07-21 (processes date=2026-07-20), NOT 07-18+07-19.** #5 promoted to VETO (S3-negative APPLIED
overrides #2 provenance DESIRED). Dates held pending CTO ratify of the ~07-18/~07-21 shape.
