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
