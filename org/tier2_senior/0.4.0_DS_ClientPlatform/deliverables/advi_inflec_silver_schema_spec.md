# Inflection Silver Layer Schema Specification

**Author:** 0.4.0_DS_ClientPlatform  
**Date:** 2026-04-21  
**Project:** ADVI_INFLEC (W3.1)  
**Status:** APPROVED — CTO SIGN-OFF 2026-04-21 via MCP. W3.2 implementation authorized.  
**Source brief:** `docs/briefs/cto-brief-inflection-partner-data-investigation.md`  
**Local data dir:** `data/inf/` (mirrors `data/black_diamond/` — scripts in `data/inf/scripts/{bronze,silver,gold}/`)  
**Agent ownership:** DS = script authorship + S3 upload + gold dispatch; AE = `0.6.1_AE_PartnerETL` owns inf-pipeline Terraform, Lambda, EC2 runner, S3 bucket provisioning

---

## 1. Overview

Three silver tables, mirroring the BD silver layout where applicable:

| Table | S3 path | Grain | Partition |
|-------|---------|-------|-----------|
| Transactions | `silver/transactions/{date}.parquet` | one row per Orion TRN row | per `trade_date` (YYYY-MM-DD) |
| AUM Snapshot | `silver/aum_snapshot/{date}.parquet` | one row per household per snapshot | per `snapshot_date` |
| Accounts Dim | `silver/accounts_dim/latest.parquet` | one row per account_id | single file (no date partition) |

All parquet files use snappy compression, written with pyarrow engine. No hive partitioning subdirectories — flat key `silver/{table}/{date}.parquet` matches the BD layout.

**Single-source-of-truth note (CTO clarification):** Unlike BD (multi-custodian, requires Schwab TRN_NNA overlay via `source_system` tagging per Phase 6a bea387a9), Inflection is single-source-of-truth Orion. No cross-source overlay is needed at the silver layer. There is no `source_system` column and no custodian-reconciliation pass.

---

## 2. Silver — Transactions

**Source:** Orion TRN CSV exports (all canonical files per `docs/briefs/cto-brief-inflection-partner-data-investigation.md` §3.2)  
**Row count (expected at full load):** ~4.29M unique transaction IDs  
**Dedup key:** `transaction_id` — globally unique per Orion; deduplicate across overlapping export files by keeping first occurrence per ID (sort files by date range start descending, process newest first so the most recent copy of any row wins on re-ingest)  
**Sort order (within each partition file):** `trade_date ASC, account_id ASC, transaction_id ASC`

### 2.1 Column Schema

| Silver column | Source Orion column | dtype | Nullable | Derivation rule |
|---------------|---------------------|-------|----------|-----------------|
| `transaction_id` | `Transaction ID` | str | No | Direct copy. Primary dedup key. |
| `trade_date` | `TransDate` | date | No | Parse `M/D/YYYY 12:00:00 AM` → date. See §4 (date parsing). NaT guard: drop rows with unparseable TransDate, log count. |
| `household_id` | `Client ID` | int64 | No | Direct. |
| `registration_id` | `Reg ID` | int64 | No | Direct. |
| `account_id` | `Account ID` | int64 | No | Direct. Primary join key to accounts_dim. |
| `account_code` | `AcctCode` | str | No | Direct (custodian account number, e.g., `657-833748`). |
| `rep_id` | `Rep ID` | int64 | No | Direct. |
| `rep_name` | `RepName` | str | No | Direct. |
| `advisor_key` | (derived) | str | No | Slug from `rep_name`. See §5 (advisor_key derivation). |
| `rep_bucket` | (derived) | str | No | Enum. See §6 (rep bucketing). Values: `individual`, `firm`, `routing`. |
| `advisor_firm` | (derived) | str | No | Partner firm tag derived from `rep_id`. See §6.1 (advisor_firm derivation, INFGRD.002). Values: `inflection_wealth_management`, `other`, `unknown`. Used by `_apply_scopefix` to filter the Inflection-only cohort. |
| `custodian` | (derived) | str | No | Derived from `AcctCode` prefix. See §7 (custodian derivation). |
| `activity_category` | `Activity Category` | str | No | Direct. 12 known values (see brief §6.1). |
| `type_desc` | `TypeDesc` | str | No | Direct. 30+ values. |
| `trans_amount` | `TransAmount` | float64 | No | Direct. Signed (positive = inflow/credit, negative = outflow/debit). 100% populated per brief. |
| `units` | `NoUnits` | float64 | No | Direct. 100% populated. |
| `nav_price` | `NAVPrice` | float64 | No | Direct. 1.0 for `FID:CASH` rows — valid, not a data error. |
| `ticker` | `Ticker` | str | No | Direct. Preserve `FID:CASH` as-is; gold layer classifies cash tickers. |
| `download_symbol` | `Dwnld Symbol` | str | Yes | Direct. May differ from `ticker` for some instruments. |
| `product_name` | `Product Name` | str | No | Direct. |
| `reg_type` | `Reg Type` | str | No | Direct (IRA, Roth, Joint, TOD, etc.). |
| `account_value` | `CurrentAccountValue` | float64 | Yes | Direct. Point-in-time account value at transaction. Nullable (sparse in some rows). |
| `cash_value` | `CurrentCashValue` | float64 | Yes | Direct. Cash balance at transaction time. Nullable. |
| `trade_status` | `fkTradeStatus` | int64 | No | Direct. Always 1 in current data; retain for schema completeness. |
| `is_managed` | `Managed Account` | bool | No | Direct. Always True in current data. |
| `description` | `Description` | str | Yes | Direct. Free-text; sparse. |
| `tran_notes` | `TranNotes` | str | Yes | Direct. Sparse. |
| `client_last_name` | `LName` | str | Yes | Direct. PII — retained in silver, masked at platinum. |
| `registration_name` | `Reg Name` | str | Yes | Direct. PII — retained in silver, masked at platinum. |
| `created_date` | `CreatedDate` | datetime[ns] | Yes | Direct. Audit timestamp. |
| `created_by` | `CreatedBy` | str | Yes | Direct. Audit field. |
| `edited_date` | `EditedDate` | datetime[ns] | Yes | Direct. Audit timestamp. |
| `edited_by` | `EditedBy` | str | Yes | Direct. Audit field. |
| `source_file` | (derived) | str | No | Originating CSV filename (e.g., `TRN.csv`, `TRN (3).csv`). For provenance and dedup audit. |

**Total columns: 32** (was 31 pre-INFGRD.002; `advisor_firm` added 2026-04-27)

### 2.2 Excluded Orion columns

None. All 29 source columns are preserved or renamed to a silver column. No columns dropped.

---

## 3. Silver — AUM Snapshot

**Source:** Orion AUM export (household-level snapshot)  
**Current state:** Single date snapshot (2026-04-21). Additional snapshots appended over time.  
**Dedup key:** `(snapshot_date, household_id)` — must be unique. Drop duplicates keeping last.  
**Sort order:** `snapshot_date ASC, household_id ASC`

### 3.1 Column Schema

| Silver column | Source Orion column | dtype | Nullable | Derivation rule |
|---------------|---------------------|-------|----------|-----------------|
| `snapshot_date` | `Date` | date | No | Parse `M/D/YYYY 12:00:00 AM` → date. NaT guard: drop rows with unparseable Date, log count. |
| `household_id` | `HH ID` | int64 | No | Direct. |
| `household_name` | `HH Name` | str | Yes | Direct. PII — retained in silver. |
| `rep_id` | `Rep ID` | int64 | No | Direct. |
| `rep_name` | `Rep Name` | str | No | Direct. |
| `advisor_key` | (derived) | str | No | Same slug derivation as TRN §5. |
| `rep_bucket` | (derived) | str | No | Same enum as TRN §6. |
| `advisor_firm` | (derived) | str | No | Same partner firm tag as TRN §6.1 (INFGRD.002). Filters to `inflection_wealth_management` cohort at silver layer. |
| `managed_value` | `Managed Value` | float64 | No | Direct. Household managed AUM. |
| `unmanaged_value` | `Unmanaged Value` | float64 | Yes | Direct. May be 0 or null. |
| `firm_managed_aum` | `Firm Managed AUM` | float64 | No | Direct. Firm-level total; constant within a snapshot (667.1M at 2026-04-21). |
| `source_file` | (derived) | str | No | Originating CSV filename. |

**Total columns: 12** (was 11 pre-INFGRD.002; `advisor_firm` added 2026-04-27)

**Load frequency note (CTO clarification):** The spec supports daily, weekly, or monthly snapshot cadence — each new snapshot appends as a new `{snapshot_date}.parquet` file. Load-frequency decision is deferred pending Andrew §10 Q5/Q6 (historical AUM approach + history start date). Schema does not change regardless of cadence.

---

## 4. Silver — Accounts Dimension

**Source:** SlickGrid account registry (active accounts) + TRN all-time account fields (closed/historical accounts)  
**Grain:** One row per `account_id`  
**Partition:** Single file `silver/accounts_dim/latest.parquet` (no date partition — dimension is current-state only)  
**Rebuild strategy:** Full rebuild at each ingest run (not incremental). ~2,851 rows, trivial.  
**Dedup key:** `account_id` — must be unique. Where TRN and SlickGrid disagree on a field, SlickGrid wins for active accounts; TRN provides fallback for historical-only accounts.

### 4.1 Column Schema

| Silver column | Source | dtype | Nullable | Derivation rule |
|---------------|--------|-------|----------|-----------------|
| `account_id` | TRN + SlickGrid | int64 | No | Primary key. |
| `account_code` | TRN + SlickGrid | str | No | Custodian account number. |
| `household_id` | TRN + SlickGrid | int64 | No | Client-household link. |
| `registration_id` | TRN | int64 | No | Registration-level ID. |
| `registration_name` | TRN | str | Yes | PII. |
| `reg_type` | TRN + SlickGrid | str | No | Account registration type (IRA, Roth, Joint, etc.). |
| `custodian` | (derived) | str | No | From AcctCode prefix. See §7. |
| `rep_id` | TRN | int64 | No | Latest rep_id seen on TRN for this account. |
| `rep_name` | TRN | str | No | Latest rep_name seen on TRN. |
| `advisor_key` | (derived) | str | No | Same slug derivation as TRN §5. |
| `rep_bucket` | (derived) | str | No | Same enum as TRN §6. |
| `advisor_firm` | (derived) | str | No | Same partner firm tag as TRN §6.1 (INFGRD.002). Filters to `inflection_wealth_management` cohort at silver layer. |
| `investment_model` | SlickGrid | str | Yes | Model family (Lighthouse, IWM, etc.). Null for accounts without an assigned model (627 accounts / 42%). |
| `is_active` | SlickGrid | bool | No | True if account appears in SlickGrid registry (active). False for historical TRN-only accounts. |
| `first_trade_date` | TRN (derived) | date | No | Earliest `trade_date` seen for this `account_id` across all TRN files. |
| `last_trade_date` | TRN (derived) | date | No | Latest `trade_date` seen. |
| `source_file` | (derived) | str | No | `"slickgrid"` for SlickGrid-sourced rows; `"trn"` for TRN-only rows. |

**Total columns: 17** (was 16 pre-INFGRD.002; `advisor_firm` added 2026-04-27)

**Per-day attribution note (CTO clarification):** `accounts_dim` is a current-state lookup table only — it reflects the latest rep assignment per account as of the most recent TRN data. Per-day tagging-gated attribution (D_00c, D_02, D_04) MUST read `rep_id` at transaction grain from `silver/transactions/{date}.parquet`, NOT from `accounts_dim`. Using `accounts_dim` for historical attribution produces CHART-vs-LEADERBOARD methodology drift (same failure mode as the STAUDT incident just closed). `accounts_dim` is valid only for current-state portal headers and account selectors.

---

## 5. Advisor Key Slug Derivation

`advisor_key` is a stable, lowercase snake_case identifier derived from `rep_name`. It is the join key for all advisor attribution — matching the gold layer's advisor slug convention used by D_00c, D_02, D_04.

**Algorithm:**
```
slug = rep_name.strip().lower()
slug = re.sub(r'[^a-z0-9\s]', '', slug)   # remove punctuation
slug = re.sub(r'\s+', '_', slug)           # spaces to underscores
slug = re.sub(r'_+', '_', slug)            # collapse multiple underscores
```

**Canonical mappings (Inflection reps as of investigation brief):**

| `rep_name` | `advisor_key` | `rep_bucket` |
|-----------|---------------|--------------|
| Jeremy Keil | `jeremy_keil` | `individual` |
| Dan Sinnen | `dan_sinnen` | `individual` |
| Tim DeMuth | `tim_demuth` | `individual` |
| John Kurcz | `john_kurcz` | `individual` |
| Kevin Christensen | `kevin_christensen` | `individual` |
| Peter Lee | `peter_lee` | `individual` |
| Patrick Scanlan | `patrick_scanlan` | `individual` |
| Daria Zalewska | `daria_zalewska` | `individual` |
| Keil Financial Partners | `keil_financial_partners` | `individual` |
| Inflection Wealth Management | `inflection_wealth_management` | `firm` |
| New Accounts Rep | `new_accounts_rep` | `routing` |

**Note — Keil Financial Partners vs Jeremy Keil:** Brief §8.1 flags these as possibly the same advisor under two rep records. Silver preserves them as separate `advisor_key` values. Gold layer and D_00c will treat them as separate entities unless/until Inflection confirms a merge. If confirmed, the merge is a one-line gold-layer coalescing step — no silver rewrite needed.

---

## 6. Rep Bucket Convention

`rep_bucket` is an enum column added at silver layer to classify advisor rows by attribution type. Downstream gold scripts use this to route rows correctly.

| Value | Applies to | Gold treatment |
|-------|-----------|----------------|
| `individual` | Named human advisors | Include in leaderboard, advisor book, per-advisor NNA |
| `firm` | "Inflection Wealth Management" (287 HH / $193.6M) | Exclude from individual leaderboard; surface as "Firm" aggregate bucket in D_04 / header metrics |
| `routing` | "New Accounts Rep" (51,670 TRN rows, $0.02M AUM) | Exclude from all individual and firm attribution; used only for data completeness / audit |

**Rationale for `firm` vs exclusion:** The 29% / $193.6M of firm-managed AUM is too large to silently discard — it must be included in firm-level AUM totals and NNA. It is excluded only from the per-advisor leaderboard view.

---

## 6.1 advisor_firm Derivation (INFGRD.002, 2026-04-27)

`advisor_firm` is a partner-firm tag derived from `rep_id`, added to silver to enable a single-chokepoint multi-firm scope filter at the silver layer (`_apply_scopefix`). It is independent of `rep_bucket` and addresses a different concern:

- `rep_bucket` answers: is this row firm-aggregate, individual-advisor, or routing?
- `advisor_firm` answers: which partner firm does this row belong to?

The Inflection Orion export carries multi-firm read access — Inflection's Orion login can see Keil Financial Partners affiliates (Tim DeMuth, Kevin Christensen, Dan Sinnen, John Kurcz, Jeremy Keil, Daria Zalewska) in addition to Inflection's own data. `rep_id` is the only field that reliably distinguishes them.

**Algorithm (mirrors silver script `_advisor_firm()`):**
```
PARTNER_FIRM_TAGS = {
    'inflection': 'inflection_wealth_management',
    # Future: 'keil': 'keil_financial_partners',
}
INFLECTION_ADVISOR_FIRM_TAG = PARTNER_FIRM_TAGS['inflection']
INFLECTION_REP_IDS = {3, 11, 12}

def advisor_firm(rep_id):
    rid = int(rep_id)  # raises ValueError on bad input -> caught -> 'unknown'
    if rid in INFLECTION_REP_IDS:
        return 'inflection_wealth_management'
    return 'other'
```

**rep_id mapping (per ADVI_INFGRD.001 Phase 0 audit):**

| rep_id | rep_name | advisor_firm | Inflection? |
|---|---|---|---|
| 3 | Inflection Wealth Management | `inflection_wealth_management` | YES (firm placeholder, 287 HH, $193.6M) |
| 11 | Patrick Scanlan | `inflection_wealth_management` | YES (2 HH, $594K) |
| 12 | Peter Lee | `inflection_wealth_management` | YES (6 HH, $5.85M) |
| 1 | New Accounts Rep | `other` | NO (also `rep_bucket='routing'`, excluded by both predicates) |
| 4 | Keil Financial Partners | `other` | NO (Keil sub-firm placeholder) |
| 5 | Jeremy Keil | `other` | NO |
| 9 | John Kurcz | `other` | NO |
| 13 | Dan Sinnen | `other` | NO |
| 14 | Tim DeMuth | `other` | NO |
| 15 | Kevin Christensen | `other` | NO |
| 18 | Daria Zalewska | `other` | NO |

**Inflection-only AUA per advisor_firm filter:** $200.0M, 295 HH (vs Andrew expectation $191M, +4.7% within ±5% tolerance).

**SCOPEFIX-2 predicate** (replaces the broadened `firm_mask | indiv_mask` from commit 0233aee1):
```
firm_scope_mask = df['advisor_firm'] == INFLECTION_ADVISOR_FIRM_TAG
```

**Phase 0 guards (CTO contract review 2026-04-24, extended INFGRD.002 2026-04-27):**

- **Guard A:** raise if `rep_id` column missing or all-NaN advisor_firm post-derivation. Detects schema regression.
- **Guard B:** raise if filtered `managed_value` sum outside $50M-$400M (`GUARD_B_AUA_LOWER` / `GUARD_B_AUA_UPPER`). Defends against silent multi-firm contamination if Orion adds a new affiliate partner-firm to the export. Runs only on AUM build path (where `managed_value` exists).
- **Guard C:** print structured per-firm rep_id breakdown before filter applies. Provides visibility on what rows are being dropped vs kept.

**Notes:**
- The Inflection Orion export is the multi-firm contamination vector. The bronze-side fix (BRONZERUN_V2 W3.B) is the proper architectural cut; this silver-layer guard is the safety net + immediate ship vehicle.
- `New Accounts Rep` (rep_id=1) is `advisor_firm='other'` AND `rep_bucket='routing'` — excluded by both predicates. Either alone would suffice; both ensure defense-in-depth.
- **Long-term:** when Inflection's Orion config supports per-employee rep_ids for all 4 employees (Peter, Noel, Patrick, Joe — currently 2 of 4 in Orion), the allowlist needs maintenance. Pattern is already extractable to `PARTNER_FIRM_TAGS[partner]` for future Keil-as-partner onboarding.

---

## 7. Custodian Derivation

Derived from `account_code` prefix (the digits before the first `-`):

| AcctCode prefix | `custodian` value |
|----------------|-------------------|
| `657`, `645`, `636`, `628`, `637`, `656`, `655`, `638` | `fidelity` |
| `231`, `237`, `177`, `238`, `196` | `schwab` |
| All others (including `X96-` and any unknown prefix) | `unknown` |

The SlickGrid registry confirms 99.4% Fidelity, 5 Schwab, 4 Nationwide Advisory Solutions. Nationwide accounts have non-standard `account_code` prefixes — derive as `unknown` until a prefix pattern is confirmed from the raw SlickGrid data.

---

## 8. Date Parsing Convention

**Orion date format:** `M/D/YYYY 12:00:00 AM` (always midnight; date-only effective)

**Parse pattern:**
```python
pd.to_datetime(df['TransDate'], format='mixed', errors='coerce').dt.normalize()
```

The `.dt.normalize()` strips the always-midnight time component and preserves the date. Stored as `datetime64[ns]` in parquet but semantically a date — downstream scripts use `.dt.date` or cast to `pd.Timestamp.date()`.

**NaT guard (per d87377a5 incident mandate):** Any row where `pd.to_datetime(..., errors='coerce')` produces NaT must be dropped before writing to silver. Log: `WARN: dropped {N} rows with unparseable TransDate`. This is a hard pre-write check — no NaT dates ever land in `silver/transactions/`.

**Same rule applies to** `AUM snapshot.Date`, `CreatedDate`, `EditedDate` — coerce, log, drop on NaT.

---

## 9. Q2 2024 Gap Handling

**Decision: Documented absence — no row-level flag.**

The Q2 2024 gap (2024-04-01 through 2024-06-30, 65 business days) means no silver partition files will exist for dates in that window at initial load. When Andrew re-downloads from Orion and re-ingests:
- Those rows ingest normally through the same `convert_orion_to_silver.py` pipeline.
- No special `data_gap` column needed — the silver layer is append-correct once the files are present.

**Pipeline metadata:** A `silver/meta/gap_manifest.json` file will document the known gap window:
```json
{
  "known_gaps": [
    {"start": "2024-04-01", "end": "2024-06-30", "reason": "Q2 2024 re-download pending", "status": "open"}
  ]
}
```

Gold layer scripts that aggregate over date ranges must check `gap_manifest.json` and warn when the aggregation window spans an open gap (same pattern as BD's pipeline-complete.json check).

**Rationale:** Row-level `data_gap=True` flags would require a semantic that doesn't exist — we don't know today what those rows will look like. Absent files are explicit; present-but-flagged rows are ambiguous.

---

## 10. NaT Guard — Outer-Join Requirement

**Any silver-layer operation that produces an outer merge (left join, right join, merge with how='outer') across tables with different date ranges MUST include an explicit NaT coercion step before writing output.**

Pattern:
```python
df = df.merge(other, on='account_id', how='left')
nat_count = df['trade_date'].isna().sum()
if nat_count > 0:
    print(f"WARN: {nat_count} NaT trade_date rows after merge — dropping")
    df = df.dropna(subset=['trade_date'])
```

This requirement traces directly to the d87377a5 C_01 incident where an outer merge silently produced NaT date rows that propagated into the gold canonical NNA table.

---

## 11. Table-Level Decisions Summary

| Decision | Resolution |
|----------|-----------|
| Dedup key (TRN) | `transaction_id` — globally unique per Orion |
| Dedup key (AUM) | `(snapshot_date, household_id)` |
| Dedup key (accounts_dim) | `account_id` |
| Sort order (TRN) | `trade_date ASC, account_id ASC, transaction_id ASC` |
| Date column name | `trade_date` (matches BD silver convention) |
| Date dtype | `datetime64[ns]` normalized to midnight (BD pattern) |
| Date parsing format | `format='mixed'` with `errors='coerce'` + NaT drop |
| Advisor key | snake_case slug from `rep_name` |
| Firm-rep handling | `rep_bucket='firm'`, include in silver, exclude from individual leaderboard at gold |
| New Accounts Rep | `rep_bucket='routing'`, include in silver, exclude from all attribution at gold |
| Q2 2024 gap | Documented absence in `gap_manifest.json`; no row-level flag |
| Custodian | Derived from AcctCode prefix; 99.4% Fidelity |
| PII fields | `client_last_name`, `registration_name`, `household_name` retained in silver; masked at platinum |
| NaT guard | Mandatory on any outer merge; also on raw date parse |
| Exchange In/Out NNA treatment | Excluded at gold layer (not in silver schema — silver is raw) |
| FID:CASH ticker | Preserve as-is in silver; cash classification happens at gold |

---

## 12. CTO Sign-Off

**CTO SIGN-OFF 2026-04-21 via MCP — 1.0.0_SA_CTO. Three clarifications per MCP body added to sections 1, 3, 4. W3.2 implementation authorized.**

Clarifications incorporated:
1. §1 — Single-source-of-truth note: Inflection is Orion-only, no cross-source overlay.
2. §3 — AUM snapshot load-frequency deferred to Andrew §10 Q5/Q6.
3. §4 — Per-day attribution must read TRN grain, not accounts_dim (CHART-vs-LEADERBOARD guard).
