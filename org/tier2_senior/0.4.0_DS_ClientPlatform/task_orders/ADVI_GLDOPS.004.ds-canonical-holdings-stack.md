# ADVI_GLDOPS.004 — DS: Build Canonical Holdings Stack (BD + Schwab RPS Reconciliation)

<task_order>
  <issuer>0.4.0_DS_ClientPlatform</issuer>
  <issued>2026-04-06</issued>
  <agent>0.4.0_DS_ClientPlatform</agent>
  <status>staged</status>
  <priority>high</priority>
  <project>ADVI_GLDOPS</project>
  <depends_on>GLDOPS.003 (complete), yahoo backfill (complete)</depends_on>
</task_order>

## Problem

The gold pipeline currently derives everything from scratch every run. There is no
immutable canonical layer — positions, NNA, and market growth are all recomputed from
silver on every execution. This creates three problems:

1. **No Schwab RPS reconciliation.** `positions_cube` (script 02) reads BD positions
   only. Schwab RPS (`daily_positions.parquet`, `daily_aua.parquet`, `daily_flows.parquet`)
   exists in silver but is never used for validation or gap-filling. BD has 6,039
   accounts with NNA events; Schwab RPS covers 1,470. For accounts in both systems,
   BD and Schwab may disagree on positions or AUA.

2. **No sealed-day guarantee.** Every full run reprocesses all ~1,500 days back to 2020.
   A bug fix in script logic retroactively changes historical values that were previously
   correct. There is no "this day is validated and locked" marker.

3. **Monolithic script 05.** Client performance, NNA, market growth, churn, and synthetic
   correction are all computed in one 1,050-line script. These are logically separate
   canonical layers that should be independently buildable, validatable, and sealable.

## Goal

Establish four canonical data stacks, each built in order and each immutable once
validated. Downstream computations read canonical tables, never re-derive them.

```
Stack 1: canonical_prices         (asset, date) -> price, source
Stack 2: canonical_holdings       (account, asset, date) -> units, price, mv
Stack 3: canonical_nna            (relationship, date) -> inflows, outflows, nna
Stack 4: canonical_market_growth  (relationship, date) -> market_growth
```

Each stack depends only on the one above it plus silver source data.

## Deliverables

### Phase 1: Canonical Holdings Table

Build `gold/canonical/holdings.parquet` — the single source of truth for what was
held in every account on every date. Grain: (date, account_id, asset_name) -> units.

**Sources to reconcile:**

| Source | What it has | Coverage | Location |
|--------|-------------|----------|----------|
| BD allocations | Account-level positions with units | All accounts, all dates | silver/allocations/ (recent), bronze/ (historical) |
| Schwab RPS positions | Account-level positions with units + market_value | Schwab accounts only, 2020-present | silver/daily_positions.parquet (682MB) |
| Positions cube (current) | Reconstructed units from BD transactions | All accounts, all dates | gold/timeseries/positions_cube/ |

**Reconciliation logic:**

1. Start with positions_cube as baseline (broadest coverage).
2. For accounts present in Schwab RPS, cross-check units per (account, asset, date).
3. Where Schwab and BD agree (within tolerance): use BD (it has more history).
4. Where they disagree: flag for review. Schwab is custodian-authoritative for
   Schwab accounts. BD may have stale/phantom positions for closed accounts.
5. For accounts NOT in Schwab (non-custodial, 401k, etc.): BD is sole source.
6. Price all positions using canonical_prices.parquet (Stack 1).
7. Output: `canonical_holdings.parquet` with columns:
   `date, account_id, asset_name, units, price, mv, source (bd|schwab|reconciled)`

**Validation gate:** total canonical AUA per day must be within 2% of Schwab RPS
`daily_aua.parquet` firm total for the Schwab-covered subset.

### Phase 2: Canonical NNA Table

Extract NNA computation from script 05 into a standalone canonical table.

Build `gold/canonical/nna.parquet` — grain: (date, account_id) -> daily_inflow,
daily_outflow. Aggregatable to relationship level.

**Sources:**

| Source | What it has | Coverage |
|--------|-------------|----------|
| BD transactions | Cash Deposit, Transfer In, Cash Withdrawal, Transfer Out | All accounts |
| Schwab RPS flows | daily_flows.parquet: contribution, withdrawal per account per day | Schwab accounts |

**Reconciliation logic:**

1. BD transactions classified by type (existing nna_flows.py logic) + garbage filter.
2. For Schwab accounts: cross-check BD daily NNA vs Schwab RPS daily_flows.
3. Where they agree: use BD (transaction-level detail).
4. Where they disagree by >$1K: flag. Schwab is authoritative for Schwab flows.
5. Validate: for matched accounts, aggregate annual NNA should be within $8M
   (established tolerance from 2025 FY analysis: $171.5M BD vs $179.2M Schwab
   on 1,469 matched accounts).

**Validation gate:** firm-level annual NNA should reconcile with both BD external_flow
and Schwab RPS flows within established tolerance.

### Phase 3: Canonical Market Growth Table

Build `gold/canonical/market_growth.parquet` — grain: (date, relationship_id) ->
market_growth. Deterministic from canonical_holdings + canonical_prices.

**Computation (already implemented in script 05, extract it):**

```
market_growth = sum(units_today * price_today) - sum(units_today * price_yesterday)
```

This is a pure function of Stacks 1 + 2. No transaction data, no NNA, no residual.

**Validation gate:** annual firm-level market_growth should be within 2pp of
model portfolio benchmark (weighted by actual model mix). 2025 FY target: 12-15%.

### Phase 4: Refactor Script 05

Refactor `05_build_client_performance.py` to READ the three canonical tables
instead of re-deriving them:

```python
# OLD (current): loads raw silver, recomputes everything
prices = load_canonical_prices(cube_dates)
flows  = load_flows_from_transactions()  # re-classifies 3.9M txns
# ... process 1500 partitions to get AUA, then residual formula ...

# NEW: reads pre-built canonical tables
holdings = pd.read_parquet('gold/canonical/holdings.parquet')
nna      = pd.read_parquet('gold/canonical/nna.parquet')
mkt      = pd.read_parquet('gold/canonical/market_growth.parquet')
# ... join and emit client_performance.parquet
```

Script 05 becomes an assembly step, not a derivation step. Runtime drops from
30-40 min to ~5 min (just joins + writes, no positions_cube processing).

### Phase 5: Sealed-Day Markers

Add a watermark system so completed days are never reprocessed:

```
gold/canonical/watermarks.json
{
  "holdings":      "2026-04-06",   // all days through this date are sealed
  "nna":           "2026-04-06",
  "market_growth": "2026-04-06"
}
```

Daily incremental: process only dates > watermark. Full rebuild: only needed if
canonical logic changes (watermark reset).

## Execution Plan

Phase 1 is the critical path — canonical holdings is the foundation. Phases 2-3
can follow quickly since the NNA and market growth logic already exist (nna_flows.py
and the direct price-change formula). Phase 4 is a refactor of script 05. Phase 5
is a small addition.

**Phase 1 subtasks:**

1a. Load and profile Schwab RPS daily_positions.parquet: schema, date range,
    account coverage, asset granularity. Determine if units match BD's definition.

1b. Build reconciliation logic: for each (date, account, asset), pick the
    authoritative source. Resolve conflicts by preferring Schwab for custodied
    accounts, BD for non-custodial.

1c. Write canonical_holdings.parquet. Validate against daily_aua.parquet.

1d. Price with canonical_prices. Validate firm AUA vs silver AUA.

**Estimated sizes:**
- canonical_holdings: ~200M rows (1500 dates x ~100K positions/day), ~2-4 GB parquet
- canonical_nna: ~10K rows (1500 dates x ~6 accounts with flows/day), ~1 MB
- canonical_market_growth: ~5M rows (1500 dates x ~3500 relationships), ~50 MB

## Acceptance Criteria

- [ ] canonical_holdings.parquet exists with BD + Schwab reconciliation
- [ ] canonical_nna.parquet exists, validated against BD external_flow + Schwab RPS
- [ ] canonical_market_growth.parquet exists, validated against model returns (2025 FY within 2pp)
- [ ] Script 05 refactored to read canonical tables instead of re-deriving
- [ ] Watermark system prevents unnecessary recomputation
- [ ] Full gold pipeline produces identical downstream output (07, 08, 09, 10, 11a, 11b)
- [ ] Daily incremental processes only new dates (watermark-gated)

## Not In Scope

- Changing the silver layer ingestion (BD exports, Schwab RPS feeds)
- Modifying portal frontend (downstream of publisher JSON, unchanged)
- Changing transaction classification rules (nna_flows.py logic preserved)
- New data sources beyond BD + Schwab RPS
