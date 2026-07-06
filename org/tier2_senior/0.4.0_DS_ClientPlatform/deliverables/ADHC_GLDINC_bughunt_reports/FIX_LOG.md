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

## FIX-016 -- INF_B_02: coerce units/nav_price to numeric (report 10 F5)
- `data/inf/scripts/gold/INF_B_02.canonical_lots.py` -- `load_transactions`. Un-coerced bronze
  passthrough consumed by `.abs()`/`>0`/`remaining*buy_price` -> object dtype TypeErrors + aborts the
  chain. `pd.to_numeric(errors='coerce')`. low/type. **Commit:** `cc8956eb8`
## FIX-017 -- INF_B_02: strip ticker on both sides of the canonical anchor (report 10 F4)
- `load_transactions` + `load_canonical_units`. A whitespace/representational ticker mismatch made the
  anchor lookup miss -> `if not anchor` DROPPED every FIFO lot for a real held position -> silent zero
  cost basis. Strip both sides. medium/merge. **Commit:** `cc8956eb8`
## FIX-018 -- INF_B_02: fail-open on the canonical-holdings read (report 10 F2)
- `load_canonical_units`. Unguarded `_read_s3(keys[-1])` violated the function's own "empty dict if
  unavailable -- fail-open" docstring -> a read error hard-aborted the chain. try/except -> `{}`.
  medium/unguarded-read. **Commit:** `cc8956eb8`
## FIX-019 -- INF_B_02: dust-scale threshold in the FIFO clamp (report 10 F3) [VALIDATE]
- `build_lots`. `scale = h / remaining_total` exploded when traceable lots were trivial dust vs H,
  inflating a stale near-noise lot to the full position at a wrong old price/year. Take the residual
  path when `remaining_total < h*1e-6`; scale only lots > 1e-9. **Changes cost-basis attribution --
  validate on next nightly `lots_latest`.** medium/numeric. **Commit:** `cc8956eb8`
## FIX-020 -- INF_B_02: residual lots for held-but-no-in-window-buys positions (report 10 F1) [VALIDATE]
- `build_lots`. The in-loop residual recovery never fired for a canonical-held (account_id, ticker)
  with zero in-window buys -> the position was 100% MISSING from gold/lots -> cost basis understated.
  Post-loop pass emits a floor-year residual (mirrors the in-loop pattern). **Changes cost-basis --
  validate on next nightly `lots_latest`.** high/merge. **Commit:** `cc8956eb8`
## FIX-021 -- INF_B_03: pin holding_period_days to Int64 (report 11 F3)
- `data/inf/scripts/gold/INF_B_03.account_gains.py` -- `process_one_date`. `.dt.days` flips
  int64<->float64 across partitions on NaT -> strict-schema-reader mismatch. `.astype('Int64')`.
  low/type. **Commit:** `0ba30a4fd`
## FIX-022 -- INF_B_03: fail-loud on systematic/newest account_gains failure (report 11 F2)
- `main`. Blanket except + unconditional return 0 hid a total schema-drift failure (written=0/rc=0 ->
  stale served gains/tax). Raise on total or newest-partition failure; tolerate old backfill.
  medium/other. **Commit:** `0ba30a4fd`
## FIX-023 -- INF_C_00: fail-loud on systematic performance failure (report 12 F1)
- `data/inf/scripts/gold/INF_C_00.canonical_performance.py` -- `main`. Blanket except + return 0 hid a
  total failure -> stale served household/account performance. `return 1` when 0 written and 0 skipped.
  high/other. **Commit:** `b9cc7c93a`
## FIX-024 -- INF_C_00: loud NNA-drop visibility (report 12 F2, partial -- see DI-2)
- `process_date`. Holdings-only spine left-drops NNA-only/liquidation accounts -> lost outflow ->
  over-stated served net_nna/growth. Now logs the count + $ magnitude of dropped NNA (full UNION-spine
  fix is a design item). medium/merge. **Commit:** `b9cc7c93a`
## FIX-025 -- INF_C_00: unseeded --start-date backfill warn (report 12 F3, partial -- see DI-3)
- `main`. `--start-date` leaves prev_aua unseeded -> boundary date `aua_change == full AUA` (spike).
  Now warned loudly (full fix = seed prev_aua, DI-3). low/empty-null. **Commit:** `b9cc7c93a`

## FIX-026 -- INF_C_01: retain unmapped-advisor NNA flow (report 13 F1, CRITICAL)
- `INF_C_01.canonical_nna.py` -- `_normalize_silver_schema`. The rep->advisor map is a hardcoded
  4-entry dict; a NEWLY-ONBOARDED advisor's rep_id (or a null rep_id) -> NaN advisor_key/rep_bucket,
  which are groupby KEYS (dropna=True) -> that advisor's ENTIRE NNA flow SILENTLY DROPPED ->
  under-counted served NNA (advisor-acquisition is Inflection's core model). Fill catch-all bucket
  (retain flow) + loud WARN (reps + $). **Commit:** `944765ba0`
## FIX-027 -- INF_C_01: require rep_id/trans_type_desc at source-selection (report 13 F2, HIGH)
- `load_all_transactions`. Source-selection required only {accountId,transDate,transTypeId} but the
  downstream classifier needs conditionally-created type_desc/advisor_key/rep_bucket -> a snapshot
  lacking rep_id/trans_type_desc passed selection then RuntimeError'd mid-classifier -> chain abort.
  Added both to the required set. **Commit:** `944765ba0`
## FIX-028 -- INF_C_01: fail-loud on missing/empty taxonomy (report 13 F3, medium)
- `_load_cashflow_taxonomy` + module init. Missing YAML -> clear error (was bare import-time
  FileNotFoundError abort); ZERO NNA types -> assert (was silent-ZERO served NNA at exit 0).
  **Commit:** `944765ba0`
## FIX-029 -- INF_C_01: surface NNA sign/direction disagreements (report 13 F4, medium -> DI-4)
- `classify_nna`. abs()+type_desc counts a negative-amount reversal as a +inflow -> over-stated NNA.
  Did NOT flip abs() (taxonomy-owner question); added a diagnostic WARN (count+$). **Commit:** `944765ba0`
## FIX-030 -- INF_C_01b: degrade-not-abort on missing account_performance (report 14 F1, HIGH)
- `INF_C_01b.role_aua_backfill.py` -- `main`. C_01b runs BEFORE its producer C_03, so a cold-start
  (absent account_performance) made `return 1` -> sys.exit(1) hard-fail the chain (bootstrap
  deadlock). Nothing consumes role_aua today -> WARN + return 0. Durable fix = dispatch reorder (DI-6).
  **Commit:** `85bc929c7`
## FIX-031 -- INF_C_02: Int64 client_id cast (report 15 F2, low)
- `INF_C_02.client_performance.py` -- `_build_daily_factor_table`. astype('int64') on nullable
  client_id raises TypeError on any <NA> -> sys.exit(1) -> C_02 aborts the whole D-chain. astype('Int64').
  **Commit:** `6432206a5`
## FIX-032 -- INF_C_02: surface dropped NA-household AUA (report 15 F1, medium -> DI-5)
- `client_performance` household groupby. dropna silently drops <NA> household_id rows -> served
  household-grain total_aua UNDER-counted (D-chain consumers). Loud WARN (count+$); repair = DI-5.
  **Commit:** `6432206a5`
## FIX-033 -- INF_C_03: align account_gains merge-key dtype (report 16 F1)
- `INF_C_03.account_performance.py`. all_perf.account_id Int64 vs all_gains.account_id str (diff
  upstream paths, no contract) -- align both to Int64 (defensive; join works today per DI-1 populated
  $180.8M, but drift would ValueError-abort / silent-0-join). **Commit:** `d06b8d4cd` (NOTE: C_03 now
  being RE-POINTED by DS~B to Orion tax_unrealized -- this fix was on the derived path.)
## FIX-034 -- INF_C_03: household_id KeyError guard (report 16 F2)
- backfill indexer raised KeyError when household_id absent from acct_dim -> degrade to null.
  **Commit:** `d06b8d4cd`
## FIX-035 -- INF_C_04: same-date holdings cross-check (report 17 F1, validator)
- cross-checked firm_aua@target_date vs holdings@independent-latest -> false drift WARN; + div-by-
  max(holdings,1) nonsense %. Now same-date holdings + skip drift when <=0. **Commit:** `b7b8c6685`
## FIX-036 -- INF_C_04: date-only compare so latest validates (report 17 F2, validator)
- tz/time-naive equality matched 0 rows -> latest AUA validation silently skipped. `.dt.date` compare.
  **Commit:** `b7b8c6685`
## FIX-037 -- INF_C_04: surface NaN total_aua (report 17 F3, validator)
- NaN total_aua invisible to firm-sum + zero-AUA check -> now flagged. **Commit:** `b7b8c6685`
## FIX-038 -- INF_C_06: re-check empty after NaT-drop + guard max/strftime (report 19 F1)
- emptiness guard was BEFORE the NaT-drop -> all-unparseable dates empty cp -> firm_ts.max() NaT ->
  json.dumps TypeError -> chain abort. Re-check empty + NaT->None. **Commit:** `331cb4bcc`
## FIX-039 -- INF_C_07: partial-pull coverage guard (report 20 F1, HIGH)
- total_aua from single global max perf date + outer-merge fillna(0) -> a tolerated PARTIAL perf pull
  silently collapses served advisor AUA/tagged_aua to ~0 firm-wide (rc=0). Now fall back to the most-
  recent >=80%-covered date + WARN. **Commit:** `4a51114a4`
## FIX-040 -- INF_C_07: Series-guard total_aua default (report 20 F2)
- ap.get(total_aua,0).fillna() is a numpy scalar -> AttributeError -> abort when col absent; Series-guard.
  **Commit:** `4a51114a4`

## Reports 21-31 (Group C tail + Group D publishers) -- condensed fix batch
Commit hashes greppable via `git log --grep "ADHC_GLDINC #NN"` (git log intermittently slow this session).
- **Report 21 / INF_C_08** (`9bcfa0f2d`): F1 advisor_key producer-mismatch WARN (silent $0 ytd_nna);
  F2 fee_bps autodetect + bps->decimal (forward-compat, A_02 no-op); F3 account_fee_map str-normalize;
  F4 Series-guard total_aua.
- **Report 22 / INF_C_09** (`18e29b9a5`): F1 pin fee-status cols to nullable boolean in both write-paths
  (PARKED artifact); F2 row-grain divergence NOTED/deferred (parked/unconsumed).
- **Report 24 / INF_D_00b** (#24): F1 pin household_id Int64 (merge-key-drift abort); F2 default
  total_aua + fail-clear on missing household_id -- centralized in load_client_performance.
- **Report 25 / INF_D_00c** (#25): F1 the only account_id INNER merge missing the sibling .astype(str)
  -> served new_clients silent 0-collapse on dtype drift; F2 net_nna fallback guard.
- **Report 26 / INF_D_00d** (#26): F1 build_nna_geo_view account_id guard (empty-hh_dim fallback KeyError
  abort); F2 None before len(); F3 household_id numeric->Int64->str ('18' vs '18.0' geo merge-miss,
  the $14M-invisible class).
- **Report 27 / INF_D_00f** (#27): F1 (HIGH) empty acct_dim nmnc=nmec=0 breaks AC-F4b.1 invariant ->
  abort; nmec=total. F2 casefold-normalize state (case-variant dup-key collision abort).
- **Report 28 / INF_D_02** (#28): F1 normalize 2 account_id merge keys before the merge (silent advisor/
  reg_type served fallback); F2 top_position guard extended (unwrapped-loop KeyError abort).
- **Report 29 / INF_D_02b** (#29): F1 (HIGH, DI-8) frozen assets input -> interim staleness WARN; F2
  empty input -> return 0 (was abort-the-D-chain); F3 account_id groupby guard.
- **Report 30 / INF_D_02c** (#30): F1 json.loads inside try + broaden except (malformed/transient
  book.json aborted the D-chain).
- **Report 31 / INF_D_02d** (#31): F1 guard ticker inside the fallback (KeyError abort); F2 missing
  firm_composition -> return 0 (cold-start asymmetry vs INF_D_03); F3 flagged DI-9.
- **Report 23 / INF_D_00**: no ~A patch -- CRITICAL live tax-bucket regression, flagged DI-7 (below).

---

## DESIGN ITEMS (flagged -- need a cross-script decision, NOT a safe autonomous per-report patch)
These are REAL findings whose correct fix changes served tax/NNA numbers via cross-script data
lineage; a naive per-report patch could worsen them. Surfaced here for a deliberate decision + CVO eye.

- **DI-1 -- INF_B_03 finding 1 (HIGH, tax liability):** `unrealized_gain = market_value - cost_basis`
  subtracts operands from DIFFERENT unit universes -- `market_value` is I_B01 holdings (positions_cube
  RAW-txn cumsum units x price) while `cost_basis` is I_B02 lots (`current_units` CLAMPED to canonical
  Orion holdings). I_B02's own docstring says raw-txn units diverge from the positions API (~3.15x
  over-retain on some books), so the subtraction mixes unit counts. Plus `fillna(0.0)` on the operands
  books a full-MV phantom gain when cost_basis is missing (or a phantom full loss when MV is unpriced).
  Flows into I_C05 tax-liability + I_C03 unrealized_gain -> materially overstated served tax numbers.
  **Decision needed:** anchor I_B01 market_value to canonical holdings (single unit base), or derive MV
  from the canonical-anchored lots' current_units x price; and stop `fillna(0)` on the operands (leave
  NaN so downstream sums exclude, don't phantom-book). Owner: CVO/CTO + DS.
- **DI-2 -- INF_C_00 finding 2 (medium, NNA/growth):** the account spine is holdings-only; NNA-only /
  liquidation-day accounts are left-dropped with their outflow -> over-stated household net_nna/growth.
  **Fix:** build the spine as the UNION of holdings + NNA accounts (carry `aua_prior` for NNA-only
  accounts). Now WARN-visible (FIX-024).
- **DI-3 -- INF_C_00 finding 3 (low, backfill):** `--start-date` leaves prev_aua unseeded -> corrupt
  boundary partition. **Fix:** seed prev_aua from the trading day before start_date, or refuse
  `--upload`+`--start-date` without a valid seed. Now WARN-visible (FIX-025).

**Validation flag:** FIX-019 + FIX-020 (INF_B_02) change served cost-basis attribution -- recommend a
CVO/DS eye on the next nightly's `gold/lots/lots_latest.parquet` (row count + per-account cost_basis
sanity vs prior) before treating the tax-lot numbers as certified.

- **DI-4 -- INF_C_01 finding 4 (medium, served NNA):** abs()+type_desc counts a negative-amount
  reversal/clawback as a +inflow -> over-stated NNA. Needs Orion taxonomy-owner confirmation (do
  reversals reuse the base type_desc?). WARN-visible now (FIX-029); CVO quantifies from tonight's WARN.
- **DI-5 -- INF_C_02 finding 1 (medium, served AUA):** <NA> household_id dropped at the household
  groupby -> served household-grain total_aua under-counted. Repair = route unassigned to a bucket vs
  upstream household-fill (served-grain decision). WARN-visible now (FIX-032).
- **DI-6 -- INF_C_01b finding 1 (DT lane, chain orchestration):** the durable fix for the C_01b
  cold-start deadlock is a DISPATCH REORDER (run C_01b AFTER C_03/C_07 in orion-gold-dispatch.sh); the
  landed FIX-030 is the defensive degrade-not-abort. Route the reorder to DT.

## DI-1 STATUS UPDATE (2026-07-06, CTO-ruled -> RE-POINT, PROMOTED to top priority)
DI-1 escalated: CVO grounded -> CTO re-ruled -> COO driving. Magnitude quantified **13.6x** (derived
served unrealized_gain **$180.8M vs Orion-native $13.3M**; the unit-mismatch limb dwarfs the $24.5M
phantom). ROOT FIX (not the (b)+(a) derivation-patch, which is RETIRED): re-point **INF_C_05**
(currently `gold/account_gains` derived, GAINS_PREFIX:67) **+ INF_C_03** to source from the native
**Orion `tax_unrealized`** dim (`build_tax_dim.py:61-70`, ST/LT-split, point-in-time), reuse the
`INF_D_02.advisor_client_detail.py:114/348` reader; **retire/demote INF_B_03 account_gains**. UNGATED
(the pull exists + is fresh-to-today; the "stale" was an mtime red-herring CVO caught). SEQUENCING
(Andrew-ruled, COO-reconciled): the sweep **CONTINUES IN-ORDER** (C_03 -> C_04 -> C_05); the re-point
grounding+design lands NATURALLY at **INF_C_05 in-pass (~report 18)**, and once reached is driven
STRAIGHT THROUGH to **DEPLOYED + CVO-verified THIS SESSION** (not deferred). Interim = leave the
number showing (Andrew's client-trust call). CTO's 4 ARCH-GATE CRITERIA to build toward:
(1) field-map 1:1 to the Orion-native Total/ST/LT Gain-Loss columns (`build_tax_dim.py:61-70`) -- READ
them, do NOT re-derive/re-subtract; (2) grain = per-account ST/LT + household, qual/non-qual map only
if C_05 emits that split; (3) INF_B_03 DEMOTE-not-silent-delete -- comp-blast account_gains consumers
first (INF_C_03 account_performance may read it; don't break non-tax readers); (4) vintage-honest
(served tax carries the Orion pull date). Path: grain-confirm RAVC -> CTO arch-gate -> impl -> deploy
-> CVO re-cert (served == Orion-native $13.3M-class, ST/LT intact, exercised on the served artifact).

## DI-7 -- INF_D_00 finding 1 (CRITICAL, LIVE, served tax BUCKET -- confirmed on the artifact)
Report 23. The ADVI_INFREF P1 LEG-1 repoint (cf4a05a9c, 2026-06-30) switched INF_D_00.load_accounts_dim
off silver/accounts_dim/latest.parquet (has tax_status) onto accounts_v2 (has NEITHER tax_status NOR
reg_type), so build_firm_tax_block falls all AUA into 'taxable' (fallback_rate=1.0, WARN-only).
**GROUNDED LIVE:** served s3://opal-data-inf/platinum/firm/clients_tab.json (LastModified 07-06 16:55)
tax = {taxable $202,542,849.81 / 100.0%, tax_deferred 0/0%, tax_free 0/0%} -- the whole $202.5M firm
AUA served 100% taxable when the tax_status.py census is ~48% IRA/Roth. Silent since 06-30 (portal
TaxCostBasisPanel, via INF_D_04 clients_tab_slim). SEPARATE from DI-1 (this is the tax CLASS bucket,
not unrealized gain). **FIX (regression repair, needs a lane -- flagged to COO 224126Z):** restore a
real reg_type/tax_status source (reg-type is registration-static so silver/accounts_dim/latest is fine
for CLASS) joined to accounts_v2; + promote fallback_rate==1.0 to a hard guard. Do NOT substitute
account_type. NOT ~A-patched (served-number regression, Andrew "discovery not sidetrack").

## DI-8 -- INF_D_02b finding 1 (HIGH, wiring/architecture, silent stale served top-holdings)
Report 29. `silver/api_dims/assets/` (INF_D_02b's input) has NO producer wired into the dispatch chain
-- its only writer `build_assets_dim.py` is unwired, and the daily `convert_assets_v2_to_silver` writes
a DIFFERENT prefix (`silver/assets_v2/`, different 58-col schema) that D_02b does not read. So
top_holdings.json republishes months-stale holdings every night with a FRESH `generated_at` (evades the
freshness monitor, which keys on regeneration). **FIX (DT/architecture):** wire `build_assets_dim.py`
into the chain ahead of INF_D_02b, OR repoint INF_D_02b at the live `silver/assets_v2/` (adapt the col
map: current_value->position_mv, ticker->asset_ticker). Interim staleness WARN landed (FIX report-29 F1).

## DI-9 -- INF_D_02d finding 3 (medium, served mix time-series methodology mismatch)
Report 31. The mix time-series classifies its CURRENT point from firm_composition.json (INF_D_03's own
`asset_class` column) but RECLASSIFIES historical quarters via the assets_v2 `product_category` keyword
classifier, defaulting any ticker absent from today's assets_v2 to `alternatives`. The two ends of the
same series use different methodologies -> a fund that is `fixed_income` at the current point but
keyword-unmatched / liquidated shows as `alternatives` historically -> QuarterlyMetricsBar renders a
FICTITIOUS fixed_income-collapse/alternatives-spike that is a classifier mismatch, not a real allocation
change. **FIX:** classify all points with ONE methodology + route unknown tickers to an explicit
`other`/`unclassified` bucket, not silently `alternatives`. Served-number methodology decision -- not
autonomously patched.

---

## Reports reviewed but NO fix applied
(reviewer verdict clean, or a finding refuted / not-actionable on DS ground-truth)

- **report 9 / `INF_B_01b`** (classify_new_securities) -- CLEAN (confirmed): `_read_s3` is unguarded
  but both callers wrap it in try/except; writes an auxiliary classification list, not a served number.
- **report 18 / `INF_C_05`** (client_tax_liability) -- GROUNDED, NOT ~A-edited: DS~B owns C_05's DI-1
  re-point this session (avoid a merge conflict). Both findings HANDED to DS~B (RAVC 222325Z):
  F1 (household_id/advisor_key unconditional access -> KeyError chain-abort) folds into the re-point
  (attribution merge survives); F2 (ST/LT term-mask -> silent $0 served liability) is RESOLVED by the
  re-point's direct tax_unrealized st/lt_gain_loss field passthrough, with a coverage-assert to add at
  the new source. Current source grounded for DS~B: reads GAINS_PREFIX derived path; ST/LT via term mask.

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
