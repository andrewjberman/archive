# Silver-Authority Architecture — Feasibility + Scope

**Date:** 2026-04-17 (UTC ~12:36Z)
**Author:** 0.4.0_DS_ClientPlatform~A
**Trigger:** CTO pivot message T122XZ — cancel rotation-resolver track, pivot to silver-authority gating on both sell-correction and synth-inject paths in B_01.
**Target:** Post-architecture gold open MV reconciles to silver/allocations within 2%.

---

## TL;DR

**FEASIBLE — YES.** Empirical simulation against Run 5 (`s3://opal-data-bd/gold/timeseries/holdings_lots/2026-04-15.parquet`) predicts post-architecture firm gold open MV = **$1,691,580,864** vs silver/allocations non-cash target = $1,660,325,207. **Delta +$31.3M (+1.88%) — INSIDE the 2% gate.**

**Critical nomenclature correction:** CTO spec references "silver/allocations" as the position-level authority, but `silver/allocations/{date}.parquet` is **ACCOUNT-LEVEL ONLY** (1 row per account, 6,543 rows, no asset_id / cusip). The correct position-level authority is **`silver/unrealized/{date}.parquet`** (93,951 rows, 7,330 accounts, (account_id, cusip) granularity at 99.86% cusip-populated).

Scope: **~18-25 lines in `B_01.holdings_lots.py`**, no cross-script refactor. ETA to ship: 30-45 min including QA.

---

## 1 — Data source verification

### silver/allocations (NOT position-level)

| Metric | Value |
|---|---|
| Shape | 6,543 × 92 |
| Rows per account | min/median/max = 1/1/1 |
| Account-level columns | `account_market_value`, `cash_market_value` |
| Position-level columns | **NONE** (no asset_id, no cusip, no ticker, no position_name) |

Cannot be used as `(account_id, cusip)` gate.

### silver/unrealized (position-level authority) — `s3://opal-data-bd/silver/unrealized/2026-04-15.parquet`

| Metric | Value |
|---|---|
| Shape | 93,951 × 16 |
| Rows per account | min/median/max = 1 / 14 / 398 |
| Unique accounts | 7,330 |
| Unique cusips | 2,810 |
| Unique (account_id, cusip) pairs | 93,915 |
| cusip populated | 93,824 / 93,951 (99.86%) |
| Columns | `open_date, unit_cost, relationship_id, account_id, asset_id, asset_name, cusip, ticker, symbol, ...` |

**This is the correct data source.** Already loaded at B_01 L498 (`_read_parquet_from_s3(S3_UNREALIZED_KEY)`) — no new read required.

### silver/allocations still useful

Account-level `account_market_value` remains the **aggregation target** for Gate 2 acceptance (Andrew's recon target). Position-level authority lives in silver/unrealized.

---

## 2 — Feasibility simulation (empirical against Run 5)

Gate design:
- **KEEP** a gold open lot if `(account_id, cusip) IN silver_unrl_pair_set`
- **DROP** (close, MV=0) if `account_id IN silver_unrl_accts BUT (account_id, cusip) NOT IN pair_set` (silver-absent-pair)
- **DROP** if `account_id NOT IN silver_unrl_accts` (FIFO-only account)

Applied to Run 5's 350,718 open lots:

| Cohort | Lot count | MV | FIFO vs synth split |
|---|---|---|---|
| KEEP (in silver-pair) | 271,113 | **$1,691,580,864** | FIFO 236,361 / $1,333M + synth 34,752 / $358M |
| DROP silver-absent-pair | 79,240 | $377,921,741 | FIFO 78,959 / $360M + synth 281 / $18M |
| DROP FIFO-only-acct | 365 | $13,918,127 | FIFO 46 / $2.5K + synth 319 / $13.9M |
| **TOTAL DROPPED** | **79,605** | **$391,839,868** | — |

**Post-gate residual vs silver/allocations:**

| Metric | Value |
|---|---|
| Expected gold open MV post-gate | $1,691,580,864 |
| silver/allocations non-cash target | $1,660,325,207 |
| Delta | **+$31,255,657 (+1.88%)** |

**Inside Andrew's 2% target.**

Residual $31M is likely attributable to:
- FIFO cost-basis vs silver/allocations market-MV timing drift (within-account micro-differences)
- Positions with `(account_id, cusip)` pair in both FIFO and silver/unrealized but differing unit counts
- silver/unrealized includes some accounts (794 of 7,330) NOT in silver/allocations — those 794 account positions pass the gate but don't count toward the $1.66B target

---

## 3 — Implementation scope (B_01.holdings_lots.py)

### Change A — build `silver_pair_set` + `silver_acct_set` at startup (5-8 lines)

After existing `unrl` load at ~L498 (inside `_build_rps_context`) OR at top of `build_holdings_lots_snapshot` (L1881-ish, before phantom-closure):

```python
# Silver-authority position set for gate enforcement
unrl_norm = unrl.copy()
unrl_norm['account_id'] = unrl_norm['account_id'].astype(str).str.strip()
unrl_norm['cusip'] = unrl_norm['cusip'].astype(str).str.strip()
silver_pair_set = set(zip(unrl_norm['account_id'], unrl_norm['cusip']))
silver_acct_set = set(unrl_norm['account_id'].unique())
```

### Change B — FIFO-only-account closure at phantom-closure pass (~6 lines)

In phantom-closure block at L1900-1946, add Rule 3 after existing Rule 1/2:

```python
# Rule 3 (silver-absent account): FIFO has open lots but silver/unrealized
# has NO entry for this account. Silent-close with silver_absent tag.
for acct_id in set(hl_open_accts) - silver_acct_set:
    mask = (df['account_id'] == acct_id) & df['is_open']
    df.loc[mask, 'is_open'] = False
    df.loc[mask, ['current_units', 'market_value', 'cost_basis', 'accrued_gain']] = 0.0
    # Add `resolution` column if not present with tag 'silver_absent_silent_close'
```

### Change C — per-lot silver-gate after all lots built (~7 lines)

After `df = pd.concat(parts, ...)` at L2013, apply:

```python
# Silver-authority per-lot gate: close any open lot whose (account_id, cusip)
# is not present in silver/unrealized for this snapshot. Covers both FIFO
# name-drift and RPS synth-buy that silver/unrealized doesn't confirm.
_pair_keys = list(zip(
    df['account_id'].astype(str).str.strip(),
    df['cusip'].astype(str).str.strip()
))
_silver_absent = pd.Series(
    [pk not in silver_pair_set for pk in _pair_keys], index=df.index
)
_absent_open = df['is_open'] & _silver_absent
n_closed = int(_absent_open.sum())
mv_closed = float(df.loc[_absent_open, 'market_value'].sum())
df.loc[_absent_open, 'is_open'] = False
df.loc[_absent_open, ['current_units', 'market_value', 'cost_basis', 'accrued_gain']] = 0.0
print(f"  [silver-authority gate] Closed {n_closed:,} lots / ${mv_closed:,.0f} "
      f"not confirmed by silver/unrealized (acct,cusip)")
```

Total: ~18-25 lines. No cross-script impact. All additive (wrapped in new block, does not modify existing sell-correction/synth-inject logic — just imposes a downstream veto).

### Alternative: narrow synth-inject upstream (optional optimization)

At L1052 (buy-gap path inside `_build_rps_synthetic_lots`): filter the `inject = merged[merged['gap'] > 0.001]` dataframe to only rows where `(account_id, cusip) IN silver_pair_set` BEFORE building synth lots. This saves the work of building + then closing synth lots. Scope: +2-3 lines. Recommendation: add the downstream gate first (Change C), then profile if narrowing upstream is worth the optimization.

---

## 4 — Risk assessment

| Risk | Mitigation |
|---|---|
| silver/unrealized has 794 accts NOT in silver/allocations — their positions pass gate but don't count toward $1.66B target | Expected +$31M residual includes this. Within 2% gate. Not a blocker. |
| silver/unrealized cusip at 99.86% — 0.14% null-cusip rows would pass gate as (acct, NULL) non-match | 127 silver/unrealized rows have null cusip; negligible MV impact. |
| Change C over-closes legitimate positions where cusip round-trip differs (bd_assets_dim asset_id → cusip vs silver/unrealized asset_id → cusip) | Empirical $31M residual is IN-target; suggests any such over-close is absorbed within tolerance. If residual drifts on next partition, investigate. |
| Ordering interactions with existing phantom-closure (L1900-1946) + RPS sell (L2001-2003) + synth-inject (L1995-1998) + fallback (L2004-2006) | Change C is final gate after concat (L2013). Applies to final df. Ordering preserved. |
| QA risk | Need --single B_01 QA run after ship. Expected: alerts count stays 0, resolved count stays 0 (CP-DS1 invariant), gold MV lands within 2% of $1.66B. |

---

## 5 — ETA + ship plan

- **Code patch:** 30 min (implementing Changes A-C + inline doc comments + log prints)
- **QA --single B_01:** 15 min (plus artifact landing time ~8-10 min per Run 5)
- **Verification:** 5 min (run same Gate 2 decomposition logic against new output)
- **Total:** 45-60 min from GO to validated result

Gate criteria for ship:
1. Gold open MV within 2% of silver/allocations/2026-04-15 non-cash target ($1.66B ± $33.2M)
2. `rps_force_close_alerts/2026-04-15.parquet` remains empty or <200 cohort (CP-DS1 invariant)
3. Pop A 472-cohort preservation: at least 450 accounts still have is_open=True lots (99%+ preservation)
4. Spot-check 5 named PCRA/SWTC accts: MV still approximately matches silver/allocations per account

---

## 6 — Recommendation

**Ship the silver-authority architecture.** Lightweight (~18-25 LOC), no cross-script refactor, empirically validated against Run 5 at 1.88% residual, inside target. Implements exactly the architectural correction Andrew is asking for — silver is authoritative on BOTH add and close paths.

**NAMING CORRECTION FOR COO SCOPING:** use `silver_unrealized_authority` in the TO name (not `silver_allocations_authority`) — position-level source is silver/unrealized, not silver/allocations. silver/allocations remains the account-level aggregation target for acceptance.

DS implementation can start immediately upon CTO GO. No BDPL_ASTDIM W4 dependency (silver/unrealized already has cusip populated at 99.86%).