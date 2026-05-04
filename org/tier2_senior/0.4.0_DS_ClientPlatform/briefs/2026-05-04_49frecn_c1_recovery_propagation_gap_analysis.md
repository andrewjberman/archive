# 49FRECN.003 — C1 Recovery Propagation Gap Analysis
**Author:** 0.4.0_DS_ClientPlatform~B  
**Date:** 2026-05-04  
**Trigger:** COO re-route; BD gold chain completed 16:43Z, `c1_recovered_accounts.json` total_recovered_count=0 (expected 58-73)  
**Audience:** 1.1.0_SA_CTO, 2.0.0_SA_COO  

---

## Executive Summary

`c1_recovered=0` is caused by **two independent failures**, not one:

1. **Detection bug in D_04** — `_C1_FIX_DATE = 2026-05-01` hard-codes a date that is strictly greater than the latest gold data date (2026-04-30). `recently_added_ids` is structurally guaranteed to be empty. Even with the date corrected, the `first_seen_in_gold >= fix_date` heuristic fails for BFIX3 targets because they are *returning* accounts with pre-existing gold history (first_seen years before fix_date).

2. **BFIX3 effectiveness gap in B_00** — The 40 RECONCILE_DROP C1 accounts are Schwab-custodied accounts with no BD positions carrying `units > 0` in BD bronze. BFIX3's rescue path is gated on `set(bd_df['account_id'].unique())`, where `bd_df` is pre-filtered to `units > 0`. These accounts never enter `bd_df` → BFIX3 cannot rescue them. Empirically confirmed: canonical_holdings @ 2026-04-30 has only 1 source='bd_new_acct' account (z0819627441, $574 silver AUA — not a C1 account).

The c1_recovered sidecar is not malfunctioning — it is accurately reporting the current state: **the 58 C1 accounts are genuinely still excluded from gold**. The underlying recovery mechanisms (BFIX3 + A_03 Option B) have not yet fixed the target accounts.

---

## Empirical Evidence

### S3 State Verification (post-chain, 2026-05-04)

| Artifact | Metric | Value |
|----------|--------|-------|
| `gold/canonical/holdings/2026-04-30.parquet` | Last modified | 15:48:36Z |
| `gold/canonical/holdings/2026-04-30.parquet` | Distinct accounts | 6,106 |
| `gold/canonical/holdings/2026-04-30.parquet` | source='bd_new_acct' accounts | 1 (z0819627441) |
| `gold/canonical/holdings/2026-04-30.parquet` | DELPHI asset accounts | 1 (z0822229381) |
| `gold/timeseries/account_performance.parquet` | Last modified | 16:10:54Z |
| `gold/timeseries/account_performance.parquet` | Accounts @ 2026-04-30 | 6,106 |
| `gold/timeseries/account_performance.parquet` | Accounts first_seen >= 2026-05-01 | **0** |
| `c1_recovered_accounts.json` | total_recovered_count | **0** |
| `out_of_scope_accounts.json` | excluded_c1_count | 58 (C1 bucket, unchanged pre/post chain) |
| `firm_composition.json` | firm AUA | $1,683,701,127.96 |
| Expected firm AUA | Per TO | ~$1,720M |
| Firm AUA gap | | ~$36.3M |

### C1 Universe Cross-Reference

| Category | Count | Silver AUA |
|----------|-------|------------|
| C1 universe (investment type, in-dim, AUA >= $100K) | 2,630 | $1,565M |
| C1 in gold @ 2026-04-30 | 2,568 | $1,504M |
| C1 NOT in gold @ 2026-04-30 | 62 | $60.8M |
| C1 not-in-gold with presence in canonical_holdings | **0** | — |
| C1 not-in-gold completely absent from canonical_holdings | **62** | $60.8M |

All 62 C1-excluded accounts have zero presence in canonical_holdings @ 2026-04-30. They are absent from the gold pipeline at its source — not gated out at C_03 or D_04.

### Sample C1 Excluded Account Profiles

| Account | Opened | First seen in gold | In canonical_holdings @ 2026-04-30 |
|---------|--------|-------------------|--------------------------------------|
| z0817527731 (IRA) | 2023-12-11 | 2023-12-11 | **NO** |
| z0817527771 (IRA) | 2023-12-11 | 2023-12-11 | **NO** |
| z0820765271 (401K) | 2025-03-28 | 2024-04-30 | **NO** |
| z0820765311 (Trust) | 2025-03-28 | 2024-04-30 | **NO** |
| z0821124031 (Charitable) | 2025-05-30 | 2024-12-31 | **NO** |
| z0822224971 (Joint) | 2025-12-22 | never | **NO** |
| z0822256171 (Joint) | 2025-12-23 | never | **NO** |
| z0822893871 (401K, $11.5M) | 2026-04-29 | never | **NO** |

Pattern: older accounts (z0817..., z0820..., z0821...) were previously in gold and dropped out — classic RECONCILE_DROP. Newer accounts (z0822...) were never in gold — C1c (genuinely new, no BD data yet).

### BFIX3 Account Detail

| Account | Silver AUA | canonical_holdings units (sample) | account_performance total_aua |
|---------|------------|-----------------------------------|-------------------------------|
| z0819627441 (BFIX3 rescue) | **$574.91** | 7.98e-17 to 9.10e-15 (epsilon) | ~$0 |
| z0822229381 (AQR DELPHI) | $1,951,010 | 3.64e-11 DELPHI units (epsilon) | ~$0 |

z0819627441 is NOT a C1 account (silver AUA $574 < $100K threshold). BFIX3 rescued this account but it is irrelevant to the 58 C1 recovery. z0822229381 has real AUA in silver ($1.95M) but epsilon AUA in gold.

---

## Root Cause Analysis

### RC-1: D_04 Detection Bug (DETECTION LAYER)

**Location:** `D_04.client_portal_summary.py:3494-3496`  
**Code:**
```python
recently_added_ids = set(
    first_seen_df[first_seen_df['first_seen_gold'] >= _C1_FIX_DATE]['account_id']
)
# _C1_FIX_DATE = pd.Timestamp('2026-05-01')
# latest gold data date = 2026-04-30
```

**Bug 1 — Date boundary:** `_C1_FIX_DATE (2026-05-01)` > `latest gold date (2026-04-30)`. `recently_added_ids` is structurally empty. No account can have `first_seen_in_gold >= 2026-05-01` when gold data only goes to 2026-04-30.

**Bug 2 — Heuristic mismatch:** BFIX3 targets are *returning* accounts. z0817527731 has been in gold since 2023-12-11. Its `first_seen_in_gold` is years before fix_date. Even if Bug 1 were fixed (by lowering `_C1_FIX_DATE` to 2026-04-30 or earlier), the RECONCILE_DROP accounts would still not be caught — their `first_seen_gold` predates the stale period.

**The heuristic was designed for C1c genuinely-new accounts** (never been in gold). Those accounts would correctly appear with `first_seen >= fix_date`. But C1c is PARKED per AC#5. For BFIX3 targets (RETURNING accounts), a different detection signal is required.

### RC-2: BFIX3 Structural Failure (PROPAGATION LAYER — B_00)

**Location:** `B_00.canonical_holdings.py:724-741`  
**Key line:**
```python
bfix3_accts = all_stale_accts & set(bd_df['account_id'].unique()) & set(alive_ids)
```

`bd_df` is pre-filtered to `units > 0` from BD bronze at the top of `process_date()`. RECONCILE_DROP accounts are **Schwab-custodied accounts with no BD positions holding units > 0**. Their BD bronze state is either:
- Completely absent from BD bronze (only Schwab holds positions), or
- All BD units are zero or near-zero (account migrated to Schwab-only)

These accounts exist in `all_stale_accts` (their Schwab positions were labeled `bd_stale` and zeroed at line 564). They are in `alive_ids` (silver/allocations AUA >= $100K). But they are **NOT in `bd_df`** (no BD units > 0) → BFIX3's intersection is empty for them → not rescued.

z0817527731 (opened Dec 2023, been in gold for 2+ years) is completely absent from canonical_holdings @ 2026-04-30. BFIX3 did not rescue it because BD bronze has no units > 0 for this account.

**BFIX3 comment at line 719** says: "Rescue alive accounts whose reconcile output has every row units<=0 (Schwab RPS not yet established for recently-opened accounts — RPS cycle lag labels all positions bd_stale)." The mechanism was designed for NEW accounts with temporary RPS lag — but the 40 RECONCILE_DROP targets are ESTABLISHED Schwab-custodied accounts where BD permanently lacks position data.

### RC-3: A_03 Option B Effectiveness Gap (PROPAGATION LAYER — A_03)

z0822229381 (AQR DELPHI, $1.95M silver) has `source='bd'` in canonical_holdings with 3.64e-11 DELPHI units — epsilon market_value ($0). A_03's UNREALIZED_DAILY injection path is either:
- Receiving epsilon units from the UNREALIZED_DAILY file for this account, or
- Encountering a float precision issue in the par-valuation step for DELPHI

The account IS present in canonical_holdings (counts toward 6,106 distinct accounts) but contributes $0 AUA. This is why account_performance also shows $0 for this account.

### RC-4: C_03 Is NOT a Gate (DS~C Confirmation)

DS~C verified: C_03 (`account_performance`) at line 210 does a LEFT join on `gains` — it includes all accounts from account_gains (B_03) with no AUA floor, no stale exclusion, and no history requirement. C_03 is not the propagation bottleneck. The gap is in canonical_holdings (B_00/A_03), not downstream.

---

## CTO's 4 Questions

### Q1: What is B's data source for the 58 accounts' historical performance?

**B = propagation fix (make the 58 accounts appear in gold with real AUA).**

Two sub-paths:

**B1 — BFIX3 fix (RECONCILE_DROP, 40 accounts):** BFIX3 needs to rescue accounts that are in `all_stale_accts AND alive_ids` but NOT in `bd_df` (no BD bronze data with units > 0). For these accounts, the correct rescue source is `schwab_df` — the Schwab positions that were labeled `bd_stale` and zeroed at line 564. Those Schwab positions were present in the reconcile process; the fix is to re-inject from `schwab_df` (with source='schwab_override') instead of `bd_df` when `bd_df` contains no data for the account.

Historical performance data for RECONCILE_DROP accounts **already exists** in account_performance.parquet (these accounts have full history from 2023-2024). No backfill of historical dates is needed. The gap is only at the CURRENT date (2026-04-30) where they were dropped. Fixing B1 adds a 2026-04-30 row with real Schwab AUA to account_gains → account_performance.

**B2 — A_03 epsilon fix (AQR/SMA/TXN_LAG, ~18 accounts):** Investigate why UNREALIZED_DAILY produces epsilon units for z0822229381 (and likely the other 5 AQR + 2 SMA + 10 TXN_LAG accounts). If the UNREALIZED_DAILY file legitimately has near-zero units (position being wound down), A_03 should add a `units < epsilon_threshold` guard (e.g., `if abs(units) < 1e-6: skip`). If it's a float precision issue in the par-valuation step for DELPHI, fix the DELPHI pricing path.

No RPS-lag imputation, zero-fill, or interpolation is required for either sub-path. The data source is Schwab positions (already present in B_00's reconcile process) for B1, and UNREALIZED_DAILY file investigation for B2.

### Q2: Is C's split clean — can A be shipped independently?

**Yes, A is fully independent.** Fix A touches only `D_04.client_portal_summary.py`. No B_00 or A_03 changes required.

However: **A alone produces near-zero output until B lands.** With A fixed (canonical_holdings source-based detection), c1_recovered would report:
- B_00_BFIX3: 1 account (z0819627441, $574 silver AUA — NOT a C1 account, will produce count=1 but AUA~$0)
- AQR_INCLUDED: 1 account (z0822229381, $1.95M silver, $0 gold AUA due to epsilon units)
- A_03_OPTION_B: whatever other accounts are in canonical_holdings with non-stale sources that are in C1 universe

The forensic value of A without B is minimal. A correctly reflects the true broken state. Shipping A now is safe — it makes the sidecar accurately detect what B_00/A_03 actually produce, rather than silently emitting 0 for the wrong reason.

**Recommended shipping sequence:** A now (diagnostic clarity), B1 + B2 as a coordinated track with a chain QA gate before PROD.

### Q3: Effort and risk on B — 1-day patch or week-arc architectural?

**B1 (BFIX3 Schwab fallback — BFIX4):**
- Scope: Add rescue path in `process_date()` for `all_stale AND alive AND NOT in bd_df` accounts, using `schwab_df` (pre-zeroing Schwab positions). Requires threading through the pre-zeroing Schwab state — currently `bd_stale` rows are zeroed at line 564 before BFIX3 runs at line 718. May need to preserve the pre-zeroed Schwab positions in a separate dataframe.
- Effort: 2-3 days development + full chain QA cycle.
- Risk: **Medium.** Changes canonical_holdings construction in B_00 (highest-sensitivity script in the BD pipeline). Must not corrupt normal reconcile path. Requires careful unit tests + end-to-end QA with expected account list.
- Classification: **Week-arc** (3-4 days development, 1-2 day QA cycle, ~1 week total).

**B2 (A_03 epsilon filter):**
- Scope: Add `if abs(units) < 1e-6: continue` guard in UNREALIZED_DAILY injection path. Alternatively, investigate the root cause of epsilon DELPHI units in UNREALIZED_DAILY for z0822229381 (may be a par-valuation precision issue).
- Effort: 0.5-1 day.
- Risk: **Low.** Additive filter, doesn't change existing reconcile path.
- Classification: **1-day patch** once root cause of epsilon units is confirmed.

**Week-arc assessment:** B1 is week-arc. B2 is 1-day patch independent of B1.

### Q4: Would B require schema changes to account_performance?

**No.** comp-blast result: `No downstream consumers found for: gold:C_03.account_performance`.

account_performance already has all required columns: `date`, `account_id`, `total_aua`, `aua_change`, `growth`, `daily_inflow`, `daily_outflow`, etc. B1 adds non-zero VALUES for recovered accounts (2026-04-30 rows with real Schwab AUA) — no new columns.

The c1_recovered sidecar schema (from D_04 386456223) is also complete. No schema changes downstream.

---

## Fix Paths

### Fix A — D_04 Detection (Independent, Ship Now)

Replace `first_seen_in_gold >= _C1_FIX_DATE` with canonical_holdings source-based detection:

```python
# New detection gate: use canonical_holdings sources directly
ch_bfix3_ids = set of account_ids in canonical_holdings @ snapshot_date where source == 'bd_new_acct'
ch_aqr_ids   = set of account_ids where any(asset_name.upper().contains('DELPHI'))
ch_optb_ids  = (c1_universe account_ids in canonical_holdings) - ch_bfix3_ids - ch_aqr_ids

c1_recovered = c1_universe[
    c1_universe['account_id'].isin(gold_account_ids)
    & c1_universe['account_id'].isin(ch_bfix3_ids | ch_aqr_ids | ch_optb_ids)
].copy()
```

This correctly detects whatever B_00/A_03 actually produce, without relying on a hard-coded date boundary. When BFIX3 successfully rescues an account (with real non-epsilon units), it will appear in ch_bfix3_ids and be counted. When B2 fixes the AQR epsilon issue, z0822229381 will appear in ch_aqr_ids.

Remove `_C1_FIX_DATE` constant and `recently_added_ids` from the function.

### Fix B1 — BFIX4 in B_00 (Week-Arc)

In `process_date()`, after computing `all_stale_accts`:
```python
# BFIX4: For all-stale alive accounts not in bd_df, rescue from Schwab positions
bfix4_candidates = all_stale_accts & set(alive_ids) - set(bd_df['account_id'].unique())
if bfix4_candidates:
    # Use pre-zeroing Schwab state (need to preserve schwab_df before line 564 zeroing)
    bfix4_rows = schwab_df_pre_stale[schwab_df_pre_stale['account_id'].isin(bfix4_candidates)]
    bfix4_rows['source'] = 'schwab_override'
    holdings = pd.concat([holdings[~holdings['account_id'].isin(bfix4_candidates)], bfix4_rows])
```
Implementation detail: requires capturing Schwab positions before the `bd_stale` zeroing step at line 564.

### Fix B2 — A_03 Epsilon Guard (1-Day Patch)

In A_03's UNREALIZED_DAILY injection path:
```python
# Skip near-zero unrealized positions (float precision artifacts, closing lots)
unrealized_df = unrealized_df[unrealized_df['units'].abs() >= 1e-6]
```
Investigate z0822229381 specifically — check UNREALIZED_DAILY file for this account to confirm epsilon units are in the source file, not introduced by A_03's processing.

### Fix C — Hybrid (CTO Lean)

Ship A immediately. Queue B1 as a separate TO (week-arc, medium risk). Ship B2 in parallel with A (1-day patch, low risk). After B1 + B2 land: re-run chain → A's detection reports the actual recovery count.

---

## State After Chain (2026-05-04 16:43Z)

The c1_recovered=0 output is **correct** for the current pipeline state. The 58 C1 accounts are genuinely not in gold. The sidecar is working as designed; the underlying recovery mechanisms have not yet rescued the target accounts.

A note on AE 0.7's observation that "BFIX3 got them into canonical_holdings": AE likely read the B_00 log line `BFIX3: re-injecting N accounts`. That log fires when `bfix3_accts` is non-empty, but the rescued accounts still pass through the `holdings[units > 0]` filter at line 746. For the 40 RECONCILE_DROP accounts, BFIX3 is not triggered at all (they're absent from bd_df) — AE's "N" refers to z0819627441 only (the 1 epsilon-unit BD account). Confirm by checking B_00 log from SSM cc09f9a8 for the exact `re-injecting N` value.

---

## Recommended Next Steps

1. **[DS~B, 1 day]** Ship Fix A (D_04 detection rewrite). Pre-commit gate + chain QA smoke.
2. **[DS~B or DS~A, 1 day]** Ship Fix B2 (A_03 epsilon guard) — after confirming z0822229381 source data.
3. **[CTO gates Andrew]** B1 (BFIX4) is week-arc + medium risk. Requires TO scoping. Gate: B1 modifies B_00 (highest-sensitivity BD script). Andrew decision on timing.
4. **[DS~B after B1 + B2 land]** Re-run full chain → verify c1_recovered_count now matches expected (58-73).
5. **[DS~B]** Close ADVI_49FRECN.003 once QA pass with c1_recovered > 0.
