# ADHC_GLDINC -- Bug-Hunt Fix Log

Running log of fixes applied from the per-agent bug-hunt reports in this folder
(workflow `wf_ebf64891-fcd`; 46 INF gold scripts reviewed 1 agent/script + adversarial verify).
**One entry per fix, citing the originating report + the commit.** Reviewed top-to-bottom
(Group A -> D), one report at a time. daily=full -> no live serving risk while fixing (INF gold
runs `--chain full` daily). Author: 0.4.0_DS_ClientPlatform~A.

Legend -- **Verify:** the adversarial-verify verdict (confirmed/plausible) when a critical/high
finding was auto-verified; "ground-truthed by DS" for mediums/lows (no verify agent ran -- I
validated against source before fixing).

---

## FIX-001 -- INF_A_-1: canonical txn snapshot selected by DATE, not LastModified
- **From report:** `review_INF_A_-1.materialize_txn_cache.py.md` + `verify_*` (report 1)
- **Severity / verify:** HIGH / verify-**confirmed**
- **File:** `data/inf/scripts/gold/lib/txn_cache_reader.py` -- `_load_canonical_snapshot`
- **Defect:** canonical full-history txn snapshot selected by S3 `LastModified` DESC with no date
  guard. Each `silver/transactions/{date}.parquet` is a full-history snapshot ending at `{date}`;
  a backfill re-upload of an OLDER date (fresh mtime, stale content) was silently selected as
  canonical -> txn cache loses every txn after the backfill date -> wrong positions_cube / gains /
  cost-basis / tax-lots, no crash.
- **Fix:** sort by the filename-encoded partition DATE via new `_partition_date()` (date desc,
  mtime tiebreak); + fail-safe WARN when newest-DATE != newest-MTIME (the backfill signature) so a
  divergence is never silent.
- **Commit:** `76dc70888` (pushed; safe-deploy auto-deployed + verified `code/gold/lib/`)

## FIX-002 -- INF_A_00: tax_status normalize-before-map
- **From report:** `review_INF_A_00.accounts_dimension.py.md` finding 2 (report 2)
- **Severity / verify:** medium / ground-truthed by DS (against `tax_status.py`)
- **File:** `data/inf/scripts/gold/lib/tax_status.py` -- `add_tax_status_column`
- **Defect:** the DataFrame path did an exact-match `.map()` with NO strip, while
  `classify_reg_type` + the module docstring apply `str(...).strip()`. `reg_type` is now sourced
  1:1 from `accounts_v2.account_type` (vocabulary not re-verified post-DWSPLT); a whitespace variant
  (e.g. `'Roth '`) missed the map -> `taxable` default -> silent wrong qualified/non-qualified tax
  split (served on `accounts_dimension_latest`, consumed by INF_C_05).
- **Fix:** normalize `.astype('string').str.strip()` before the map (case kept sensitive BY DESIGN --
  Orion emits canonical case); + log distinct unmapped non-null `reg_type` values so real vocabulary
  drift surfaces instead of silently defaulting.
- **Commit:** `1e54a311a` (pushed; safe-deploy auto-deployed + verified)

## FIX-003 -- INF_A_00: registrationName column guard
- **From report:** `review_INF_A_00.accounts_dimension.py.md` finding 1 (report 2)
- **Severity / verify:** medium (latent -- fires only on reduced-surface schema drift) / ground-truthed by DS
- **File:** `data/inf/scripts/gold/INF_A_00.accounts_dimension.py` -- `build_accounts_dimension`
- **Defect:** the txn-cache loader WARNs-not-raises on a missing requested column, so an absent
  `registrationName` -> bare `KeyError` at the `groupby['registrationName']` -> `sys.exit(1)` ->
  whole no-timeout CHAIN_FULL aborts at the A-stage.
- **Fix:** guard `if 'registrationName' in txns.columns` before the merge; else set
  `registration_name = pd.NA` + WARN (graceful degrade, chain proceeds).
- **Commit:** `1e54a311a` (pushed; safe-deploy auto-deployed + verified)

## FIX-004 -- INF_A_01: drop <NA> account_id before dedup (silent collapse)
- **From report:** `review_INF_A_01.advisor_assignments.py.md` finding 1 (report 3)
- **Severity / verify:** medium / ground-truthed by DS
- **File:** `data/inf/scripts/gold/INF_A_01.advisor_assignments.py` -- `build_advisor_assignments`
- **Defect:** `account_id` coerced to `<NA>` on parse failure (L127), then
  `drop_duplicates(subset=['account_id'])` treats every `<NA>` as equal -> multiple accounts with a
  blank/non-numeric account_id silently COLLAPSE to one row; the rest vanish from
  `advisor_assignments` -> downstream advisor rollups (INF_C_07, INF_D_00f) under-count, no error.
- **Fix:** explicitly `dropna(subset=['account_id'])` with a loud WARN count BEFORE the dedup.
- **Commit:** `7dcc02c83`

## FIX-005 -- INF_A_01: distinguish rep_id coercion-failure from allowlist drop
- **From report:** `review_INF_A_01.advisor_assignments.py.md` finding 2 (report 3)
- **Severity / verify:** low / ground-truthed by DS
- **File:** `data/inf/scripts/gold/INF_A_01.advisor_assignments.py` -- `build_advisor_assignments`
- **Defect:** a present-but-non-numeric `rep_id` (coercion failure) was folded into the "not in
  INFLECTION_REP_IDS allowlist" WARN and silently dropped, misdirecting diagnosis of a real
  upstream data problem.
- **Fix:** capture the present-but-non-numeric count before coercion + log it distinctly; reword the
  allowlist WARN. (Diagnostics only -- the row is still dropped; now the cause is visible.)
- **Commit:** `7dcc02c83`

## FIX-006 -- INF_A_03: coerce units (bronze noUnits) to numeric before position arithmetic
- **From report:** `review_INF_A_03.positions_cube.py.md` finding 1 (report 5)
- **Severity / verify:** medium (type-issue) / ground-truthed by DS
- **File:** `data/inf/scripts/gold/INF_A_03.positions_cube.py` -- `load_transactions`
- **Defect:** `units` is an un-coerced passthrough from bronze (silver reads `pd.read_json(dtype=False)`,
  coerces only ids/dates) but is consumed by `groupby.sum -> cumsum -> units_arr > 1e-9`. Object/string
  `noUnits` -> string-concat + `TypeError` -> no-timeout chain abort; a NaN unit also poisons `cumsum`
  and survives the `!= 0` zero-drop.
- **Fix:** `pd.to_numeric(errors='coerce').fillna(0.0)` after the rename (mirrors `coerce_id_columns`).
- **Commit:** `a98c8598c`

## FIX-007 -- INF_A_04: coerce household_id merge key to Int64 (verify-confirmed HIGH crash)
- **From report:** `review_INF_A_04.client_dimension.py.md` finding 1 (report 6)
- **Severity / verify:** HIGH / verify-**confirmed**
- **File:** `data/inf/scripts/gold/INF_A_04.client_dimension.py` -- `build_client_dimension`
- **Defect:** `agg.household_id` is Int64 (from INF_A_00's coerced accounts dim) but
  `household_names.household_id` is an un-coerced object passthrough from the aum_snapshot silver;
  `pandas.merge` on Int64-vs-object (populated) raises `ValueError` -> `sys.exit(1)` -> whole
  no-timeout chain aborts at A_04.
- **Fix:** coerce both merge keys to Int64 before the merge (SILVER-ID-DTYPE-UNIFY) -- cannot crash +
  names join on the numeric path.
- **Commit:** `e6f608e29`

## FIX-008 -- INF_A_04: surface silent all-null household_name
- **From report:** `review_INF_A_04.client_dimension.py.md` finding 2 (report 6)
- **Severity / verify:** low / ground-truthed by DS
- **File:** `data/inf/scripts/gold/INF_A_04.client_dimension.py` -- `load_household_names`
- **Defect:** a missing HH Name/HH ID column -> empty fallback -> every household_name NULL estate-wide
  in served client_dimension, chain stays green (one quiet WARN).
- **Fix:** upgrade to a prominent impact-stating log (non-fatal -- a display-field gap should not
  hard-abort the chain, but no longer silent).
- **Commit:** `e6f608e29`

## FIX-009 -- INF_B_00: guard bronze-MV over-count from un-deduped pmv (silent AUA)
- **From report:** `review_INF_B_00.canonical_holdings.py.md` finding 1 (report 7)
- **Severity / verify:** medium (silent firm-AUA over-count) / ground-truthed by DS
- **File:** `data/inf/scripts/gold/INF_B_00.canonical_holdings.py` -- `build_snapshot_reconciled`
- **Defect:** `build_snapshot` does not dedup pmv to (account_id, ticker) but bronze IS deduped, so the
  outer-merge is many-to-one and the `market_value = _bronze_mv` override assigns the FULL bronze MV to
  EACH duplicate pmv row -> firm AUA (the number D-max exists to tie to Orion's canonical Total) silently
  over-counted. INERT today (pmv is unique -- ties to Orion at the cent).
- **Fix:** no-op-when-unique dedup guard on pmv_out (+ WARN) before the reconciliation merge.
- **Commit:** `08f42804a`

## FIX-010 -- INF_B_00: fail-loud on empty accounts_v2 (was raw min() ValueError)
- **From report:** `review_INF_B_00.canonical_holdings.py.md` finding 2 (report 7)
- **Severity / verify:** medium / ground-truthed by DS
- **File:** `data/inf/scripts/gold/INF_B_00.canonical_holdings.py` -- `main`
- **Defect:** `min()/max()` on empty accounts_v2 -> raw `"min() arg is an empty sequence"` ValueError ->
  `sys.exit(1)` -> chain abort at B_00 with a misleading message (the clean guard deeper never reached).
- **Fix:** explicit empty-check with a clear ERROR + `sys.exit(1)` before the min/max log.
- **Commit:** `08f42804a`

## FIX-011 -- INF_B_00: float64 pmv_market_value on the AC8 bronze-only path
- **From report:** `review_INF_B_00.canonical_holdings.py.md` finding 3 (report 7)
- **Severity / verify:** low (type-issue) / ground-truthed by DS
- **File:** `data/inf/scripts/gold/INF_B_00.canonical_holdings.py` -- `_build_bronze_only`
- **Defect:** `'pmv_market_value': None` made the column object dtype on this path (float64 elsewhere) ->
  a multi-partition read (pd.concat / pyarrow dataset) could raise a null-vs-double schema mismatch.
- **Fix:** `float('nan')` so every path emits float64.
- **Commit:** `08f42804a`

## FIX-012 -- INF_B_01: fail-loud on a required-date holdings failure (was always exit 0)
- **From report:** `review_INF_B_01.holdings_lots.py.md` finding 1 (report 8)
- **Severity / verify:** HIGH (silent success-on-failure) / ground-truthed by DS
- **File:** `data/inf/scripts/gold/INF_B_01.holdings_lots.py` -- `main`
- **Defect:** the ThreadPool `as_completed` loop caught every per-date error as a WARN and `main()`
  returned 0 unconditionally, so a failed newest-date left `gold/holdings/{today}.parquet` stale/absent
  while the chain proceeded as "success" (no ChainFailed alarm) -> downstream B_03/D_03/D_06/D_07 served
  stale.
- **Fix:** collect failures; raise on total failure OR a newest-partition failure; tolerate older
  backfill-partition failures (they retain prior S3 partitions).
- **Commit:** `8aaa1317a`

## FIX-013 -- INF_B_01: surface UNPRICED holdings (silent AUA under-count)
- **From report:** `review_INF_B_01.holdings_lots.py.md` finding 2 (report 8)
- **Severity / verify:** medium / ground-truthed by DS
- **File:** `data/inf/scripts/gold/INF_B_01.holdings_lots.py` -- `process_one_date`
- **Defect:** a ticker absent from canonical_prices -> price NaN -> market_value NaN -> downstream sums
  (skipna=True) silently treat as 0 -> under-counted AUA/concentration; only a whole-day-empty WARN.
- **Fix:** count + log unpriced rows (+ sample tickers) per date.
- **Commit:** `8aaa1317a`

## FIX-014 -- INF_B_01: dedup canonical_prices per ticker before the join
- **From report:** `review_INF_B_01.holdings_lots.py.md` finding 3 (report 8)
- **Severity / verify:** low (latent double-count) / ground-truthed by DS
- **File:** `data/inf/scripts/gold/INF_B_01.holdings_lots.py` -- `process_one_date`
- **Defect:** the left-merge trusts canonical_prices unique per (date, ticker); a future dup would
  fan-out the holding row -> silent double-count.
- **Fix:** `drop_duplicates(subset=['ticker'], keep='last')` before the merge.
- **Commit:** `8aaa1317a`

## FIX-015 -- INF_B_01: fail-loud on required-column loss from positions_cube
- **From report:** `review_INF_B_01.holdings_lots.py.md` finding 4 (report 8)
- **Severity / verify:** low (schema-drift) / ground-truthed by DS
- **File:** `data/inf/scripts/gold/INF_B_01.holdings_lots.py` -- `process_one_date`
- **Defect:** `output_cols` filtered to `available` silently dropped a missing required column (e.g.
  account_id) -> downstream INF_B_03 KeyErrors far from the cause.
- **Fix:** assert `date/account_id/ticker/units` present, raise on drift; keep custodian defaulted.
- **Commit:** `8aaa1317a`

---

## Reports reviewed but NO fix applied
(reviewer verdict clean, or a finding refuted / not-actionable on DS ground-truth)

- **report 3 / `INF_A_01` finding 3** (low, unguarded `rep_name` access) -- REAL but not actionable
  in isolation: its trigger (a walk-back to a pre-rename accounts_v2 partition missing
  `representative_name`) aborts at **INF_A_00 upstream first** (identical dependency, runs before),
  so guarding A_01 alone changes nothing. Proper fix = a shared required-source-column validation
  across A_00/A_01 -- deferred as a small robustness follow-up, not a per-report fix.
- **report 4 / `INF_A_02`** (fee_rate_history) -- CLEAN (confirmed): a DEPRECATED no-op (early
  `sys.exit(0)`, no data processing). Reviewer verdict correct; nothing to fix.
- **report 5 / `INF_A_03` finding 2** (low, skip-gate freshness key = per-date silver vs the actual
  single canonical snapshot) -- REAL but INERT: `orion-gold-dispatch.sh` never exports
  `INFINC_PHASE1=1`, so `should_skip` always returns COMPUTE (every partition recomputed). Bites only
  if phase-1 incremental is switched on -> fix belongs to that feature's enablement, not here.
- **report 7 / `INF_B_00` finding 4** (low, skip-gate `input_keys` omit accounts_v2 + bronze assets)
  -- REAL but INERT for the same reason (`INFINC_PHASE1` off). Deferred to phase-1 enablement.
