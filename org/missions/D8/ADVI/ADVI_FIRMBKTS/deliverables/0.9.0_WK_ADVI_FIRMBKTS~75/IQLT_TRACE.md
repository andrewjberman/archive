# FB-j-12 -- IQLT -69.2 percent trace (read-only)

Record: `IQLT_TRACE.json` (same folder). Read at 2026-10-13T09:59:36Z. No write verb, no producer run, no product file edited.
Downloads sit in `C:/dev/wk-firmbkts-75-data/` (outside the checkout). No account number or client name is printed.

## Verdict

**DATA_DEFECT** (claim: measured). The served -69.2 percent is a market-value defect in B_01's silver-noncash cap, not a price defect, not a cost-basis defect, and not a real loss.

## The figures traced

| Item | Published bullet (DRYRUN10_FIGURES) | Measured here (served 2026-10-09 object) |
|---|---|---|
| Accounts / open lots | 31 / 61 | 30 / 60 |
| Quantity (units) | not published | 11,788.6717 |
| Market value | 134,377.61 | 134,350.71 |
| Cost basis | 436,698.87 | 436,515.92 |
| Unrealized (accrued_gain) | -302,321.26 | -302,165.22 |
| Loss percent | -69.23 | -69.22 |

The reconstruction differs from the bullet by one lot and one account (182.95 cost, 26.90 market value). See surprise row S4.

## Prices (2026-10-09)

- `silver/prices/canonical_prices.parquet`, IQLT row, source yahoo_finance: **49.84**
- `silver/prices/2026-10-09.parquet`, IQLT row, source carry_forward: **49.31**
- The lots carry current_price 49.84, the value B_01 used.
- Custodian (`silver/unrealized/2026-10-09.parquet`): 11 IQLT rows firm-wide (11 accounts, MV 1,322,890.07); **none** in the 108 accounts mapped to the advisor. No custodian price could be read for these lots.

## Cost check

All 60 open lots checked against canonical prices within five days of acquisition. Per-share cost runs 32.68 to 40.98 (unit-weighted 37.03). **0 of 60 flagged** at the 20 percent band. Canonical close near the 2023-03-14 first acquisition: 31.38.

## Mechanism

1. `B_01.holdings_lots.py` writes the lot's `market_value` as units times price, then `_apply_silver_noncash_cap` scales `market_value` on class B and C open lots (no custody row) by a per-account factor. The docstring states `cost_basis` and `current_price` are not modified.
2. For this advisor's IQLT lots the scale is 0.2287. Uncapped market value is **587,547.40** (= 11,788.6717 x 49.84), a **+151,031 gain, +34.6 percent** on the 436,516 cost.
3. The bullet reads the capped value against the uncapped cost, which produces -302,165 and -69.2 percent.
4. Firm-wide on the same object, 64,629 of 492,998 open lots (3,057 accounts, 1,007 tickers) are compressed. On 99.99 percent of open lots uncapped market value equals units times price.

## Scope

- Dry run: IQLT appears in 2 of 39 bullets, both for `garrett_newberry` (top_loser, tax_loss_candidate).
- Firm: the same cap governs any bullet resting on a compressed market value.

## Open, not settled here

- **Unit count.** Custody holds no IQLT in the advisor's 108 mapped accounts, which is the condition the cap reads as phantom. Whether those units are held is a unit-count question this trace does not answer. Either way the -69.2 percent is not a market loss.
- **Account rule.** The advisor-to-account rule used here is `advisor_assignments_history` (is_current, role value "Garrett Newberry"). The producer's rule for `positions.json` was not read.
- **Object date.** The 2026-10-09 lots object was last written 2026-10-13T05:06:00Z.

Scripts: `iqlt_lots_read.py`, `iqlt_advisor_map.py`, `iqlt_price_check.py`, `iqlt_cost_check.py` (same folder).
