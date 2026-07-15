# cot fix-wave FIX LOG — OPAL_GLDRNS.C1 drive (0.4.0_DS_ClientPlatform~C, 2026-07-15)

Drive executed under OPAL_GLDRNS.C1 + Andrew-direct fix-wave GO ("Ok fix it now", ~21:1xZ,
recorded lane_c_fix_wave_go_record.md). The per-agent finding reports live in
`org/tier1_exec/1.0.0_SA_CTO/deliverables/cot_gold_bughunt_reports/` (CTO-authored, 07-07);
that folder's FIX_LOG scaffold is BASE_EXEC-laned, so the drive log lives HERE — CTO may fold
it in. Full triage (re-keyed to the REAL nightly, SSM doc `opal-cot-gold-run`):
`COT_GLDRNS_C1_TRIAGE.md`. All four fixes deployed via safe-deploy on push + independently
verified `comp-pipescript deployed` MATCH; the SCHEDULED 02:03Z nightly is the validation run.

## FIX-001 -- A_00: incremental snapshot-union corrodes established accounts (verify_09, CRITICAL, live+growing 13->38)
- **File:** `data/cot/scripts/gold/A_00.accounts_dimension.py` -- `build_accounts_dimension` / `_run_incremental`
- **Defect:** in incremental mode the snapshot union tested only the window's txn accounts, so the whole book re-entered as null-metadata rows and `merge_incremental` overwrote real name/tax_status/state fields nightly.
- **Fix:** `known_account_ids` (the existing dimension's ids) passed into the union test -- `_extra` now only genuinely-new accounts. (+2 preexisting lint clears for the gate.)
- **Commit:** `20c5f9c96`. **Acceptance (CTO):** tomorrow's dim shows corrupted-count FROZEN at 38, tax diversity on newly-updated accounts. **Repair of the existing 38 + book-wide 'taxable' stamp = the SEPARATE CTO-gated --full rebuild.**

## FIX-002 -- C_06: unguarded dead read of retired C_02's frozen artifact (verify_23, latent chain-abort fuse)
- **File:** `data/cot/scripts/gold/C_06.client_mix_timeseries.py` -- `load_static_tables`
- **Defect:** `cp_daily_total` computed and never consumed; producer C_02 retired 06-22; deleting the frozen artifact would abort this REQUIRED nightly step.
- **Fix:** read deleted (import + return + unpack cleaned). C_02's stale artifact is now safe to purge (easy-win 8, held for CTO).
- **Commit:** `293ab5fe6`.

## FIX-003 -- cot_silver_merge: key ID columns forced to string pre-object-loop (verify_17 root, hardening)
- **File:** `data/cot/scripts/silver/cot_silver_merge.py` -- `process_xlsx_to_parquet`
- **Defect:** the cot fork dropped the 49F producer's explicit ID cast; a numeric BD delivery would land int64 IDs in silver and silently miss every string-keyed join (the B_01 Gate-3 lots-wipe trigger).
- **Fix:** account_id/relationship_id/portfolio_id/account_number/contra_account_number cast (null-preserving, integral-float-safe). **Blast grounded live (CTO rider):** cot IDs are 'z'-prefixed strings today -> the cast is a NO-OP on current data, pure drift-hardening. transaction_id + asset_id EXCLUDED deliberately: int64 across existing history; a dtype fork breaks cross-partition dedup (int 845418533 != str '845418533') -- unify only at the consolidation-port history rewrite.
- **Commit:** `5930dd45d`.

## FIX-004 -- B_00: required-column guard on snapshot partitions (verify_04 + verify_07, both HIGH)
- **File:** `data/cot/scripts/gold/B_00.canonical_holdings.py` -- `_build_canonical_from_snapshot`
- **Defect:** absent `units` -> AttributeError chain-abort; absent `market_value` -> silent $0-AUA canonical; account_id/asset_name -> KeyError. Only `ticker` was guarded.
- **Fix:** presence check on all four; missing -> named RuntimeError citing the partition (loud, actionable). (+3 preexisting E702 clears.)
- **Commit:** `b0182ce05`.

## DESIGN ITEMS + NO-FIX

Carried in `COT_GLDRNS_C1_TRIAGE.md` §2 (easy wins 5-9, held at CTO gates), §3 (dormant
booby-trap register + trash list), §4 (port-time design items D1-D6). Refuted/diagnostic-tier
findings adjudicated per-script in the triage table (§6).
