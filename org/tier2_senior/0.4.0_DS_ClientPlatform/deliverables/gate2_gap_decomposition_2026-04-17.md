# Gate 2 Gap Decomposition — CP-DS1 Firm-MV Overage Analysis

**Date:** 2026-04-17 (UTC ~12:17Z)
**Author:** 0.4.0_DS_ClientPlatform~B (joint deliverable with ~A on code-path mechanism; this file is the account-level data audit)
**Trigger:** CTO T115511Z / COO T120XZ — decompose the $423M gap between Run 5 `gold/timeseries/holdings_lots/2026-04-15.parquet` open MV and `silver/allocations/2026-04-15.parquet` non-cash target.

---

## TL;DR

**92% of the $423M Gate 2 overage is pre-existing RPS synthetic-lot injection ($390.7M of $423.1M). CP-DS1 did NOT introduce it.** The injection path is the buy-gap mechanism from ADHC_HISTRY P2 (~`5800ae2a`, 2026-04-05). Gate 2 gap is broadly distributed (Top 200 accts = 52% of overage). **Recommendation: SHIP CP-DS1 on Gate 1 acceptance. Gate 2 is a separate CP-SYNTHETIC follow-up TO, not a CP-DS1 blocker.**

---

## 1 — Firm-level numbers (observed)

| Metric | Value |
|---|---|
| gold open MV (Run 5 holdings_lots/2026-04-15) | **$2,083,420,732** |
| silver/allocations non-cash target | $1,660,325,207 |
| **gold - alloc (Gate 2 gap)** | **+$423,095,525** (+25.5% over target) |
| of which: rps_synth injection MV | **$390,662,552 (92.3% of gap)** |
| of which: FIFO-only accounts (in gold, not in silver/allocations) | $43,677,626 (10.3% of gap) |
| residual (all other sources combined) | -$11,244,653 (gold slightly under alloc on the non-synth, in-common accts) |

**Decomposition:** $390.7M + $43.7M = $434.4M additive pressure, partially offset by -$11.2M under-representation on ex-synth in-common accts → net +$423.1M.

## 2 — Account-count distribution

| Cohort | Count | Gold MV | Alloc non-cash MV |
|---|---|---|---|
| accts in gold open (7,291) | 7,291 | $2,083M | — |
| accts in silver/allocations non-cash (5,944) | 5,944 | — | $1,660M |
| **in BOTH** | 5,936 | ~$2,040M | $1,660M |
| **in GOLD but NOT in alloc (FIFO-only)** | **1,355** | **$43.7M** | $0 |
| in ALLOC but NOT in gold (silver-only) | 8 | $0 | ~$0 |

**FIFO-only cohort (1,355 accts, $43.7M)** — these are accounts where FIFO has open lots from historical BD txn activity but silver/allocations 2026-04-15 has no entry. Candidates: terminated / closed-out accounts where transactions never finalized, or accounts on a parallel ledger not surfacing in allocations. **Gate 2 follow-up: confirm via silver/allocations historical scan whether these accts ever appeared, and whether force-close is warranted.**

## 3 — Concentration of the $423M overage

| Cohort | Cumulative gold-minus-alloc |
|---|---|
| Top 20 accts | $64.2M (15.2%) |
| Top 50 accts | $123.8M (29.3%) |
| Top 100 accts | $164.5M (38.9%) |
| Top 200 accts | $218.0M (51.5%) |
| Top 500 accts | ~$310M (73%) |
| All 7,291 accts | $423.1M (100%) |

**Moderately distributed — NOT a single-cohort issue.** Top 200 accts cover ~50% but the long tail (5,000+ accts) also contributes meaningfully. This rules out "one sub-master feed is broken" as the sole cause.

## 4 — Top 20 over-reporting accounts

| acct | gold_mv | alloc_noncash | gold-alloc | synth_mv | n_lots |
|---|---|---|---|---|---|
| z0814293421 | $17.75M | $56k | **+$17.69M** | $17.69M (100% synth) | 175 |
| z0820603691 | $10.58M | $0 | +$10.58M | $10.58M (100% synth) | 13 |
| z0819425671 | $12.07M | $5.46M | +$6.61M | $1.40M | 199 |
| z0820852301 | $12.99M | $9.20M | +$3.79M | $3.38M | 49 |
| z0822224971 | $8.52M | $5.03M | +$3.49M | $0 | 5 |
| z0818927251 | $25.55M | $22.11M | +$3.44M | $3.77M | 385 |
| z0814307721 | $6.29M | $2.86M | +$3.43M | $1.53M | 67 |
| z0820583781 | $8.21M | $5.06M | +$3.16M | $3.20M | 56 |
| z0822080411 | $5.08M | $1.95M | +$3.13M | $1.37M | 113 |
| z0817114311 | $6.94M | $4.15M | +$2.79M | $2.04M | 79 |
| ...(Top 20 tail) | | | ≈$1-3M each | | |

**Observations:**
- Accts like z0814293421 (99.99% synth) and z0820603691 (100% synth) are RPS-dominant — Schwab has positions that silver/allocations does not reflect.
- Accts like z0822224971 ($0 synth but $3.49M overage) are pure FIFO over-count — phantom positions CP-DS1 did NOT close (because RPS has no row → absence-of-row → _has_rps_row gate skips per ae759bbb).
- Mix of patterns. Not a single mechanism.

## 5 — Mechanism decomposition

### A. Synthetic lot injection ($390.7M — 92% of gap)

- Path: `_build_rps_synthetic_lots()` buy-gap injection (B_01 L1052+). Existed pre-CP-DS1.
- When RPS has position (account_id, cusip) that FIFO lacks, injects synthetic lots at `lot_id = '{account}:{asset}:rps_synth:1'`.
- Reasonable intent: FIFO's transaction history misses some Buys (BD feed lag, account-migration events). RPS is authoritative custodial view → inject.
- Side effect: if RPS says position is open but silver/allocations doesn't reflect it (because allocation aggregation window differs from RPS settlement, or because allocation uses a different cost basis), the synth lot is "real per Schwab" but doesn't match the BD aggregation target.
- **Pre-existing — CP-DS1 didn't change this logic.** CP-DS1 only changed the sell-correction merge key (name → cusip).

### B. FIFO-only accounts ($43.7M — 10.3% of gap)

- 1,355 accts where gold has positions + silver/allocations has none.
- FIFO-only cohort overlaps significantly with the 472 chronic-mapped-zero-RPS (~A's path-B result) and the terminated-account cohort (accts BD removed from allocation but whose txn history still has open Buys).
- The `phantom lot reconciliation` pass at L1810 handles this — Rule 1 zeroes accts with alloc_aua < $100, Rule 2 zeroes accts where lot_mv > 2x alloc_aua AND lot_mv > $50K. Some of the 1,355 are caught; some aren't (smaller MV, below-threshold).

### C. Residual (offset, -$11.2M)

- For the 5,936 accts in both gold + alloc, gold slightly undercounts alloc on average. Likely attributable to snapshot timing skew (silver/allocations is 2026-04-15 close, gold FIFO lots consume sells through 2026-04-15, but silver/unrealized may include intraday movements).

## 6 — Ship-vs-fix call

### SHIP CP-DS1 (recommended)

- **Gate 1 PASS** — structural fix complete. Force-close cohort 0 alerts, 0 resolved. The chronic halt is eliminated.
- **92% of Gate 2 gap is pre-existing**, not caused by CP-DS1. Blocking CP-DS1 ship on Gate 2 would mean blocking on a mechanism that existed for weeks pre-CP-DS1 — rejection of CP-DS1 wouldn't fix Gate 2 either.
- **CP-DS1 benefits:** clean CUSIP-keyed matching, no more name-drift force-closes, pathway to WP-9 retired.
- **Residual Gate 2 gap is a SEPARATE investigation** — not blocking.

### NEW TOs to author (Gate 2 follow-ups, not CP-DS1 scope)

1. **CP-SYNTHETIC.A1 — Synthetic lot injection audit** (P0 P1 next): investigate the $390.7M synth injection. For each acct where synth_mv > alloc_noncash, determine whether Schwab RPS is correct (silver/allocations undercounts) or RPS is over-representing (mapping or timing error). Owner: DS (~B).

2. **CP-SYNTHETIC.A2 — FIFO-only account coverage** (P1): 1,355 accts with gold MV but no silver/allocations row. Classify: (a) terminated accts (FIFO should close), (b) parallel-ledger accts (expected FIFO-only), (c) allocation-feed gaps. Owner: DS (~B).

3. **CP-SYNTHETIC.A3 — Phantom lot reconciliation threshold tuning** (P2): L1810 Rule 2 (`lot_mv > 2x alloc_aua AND lot_mv > $50K`) may miss smaller-MV phantom cases. Revisit thresholds with current Gate 2 data. Owner: DS.

## 7 — Cross-reference with ~A joint deliverable

~A (code-path mechanism audit): responsible for task 1 (synthetic-buy MV via code trace), task 2 (B_01 L1810 firing audit), task 3 (Pop A FIFO persistence in Run 5), task 4 (FIFO-only mechanism verification).

This deliverable (account-level data audit): responsible for task 1 ($ total measured), task 4 ($ quantification of FIFO-only cohort), ranking + concentration analysis.

Both halves merge into `gate2_gap_decomposition_2026-04-17.md` on deliverable commit.

## 8 — Evidence + reproduction

```bash
aws s3 cp s3://opal-data-bd/gold/timeseries/holdings_lots/2026-04-15.parquet /tmp/council_b/
aws s3 cp s3://opal-data-bd/silver/allocations/2026-04-15.parquet /tmp/council_b/

python
>>> import pandas as pd
>>> lots = pd.read_parquet('/tmp/council_b/holdings_lots_2026-04-15.parquet')
>>> alloc = pd.read_parquet('/tmp/council_b/alloc_2026-04-15.parquet')
>>> open_lots = lots[lots['is_open'] == True]
>>> open_lots['is_synth'] = open_lots['lot_id'].str.contains(':rps_synth:')
>>> open_lots['market_value'].sum()               # $2,083,420,732
>>> open_lots[open_lots['is_synth']]['market_value'].sum()   # $390,662,552
>>> (alloc['account_market_value'] - alloc['cash_market_value']).sum()  # $1,660,325,207
```

Numbers are deterministic and reproducible from current S3 state.

## 9 — RAVC

- CTO request (T115511Z) + COO GO (T120XZ): addressed.
- CP-DS1 TO Gate 1 acceptance: all 8 criteria met.
- CP-DS1 TO Gate 2 completion_target: 25.5% over target — attributed 92% to pre-existing synthetic-injection, 10% to FIFO-only cohort. Both are scoped out of CP-DS1.

Andrew decision input: SHIP CP-DS1 on Gate 1 acceptance; CP-SYNTHETIC.A1-A3 TOs next.
