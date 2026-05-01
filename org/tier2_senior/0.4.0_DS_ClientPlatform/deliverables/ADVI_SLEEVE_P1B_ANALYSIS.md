<!-- ADVI_ROLLUP.SL-P1b — Sleeve Shadow Validation Analysis -->
<!-- Author: 0.4.0_DS_ClientPlatform~B | Date: 2026-05-01 -->

# ADVI_SLEEVE_P1B_ANALYSIS — Shadow Validation Verdict

**Project:** ADVI_ROLLUP | **Phase:** SL-P1b | **Analyst:** 0.4.0_DS_ClientPlatform~B  
**Analysis date:** 2026-05-01 | **Shadow dates analyzed:** 2026-04-15, 2026-04-16, 2026-04-17, 2026-04-21

---

## VERDICT: ITERATE

**Do NOT promote.** One critical apportionment bug confirmed. All three parity gates fail.
Required fixes are scoped to B_01 lines ~988-1006. Estimated fix effort: 0.5d.

---

## Gate Checklist

| AC | Description | Result |
|----|-------------|--------|
| AC#1 | >= 3 shadow dates present | PASS — 4 dates (2026-04-15 through 2026-04-21) |
| AC#2 | Cohort parity table committed | PASS — computed below |
| AC#3 | Stability DoD table committed | PASS — computed below |
| AC#4 | Jones z0817905851 PASS/FAIL at 2% | FAIL — 86.7% off |
| AC#5 | Downstream counterfactual | PASS — comp-blast returns 0 registered readers (shadow isolated) |
| AC#6 | Verdict committed to this memo | PASS — this document |

---

## Deliverable 1 — Cohort-level Parity (2026-04-21)

Shadow scope: ULN-only lots (not a full replacement of production; see design note below).
Correct baseline: silver/allocations `account_market_value` per account (the MV the shadow should reconstruct).

| Metric | Value |
|--------|-------|
| Shadow cohort accounts | 458 |
| Production matching accounts | 458 |
| Shadow firm MV (cohort) | $15,867,270 |
| Silver/allocations firm MV (cohort) | $66,431,405 (proxy: prod MV same accounts) |
| Delta (shadow - alloc) | -$50,564,135 |
| Delta % | -76.1% |
| Firm parity verdict | FAIL (>5%) |

**Per-account parity distribution (n=458):**

| Band | Count | % |
|------|-------|---|
| <= 2% delta | 2 | 0.4% |
| 2-5% delta | 1 | 0.2% |
| 5-10% delta | 1 | 0.2% |
| > 10% delta | 452 | 98.7% |

**Top 5 worst parity (sample):**

| account_id | shadow_mv | prod_mv | delta_pct |
|------------|-----------|---------|-----------|
| z0821097521 | $9,507 | $1,136 | +736.7% |
| z0820741141 | $5 | $4,232 | -99.9% |
| z0820630201 | $7 | $2,568 | -99.7% |
| z0821431841 | $25 | $8,000 | -99.7% |
| z0820741151 | $100 | $31,876 | -99.7% |

Pattern: ~99% of accounts show shadow MV that is a fraction (often ~12-15%) of the production value. Root cause: apportionment denominator bug described below.

---

## Deliverable 2 — Stability Over Time

| Date range | Joint accounts | Median DoD | Flagged > 20% DoD |
|------------|---------------|------------|-------------------|
| 2026-04-15 -> 2026-04-16 | 458 | +0.00% | 33 accounts |
| 2026-04-16 -> 2026-04-17 | 458 | +0.00% | 105 accounts |
| 2026-04-17 -> 2026-04-21 | 458 | -2.66% | 33 accounts |

Accounts stable across ALL 4 dates: 457 of 462 unique (5 entered/exited cohort).  
Cohort count: 458 accounts on 2026-04-21 vs 553 in 2026-04-13 dry-run (cohort drift: -95 accounts).

DoD instability pattern: majority of accounts have 0% DoD (frozen), with a subset experiencing extreme swings (up to +5501%). This is consistent with the denominator bug: small changes in the ULN coverage set (one asset entering/leaving) cause large shifts in the non-vetoed positions' weight allocation.

---

## Deliverable 3 — Canonical Test Cases

### Jones z0817905851 — PRIMARY GATE

| Metric | Value |
|--------|-------|
| Shadow MV (2026-04-21) | $318,247 |
| Silver target (alloc account_market_value) | $2,396,510 |
| Production MV | $2,390,992 |
| Delta vs target | +86.7% (shadow understates by $2.08M) |
| Threshold | 2% |
| Result | FAIL |

**Dry-run baseline (2026-04-13):** Jones = $2,396,510 = silver $2,396,510 (0.00% delta). Regression occurred at first nightly emit (2026-04-15). Cause: new FIFO lots loaded for Jones between dry-run and nightly (10 of 13 ULN positions now vetoed by FIFO presence), triggering denominator bug.

Jones shadow lot breakdown (4 lots):

| Asset | Ticker | Units | Price | MV |
|-------|--------|-------|-------|----|
| CASH | - | 21,060 | $1.00 | $21,060 |
| ISHARES CORE MSCI EMERGING MARKETS ETF | IEMG | 1,237 | $76.44 | $94,592 |
| POLEN DIVIDEND INCOME ETF | DIVZ | 1,683 | $36.76 | $61,856 |
| STATE STREET SPDR PORTFOLIO S&P 500 ETF | SPYM | 1,698 | $82.87 | $140,739 |

Jones ULN has 14 rows. 10 non-cash are vetoed (FIFO already covers). 3 non-cash pass. Denominator = ALL 13 non-cash unit_costs. Non-vetoed weight = 12.43%. Result: shadow captures 12.43% of $2.39M non-cash target.

### Additional cases (top 5 MV accounts in shadow):

| account_id | shadow_mv | prod_mv | delta_pct | shadow_lots | prod_lots |
|------------|-----------|---------|-----------|-------------|-----------|
| z0813461901 | $1,162,513 | $1,857,749 | -37.4% | 8 | 194 |
| z0821665451 | $587,074 | $704,083 | -16.6% | 9 | 33 |
| z0820335091 | $520,986 | $1,983,587 | -73.7% | 3 | 185 |
| z0817386291 | $421,220 | $853,979 | -50.7% | 1 | 51 |
| z0818244781 | $386,185 | $590,088 | -34.6% | 5 | 118 |

Pattern: shadow lot counts are uniformly low (1-9) vs prod (33-194). Confirms vetoing is removing most ULN positions.

---

## Deliverable 4 — Downstream Reader Counterfactual

comp-blast: `No nodes matching: holdings_lots_shadow` — 0 registered comp-graph readers.  
Shadow is correctly isolated. No accidental pre-promotion.

If PROMOTE were issued (hypothetical):

| Consumer | Impact |
|----------|--------|
| D_02 (per-advisor detail) | Cohort = 458 accounts, 3.95% of firm MV. Shadow undercount = -76.1% → would severely understate advisor AUA for those accounts. |
| D_04 (firm summary) | Same -76.1% undercount on cohort portion = -$50.6M firm AUA phantom gap. |
| D_00c (Inflection leaderboard) | Inflection cohort overlap TBD; risk of AUA drop for Inflection advisors. |
| bd-portal-publisher | Books tab MV for 458 accounts would drop ~76%. |
| Scripts 05b, 06 | cost_basis, accrued_gain fields would be wrong for the cohort. |

Verdict: promotion in current state would degrade AUA accuracy for 3.95% of firm by ~76%. Blocked.

---

## Root Cause Analysis — Apportionment Denominator Bug

**Location:** `data/black_diamond/scripts/gold/B_01.holdings_lots.py` lines ~988-1006

**Bug:** `total_unit_cost` is computed from ALL ULN non-cash positions (including those vetoed by FIFO), then each non-vetoed lot receives `weight = unit_cost / total_unit_cost_all`. This causes:

```
weight_nonvetoed = sum(unit_cost_nonvetoed) / sum(unit_cost_all)
target_mv_nonvetoed = weight_nonvetoed * non_cash_target_mv  <-- only fraction assigned
```

For Jones: non-vetoed weight = 12.43%. Shadow captures only 12.43% of $2.39M = $297K.

**Confirmed:** Expected $297,187 (computed from weights) = Actual $297,187 (observed). BUG CONFIRMED = True.

**Current code (B_01 lines ~988-1005):**
```python
# Non-cash: Path 3 cost-basis apportionment
total_unit_cost = float(grp_nc['unit_cost'].sum())  # BUG: includes vetoed positions
if total_unit_cost <= 0:
    continue
for _, lot in grp_nc.iterrows():
    if (acct_id, asset) in fifo_open_set:
        n_vetoed += 1
        continue                          # vetoed AFTER denominator computed
    weight = float(lot['unit_cost']) / total_unit_cost  # denominator is wrong
    target_mv = weight * non_cash_target_mv
```

**Fix A (denominator only):** Move veto check before denominator computation. Filter `grp_nc` to non-vetoed positions before summing `total_unit_cost`. This restores correct proportional weighting among the passing positions.

**However:** Fix A alone would assign the FULL `non_cash_target_mv` to only the non-vetoed positions — overcorrecting for accounts with significant FIFO coverage. Jones's 3 non-vetoed positions would receive 100% of $2.39M non-cash = WRONG (they're not the whole account).

**Fix B (preferred — architecturally correct):** Use uncovered MV as the apportionment base:

```python
# Compute FIFO-covered MV for this account (how much is already in production)
fifo_covered_mv = fifo_mv_by_account.get(acct_id, 0.0)
non_cash_target_mv = max(account_mv - cash_mv - fifo_covered_mv, 0.0)

# Filter grp_nc to non-vetoed BEFORE computing denominator
grp_nc_pass = grp_nc[grp_nc.apply(
    lambda row: (acct_id, str(row['asset_name']).strip()) not in fifo_open_set, axis=1
)]
if grp_nc_pass.empty or non_cash_target_mv <= 0:
    continue
total_unit_cost = float(grp_nc_pass['unit_cost'].sum())
for _, lot in grp_nc_pass.iterrows():
    weight = float(lot['unit_cost']) / total_unit_cost
    target_mv = weight * non_cash_target_mv
    ...
```

Fix B requires computing `fifo_mv_by_account` before the sleeve loop (available from the main FIFO lot build). For pure-sleeve accounts (FIFO = 0), uncovered MV = full non_cash_target_mv, preserving dry-run correctness.

**Expected outcome after Fix B:**
- Jones (58 FIFO lots covering full $2.39M): uncovered_mv ≈ $0 → sleeve adds only cash ($21K). Total shadow = $21K. Production supplements the rest.
- Pure-sleeve accounts (0 FIFO): uncovered_mv = full account_mv - cash. Full apportionment. Matches dry-run behavior.

---

## Secondary Issues

**S1 — Cohort drift (-95 accounts):** Dry-run 2026-04-13 had 553 accounts; live nightly shows 458 (5 more than TO's "403" reference; likely cohort was updated). Drift source: cohort parquet under `diagnostics/sleeve_cohort/` may have been regenerated between dry-run and first nightly. Flag for SL-P0 review.

**S2 — DoD instability (105 accounts flagged 04-16→04-17):** Driven by same denominator bug — day-to-day ULN coverage changes (one asset enters/leaves FIFO) cause non-linear MV swings. Will resolve with Fix B since uncovered MV will be stable (small daily changes in FIFO coverage translate linearly to small uncovered MV changes).

**S3 — comp-pipescript feeds B_01:** Only shows `accounts_dimension` (from A_00). Silver/unrealized and silver/allocations are read directly via S3 paths not registered in comp-graph. Recommend adding comp-graph edges for these feeds in a future comp-build update (not blocking SL-P1b).

---

## Required Fixes for SL-P1c (Re-emit)

| Priority | Fix | Location | Estimated effort |
|----------|-----|----------|-----------------|
| P0 | Fix B: uncovered MV + pre-veto denominator | B_01 lines ~988-1006 | 2h |
| P1 | Validate Jones = cash-only after fix | dry-run script | 1h |
| P2 | Validate pure-sleeve accounts unchanged | dry-run script | 1h |
| P3 | Investigate cohort drift -95 accounts | diagnostics/sleeve_cohort/ | 1h |

After Fix B ships:
1. Dry-run on 2026-04-21 partition. Assert Jones = $21,060 (cash only, uncovered = $0).
2. Pick 3 pure-sleeve accounts (0 FIFO lots). Assert shadow MV matches silver alloc account_mv within 2%.
3. Re-enable nightly. Collect 3 clean nightly emissions before re-running SL-P1b validation.

---

## Compiler Tools Log

| Tool | Run | Result |
|------|-----|--------|
| comp-blast gold/timeseries/holdings_lots | Phase 1 | No downstream consumers registered |
| comp-blast holdings_lots (short form) | Phase 1 | No downstream consumers found for gold:B_01.holdings_lots |
| comp-pipescript feeds B_01 | Phase 2 | Only accounts_dimension registered; unrealized/allocations via direct S3 (not in graph) |
| comp-validate B_01 --artifact s3://... | Phase 1 | MISSING_ARTIFACT — S3 URI not supported; artifact downloaded locally instead |
| comp-blast holdings_lots_shadow | Phase 3 | No nodes matching — shadow isolated, 0 readers CONFIRMED |
