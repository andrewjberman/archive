# Brief: Account Mapping Gap — 335 Managed Accounts Invisible to Reconciliation

**Author:** 0.4.0_DS_ClientPlatform (validation session)
**Date:** 2026-04-06
**Project:** ADVI_GLDOPS
**Relates to:** GLDOPS.004 (Canonical Holdings Stack)

---

## Executive Summary

350 Schwab accounts holding $69.3M in AUA are excluded from the canonical holdings reconciliation pipeline (02b) because they are missing from `schwab_bd_account_mapping.parquet`. 335 of those accounts already exist in BD with full data — dimension table, positions cube, allocations, unrealized lots, and buy transactions. The mapping table simply was never updated to link their Schwab IDs to their BD IDs.

The root cause is that the mapping builder (`_schwab_bd_match_v3.py`) only uses realized (sell) transactions to fingerprint-match accounts. New accounts that have only purchased — never sold — are invisible to it. The gap is growing at ~3 accounts per trading day.

The fix is mechanical: BD's `account_number` field (in unrealized data) zero-padded to 10 digits equals the Schwab account ID for 98.6% of all mappings. A direct lookup resolves 335 of 350 accounts instantly.

---

## The Gap

### Current state (2026-04-02)

| Metric | Value |
|--------|-------|
| Unmapped Schwab accounts | 350 |
| Matchable via BD `account_number` | 335 |
| Truly unknown to BD | 15 ($650K, mostly Schwab proprietary products) |
| Total invisible AUA | $69.3M |
| Growth rate | ~3 new accounts/day, ~$840K/day |

### Growth trajectory

| Date | Unmapped | MV |
|------|------:|------:|
| 2026-01-20 | 110 | $5.7M |
| 2026-02-09 | 130 | $11.5M |
| 2026-03-03 | 211 | $35.7M |
| 2026-04-02 | 350 | $69.3M |

The acceleration began in early February 2026. 232 of the 335 matchable accounts opened in 2026. All are actively managed Opal clients — 196 hold 10+ model portfolio tickers (DIVZ, IDVZ, PFOE, SPYM, BIV, IEFA, etc.).

---

## Where BD Already Has These Accounts

| BD Data Source | Found | Notes |
|---|---:|---|
| Accounts dimension (script 00) | 330 / 335 | Name, open date, advisor, strategy |
| Silver allocations (daily AUA) | 329 / 335 | BD reports their AUA |
| Positions cube (script 02) | 329 / 335 | FIFO-reconstructed holdings |
| Unrealized (current lots) | 335 / 335 | Cost basis, CUSIPs, `account_number` |
| Realized (sell history) | 2 / 335 | Almost none have sold |
| Transactions (all files) | 330 / 335 | 240 have Buy txns, 330 have any txn |

BD is not lagged. BD is not missing data. For every account checked, **BD and Schwab agree on share counts down to the unit** (e.g., DIVZ 340 = DIVZ 340, PFOE 337 = PFOE 337). BD actually leads — accounts appear in BD's dimension table and positions cube first, then show up in Schwab RPS days to weeks later.

### Timeline pattern (287 accounts opened 2025+)

| Pattern | Count | % |
|---------|------:|--:|
| BD and Schwab appear within 2 days | 155 | 54% |
| BD opens first, Schwab follows 2-30 days later | 84 | 29% |
| BD opens first, Schwab follows 30+ days later | 47 | 16% |
| Schwab appears before BD | 1 | <1% |

---

## Root Cause

The mapping builder (`_schwab_bd_match_v3.py`) matches accounts via shared `(cusip, trade_date)` fingerprints from `silver/realized/bd_realized_compact.parquet`. A sell of the same security on the same date in both BD and Schwab = same account.

**New accounts that have only bought, never sold, produce zero realized rows.** The matcher cannot see them. Only 2 of 335 accounts have any realized history.

The irony: the mapping relationship is trivial for 98.6% of accounts. BD's `account_number` field (from unrealized or transactions) zero-padded to 10 digits **is** the Schwab account ID. No fingerprinting needed.

| Match method | Coverage |
|---|---|
| `account_number.zfill(10) == schwab_account_id` | 98.6% of all mappings |
| Fingerprint fallback (cusip + trade_date) | 1.4% (93 accounts with non-numeric BD account_numbers) |

---

## Impact on 02b (Canonical Holdings)

The GLDOPS.004 dry run reported:

- 43.4% reconciled
- 29.5% schwab_override
- 9.3% schwab gap-fill
- 17.8% BD-only

These numbers are computed against an incomplete mapping. The "schwab gap-fill" category (positions Schwab has that BD doesn't) is inflated — many of those Schwab-only positions belong to accounts BD knows about but can't join. Once the mapping is complete, gap-fill shrinks and reconciled/override grow, giving a more accurate picture of true FIFO drift.

---

## Recommended Fix

### 1. Add `account_number` lookup to the mapping builder

After the existing realized-based fingerprint match, do a direct lookup against `silver/unrealized/unrealized_gain_loss.parquet` for any Schwab accounts still unmapped:

```
for each unmapped schwab_id:
    if schwab_id in unrealized.account_number.zfill(10):
        map schwab_id -> unrealized.account_id
```

This resolves 335 accounts immediately. The fingerprint path remains as fallback for the ~1.4% of accounts with non-numeric BD account_numbers.

### 2. Make mapping refresh a pre-step in the pipeline

The mapping should not depend on manual diagnostic runs. Two options:

**Option A:** Run the enhanced mapper as a pre-step in `run_gold_layer.sh`, before 02/02b. Same pattern as `build_canonical_prices_v2` and `inject_scoped_overrides`.

**Option B (preferred):** Embed self-healing mapping logic directly in 02b's startup. On each run:
1. Load current mapping
2. List all Schwab RPS account IDs for the date range
3. For any unmapped, lookup BD `account_number` from unrealized
4. Append new matches, write updated mapping to S3
5. Proceed with reconciliation

Option B is self-healing — every run catches new accounts automatically. No separate script, no scheduling, no manual trigger.

### 3. Schwab coverage extends to 2024-01-01

The other DS session built the Schwab silver pipeline from 52 RPS files (2026-01-20 to 2026-04-02) found on OneDrive. The full archive (2024-01-01 to 2026-01-19) is in `opal-data-schwab` (currently being restored from accidental deletion). Once restored, consolidate into `opal-data-bd/schwab/bronze/` and re-run the converter. This extends reconciliation from 52 trading days to ~550+.

---

## The 15 Truly Unknown Accounts

15 Schwab accounts ($650K) do not appear in any BD data source:

- 5 hold Schwab proprietary products (SCBP1, SCGN1, SCGT1)
- 4 hold T. Rowe Price funds (TLVAX, TPAIX, TPLNX) — $462 each
- 1 holds an Opal model signature (DIVZ, IDVZ, etc.) — $137K — **this one warrants investigation**
- Remainder: small positions in individual stocks or ETFs

These are likely non-managed accounts on the Schwab platform. The single account with Opal model holdings (`0071040534`, $137K) should be investigated — it may be a newly onboarded account that BD hasn't ingested yet.

---

## Sequence of Work

1. Restore `opal-data-schwab` and consolidate bronze RPS into `opal-data-bd/schwab/bronze/`
2. Re-run converter with `--force` for full 2024-2026 silver coverage
3. Enhance mapping builder (add unrealized `account_number` lookup)
4. Rebuild mapping — expect jump from 6,510 to ~6,845 pairs
5. Re-run 02b dry run with complete mapping to get accurate reconciliation numbers
6. Add watermarks before any production writes
7. Wire 02b into `run_gold_layer.sh` (only after script 05 is ready to consume it)

---

## Data Sources Referenced

| Source | Path | Purpose |
|--------|------|---------|
| Account mapping | `gold/dimensions/schwab_bd_account_mapping.parquet` | Schwab-BD ID join table (6,510 pairs) |
| Schwab RPS (silver) | `schwab/silver/rps/date={YYYYMMDD}/data.parquet` | Schwab custodial position snapshots |
| BD unrealized | `silver/unrealized/unrealized_gain_loss.parquet` | Current lots, has `account_number` |
| BD realized | `silver/realized/bd_realized_compact.parquet` | Sell history, used by v3 matcher |
| Positions cube | `gold/timeseries/positions_cube/{date}.parquet` | BD FIFO-reconstructed holdings |
| Accounts dimension | `gold/dimensions/accounts_dimension_latest.parquet` | Account metadata |
| Silver allocations | `silver/allocations/{date}.parquet` | BD daily AUA |
| BD transactions | `silver/transactions/{date}.parquet` | All transaction types |
