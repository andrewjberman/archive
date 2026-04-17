# ADVI_ROLLUP.CP-DS1 — Acceptance Targets (post-WP-9 cohort + AUA validation)

**Date:** 2026-04-17 (UTC ~04:55Z)
**Author:** 0.4.0_DS_ClientPlatform~B
**Trigger:** 2.0.0_SA_COO research request 20260417T044753Z — CP-DS1 acceptance gate needs (1) post-cutover force-close cohort target, (2) firm total_aua from silver/allocations/2026-04-15 as gold-chain validation gate.

---

## TL;DR

| Gate | Target | Source |
|---|---|---|
| **Post-CP-DS1 force-close cohort size** | **< 50 accounts** | Analytical decomposition of 261 baseline residual (below) |
| **Firm total_aua (gate)** | **$1,694,648,746.14** (silver/allocations/2026-04-15) | Parquet pull `s3://opal-data-bd/silver/allocations/2026-04-15.parquet`, `sum(account_market_value)` |
| 2% tolerance band | **$1,660,755,771 – $1,728,541,721** | total × 0.98 to 1.02 |
| Non-cash subtotal (B_01 holdings_lots scope) | **$1,660,325,207** (cash $34.3M = 2.03% of total) | `cash_market_value` summed + subtracted |
| Unique accounts in silver/allocations | **6,543** (all `account_is_open=True`) | Deduped by `account_id` (no duplicates) |

Firm total_aua and 2% band are observed — pulled directly from S3 silver/allocations/2026-04-15.parquet this session (commit `c8555120` + this deliverable). The < 50 cohort target is a forecast — see §2 for the decomposition and confidence bands.

---

## 1 — AUA validation gate (observed)

### Method
- `aws s3 cp s3://opal-data-bd/silver/allocations/2026-04-15.parquet` → local
- pandas read: 6,543 rows × 92 columns, unique `account_id` = 6,543 (one row per account, no duplicates)
- `account_is_open == True` on 100% of rows (partition is already open-only)
- Columns used: `account_market_value` (per-account total MV), `cash_market_value` (cash portion)

### Numbers

| Metric | Value |
|---|---|
| **Firm total_aua (2026-04-15 source of truth)** | **$1,694,648,746.14** |
| Cash portion (`cash_market_value`) | $34,323,539.33 (2.03%) |
| Non-cash portion (holdings-lots scope) | $1,660,325,206.81 |
| Distribution mean | $259,001 per account |
| Distribution median | $67,412 per account |
| Distribution max | $34,896,600 per account |
| Accounts with MV > 0 | 6,369 |
| Accounts with MV = 0 | 141 |
| Accounts with MV < 0 (short / billing adj) | 33 |

### 2% tolerance band

| Bound | Value |
|---|---|
| Lower (-2%) | $1,660,755,771.22 |
| Source truth | $1,694,648,746.14 |
| Upper (+2%) | $1,728,541,721.06 |

### Important subtlety — cash coverage

`B_01.holdings_lots.py` emits positions derived from transactions (Buys / Sales → FIFO lots + RPS sell-corrections). It does NOT model cash balances as separate lot rows (cash-refactor work is WP-5, separate lane). So when the firm-level gold chain aggregates `holdings_lots.market_value`, the result is comparable to **non-cash $1,660,325,207**, NOT the $1,694,648,746 headline.

**Recommended application of 2% gate:** apply to non-cash subtotal, not headline total. Concretely:
- Gold `holdings_lots` firm MV should land in: **$1,626,919,000 to $1,693,731,000** (non-cash ±2%)
- Headline firm total_aua (for surface to consumers that need cash-inclusive): requires separate assembly from `holdings_lots` non-cash + cash reconciliation path. If CP-DS1 also takes cash coverage onto itself, apply 2% to $1,694,648,746.

If the interpretation is "gold firm total_aua must match silver/allocations firm total_aua within 2%, INCLUDING cash," the gate at $1,694,648,746 ±2% is the target and gold needs a cash source (WP-5 dependency). Flagging this explicitly for ~D / Andrew to disambiguate before setting gate.

---

## 2 — Post-CP-DS1 force-close cohort target (forecast)

### Baseline (pre-CP-DS1, post-option-d, post-CUSIP-exemption)

| Stage | Accts | Source |
|---|---|---|
| 2026-04-15 first halt (pre-any-fix) | 1,307 | Observed (717764fe commit body) |
| Post-CUSIP-exemption forecast (8eda12a3) | ~261 | ~A Phase 4 forecast (80% drop) |
| Post-option-d forecast (ec2c1efc, drops T+1 inflation) | ~261 | ~A §5 (option d does not change count; it removes the 1,169 inflation factor) |

### Decomposition of the 261 baseline (analytical)

The 261 is composed of heterogeneous sub-pathologies. CP-DS1 (CUSIP-keyed FIFO replay per WP-9) eliminates only one of them. Based on ~A historical forensics + z0814307721 drill:

| Sub-pathology | Est. share | CP-DS1 eliminates? | Post-CP-DS1 residual |
|---|---|---|---|
| Name-drift false-positives (CUSIP cycles through different `asset_name` between BD txn and Schwab RPS) | 60–80% (~155–210 accts) | **Yes — CUSIP keying bypasses name-drift entirely** | ~0 |
| Txn-orphan FIFO (FIFO has Buy without matching Sale; RPS correctly says closed; BD silver/transactions never emitted the close event) | 15–30% (~40–80 accts) | **No — CUSIP-keying doesn't change the fact that txn feed is incomplete.** Needs a separate exemption or upstream BD-txn-feed fix. | ~40–80 |
| Settlement-in-flight / T+1 operational noise | ~3–5% (~10–15 accts) | No — this is a timing artifact, always present | ~10–15 |
| PCRA/SWTC structurally-different-feed | already excluded by `bd_covered_with_rps` cohort restriction under dryrun_mode=True (1eb495b0) | Already out of the 261 | 0 |

**Post-CP-DS1 residual point estimate: 50–95 accounts.**

### Acceptance target recommendation: **< 50 accounts**

| Threshold | Implication |
|---|---|
| **< 50 (recommended)** | Clean CP-DS1 acceptance. Aligns with optimistic end of decomposition (txn-orphan + operational ≈ 50). 75% margin below `BD_FORCE_CLOSE_LIMIT=200`. |
| < 20 | Too aggressive. Requires near-zero txn-orphan FIFO, which is a BD transaction feed completeness guarantee, not something WP-9's scope covers. |
| < 100 | Too loose. Does not distinguish "CP-DS1 worked and operational residual is manageable" from "CP-DS1 partially worked and we have a secondary defect." |

If post-CP-DS1 residual lands **50–100**, do not fail acceptance — flag as **WARN**, open an immediate follow-up TO investigating the txn-orphan FIFO path (candidate: "orphan Buy exemption" parallel to the existing CUSIP exemption, or upstream BD-txn-feed gap fix).

If post-CP-DS1 residual lands **> 100**, CP-DS1 is not sufficient. Investigate before cutover.

### Confidence

Medium. The decomposition is an educated breakdown from ~A's drill + historical forensics, not a measurement. The only measurement that sharpens this is a QA `BD_FORCE_CLOSE_OVERRIDE=1` single run with full diagnostic capture (per earlier ~B recommendation / ~A §8 rec 6). That run converts the 261 forecast into an observed breakdown — critical input for CP-DS1 design.

---

## 3 — Evidence / commands

```bash
aws s3 ls s3://opal-data-bd/silver/allocations/ | grep 2026-04-15
# 2026-04-16 18:03:21  1163497 silver/allocations/2026-04-15.parquet

aws s3 cp s3://opal-data-bd/silver/allocations/2026-04-15.parquet /tmp/council_b/alloc_2026-04-15.parquet
# 1.1 MiB downloaded

python
>>> import pandas as pd
>>> df = pd.read_parquet(r'C:\Users\AndrewBerman\AppData\Local\Temp\council_b\alloc_2026-04-15.parquet')
>>> df.shape
(6543, 92)
>>> df['account_market_value'].sum()
1694648746.1405...
>>> df['cash_market_value'].sum()
34323539.33...
```

Reproducibility: any DS / AE / CTO session can pull the same parquet and verify the sum. Numbers are stable (partition is T-1 close, not subject to late-binding updates once landed).

---

## 4 — RAVC

- ACK delivered to COO at 20260417T043322Z (prior request crossover).
- COMPLETE delivered with this deliverable path.
- Scope: acceptance-target research only. Does not author CP-DS1 TO itself (COO owns) nor pre-judge the cutover execution plan.
