# Brief: Canonical Data Stack — Session 2 Build Summary

**Author:** 0.4.0_DS_ClientPlatform
**Date:** 2026-04-06
**Project:** ADVI_GLDOPS
**Task Order:** ADVI_GLDOPS.004

---

## What Was Built

Two new gold layer scripts and three bronze-to-silver converters that establish the first two layers of an immutable canonical data stack for the advisory pipeline.

### Layer 1: Canonical Positions (02b)

**Script:** `data/black_diamond/scripts/gold/02b_build_canonical_holdings.py`

Reconciles BD's FIFO-reconstructed positions (02 positions_cube) with Schwab's custodial position snapshots (RPS). For every account on every date, produces one authoritative row per position with a source tag indicating provenance.

**What it does on each run:**
1. Loads the existing Schwab-BD account mapping (6,424 pairs)
2. Self-heals the mapping by scanning BD unrealized for `account_number` — zero-padded to 10 digits equals the Schwab ID. Adds ~1,534 new pairs that the old realized-fingerprint matcher missed (buy-only accounts).
3. Builds a CUSIP bridge from BD unrealized + realized (8,330 entries, 98.1% Schwab CUSIP coverage) to resolve Schwab CUSIPs to BD asset names
4. For each date, reads the positions_cube partition and the Schwab RPS partition
5. Applies three exclusion layers: ghost accounts (4), BD account closures (371, date-aware), silver allocations phantom gate (accounts with AUA >= $100)
6. Full outer joins BD + Schwab on (account_id, asset_name)
7. Classifies each position: `bd` (BD only), `schwab` (gap-fill), `reconciled` (both agree), `schwab_override` (disagree, Schwab wins)
8. Prices with canonical_prices, writes date-partitioned parquet

**Key result (2026-04-02 dry run):**

| Source | Positions | % |
|--------|-----------|---|
| reconciled | 44,647 | 47.5% |
| schwab_override | 27,965 | 29.7% |
| bd (non-Schwab accounts) | 12,686 | 13.5% |
| schwab (gap-fill) | 8,785 | 9.3% |

47.5% of all positions are now cross-validated between BD and Schwab. The 29.7% override rate confirms significant FIFO drift in BD's reconstruction — exactly the problem this layer solves.

**Output:** `gold/canonical/holdings/{YYYY-MM-DD}.parquet`
**Schema:** `date, account_id, asset_name, units, price, market_value, source, bd_units, schwab_units, ticker`

### Layer 2: Canonical Lots (03b)

**Script:** `data/black_diamond/scripts/gold/03b_build_canonical_lots.py`

Produces per-lot tax detail for both open (unrealized) and closed (realized) positions.

**Gating model (transitive, not re-implemented):**
- Unrealized lots: gated by canonical_holdings (02b output) — only accounts/positions that survive 02b's exclusions get lots. 02b itself is gated by BD closures + silver allocations + ghost exclusion. 03b inherits this transitively, it does not re-implement the exclusion logic.
- Realized lots: gated by accounts_dimension closure date (not canonical holdings), because an account can close its last position and still need that day's realized lots for tax purposes.
- AUA benchmark: lot coverage is measured against BD silver allocations ($1.632B) — this is BD's official AUA. Not canonical holdings ($1.875B), which includes Schwab enrichment above what BD acknowledges.

**What it does on each run:**
1. Inherits the same self-healing account mapping and CUSIP bridge as 02b (loaded once, passed through)
2. Loads BD unrealized (current lot snapshot: open_date, unit_cost) and BD realized (all historical closures)
3. Loads Schwab ULN (non-taxable unrealized lots) + ULT (taxable unrealized lots) + RLD (realized lots) for the date
4. For unrealized: Schwab lots are primary for Schwab-custodied accounts (full tax detail). BD-only lots emitted only for dates near the snapshot (avoids temporal mismatch — BD unrealized is a current-state snapshot, not a time series).
5. For realized: gated by accounts_dimension closure date, so accounts closing their last position still get realized lots recorded

**Key result (2026-01-23 dry run):**

Two AUA numbers:

| Source | AUA (2026-04-02) | What it is |
|--------|-------------------|------------|
| BD silver allocations | $1.632B | BD official AUA — the anchor. 6,090 alive accounts. |
| Canonical holdings (02b) | ~$1.875B | BD + Schwab reconciled (+$243M / +14.9% over BD) |

The $243M gap is entirely Schwab enrichment — positions Schwab's custodial record sees that BD's allocations don't report. 03c (capital gains aggregation) can decompose this drift daily by account.

| Metric | Value |
|--------|-------|
| BD silver AUA (benchmark) | $1,632,000,000 |
| Unrealized lots MV | $564,935,998 |
| Lot coverage vs BD AUA | 34.6% |
| Unrealized G/L | $70,057,638 |
| Realized lots (that day) | 514 |
| Realized G/L | $171,550 |

34.6% coverage reflects ULN-only (retirement accounts). ULT (taxable brokerage) conversion is in progress — once complete, coverage is projected to reach ~83% of BD AUA. The remaining ~17% is BD-only accounts with no Schwab custody.

**Output:**
- `gold/canonical/lots_unrealized/{YYYY-MM-DD}.parquet` — open tax lots
- `gold/canonical/lots_realized/{YYYY-MM-DD}.parquet` — closed tax lots

**Schema (unrealized):** `date, account_id, asset_name, cusip, ticker, acquired_date, lot_index, source, quantity, current_price, market_value, cost_basis, cost_per_share, adjusted_cost_basis, original_purchase_price, unrealized_gain_loss, days_held, holding_type, disallowed_loss`

**Schema (realized):** `date, account_id, asset_name, cusip, ticker, closing_date, acquired_date, source, quantity, proceeds, proceeds_per_share, cost_basis, cost_per_share, adjusted_cost_basis, original_purchase_price, gain_loss_dollars, gain_loss_pct, adjusted_gain_loss_dollars, days_held, holding_type, disallowed_loss`

Both carry `account_id` + `holding_type` (S/L) + gain/loss fields for direct downstream aggregation of per-account capital gains.

---

## Schwab Data Pipeline

### New S3 layout

All Schwab data consolidated under `opal-data-bd/schwab/`:

```
opal-data-bd/schwab/
  bronze/     52 raw CRS*.RPS files (uploaded from local OneDrive)
  silver/
    rps/      558 partitions  2024-01-12 to 2026-04-02  (positions)
    uln/      316 partitions  2024-01-12 to 2026-02-26  (unrealized lots, non-taxable)
    ult/      converting      2024-01-12 to 2026-02-26  (unrealized lots, taxable)
    rld/      590 partitions  2023-01-17 to 2026-03-30  (realized lots)
```

### Converters built

| Script | Input | Output | Status |
|--------|-------|--------|--------|
| `bronze/convert_schwab_rps_to_silver.py` | CRS*.RPS | `schwab/silver/rps/` | Done (558 dates) |
| `bronze/convert_schwab_lots_to_silver.py uln` | CRS*.ULN | `schwab/silver/uln/` | Done (316 dates) |
| `bronze/convert_schwab_lots_to_silver.py ult` | CRS*.ULT | `schwab/silver/ult/` | In progress |
| `bronze/convert_schwab_lots_to_silver.py rld` | CRS*.RLD | `schwab/silver/rld/` | Done (590 dates) |

All converters read from both `opal-data-schwab/01_raw/` (existing archive) and `opal-data-bd/schwab/bronze/` (new consolidated location), with opal-data-bd taking priority.

### RPS consolidation

558 silver/RPS partitions copied this session from `opal-data-schwab/silver/RPS/` (restored bucket, confirmed 18,310 objects / 319GB intact) into `opal-data-bd/schwab/silver/rps/`. Full 2-year Schwab position history now in one location. The `opal-data-schwab` bucket remains the archive; `opal-data-bd/schwab/` is the active operational path.

---

## Watermarks (sealed-day immutability)

02b includes a watermark system:
- `gold/canonical/watermarks.json` tracks sealed dates
- Sealed dates skipped on subsequent runs (no silent overwrite)
- `--force` required to reprocess a sealed date
- `--no-seal` for testing
- Not yet in 03b (acknowledged as next step)

---

## Account Mapping Self-Healing

The original `schwab_bd_account_mapping.parquet` (6,424 pairs) was built by fingerprinting realized transactions — accounts that only bought (never sold) were invisible. A validation brief (`briefs/2026-04-06_account_mapping_gap_brief.md`) identified 335 Schwab accounts ($69.3M AUA) missing from the mapping.

Both 02b and 03b now self-heal on every run: BD's `account_number` zero-padded to 10 digits = Schwab account ID for 98.6% of accounts. This added 1,534 new mappings (total 7,958). Every new client onboarded is picked up automatically the moment they appear in BD unrealized — no manual mapping runs needed.

---

## Reviewer Feedback Incorporated

### 02b (external review):
- Dead code (`price_holdings` non-vectorized) — removed
- Dual `S3_CANONICAL_PRICES_KEY` definition — fixed, imported from s3_layout
- Silver allocations per-date S3 calls — replaced with parallel batch preload
- Watermarks — implemented

### 03b (other DS review):
- **BD unrealized is a snapshot, not a time series** — BD-only lots now restricted to dates within 7 days of the snapshot. Historical dates emit Schwab-sourced lots only.
- **Unrealized loaded twice** — loaded once at startup, passed to mapping + CUSIP bridge + lots builder
- **Realized alive gate too strict** — realized lots now gated by accounts_dimension closure date, not canonical holdings. Accounts closing their last position still get realized lots recorded.

### ULT discovery (other DS brief):
- ULN only covers retirement accounts (non-taxable). ULT covers taxable brokerage accounts — where lot detail matters most for tax purposes.
- Zero overlap between ULN and ULT. Combined coverage: ~99.9% of Schwab accounts.
- ULT added to converter and 03b. Conversion in progress.

---

## Files Created

| File | Purpose |
|------|---------|
| `data/black_diamond/scripts/gold/02b_build_canonical_holdings.py` | Canonical positions (BD + Schwab reconciliation) |
| `data/black_diamond/scripts/gold/03b_build_canonical_lots.py` | Canonical lots (unrealized + realized, tax detail) |
| `data/black_diamond/scripts/bronze/convert_schwab_rps_to_silver.py` | RPS bronze-to-silver converter |
| `data/black_diamond/scripts/bronze/convert_schwab_lots_to_silver.py` | ULN/ULT/RLD bronze-to-silver converter |

## Files Modified

| File | Change |
|------|--------|
| `data/black_diamond/scripts/gold/lib/s3_layout.py` | Added canonical holdings keys, canonical lots keys, canonical prices key, Schwab silver prefixes, watermark key |

---

## What's Not Done

| Item | Why |
|------|-----|
| Full backfill (02b across 2,284 dates) | Run on EC2, not local |
| Wire into run_gold_layer.sh | Wait for script 05 cutover |
| Script 05 refactor | Separate task — 05 reads canonical_holdings instead of positions_cube |
| 03c capital gains aggregation | Per-account-per-day rollup of unrealized + realized G/L from 03b |
| ULN gap (2026-02-27 to 2026-04-02) | Waiting for local file downloads to complete |
| ULT conversion | In progress — 03b dry run numbers are pre-ULT (retirement accounts only). Coverage will jump from ~34% to ~83% once ULT completes. |
| Watermarks for 03b | Same pattern as 02b, not yet added |
| Upload scripts to S3 code path | After validation on EC2 |

---

## Canonical Stack Architecture

```
canonical_prices (silver)                     [EXISTS]
  -> 02  positions_cube (BD FIFO replay)      [EXISTS]
  -> 02b canonical_holdings (BD + Schwab)     [BUILT]   <-- this session
    -> 03b canonical_lots (tax lots)          [BUILT]   <-- this session
      -> 03c capital_gains (per-acct rollup)  [NEXT]
    -> canonical_nna (rollup of 02b + txns)   [FUTURE]  -- not a separate layer,
    -> canonical_market_growth (rollup of 02b)  [FUTURE]    aggregations of existing layers
      -> 05 client_performance (assembly)     [REFACTOR]
```

Each layer depends only on the one above it. Each layer is built once per day, validated, and sealed. Downstream scripts read canonical tables instead of re-deriving from silver.

Note: canonical_nna and canonical_market_growth are not independent builds — they are aggregations of canonical_holdings and canonical_lots. Once 03c (capital gains aggregation) exists, NNA becomes a transaction-flow rollup against the canonical account set, and market_growth becomes `holdings[today].mv - holdings[yesterday].mv` per relationship. Script 05 shrinks from 1,055 lines / 30-40 min to a thin assembly step.
