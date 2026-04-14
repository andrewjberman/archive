# Brief: Asset Dimension + Canonical Prices + Classification Refactor

**Author:** 0.4.0_DS_ClientPlatform
**Date:** 2026-04-14
**Addressed to:** 1.0.0_SA_CTO
**Status:** Proposal — awaiting CTO decomposition into task orders
**Prompted by:** Investigation into 49 Financial "Alternatives" valuation instability

---

## 1. Motivation

Andrew asked why 49 Financial's Alternatives AUA dropped from $84M on 2026-04-09 to $62M on 2026-04-10, when the historical range has been $65–90M. The investigation uncovered three distinct, overlapping problems that together drive the instability — and a phantom $23M valuation on a single bond that had gone undetected. None of this can be cleanly fixed with a point patch. It requires a coordinated refactor across the silver ingestion layer, canonical prices, classification, and the gold composition artifacts.

---

## 2. Findings from the 49F investigation

### 2.1 No silver-certified "Alternatives" AUA exists

- `silver/allocations/*.parquet` is account-level (92 cols) and has **no asset-class breakdown**. The only holding-level classification we get from BD today is `account_type` / `account_category` / `account_registration_type`, which is the *account registration* (Insurance / Annuity / TermLife) — not the underlying holdings.
- Portal's "Alternatives" is entirely derived downstream in `D_03.composition_artifacts.py`, `D_00b.portal_timeseries.py`, and `C_06.client_mix_timeseries.py` via `classify_series` → `ETFClassifier` (DynamoDB-backed) + `B_01b.classify_new_securities.py` name-keyword heuristics.

### 2.2 BD has its own holding-level classification in the `Asset_OpalCapital_dimTable`

- Andrew staged 16 xlsx exports (pre-2024 folder + 2024–25 folder + 2026 file) totaling ~3.93M transactions and 10,634 unique AssetIDs spanning 2020-03-06 → 2026-04-13.
- Every transaction row carries: `TransactionID`, `Relationship ID`, `AccountID`, `AssetID`, `Asset SuperClass`, `Class`, `Segment`, `Asset Name`, `Symbol`, `Ticker`, `CUSIP`, `Alternative Identifier`, `Trade Date`, `Settle Date`, `Entry Date`, `Price`, `Transaction Type`, `Transaction Sub Type`, `External Flow`, `Has Contra Account`, `Contra Account Number`, `Coupon Rate`, `First Payment Date`, `Last Payment Date`, `Last Dividend`, `Custodial Cost Basis Sync`.
- **BD does not use an "Alternatives" SuperClass.** Their taxonomy is: `Equities`, `Fixed Income`, `Cash & Cash Equivalents`, `DIVERSIFIER`, `To Be Classified`, `Unclassified`. For 49F on 04-10 (matched $1,641M of $1,653M):

  ```
  Equities                    $1,223M   (74.6%)
  Fixed Income                $  319M   (19.4%)
  To Be Classified            $   70M   ( 4.3%)
  Cash & Cash Equivalents     $   21M   ( 1.3%)
  Unclassified                $    5M   ( 0.3%)
  DIVERSIFIER                 $    2M   ( 0.1%)
  ```

### 2.3 Policy decision from Andrew

**Everything BD classifies as `To Be Classified` counts as Alternatives in our book.** That resolves the classification ambiguity going forward — it's a deterministic, BD-certified signal we inherit instead of deriving. BD's "To Be Classified" spans: structured notes (Shield/Buffer/Point-to-Point/Barrier), annuities, CITs, target-date funds, balanced funds, private fund feeders, options, and a long tail of items BD's security master hasn't mapped.

### 2.4 Join key analysis

| Key | Coverage | Stable? | Notes |
|---|---|---|---|
| `CUSIP` | 88.4% of 10,634 BD AssetIDs | **Yes** — one benign duplicate in 7,767 (NBN reclassification) | **Primary join key.** Ticker→CUSIP has zero conflicts. |
| `AssetID` | 100% of dim, 100% of silver/fees, 100% of silver/transactions | No — BD issues a new AssetID when they reclassify an asset (NBN: Equities/Small Cap Core → Equities/Financials = 2 AssetIDs, 1 CUSIP) | Use for current-state joins, not historical |
| `TransactionID` | 100% of dim, 100% of silver/fees, 100% of silver/transactions | Yes — immutable | **Primary enrichment key** for per-txn BD SuperClass |
| `Ticker` | 69.5% of dim | Yes for public securities | Fallback only; missing on structured notes & annuities |
| `Alternative Identifier` | 12.3% of dim | Unknown | Appears to cover internal BD products (annuities, some CITs) |
| `Asset Name` | 98.9% of dim | No (case/spacing drift) | Fuzzy fallback only |

**Our existing tables' ID coverage is a major gap:**

| Table | transaction_id | asset_id | cusip | ticker | asset_name |
|---|---|---|---|---|---|
| `silver/fees` | yes | yes | **yes** | no | yes |
| `silver/transactions` | yes | yes | **no (dropped)** | no | yes |
| `silver/allocations` | no | no | no | no | no |
| `gold/holdings_lots` | no | no | no | partial (91.8%) | yes (99.9%) |
| `gold/positions_cube` | no | no | no | no | yes |

Gold cannot join to BD's asset dim on a durable key today. Ticker+Asset Name is the only path, and it fails exactly where we need it most — structured notes and bonds that share an issuer name with a public equity.

### 2.5 The $23M BNP Paribas phantom (representative pattern)

Account `z0819189891` holds a BNP Paribas bond (CUSIP `05613L3H2`, "BNP PARIBAS SA", 215,000 face-value units, cost $1.02/unit = 101.88% of par, cost basis $219K, real MV ≈ $219K). Our gold layer tagged this holding with ticker `BNPQF` (the equity ADR) because `B_01b` / ticker-override logic matched on asset-name prefix. `build_canonical_prices_v2.py` then looked up `BNPQF` on Yahoo → $107.01 → multiplied by the 215,000 face-value "units" = **$23,007,150 phantom**.

Scanning 49F's open holdings_lots for the same pattern (cost_per_unit < $5 bond-like, current_price > $20 equity-like, yahoo_finance price source, meaningful size):

| MV shown | MV real est | Asset | Ticker wrong | Notes |
|---|---|---|---|---|
| $23.0M | $0.22M | BNP PARIBAS SA (bond) | BNPQF | ADR ticker applied to bond |
| $860K | $9K | WELLS FARGO 4.15% 01/24/2029 | WFC | Equity ticker applied to bond |
| $595K | $4K | NEWMONT CORP 2.8% 10/01/2029 | NEM | Equity ticker applied to bond |

That's **~$24.3M of phantom MV in 49F alone from three bonds**. Our previous ~$90M "Alternatives" figure was substantially driven by mispriced instruments that happen to also land in TBC classification — meaning the inflation didn't just distort alts, it distorted firm-level AUA.

The same scan also surfaced ~$27M more of suspect patterns (leveraged ETFs, fund tickers with placeholder cost basis). Those need individual review but are lower priority than the bond phantoms.

### 2.6 The day-to-day swing

Holdings are stable 04-07 → 04-10 (33 positions drop, 29 add — essentially unchanged). Total 49F AUA is stable (~$1.6B). But `alternatives` swung $95M → $62M while `fixed_income` swung $306M → $345M in opposite directions on the same days. Andrew noted the DDB classification is NOT re-resolved daily, so the swing is driven elsewhere — most likely the BNP phantom and similar cases flipping between classes as ticker resolutions land differently, or the classification output being sensitive to when `B_01b` adds new securities. This needs dedicated tracing (part of the plan below) but is NOT the primary motivator — the primary motivator is the structural fragility that allows a $23M phantom to persist for months.

---

## 3. Proposed Work Packages

All work packages should target **append-only, immutable point-in-time artifacts** — ledger semantics, not mutable state. Once written, a day's file is never rewritten.

### WP-1: Bronze + Silver `asset_dim_txn` ingestion pipeline

**Owner:** AE / 0.6.0_AE_PartnerETL (by analogy with the fees pipeline)
**Pattern:** mirrors `silver/fees/` exactly.

- `bronze/assets/Asset_OpalCapital_dimTable_{start}_to_{end}.xlsx` — raw xlsx dumps, forward-filled overlaps preserved
- `silver/assets/{YYYY-MM-DD}.parquet` — partitioned by `trade_date`, dedup key `transaction_id`
- `data/black_diamond/scripts/silver/convert_assets_to_silver.py` — `--backfill | --latest | --file`
- `data/black_diamond/scripts/silver/merge-daily-assets-incremental.py` — daily append from new xlsx
- Snake_case schema (31 cols preserved): `transaction_id, relationship_id, account_id, asset_id, asset_super_class, class, segment, asset_name, asset_display_name, original_asset_name, symbol, ticker, cusip, alternative_identifier, trade_date, settle_date, entry_date, price, transaction_type, transaction_sub_type, action, external_flow, has_contra_account, contra_account_number, contra_account_name, description, last_dividend, coupon_rate, first_payment_date, last_payment_date, custodial_cost_basis_sync`

### WP-2: Silver asset dimension (derived reference table)

**Owner:** DS / 0.4.0_DS_ClientPlatform
**Output:** `silver/bd_assets.parquet` — one row per `asset_id` with BD-certified classification, **point-in-time** (written daily, each daily file immutable).

- Derived from `silver/assets/*.parquet` (all history)
- Columns: `asset_id, symbol, ticker, cusip, alternative_identifier, asset_super_class, class, segment, asset_name, first_seen_trade_date, last_seen_trade_date, last_txn_date, txn_count`
- **Secondary index**: `silver/bd_assets_by_cusip.parquet` (one row per CUSIP, most recent AssetID winning ties) — handles the 1-in-7,767 reclassification case (NBN) by preserving both AssetIDs with `valid_from`/`valid_to`.
- **Tertiary index**: `silver/bd_assets_by_ticker.parquet` for ticker-primary lookups (public equities).

### WP-3: Backfill CUSIP into `silver/transactions`

**Owner:** AE / 0.6.0_AE_PartnerETL (owns merge-daily-incremental.py)

- The raw BD transactions xlsx carries `CUSIP`. Current `merge-daily-incremental.py` drops it. One-line schema addition.
- Re-run backfill: adds `cusip` to all historical silver/transactions partitions.
- After WP-3, both `silver/fees` and `silver/transactions` carry `{transaction_id, asset_id, cusip}` — the full enrichment toolkit.

### WP-4: Enrich `gold/holdings_lots` and `gold/positions_cube` with CUSIP + AssetID

**Owner:** DS / 0.4.0_DS_ClientPlatform

- `holdings_lots` is built from `canonical_lots` which is built from BD unrealized. BD unrealized source has CUSIP — must be plumbed through `B_01.holdings_lots.py` and `B_02.canonical_lots.py`.
- For lots that cannot be re-sourced (pre-ingestion), enrich via `(ticker, asset_name)` fallback join against `silver/bd_assets_by_ticker` / `silver/bd_assets`.
- Add `cusip`, `asset_id`, `bd_super_class`, `bd_segment` columns. This is the foundation for everything downstream.

### WP-5: Canonical Prices refactor — CUSIP-primary price resolution

**Owner:** DS + AE (shared)
**Target file:** `data/black_diamond/scripts/gold/build_canonical_prices_v2.py`

Current flow: `ticker → Yahoo → price`. This is what broke BNP. Proposed flow:

1. **Input key is `cusip`**, with fallback to `ticker` only when cusip is absent and the asset is confirmed equity-like (BD `Equities` SuperClass).
2. For assets with BD `Fixed Income` SuperClass: **never** route to Yahoo. Use BD's carried cost_per_unit (accreted to par over time) as the default, override with BD's own price-feed when available via the new asset dim (the `Price` field on recent transactions is BD's per-unit price and is reliable for bonds).
3. For assets with BD `To Be Classified` SuperClass (annuities, CITs, structured notes): **never** route to Yahoo. Use latest transacted price from silver/assets or carry_forward.
4. Add a price-quality column that distinguishes `yahoo_equity`, `bd_txn_price`, `carry_forward`, `par_value`, `custodial_override`.

**Stable rolling prices across weekends/holidays:**
- Refactor into an append-only daily ledger: `gold/canonical_prices/{YYYY-MM-DD}.parquet`, one row per `(cusip_or_ticker, date)`.
- Weekends/holidays carry forward from the last trading day with a `source='carry_forward'` tag.
- The build is deterministic: given silver/assets up through day D, the canonical price for day D is fully determined. Re-running produces byte-identical output. No in-place rewrites.

**Cash as a first-class asset (folded in here from WP-10 #3):**

Cash is currently invisible to gold (`holdings_lots` and `positions_cube` model securities only). Silver's `account_market_value` includes `cash_market_value` per account — $40.5M firm-total for 49F. This is the single biggest cause of joint-account undershoots in the gold/silver reconciliation, materially distorting per-account AUA.

Once silver/assets is online, cash becomes deterministic:
- BD asset_dim treats CASH as a transactable asset. Action ∈ {`Cash Deposit`, `Cash Withdrawal`, `Bank Interest`, `Dividend` (cash leg), `Management Fee`, `Buy` / `Sale` (cash legs), `EF Transfer Out` (CASH), `Journal` (CASH)}. Each carries `account_id` and `Price` (always $1.00 for sweep cash; ~$1.00 for money-market funds with daily NAV reset).
- Cumulative signed market_value per `account_id` over silver/transactions = current cash balance. Reproducible from a flat replay; no daily snapshot needed at the source.

Mechanics inside this WP:

1. Add `CASH` and per-account sweep money-market tickers (FZSXX, SWVXX, etc.) to canonical prices with `source = 'cash_par'`, fixed price 1.00. No Yahoo lookup, no carry-forward. Daily ledger gets a CASH row per trading day.
2. Build `gold/cash_balances/{YYYY-MM-DD}.parquet` from silver/transactions cumulative-flows replay. One row per `(account_id, date)`. Append-only — once written, immutable.
3. In `B_01.holdings_lots.py` (touched by WP-4), inject a synthetic CASH lot per account_id with `current_units = cash_balance`, `current_price = 1.00`, `market_value = cash_balance`, `price_quality = 'cash_par'`. `D_03.composition_artifacts.py::classify_series` already returns `cash` for asset_name = CASH (line 124) — natural classification at the lot level.
4. Reconciliation invariant: `silver.account_market_value` == `sum(gold.holdings_lots.market_value where account_id=X AND is_open=True)` to within $1 for any account where silver has a row. Becomes an automatable check in WP-10's nightly diagnostic.

**Non-destructive layering — Opal's cash-as-fixed-income convention:**

Per Andrew's 2026-04-14 directive, Opal treats cash as `fixed_income` for downstream presentation (same bucket as short-term Treasuries). The cash refactor needs to ease in without forcing a taxonomy debate or touching the frontend. Approach: **dual classification at write, configurable folding at read.**

At the CASH lot's write site (canonical_prices, holdings_lots, gold/cash_balances):
- `asset_class = 'cash'` — BD-true natural classification
- `bd_super_class = 'Cash & Cash Equivalents'` — BD-source-of-truth, immutable
- `price = 1.00`, `price_quality = 'cash_par'`

At the read/aggregation site (`D_03.composition_artifacts.py::compute_period_views`, `D_00b.portal_timeseries.py`, `C_06.client_mix_timeseries.py`):
- Add config constant `CASH_FOLD_INTO = 'fixed_income'` (default, Opal convention)
- Mix-view aggregator applies `if asset_class == 'cash': asset_class = CASH_FOLD_INTO` before bucketing
- Flip `CASH_FOLD_INTO = None` to surface cash as a standalone bucket on portal — single config change, no schema migration, no historical re-publish

Non-destructive properties:
1. **Frontend untouched.** Portal continues to render equity/fixed_income/alternatives/other buckets. Fixed_income just gets bigger by the cash amount (~$40M for 49F).
2. **Existing `classify_asset` paths untouched.** D_03.classify_series still returns 'cash' for CASH at line 124 — correct and unchanged.
3. **Diagnostic/audit always sees cash separately.** The lot ledger and `gold/cash_balances` parquet retain the distinct CASH classification — only the frontend-facing rollup folds it.
4. **Short-term Treasury bills/funds unaffected.** SHV / BIL / SGOV / F/M US TREASURY ETFs / etc. have their own CUSIPs and BD super_class = `Fixed Income`. They don't go through the CASH path; the cash-fold logic only touches synthetic CASH lots from the BD-balance ledger.
5. **Per-firm flexibility.** Future firms that prefer cash-separately (or treat cash differently from short-term Treasuries) flip the flag without redeploys.

Net effect for 49F under default (`fixed_income` fold):
```
Today:                 equity $1,217M  fixed_income $345M  alternatives $62M  total $1,625M
Post-WP-5+10 (folded): equity $1,217M  fixed_income $385M  alternatives $62M  total $1,664M  (silver matches)
Post-WP-5+10 (split):  equity $1,217M  fixed_income $345M  alternatives $62M  cash $40M  total $1,664M
```

This is the cleanest version of "include cash" — sourced from BD's authoritative txn ledger, deterministic, append-only, no double-counting risk between cash-balance and money-market-fund holdings (since money-market funds are a separate asset_id with their own NAV stream), and no destructive change to current portal behavior.

### WP-6: Classification refactor — append-only, BD-primary

**Owner:** DS / 0.4.0_DS_ClientPlatform
**Target files:** `B_01b.classify_new_securities.py`, `lib/etf_classifier.py`, `lib/mix_views.py` (MIX_ASSET_CLASSES)

- **Primary classification source**: BD `Asset SuperClass` from `silver/bd_assets` (joined via CUSIP → AssetID → SuperClass).
- **Our 4-class mapping is fixed and transparent**:
  ```
  BD: Equities                 -> our: equity
  BD: Fixed Income             -> our: fixed_income
  BD: Cash & Cash Equivalents  -> our: cash
  BD: DIVERSIFIER              -> our: alternatives
  BD: To Be Classified         -> our: alternatives          (per Andrew's 2026-04-14 decision)
  BD: Unclassified             -> our: other
  ```
- **Keep the current DDB `ETFClassifier` only as fallback** for assets that don't yet exist in `silver/bd_assets` (new tickers appearing between daily ingests). Demote it from primary to fallback.
- **Append-only classification ledger**: `silver/bd_asset_classifications/{YYYY-MM-DD}.parquet`. Each daily file is immutable; the "current" classification is always the latest file. Reclassifications by BD (AssetID changes) are visible as new rows, not overwrites — full audit trail.
- Deprecate the `B_01b` keyword heuristics for the BD-covered universe (~98% of 49F holdings). Keep for the ~2% unmatched tail only, with a warning log.

### WP-7: Phantom valuation scan + one-time remediation

**Owner:** DS / 0.4.0_DS_ClientPlatform

- Build `diag_phantom_valuations.py`: scan `gold/holdings_lots` latest for `(cost_per_unit < $5) AND (current_price > $20) AND (price_quality = 'yahoo_finance')` — flags bond-priced-as-equity. Cross-check against `silver/bd_assets` to confirm the asset is actually `Fixed Income` or `To Be Classified`.
- Initial 49F scan shows 3 definite phantoms totaling ~$24.3M (BNP, WFC 4.15% '29, NEWMONT 2.8% '29). Run across the full book for all partners.
- One-time correction: publish a `ticker_overrides.json` entry for each phantom, forcing cost-basis price carry-forward until WP-5 is deployed and handles them structurally.
- The report itself goes into `data/black_diamond/scripts/diagnostics/` as a permanent diagnostic that runs nightly as part of the gold QC pass.

### WP-8: Regression test — 49F alternatives time-series stability

**Owner:** DS / 0.4.0_DS_ClientPlatform

- Rebuild 49F's monthly Alternatives time series from Jan-2024 → Apr-2026 using the new (post-WP-6) classification (TBC + DIVERSIFIER → alternatives, everything else excluded).
- Post-fix expected: smooth monthly curve with no >$10M day-to-day swings. Current curve has 04-07→04-10 swing of $33M and 2025-06-10 single-day drop of $18M. Both should disappear.
- This is the acceptance test for the overall refactor.

### WP-10: Account-ID lifecycle + cash-as-position + reconciliation harness

**Owner:** DS / 0.4.0_DS_ClientPlatform

**Motivation — gold vs silver reconciliation, 49F as of 2026-04-10:**

(2026-04-14 correction: the firm-facing reconciliation is much tighter than initial raw-`holdings_lots` analysis suggested. The pipeline already filters orphans via AP gate + architect-lookup + ghost exclusion. Comparing the correct gold artifact:)

```
Silver authoritative (allocations.account_market_value):     $1,681,963,293
Gold pipeline output (firm_mix_views.json, firm_composition): $1,624,913,423
Delta:                                                          -$57,049,871  (-3.39%)
  ... of which cash:                                            -$40,496,558  (silver cash, not modeled in gold)
  ... residual non-cash gap:                                    -$16,553,313  (-1.01% of silver non-cash)
```

The "always within a couple percent" reconciliation is real. The earlier framing of "+$208M overstatement" was an artifact of comparing the wrong table — raw `holdings_lots` is an internal stage that includes accounts the pipeline drops downstream via architect-lookup (no architect → not in firm composition) and AP gate. Those orphan positions are NOT showing up on the portal — they're invisible to consumers.

So the WP-10 scope is two distinct problems, neither of which is "drop $200M":

**Problem 1 — Cash invisibility (-$40M, structurally addressable):**

Silver's `account_market_value` includes per-account `cash_market_value`. Gold models securities only. Joint-account undershoots are dominated by missing cash:
- WALDROP LLC: silver $10.4M = $2.1M cash + $8.3M securities. Gold $8.3M matches non-cash exactly.
- McQueen IRA: silver $1.9M, $1.0M of which is cash.

Fully closed by WP-5's cash-as-asset refactor (BD-balance-sourced from silver/transactions, fixed price 1.00, synthetic CASH lots in holdings_lots, dual-classification with Opal-fold-to-fixed-income at read).

**Problem 2 — Non-cash residual (-$17M, 1.01%):**

This is the actual remaining gap between gold and silver post-cash. Two components observed:
- **Multi-custodian plan sleeves** (PCRA Trust z0817905851 silver $2.4M, gold $82K, Schwab RPS $80K agree; BD silver shows $2.3M from a non-Schwab plan-sponsor feed our pipeline doesn't ingest). Pattern repeats on a tail of trust/401k accounts.
- **Per-account joint-tail discrepancies** ($13K–$1M each across ~600 accounts), likely a mix of: bond price drift between BD's pricing and ours (the BNP/WFC/NEWMONT phantom pattern at smaller scale), illiquid-asset valuation lag, intra-day timing, partial position misses. Most are noise; a handful materially overlap with WP-7 (phantom valuation scan) and WP-11 (scoped overrides).

**Decoupled hygiene — `holdings_lots` orphan cleanup (NOT firm AUA fix):**

Raw `gold/holdings_lots` carries 2,073 accounts ($237M) that are not in current silver/allocations. The gold pipeline already drops them from firm composition via architect-lookup (rel_architect_lookup) and AP gate, so they don't distort firm AUA today. But:

- They inflate per-account joins inside our analytics pipeline (anything that consumes `holdings_lots` directly without re-applying the architect filter risks double-counting).
- They include the 1,776-account "DARK" subset (no fee record, no txn in 6-year asset_dim, no Schwab RPS) which represents one of three things: (a) genuinely closed positions BD shipped once and never updated, (b) initial-ingest artifacts, OR (c) legitimate AUA at non-Schwab custodians (Empower / Fidelity / Principal recordkeepers) BD lost visibility on. Per Andrew's 2026-04-14 note: this $200M is presumed to exist somewhere in silver under different account_ids — the lifecycle classifier isn't authority to drop them.

Per Andrew's directive: **do not auto-retire orphan accounts.** They may represent real AUA that BD tracks under a different account_id structure (relationship reorganization, entity changes, recordkeeper migrations). The pipeline's architect-filter already handles them correctly for firm aggregations; aggressive lifecycle-based retirement risks dropping legitimate positions.

**Root cause #1 — BD account-ID lifecycle (the $206M):**

For 64 relationships covering $206.4M of orphan MV, the same `relationship_id` exists in silver under a **different** `account_id`. Two sub-patterns identified by case-investigation:

- **Pattern B — renamed/reissued same account** (e.g., rel `z0880615` Waldrop family: 14 accounts split between gold-orphan IDs `z0814305021` "SLAT - Managed" and silver IDs `z0813232471` "SLAT Managed", `z0814304391` "Waldrop Investments LLC" vs `z0820403231` "WALDROP INVESTMENTS LLC-CORPORATION"). Same underlying account, BD reissued the ID and slightly renamed. **Dedup-compatible** — the orphan is a stale identifier for a position currently held under the silver/joint account_id.
- **Pattern C — different real account, same client** (e.g., rel `z0880629` Mitchell: orphan `z0814305081` $27.7M holds Kensington/JHQTX/PIMIX/Cohen-Steers — institutional 401(k) shares — while joint `z0812974881` $14M holds short-duration bond ETFs and T-bills — Schwab brokerage cash-mgmt sleeve; **zero of 100 orphan positions overlap any of 25 joint positions**). Different real accounts owned by the same client. The orphan was a real account at a deprecated recordkeeper that BD stopped sending us silver rows for; our gold retained the last-known lots from late 2022.

**Pattern A — `relationship_id = 0` catch-all:** 1,157 orphans worth **$123M** under the null relationship. 190 silver accounts ($51M) also live there. Cannot dedup by relationship_id since "0" is shared across unrelated clients. Largest single contributor to the orphan total.

**Update from 2026-04-14 position-overlap analysis (Andrew + DS):**

Per-relationship dedup hypothesis tested against rel `z0880615` (Waldrop, 14 accounts). Result: **zero exact unit matches** between any orphan and any silver-side account. Best overlap "Waldrop DAF" → "NATIONAL CHRISTIAN CHARITABLE" was 10 of 101 assets, no unit matches. The orphan accounts hold genuinely different positions from their joint twins. The naming similarity ("SLAT - Managed" vs "SLAT Managed", "Waldrop Investments LLC" vs "WALDROP INVESTMENTS LLC-CORPORATION") reflects the same family operating multiple distinct legal entities, with BD silver tracking the current one and gold retained the closed/predecessor entity's last-known holdings.

So Pattern B (renamed/reissued same account, dedup-compatible) does NOT exist at scale. All orphans are Pattern C (real legacy account at deprecated vehicle/recordkeeper). The unifying rule is **silver_dropped**, not relationship dedup.

**Account-ID lifecycle classifier — POC validated:**

POC built against current 3-month silver/allocations history (2026-01-16 → 2026-04-10). For each `account_id` ever seen in any silver/allocations partition, capture `last_seen_in_silver_allocations`. Cross-reference with current Schwab RPS for active-Schwab validation.

Applied to 49F's 2,073 gold-only orphans:

| Bucket | Accts | MV | Action |
|---|---|---|---|
| ACTIVE_SCHWAB (validated by Schwab RPS within 5d) | 149 | $36.1M | KEEP |
| RECENTLY_DROPPED (last-seen silver < 90d, not Schwab-active) | 11 | $1.8M | KEEP, monitor |
| RETIREABLE (no silver presence in available history, no Schwab RPS) | 1,913 | **$199.2M** | DROP from firm aggregations |

The single rule — **`account_id present in last 90 days of silver/allocations OR validated by Schwab RPS within 5 days`** — collapses the orphan bucket from $237M → $38M without per-relationship investigation.

Threshold caveat: silver/allocations history currently only goes back to 2026-01-16. The 90-day threshold needs longer silver history (BD bronze backfill currently in progress, separate AE work). Until then, "RETIREABLE" effectively means "never seen in current silver" which is conservative — the 11 RECENTLY_DROPPED bucket is the sole near-miss tier.

Per-account `position_status` enum ('active', 'active_schwab', 'recently_dropped', 'retireable', 'null_relationship_unresolved') is written into the `gold/holdings_lots` schema. Firm aggregations sum only `active*` rows; `retireable` rows are retained in the lot ledger for full audit history.

**Root cause #2 — Cash is invisible to gold (the $40M / firm × N firms):**

Silver's `account_market_value` includes `cash_market_value` per account ($40.5M firm-total for 49F). Gold/holdings_lots and positions_cube model only securities. For WALDROP LLC: silver $10.4M = $2.1M cash + $8.3M securities; gold $8.3M matches the securities exactly. Every joint-account undershoot has a cash component.

Cash CAN be modeled deterministically once silver/assets is online (WP-1):
- BD's asset_dim treats CASH as a transactable asset (Action ∈ Cash Deposit / Cash Withdrawal / Bank Interest / Dividend / Management Fee / Buy-cash-leg / Sale-cash-leg / EF Transfer Out (CASH))
- Sum of signed market_values per account_id over txn history = current cash balance
- Price = 1.00 always; no Yahoo lookup, no carry-forward needed

Folded into the canonical-prices refactor (WP-5) and gold-holdings build (WP-4): emit a synthetic `CASH` lot per account_id per day with `units = bd_cash_balance`, `price = 1.00`, `price_quality = 'cash_par'`. Per-account silver MV reconciles to gold MV to within $1 by construction.

**Work:**

1. **Account-ID lifecycle table**: `silver/account_id_history.parquet`. Owner DS. Backfill from full silver/allocations + silver/transactions + silver/fees + asset_dim history. Status classifier per account.
2. **Lifecycle-aware orphan retirement**: in `gold/holdings_lots` build (B_01), filter open positions by account status. `silver_dropped` and `null_relationship_unresolved` excluded from firm aggregations but retained in the lot ledger with `position_status` tag for audit. 
3. **Cash ledger** (folded into WP-5): `gold/cash_balances/{YYYY-MM-DD}.parquet` from silver/transactions cumulative flows. Synthetic CASH lot injected into holdings_lots downstream.
4. **Lot dedup audit**: scan `gold/holdings_lots` for exact-duplicate `(account_id, ticker, current_units, cost_per_unit, acquisition_date)` rows. The top orphan account (`z0814305081`) shows every position duplicated 2-3x (PIMIX 57,751 units appears twice). Materially distinct bug from account-ID lifecycle — fix by enforcing `lot_id` uniqueness upstream and one-time historical dedup.
5. **Multi-custodian coverage gap** (residual after dedup): joint-account undershoots where BD silver shows MV absent from BOTH gold AND Schwab RPS (e.g., PCRA Trust `z0817905851` silver $2.4M, gold $82K, RPS $80K). These are plan-sponsor CIT / managed-account sleeves BD aggregates from a feed our pipeline doesn't subscribe to. Catalog by `portfolio_group` / `manager` fields, surface to Andrew; resolution is escalation to BD, not code.
6. **Daily reconciliation diagnostic**: `data/black_diamond/scripts/diagnostics/diag_gold_silver_reconciliation.py`. Runs nightly post-gold. Outputs per-firm over/under delta, top 25 over/undershoots, set diffs of accounts. JSON to `diagnostics/output/gold_silver_recon_YYYY-MM-DD.json`. Alerts if firm-level abs delta exceeds 1% of silver total. Stretch: diff against the prior day to surface single-day regressions (e.g., a $20M alt swing).

**Acceptance:**
- Joint-account abs delta < 1% of silver total (vs current 25%).
- Gold-only orphan bucket < $20M (vs $237M); the residual must be all true Schwab-validated.
- Silver-only ingestion gap < $10M (vs $55.9M).
- Per-account `silver.account_market_value == gold.sum(holdings_lots.market_value)` to within $1 for ≥99% of joint accounts.

### WP-11: Scoped price overrides for confirmed bond phantoms

**Owner:** DS / 0.4.0_DS_ClientPlatform
**Target files:** `data/black_diamond/scripts/silver/bd_price_update.py::_SCOPED_PRICE_OVERRIDES`, `data/black_diamond/scripts/silver/inject_scoped_overrides.py::_INCEPTION_DATES`

Per Andrew's 2026-04-14 directive — add these three phantom-bond entries to the scoped overrides list so the 04-15+ canonical prices run produces correct MVs. This is the tactical fix from Section 6, formalized as a WP:

```python
{"asset_name": "BNP PARIBAS SA",                    "ticker": "BOND_BNP_05613L3H2",  "price": 1.02},
{"asset_name": "WELLS FARGO & CO 4.15% 01/24/2029", "ticker": "BOND_WFC_415_2029",   "price": 0.95},
{"asset_name": "NEWMONT CORP 2.8% 10/01/2029",      "ticker": "BOND_NEM_28_2029",    "price": 0.87},
```

Inception dates (first acquisition in holdings_lots): BNP 2024-10-15, WFC ~2023-Q1, NEM ~2023-Q2 (verify from `silver/bd_transactions` before injection). Prices picked as cost_per_unit — reasonable proxy for IG bonds holding near par until BD-feed pricing is integrated in WP-5.

Post-injection firm impact (49F only): gold total drops by ~$24.3M. Alternatives bucket drops correspondingly (BNP TBC). This closes 10% of the $207M firm-total over-reporting immediately.

**This WP is pre-approved and should ship before the full refactor.**

### WP-9: CUSIP-keyed FIFO replay + phantom reclassification

**Owner:** DS / 0.4.0_DS_ClientPlatform
**Prereq:** WP-3 (CUSIP in silver/transactions) + WP-4 (CUSIP in gold/holdings_lots)

The legacy phantom diagnostic (`data/black_diamond/scripts/diagnostics/adhc_histry_005_phantom_schwab.py`) identifies 10,832 "phantom" positions worth $177M — positions that FIFO replay shows as open but are in neither BD unrealized nor BD realized. The diagnostic keys positions by `(account_id, asset_name)`, with a two-entry `NAME_ALIASES` dict (OPAL↔POLEN only) as the sole defense against name drift.

The asset_dim provides definitive evidence that most of these are real rotations that our FIFO fails to match due to asset-name drift:

- **25,985 non-cash rotation-OUT events** in the 2024-25 dim slice alone (`ACAT Out` 4,304; `EF Transfer Out` 10,631; `JNL - SHORT` 4,011; `FTP - DEBIT` 2,237; plain `Transfer Out` 422), covering 22,241 unique `(account_id, asset_id)` pairs across 2,402 accounts and 2,004 assets.
- CUSIP is populated on these events, invariant across name changes. AssetID is 100% populated. TransactionID is immutable.
- The failure pattern: a `Buy` in 2022 for "POLEN DIVIDEND INCOME ETF" paired with an `ACAT Out` in 2024 for "OPAL INTERNATIONAL DIVIDEND INCOME ETF" — same CUSIP `210322707`, different name string. Our `(account_id, asset_name)`-keyed FIFO can't match them.

Contra Account was initially attractive as a Schwab-counterparty bridge but is populated on only 5,795 of 2.3M txns (almost all management-fee rebates and cash journals between related accounts, not asset rotations). Direction signal must come from the `Action` field.

Work:

1. Rewrite `compute_fifo()` in `adhc_histry_005_phantom_schwab.py` (and siblings `adhc_histry_001/002/003/004`, `diag_phantom_fifo_replay.py`) to key on `(account_id, cusip)`.
2. Consume asset_dim's `Action` granularity — distinguish `ACAT Out` (gone to another custodian), `EF Transfer Out` (external flow), and `JNL - SHORT` (internal journal) for reporting, not just a blanket SELL.
3. Re-run the phantom hunt post-WP-3/4. Categorize remaining phantoms:
   - (a) Explained by rotation event in asset_dim → resolved, flag as `rotation_explained` in holdings ledger.
   - (b) No rotation event but position still vanished → genuine BD data issue, escalate.
4. Output: `data/black_diamond/scripts/diagnostics/output/phantom_resolution_YYYY-MM-DD.json` with per-phantom cause tags.
5. Acceptance: <$10M residual unexplained phantom MV (vs current $177M).

Long-run: once WP-9 lands cleanly, the `NAME_ALIASES` dict and the "silver allocations phantom gate" (`02b_build_canonical_holdings.py` Step 5) become vestigial — both are patches for the (account_id, asset_name) fragility that CUSIP resolves structurally.

---

## 4. Sequencing & Dependencies

```
WP-1 (AE: bronze/silver assets) ──┐
                                  ├── WP-2 (DS: bd_assets dim) ──┐
WP-3 (AE: cusip in silver/txns) ──┘                               │
                                                                   ├── WP-5 (canonical prices refactor)
WP-4 (DS: gold cusip backfill) ──────────────────────────────────┤
                                                                   ├── WP-6 (classification refactor)
                                                                   │
                                                                   ├── WP-7 (phantom scan) ── WP-8 (regression)
                                                                   │
                                                                   └── WP-9 (cusip-keyed FIFO + phantom reclass)
```

Critical path: WP-1 → WP-2 → WP-4 → WP-5/WP-6 → WP-8. WP-3 parallel with WP-1. WP-7 can start in parallel with WP-4 (uses current gold + silver/assets directly). WP-9 runs after WP-3/4 and delivers independently of WP-5/6/8.

**WP-11 ships first** — standalone tactical fix, no dependencies, one-day turnaround.
**WP-10 runs independently** — uses current silver + Schwab RPS + gold/holdings_lots. Can begin immediately. Findings feed into WP-9 (account retirement + lot dedup overlap with FIFO phantom reclassification) but neither blocks the other.

---

## 5. Open Questions for CTO

1. **Policy: TBC = alternatives.** Confirmed by Andrew 2026-04-14. Do we also fold `DIVERSIFIER` into alternatives (seems correct) and `Unclassified` into `other` (also seems correct)? Or does `Unclassified` also get rolled into alternatives for consistency?
2. **AssetID reclassification handling.** The NBN example shows BD occasionally issues a new AssetID for the same CUSIP when they reclassify. Do we want a formal `asset_id_history` table tracking these transitions, or is "latest wins, tagged by valid_from" enough?
3. **Canonical prices scope.** WP-5 as scoped covers price *resolution logic*. Does it also need to cover the weekend/holiday roll-forward refactor Andrew mentioned, or is that a separate WP? (I'd fold it in — same file, same code path.)
4. **Ownership boundary for WP-3.** `merge-daily-incremental.py` is AE-owned but the silver/transactions schema change propagates into gold. Should DS produce a schema-change PRD that AE implements?
5. **Ticker-override file governance.** Post-WP-5, `ticker_overrides.json` becomes vestigial for BD-covered securities but is still needed for the ~2% tail. Should we migrate overrides into the same `silver/bd_asset_classifications` ledger with a `source='manual_override'` tag?
6. **Phantom remediation retro-active scope.** The BNP phantom has existed since 2024-10-15 (first transfer-in). Do we re-publish historical gold partitions with corrected prices, or stamp a "correction applied from 2026-04-XX forward" line and leave history as-is?
7. **DDB `ETFClassifier` sunset.** Once WP-6 is in place and BD-covered assets are classified from silver, what do we do with the DynamoDB table? Keep for the fallback tail, or retire entirely in favor of a flat-file fallback?
8. **Phantom write-off scope.** After WP-9 categorizes the 10,832 phantoms, the `rotation_explained` bucket should be closed silently in our FIFO ledger (they were real rotations; no money lost). For the residual `genuine_data_issue` bucket, do we escalate each one to BD Support individually, or package them into a quarterly BD-feed-quality report?

---

## 6. Immediate tactical action (does NOT require the full refactor)

Independent of the plan above, the BNP phantom should be fixed in the next gold run. Fastest path:

1. Add ticker override: `{"asset_name": "BNP PARIBAS SA", "cusip": "05613L3H2", "force_price_source": "carry_forward"}` (or equivalent in `ticker_overrides.json`).
2. Same for `WELLS FARGO & CO 4.15% 01/24/2029` (CUSIP TBD from silver/fees) and `NEWMONT CORP 2.8% 10/01/2029`.
3. Re-run `build_canonical_prices_v2.py → inject_scoped_overrides → D_03.composition_artifacts.py`.
4. Verify 49F total AUA drops by ~$24.3M and Alternatives drops by the corresponding TBC component.

This should happen before the CTO decomposes the full refactor — it's a bleeding fix, not a strategic fix.

---

**Appendix A — investigation artifacts (local, not committed):**
- `C:\Users\AndrewBerman\AppData\Local\Temp\altvaln\asset_dim_combined.parquet` — 2024-25 BD asset dim (2.3M txns, 8,790 AssetIDs)
- `alloc_2026-04-10.parquet`, `pc_2026-04-{07,08,09,10}.parquet`, `hl_2026-04-{07,09,10}.parquet`, `ap.parquet`, `fmv.json`, `fmvd.json`, `firmcomp.json`, `hmm.json` — 49F diagnostic slices

**Appendix B — full 49F phantom scan available on request (scan logic captured, not yet committed).**
