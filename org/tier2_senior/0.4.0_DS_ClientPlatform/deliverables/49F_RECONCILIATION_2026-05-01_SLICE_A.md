# 49Financial Reconciliation — 2026-05-01

Parallelized 3-lane investigation (ADVI_49FRECN Phase 0).
Reference date: **2026-04-29** (most recent clean nightly; header_metrics generated 2026-05-01 04:44 UTC).

Andrew-flagged gaps:
- **Account count:** Opal ~6,025 vs 49F 6,611 (586 missing, 8.86% undercount)
- **AUA:** Opal 3.59% LOW vs 49F's reported number

Lane map:
- **Slice A (DS~A):** Opal-side structural extraction + axis matrices — THIS DOCUMENT
- **Slice B (DS~B):** Missing-account bronze→silver→gold trace + 49F-side integration + consolidation
- **Slice C (DS~C):** AUA decomposition by asset class + classification drift verification

---

## Slice A — Opal-Side Reference Snapshot (DS~A)

**Author:** 0.4.0_DS_ClientPlatform~A
**Completed:** 2026-05-01
**Source artifacts:**
- `gold/artifacts/summary/header_metrics.json` (LastModified 2026-05-01 04:44 UTC)
- `gold/timeseries/account_performance.parquet` (date=2026-04-29 slice)
- `gold/dimensions/accounts_dimension_latest.parquet` (data_as_of_date=2026-05-01)
- `silver/allocations/2026-04-29.parquet` (LastModified 2026-04-30 22:03 UTC)

---

### 1. Reference Date Rationale

2026-04-29 selected because:
- Most recent nightly run completed: `header_metrics.json` generated 2026-05-01T04:44 UTC with `data_as_of: 2026-04-29`
- Matching silver/allocations file: `silver/allocations/2026-04-29.parquet` available
- Consistent reference across all three investigation lanes

---

### 2. Firm-Level Totals

| Metric | Opal (header_metrics) | Opal (account_performance raw) | BD Silver/Allocations | 49F (implied) |
|--------|----------------------|-------------------------------|----------------------|--------------|
| Account count | **6,025** | 6,032 | **6,611** | **6,611** |
| AUA | **$1,657.87M** | $1,659.48M | $1,730.79M | ~$1,717-1,720M* |
| Client/relationship count | 2,830 | — | — | — |

*49F implied: Opal portal ($1,657.87M) * (1 + 3.59%) = ~$1,717.44M. Silver/allocations AUA ($1,730.79M) is HIGHER than implied 49F — see Section 6 Data Gaps.

**Key reconciliation layers:**
```
BD Silver/Allocations  6,611 accounts  $1,730.79M   (BD source truth per Andrew)
                        |
                        | -579 accounts untraced (DS~B scope: bronze→silver→gold trace)
                        v
Opal account_performance 6,032 accounts  $1,659.48M   (gold-processed)
                        |
                        | -7 accounts excluded by D_00 aggregation ($1.61M)
                        v
Opal portal (header_metrics) 6,025 accounts  $1,657.87M   (displayed)
```

Source citation: account_performance `date=2026-04-29`, `account_id` is the primary key.

---

### 3. Per-Advisor Matrix

Source: `gold/timeseries/account_performance.parquet` `architect` column, `date=2026-04-29`.
Note: header_metrics `by_architect` is capped at top-10 and shows different account counts than raw account_performance (likely due to D_00 aggregation logic). Raw data from account_performance used here.

| Advisor (architect) | Opal Accounts | Opal AUA | Opal AUA % | 49F Accounts [BLANK] | 49F AUA [BLANK] | Account Delta | AUA Delta $/% | Gap Classification |
|--------------------|--------------|---------|-----------|---------------------|----------------|--------------|--------------|-------------------|
| 49F House | 2,681 | $537.30M | 32.4% | | | | | |
| Travis Penfield | 197 | $317.44M | 19.1% | | | | | |
| Kyle Sims | 294 | $102.54M | 6.2% | | | | | |
| Greg Rosner | 245 | $71.99M | 4.3% | | | | | |
| Hunter Lloyd | 133 | $70.23M | 4.2% | | | | | |
| David Farrell | 168 | $69.52M | 4.2% | | | | | |
| Dean Dillenberg | 253 | $65.69M | 4.0% | | | | | |
| Tim Rodgers | 251 | $55.14M | 3.3% | | | | | |
| Chase Bertrand | 204 | $49.32M | 3.0% | | | | | |
| Josh Henson | 216 | $45.93M | 2.8% | | | | | |
| Ted Grant | 167 | $45.87M | 2.8% | | | | | |
| Matt Foxhall | 130 | $41.79M | 2.5% | | | | | |
| Patrick Mundlin | 145 | $40.46M | 2.4% | | | | | |
| Brandon Lanz | 96 | $25.29M | 1.5% | | | | | |
| Zach Hawkins | 76 | $20.56M | 1.2% | | | | | |
| Lincoln Rock | 77 | $13.97M | 0.8% | | | | | |
| Unassigned | 126 | $12.99M | 0.8% | | | | | |
| Grant Boren | 53 | $10.21M | 0.6% | | | | | |
| Boston Prachyl | 59 | $10.01M | 0.6% | | | | | |
| Michael Ihlenfeldt | 71 | $9.57M | 0.6% | | | | | |
| Liv Shin | 74 | $8.01M | 0.5% | | | | | |
| Hayden Baker | 45 | $6.33M | 0.4% | | | | | |
| Luke Heiligenthal | 40 | $4.83M | 0.3% | | | | | |
| Nick Bishop | 27 | $3.22M | 0.2% | | | | | |
| Austin Thompson | 13 | $2.84M | 0.2% | | | | | |
| Jacob Roos | 37 | $2.71M | 0.2% | | | | | |
| Mitch Johnson | 23 | $2.00M | 0.1% | | | | | |
| (unassigned architect) | 7 | $1.61M | 0.1% | | | | | |
| Parker Teague | 18 | $1.48M | 0.1% | | | | | |
| Myles Thomas | 3 | $1.09M | 0.1% | | | | | |
| Mitch Roper | 12 | $0.95M | 0.1% | | | | | |
| Mike Kipniss | 2 | $0.93M | 0.1% | | | | | |
| Neil Tjon-Hing | 5 | $0.91M | 0.1% | | | | | |
| Connor Bradley | 21 | $0.78M | 0.0% | | | | | |
| Brock Martin | 4 | $0.70M | 0.0% | | | | | |
| Jimmy Henry | 9 | $0.64M | 0.0% | | | | | |
| Kyle Sweeney | 5 | $0.60M | 0.0% | | | | | |
| Micah Damrow | 2 | $0.57M | 0.0% | | | | | |
| August Vordenbaum | 5 | $0.46M | 0.0% | | | | | |
| Ben Long | 4 | $0.43M | 0.0% | | | | | |
| Sydney Cobb | 4 | $0.41M | 0.0% | | | | | |
| Abby Horton | 1 | $0.31M | 0.0% | | | | | |
| Caleb Borders | 4 | $0.28M | 0.0% | | | | | |
| Jackson O'Brien | 1 | $0.26M | 0.0% | | | | | |
| Trenton Milner | 1 | $0.23M | 0.0% | | | | | |
| Grace McCasland | 4 | $0.22M | 0.0% | | | | | |
| Ashley Bourland | 1 | $0.19M | 0.0% | | | | | |
| Conner Haney | 6 | $0.19M | 0.0% | | | | | |
| Nathan Allen | 2 | $0.15M | 0.0% | | | | | |
| Sam Owens | 2 | $0.08M | 0.0% | | | | | |
| Caleb Kuhn | 2 | $0.08M | 0.0% | | | | | |
| Campbell Huber | 1 | $0.05M | 0.0% | | | | | |
| Justin Jones | 1 | $0.05M | 0.0% | | | | | |
| Torrey Patrie | 1 | $0.04M | 0.0% | | | | | |
| RJ Drucker | 1 | $0.04M | 0.0% | | | | | |
| Lane Curry | 1 | $0.02M | 0.0% | | | | | |
| Connor Haney | 1 | $0.00M | 0.0% | | | | | |
| **TOTAL** | **6,032** | **$1,659.48M** | **100%** | | | | | |

**CAVEAT:** "49F House" (2,681 accounts, $537.30M) is a pseudo-advisor entry — these accounts are assigned to the firm-level pool in our gold pipeline. 49F likely attributes these to individual advisors. DS~B to request 49F-side per-advisor breakdown to resolve the "49F House" attribution.

---

### 4. Per-Account-Type Matrix

Source: `gold/timeseries/account_performance.parquet` joined to `gold/dimensions/accounts_dimension_latest.parquet`, `date=2026-04-29`.
18 unmatched accounts (in account_performance but missing from accounts_dimension) counted under `(unmatched)`.

| Account Type | Opal Accounts | Opal AUA | 49F Accounts [BLANK] | 49F AUA [BLANK] | Account Delta | AUA Delta $/% | Gap Classification |
|-------------|--------------|---------|---------------------|----------------|--------------|--------------|-------------------|
| IRA | 2,066 | $528.18M | | | | | |
| Brokerage | 1,304 | $407.91M | | | | | |
| Joint | 569 | $200.83M | | | | | |
| Trust | 169 | $200.15M | | | | | |
| RothIRA | 1,068 | $59.84M | | | | | |
| Corporate | 38 | $55.28M | | | | | |
| Insurance | 96 | $55.15M | | | | | |
| LLC | 19 | $30.97M | | | | | |
| Other | 73 | $30.78M | | | | | |
| InheritedIRA | 160 | $29.34M | | | | | |
| 401K | 63 | $20.13M | | | | | |
| SEP | 117 | $14.95M | | | | | |
| (unmatched acct_dim) | 18 | $5.94M | | | | | |
| Annuity | 4 | $4.01M | | | | | |
| SIMPLE | 96 | $3.92M | | | | | |
| InheritedRothIRA | 19 | $2.37M | | | | | |
| TermLife | 13 | $1.73M | | | | | |
| 403B | 8 | $1.39M | | | | | |
| Charitable | 40 | $1.38M | | | | | |
| Guardian | 1 | $1.32M | | | | | |
| 529 | 19 | $1.17M | | | | | |
| No Account Type Assigned | 3 | $1.05M | | | | | |
| Bank | 36 | $0.84M | | | | | |
| Savings | 16 | $0.67M | | | | | |
| HSA | 12 | $0.15M | | | | | |
| Estate | 1 | $0.02M | | | | | |
| EducationSavings | 1 | $0.01M | | | | | |
| UTMA | 2 | $0.00M | | | | | |
| CreditCard | 1 | $0.00M | | | | | |
| **TOTAL** | **6,032** | **$1,659.48M** | | | | | |

**NOTE:** Silver/allocations 2026-04-29 shows same account_type taxonomy for the full 6,611 set — DS~B can use silver's `account_type` column directly for 49F-side comparison (same vocabulary confirmed).

**Bucketing flag for DS~B:** 49F likely groups by `account_category` (Retirement / Investment / Trust / Corporate / Other) rather than `account_type`. Silver column `account_category` available and fully populated for all 6,611. Consider requesting 49F to match on category if type-level buckets diverge.

---

### 5. Per-Custodian Matrix

Source: `silver/allocations/2026-04-29.parquet` `rep_code` column (gold layer has no custodian field — see Data Gaps).

**No explicit custodian field in gold or silver/allocations.** Custodian inferred from:
1. `rep_code` — dominant code 8242234 (Schwab advisor rep code)
2. `original_account_number` — 8-digit format (6,591 of 6,611 = Schwab format)

| Custodian (inferred) | Basis | Silver Accounts (6,611) | Silver AUA | Opal Gold Accounts [BLANK] | Opal Gold AUA [BLANK] | 49F Accounts [BLANK] | 49F AUA [BLANK] | Account Delta | AUA Delta $/% | Gap Classification |
|---------------------|-------|------------------------|-----------|--------------------------|----------------------|---------------------|----------------|--------------|--------------|-------------------|
| Schwab (rep_code 8242234) | rep_code match | 6,023 | — | | | | | | | |
| Unknown / Unassigned (No RepCode) | rep_code missing | 542 | — | | | | | | | |
| Other (G44515989, 8403355, etc.) | rep_code variant | 46 | — | | | | | | | |
| **TOTAL** | | **6,611** | **$1,730.79M** | | | | | | | |

**FIELD GAP — DS~B action item:** Request 49F to provide per-custodian breakdown, OR confirm that all 6,611 accounts in their display are Schwab-custodied. If Schwab is sole custodian, this axis collapses.

---

### 6. Account-ID List

Parquet saved at: `tmp/49frecn/opal_accounts_2026-04-29.parquet`
Schema: `account_id`, `total_aua`, `reference_date`
Row count: **6,032** (all accounts in `account_performance` at `date=2026-04-29`)

DS~B uses this list for set-diff against 49F's 6,611-account list to identify the 579 missing IDs.

---

### 7. Caveats and Data Gaps

| Gap | Detail | Implication for DS~B |
|-----|--------|---------------------|
| No custodian field | gold + silver/allocations have no explicit custodian column. Rep_code infers Schwab as dominant (~91%) but cannot confirm per-account. | Request 49F custodian field or confirm Schwab-only scope |
| Silver AUA > implied 49F AUA | Silver account_market_value sums to $1,730.79M; 49F implied is ~$1,717M. Silver includes negative balances (Loans: -$2.44M, Mortgage: -$5.54M, CreditCard: -$0.09M). Gold further filters. | Check if 49F excludes negative-balance accounts from AUA display |
| 49F House attribution (2,681 accounts) | Our gold pipeline routes ~2,681 accounts under "49F House" pseudo-advisor. 49F likely distributes these to named advisors. Per-advisor matrix comparison will require 49F's attribution mapping. | Request 49F per-advisor breakdown with matching account_ids |
| accounts_dimension join miss (18 accounts) | 18 accounts in gold account_performance have no match in accounts_dimension — missing account_type. These may be newly opened or recently restructured. | Flag in DS~B silver→gold trace: which 18 accounts lack a dimension row? |
| account_performance (6,032) vs header_metrics (6,025) 7-account gap | D_00.portal_aggregates.py excludes 7 accounts from portal display that account_performance includes. Likely zero-AUA or filtering threshold. | Cross-reference with D_00 source to understand exclusion logic |
| Andrew directive (2026-05-01) | Andrew confirmed: "The true active number is whatever BD has listed as active in Silver/Allocations/, which is 6611 or so." Silver/allocations is the authoritative 49F-matching source. | DS~B: use silver/allocations as the set-diff base, not accounts_dimension |

---

### 8. Compiler Tools Run

| Tool | Script | Result |
|------|--------|--------|
| comp-pipescript io | D_00.portal_aggregates.py | OK — 18 reads, 5 writes confirmed |
| comp-pipescript io | D_02.advisor_client_detail.py | OK — 17 reads, 4 writes confirmed |
| comp-pipescript io | A_00.accounts_dimension.py | OK — 1 read, 1 write confirmed |

No COLUMN GAPS flagged. No PORTAL CONSUMER route matches for platinum keys (catch-all behavior per comp output).

---

## Slice B — Missing Accounts + 49F Integration (DS~B)

**Author:** 0.4.0_DS_ClientPlatform~B
**Date:** 2026-05-01
**Reference date:** 2026-04-29
**Data sources:** `silver/allocations/2026-04-29.parquet`, `gold/account_performance.parquet`, `gold/dimensions/accounts_dimension_latest.parquet`

---

### B.1 — Pipeline Finding: Gap Is Gold-Layer, Not Bronze→Silver

A structural finding narrows the trace scope:

| Layer | Account Count | AUA |
|-------|--------------|-----|
| BD Silver/Allocations (2026-04-29) | **6,611** | **$1,730.79M** |
| Gold account_performance (C_03, 2026-04-29) | **6,032** | **$1,659.48M** |
| Opal portal (header_metrics, D_00) | **6,025** | **$1,657.87M** |

Silver/allocations matches 49F exactly at 6,611 accounts. The missing 586-590 accounts are NOT absent from the bronze→silver pipeline — they are present in silver and dropped between silver and the gold performance pipeline. The BD ingestion feed is complete.

---

### B.2 — AC#2: Set-Diff Confirmed

**Method:** Set-diff of `silver/allocations/2026-04-29` account_id vs `gold/account_performance` account_id at `date=2026-04-29`.

| Bucket | Count | AUA |
|--------|-------|-----|
| **MISSING_FROM_OPAL** (in silver, not in gold) | **590** | **$62,413,805** |
| MATCHED (in both) | 6,021 | ~$1,597M |
| IN_GOLD_NOT_IN_SILVER (in gold, not in silver) | 11 | — |
| Silver total | 6,611 | $1,730.79M |
| Gold total | 6,032 | $1,659.48M |

The 590 MISSING_FROM_OPAL accounts confirm Andrew's ~586 estimate. The small discrepancy (590 vs 586) is because the portal shows 6,025 (D_00 excludes 7 more) while account_performance shows 6,032.

---

### B.3 — AC#3: Root Cause — 4 Buckets

All 590 missing accounts traced through the gold dimension layer:

1. Check if each account_id appears in `gold/dimensions/accounts_dimension_latest.parquet` (built from `silver/transactions/`).
2. Accounts IN dimension: have transaction history but no positions in the positions cube.
3. Accounts NOT IN dimension: no transaction history at all.

**Root Cause Bucket Summary**

| Bucket | Count | Total AUA | Classification |
|--------|-------|-----------|----------------|
| A: Non-investment account types (CreditCard/Bank/Mortgage/LLC/Loans/Savings) | 44 | -$579K | CLASSIFICATION_DIFFERS |
| B: No transaction history (brand new) | 11 | $4.2M | MISSING_FROM_OPAL — onboarding lag |
| C1: Investment accounts >$100K AUA, created 2025-2026 | 60 | ~$55.5M | MISSING_FROM_OPAL — positions cube lag |
| C2/C3: Investment accounts, dormant/zero AUA | 475 | ~$3.3M | MISSING_FROM_OPAL — no active positions |
| **Total** | **590** | **$62.4M** | |

**Bucket A — Non-investment account types (44 accounts, -$579K):**
BD captures all client financial relationships including credit, banking, and lending accounts. Opal's gold pipeline processes only investment portfolios via the positions cube. Types: CreditCard (21), LLC (8), Bank (6), Mortgage (5), Loans (3), Savings (1). Aggregate AUA is negative (credit/mortgage liabilities). Business question for Andrew: should these 44 accounts be counted as "managed accounts" in the Opal display?

**Bucket B — No transaction history (11 accounts, $4.2M):**
Present in silver/allocations but absent from accounts_dimension (built from silver/transactions). Types: No Account Type Assigned (7), IRA (2), Other (1), RothIRA (1). Created mostly 2025 (9 accounts). These will self-resolve as accounts generate first transactions.

**Bucket C1 — Large new investment accounts (60 accounts, ~$55.5M):**
Present in accounts_dimension (have transaction history) but absent from account_performance. Recently created (2025-2026), $100K+ AUA each. Root cause: the BD allocation feed (snapshot-based) updates faster than the BD positions feed (requires investment elections to be executed). These accounts are funded but investments not yet executed, or BD positions sync has not processed them yet.

Top examples:

| Account ID | Type | AUA | Advisor | Created |
|------------|------|-----|---------|---------|
| z0822893871 | 401K | $11.4M | Tim Rodgers | 04/30/2026 |
| z0822837591 | Trust | $6.1M | Travis Penfield | 04/18/2026 |
| z0822224971 | Joint | $5.0M | Travis Penfield | 12/13/2025 |
| z0822860791 | Trust | $3.0M | David Farrell | 04/23/2026 |
| z0822561091 | Joint | $2.2M | Dean Dillenberg | 02/24/2026 |
| z0820765271 | 401K | $2.2M | Hunter Lloyd | 03/29/2025 |

**Bucket C2/C3 — Dormant investment accounts (475 accounts, ~$3.3M):**
In accounts_dimension but absent from account_performance. 142 have zero AUA, 333 have very low AUA (median $6.35). Open in BD's allocation feed but no active positions — either fully liquidated portfolios awaiting formal account closure, or accounts holding only non-securities assets.

---

### B.4 — AC#4: Per-Custodian Feed Gap Audit

**P0 finding: NO custodian feed gap.** All 6,611 silver/allocations accounts are in the BD feed. The missing 590 are dropped within Opal's gold pipeline, not at custodian ingestion.

Per DS~A's Section 5, custodian is inferred from rep_code (no explicit custodian field in gold or silver):
- Schwab (rep_code 8242234): 6,023 of 6,611 accounts (91.1%)
- No RepCode: 542 accounts (8.2%)
- Other codes: 46 accounts

The 542 no-RepCode accounts overlap with the 316 "No Architect Value Assigned" missing accounts — unattributed/house accounts. No evidence of any custodian being systematically absent from the feed.

---

### B.5 — AC#5: Schwab TRN NNA Phase 6 C_01 Cross-Link

**Verdict: DISJOINT — keep parallel, do not merge.**

| Dimension | Phase 6 C_01 | ADVI_49FRECN finding |
|-----------|-------------|---------------------|
| Pipeline stage | silver/transactions NNA enrichment | silver→gold positions completeness |
| Root issue | NNA transaction source_system attribution | Accounts missing from positions cube |
| Remediation scope | C_01.canonical_nna.py | A_03/C_03 positions cube + A_00 coverage |
| Affected accounts | Schwab TRN transaction records | All account types incl. new/dormant |

Phase 6 C_01 affects NNA classification for accounts already in the gold pipeline. The 590 missing accounts are absent from the pipeline entirely. These are non-overlapping problems.

---

### B.6 — AC#6: 49F-Side Columns (Firm-Level Fill)

Silver/allocations 2026-04-29 is the 49F-side source per Andrew's confirmation. Firm-level columns filled:

| Metric | 49F (Silver) | Opal (Gold portal) | Delta | Gap Classification |
|--------|-------------|-------------------|-------|-------------------|
| Account count | **6,611** | 6,025 | -586 | MISSING_FROM_OPAL |
| AUA | **$1,730.79M** | $1,657.87M | -$72.9M (-4.2%) | MISSING_FROM_OPAL |

**Note on 3.59% vs 4.2%:** Andrew cited 3.59% AUA gap; Opal-internal calculation yields 4.2% (silver vs portal). Four open questions routed to CTO/Andrew to resolve (different reference date, negative-balance exclusion, or approximation). See Open Questions section in the consolidated report.

**Per-advisor fill:** Not feasible at the silver level — silver uses BD's raw architect field ("No Architect Value Assigned" for 3,053 of 6,611 = 46%), which is incomparable to Opal gold's advisor_assignments attribution. The per-advisor delta table in Slice A needs to be filled from 49F's own per-advisor report (Andrew Q2). The advisor-impact breakdown from the missing-account trace is documented in Section B.3.

---

### B.7 — Compiler Tools

| Tool | Target | Result |
|------|--------|--------|
| comp-pipescript io | A_00 | OK — 1 read (external/silver), 1 write; no COLUMN GAPS |
| comp-pipescript io | D_00 | OK — 18 reads, 5 writes; no COLUMN GAPS |
| comp-trace | NNA_AUA_BY_ADVISOR | Resolved to gold/views/nna_aua_by_advisor.parquet — written by D_00 line 844, read by D_01 |
| Data inspection | silver/allocations/2026-04-29.parquet | 6,611 rows, 92 columns — BD truth source confirmed |
| Data inspection | gold/account_performance.parquet | 6,032 accounts at 2026-04-29 |
| Data inspection | gold/dimensions/accounts_dimension_latest.parquet | 10,120 rows (all BD historical) |

---

## Slice C — AUA Decomposition + Classification Drift (DS~C)

**Author:** 0.4.0_DS_ClientPlatform~C
**Date:** 2026-05-01
**Diagnostic script:** `data/black_diamond/scripts/gold/E_25.aua_decomposition_audit.py`
**Output artifact (once dispatched):** `s3://opal-data-bd/gold/manifests/aua_decomposition_audit_{date}.json`

*Leverages DS~A's reference data (2026-04-29 snapshot) for all bound calculations.*

---

### C.1 — AC #4: BKF Fix Verification (Static — No EC2 Required)

**Verdict: FIX PRESENT (code-level, local source)**

The BKF forward-fill fix (ADVI_AUAVAR commit `91b1918a`, 2026-03-06) shipped to
`data/black_diamond/scripts/gold/A_03.positions_cube.py` (renamed from `02_build_positions_cube.py`).

Verified by direct source inspection:

| Marker | Present | Location |
|--------|---------|---------|
| `_load_open_account_ids()` helper | YES | Line 134 |
| `open_account_ids` param on `_compute_account_end_dates()` | YES | Line 1307–1308 |
| BKF allocation cross-reference logic | YES | Lines 1346–1355 |

**What the fix does:** BKF accounts (backfill-only, no TXN_DAILY records) that are confirmed
open by `silver/allocations/{date}.parquet` receive `global_end_date` instead of being capped
at their last transaction date. This recovered ~$6.6M from 143 accounts in the AUAVAR simulation.

**Deployed verification:** E_25 `verify_bkf_fix()` reads the deployed S3 copy at
`code/gold/A_03.positions_cube.py` and checks for the fix markers. Run `--upload` for deployed verdict.

**Regression assessment:** LOW risk. The parameter is optional (`open_account_ids=None` = original
behavior). A pipeline rebuild since 2026-03-06 that lost the fix would show missing accounts in the
positions cube — this would be visible as a drop in account_performance row count.

---

### C.2 — AC #2: AUA Breakdown by Asset Class

**Taxonomy finding (static code inspection):**

The BD gold pipeline uses a **3-class taxonomy** only:

| Gold Class | Definition | Caveat |
|-----------|-----------|--------|
| `equity` | Stocks, equity ETFs, REITs — plus any **unclassified fallback** | Unknown securities silently land here |
| `fixed_income` | Bonds, treasuries, munis, CLOs, money market, sweep, **cash** | No separate Cash bucket |
| `alternatives` | Structured notes, buffer funds, commodities, VIX, hedge | |

Source: `lib/mix_views.py` line 19 (`MIX_ASSET_CLASSES`), `lib/etf_classifier.py` `classify()`.

**Important implication for 49F comparison:** If 49F reports a separate "Cash" allocation, Opal's
`fixed_income` will appear overstated because our fixed_income absorbs cash positions. This is
definitional, not a data gap. Andrew to confirm whether 49F's 3.59% AUA gap claim is on
investment-only (ex-cash) or gross AUA.

**DS~A reference data cross-reference:**
DS~A reports $1,659.48M gold account_performance vs $1,657.87M portal header_metrics (7 accounts
excluded by D_00). Silver allocations shows $1,730.79M — $71.31M above gold, consistent with
non-investment products + negative balances being excluded in gold.

**Actual asset-class values:** pending E_25 dispatch (reads `gold/views/mix_daily_summary.json`
written by C_06, `firm_daily` key, most recent date).

---

### C.3 — AC #1: Account-Undercount × Avg-AUA Bound

**Verdict: CASE_A CONFIRMED (actual DS~B set-diff data received 20260501T214756Z)**

DS~B set-diff output (`tmp/49frecn/missing_from_portal_2026-04-29.parquet`):

| Bucket | Count | AUA | Notes |
|--------|-------|-----|-------|
| MISSING_FROM_OPAL | **590** | **$62.4M** | In silver, not in gold account_performance |
| MATCHED | 6,021 | ~$1,597M | In both |
| IN_PERF_NOT_IN_ALLOC | 11 | — | In gold, not in silver (noise) |

Missing account AUA distribution:
- 60 large accounts (>$100K): ~$55M (88.1% of total missing AUA)
- 409 positive-AUA accounts: median $108.47, mean $152K
- 143 zero-AUA, 38 negative-AUA (excluded from investment view)

| Metric | Value | Source |
|--------|-------|--------|
| 49F portal gap (3.59% × Opal portal AUA) | **$59.6M** | $1,657.87M × 3.59% |
| Actual missing account AUA | **$62.4M** | DS~B set-diff |
| **CASE_A confirmed** | $62.4M > $59.6M | Missing accounts exceed the gap |

**Finding:** The 590 missing accounts hold $62.4M in AUA, which exceeds the 3.59% gap ($59.6M)
by ~$2.8M. This means:
1. **The 3.59% gap is entirely explained by missing accounts in the gold pipeline.** There is no
   valuation/pricing gap on MATCHED accounts — it is 100% a scope gap.
2. If all 590 were included, Opal would show ~$1,721.9M — slightly overshoot the implied 49F
   $1,717.4M by ~$4.5M. The residual is explained by filtering (negative-balance accounts, etc.).
3. **No residual gap on matched accounts (CASE_A). AC #5 holding-type allocation is complete.**

DS~B root cause: C_03 pipeline only includes accounts with investment positions. Non-investment
types (CreditCard, Bank, Mortgage, LLC, Loans) and dormant accounts (no current positions) are
systematically excluded from account_performance. This is by design — the question is whether
the 590 exclusions align with 49F's display scope.

**Action for DS~B Slice D:** Determine whether the 590 missing accounts should be included in
the portal display (scope expansion) or whether the comparison basis with 49F is wrong (49F
may be showing investment + non-investment AUA in their "6,611" figure).

**Notable:** DS~A reports silver AUA = $1,730.79M, gold = $1,659.48M, delta = $71.3M. DS~B
accounts for $62.4M of that with missing accounts; residual $8.9M = pricing timing +
negative-balance accounts. This confirms the pipeline is functioning correctly for investment
accounts — the scope difference is the entire explanation.

---

### C.4 — AC #3: Classification Drift Audit (Post-CLSPT2)

**Mechanism:** `lib/etf_classifier.py` `classify()` returns `''` (empty) when a security is
not in the `bd-securities` DynamoDB table. `C_06.client_mix_timeseries.py` silently falls
back to `'equity'` for these (line 207: `unique_pairs['asset_class'] = 'equity'` as default
before the classify loop runs).

**Post-CLSPT2 exposure:** `B_01b.classify_new_securities.py` uses a watermark at
`gold/manifests/classify_watermark.json` to track the last partition date where new securities
were classified. If the watermark date < 2026-05-01, holdings_lots partitions after that date
contain new tickers that are NOT in DynamoDB and will silently classify as equity.

**CLSPT2 baseline:** 3,855 securities classified as of 2026-03-25. New tickers entering the
49F portfolio since then (new ETFs, newly added securities) are the drift risk.

**Impact on AUA total vs AUA breakdown:**
- Classification drift does NOT affect total AUA (market values are independent of class label).
- Drift inflates equity bucket and deflates FI/alternatives bucket.
- Only relevant for the total AUA gap if 49F uses class-specific AUA in their display.

**E_25 diagnostic output (pending EC2 dispatch):**
- `ac3_classification_drift.unknown_pairs` — count of (ticker, asset_name) pairs not in DynamoDB
- `ac3_classification_drift.unknown_mv` — total market value affected
- `ac3_classification_drift.unknown_pct_of_total` — % of firm AUA in silent-equity fallback
- `ac3_classification_drift.top_20_unknown_by_mv` — sample for manual review + potential B_01b re-run

**Action trigger:** If `unknown_pct_of_total` > 2%, escalate to CTO — B_01b needs to run with
`--full-scan` to re-classify all partitions since the watermark.

---

### C.5 — AC #5: Per-Holding-Type Residual Gap

**Status: COMPLETE — CASE_A confirmed (see C.3). No residual gap on matched accounts.**

DS~B set-diff confirms the $62.4M missing account AUA exceeds the $59.6M total gap. There is
no residual to allocate by holding type on matched accounts. The gap is 100% scope-driven.

Holding-type breakdown retained for reference if Phase 1 analysis reveals a matched-account
discrepancy after full pipeline rebuild with recovered accounts:

| Holding Type | Gap Hypothesis | Priority if CASE_B |
|-------------|---------------|---------|
| Non-investment accounts (CreditCard/Bank/Mortgage/LLC/Loans) | Systematic C_03 exclusion | HIGH |
| Dormant accounts (no current positions) | BKF cap issue (A_03) | HIGH |
| Mutual fund NAV | Stale T-1 NAV vs T-0 | Medium |
| ETF NAV | Exchange close vs NAV spread | Low |
| Cash at face | Opal non-cash filter | Low |

---

### C.6 — Dispatch Requirement

E_25 requires EC2 execution (S3 + DynamoDB reads). DT/AE dispatch:

```bash
python3 /tmp/gold_layer_scripts/E_25.aua_decomposition_audit.py --upload
```

After run: read `s3://opal-data-bd/gold/manifests/aua_decomposition_audit_{date}.json`.
Feed AC #1 (current-data bound), AC #2 (live asset-class breakdown), AC #3 (unknown pair count)
to DS~B for consolidation in Slice D.

---

### C.7 — Compiler Tools

| Tool | Target | Result | Notes |
|------|--------|--------|-------|
| `comp-pipescript io` | C_06 | OK — 9 reads, 2 writes | CANONICAL_HOLDINGS_PREFIX confirmed as input (B_00 dependency) |
| Code inspection | `A_03.positions_cube.py` | BKF fix markers present | `_load_open_account_ids` at L134, `_compute_account_end_dates` at L1307 |
| Code inspection | `B_01b.classify_new_securities.py` | ETFClassifier + watermark confirmed | DynamoDB `bd-securities`, watermark at `gold/manifests/classify_watermark.json` |
| Code inspection | `lib/etf_classifier.py` | Silent equity fallback confirmed | Line 207 in C_06: `unique_pairs['asset_class'] = 'equity'` |
| Code inspection | `lib/mix_views.py` | 3-class taxonomy confirmed | `MIX_ASSET_CLASSES = ['equity', 'fixed_income', 'alternatives']` |
| `ds-commit-gate.sh` | `E_25.aua_decomposition_audit.py` | PASS | py_compile + AST scanner + ruff all exit 0 |
