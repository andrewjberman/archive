# Brief — ADVI_49FRECN.003 Option A: Sidecar Detection Fix (DRAFT — NOT SHIPPED)

**Author:** 0.4.0_DS_ClientPlatform~C
**Date:** 2026-05-04
**Status:** DRAFT — local edit only; awaiting CTO ratification before commit
**Gate:** py_compile PASS | AST scan PASS | ruff PASS

---

## Problem Statement

The `build_c1_recovered_accounts()` function in `D_04.client_portal_summary.py` uses a
`first_seen_in_gold >= _C1_FIX_DATE` heuristic to detect C1-recovered accounts. This relies
on `account_performance` (C_03 output) to determine when an account "first appeared in gold."

**Root cause of sidecar = 0:**

BFIX3-rescued RETURNING accounts have prior gold history (they were in gold before going stale,
so `first_seen_gold < 2026-05-01`). After BFIX3, they return to `canonical_holdings` (B_00
output) — but C_03 cannot rebuild their timeseries without prior `account_gains` from B_03
(propagation gap, confirmed by AE 0.7 Step 16: account_performance = 6,106 accounts,
canonical_holdings has 58 more). The date filter therefore excludes them.

**Evidence (chain run cc09f9a8, 2026-05-04T16:43Z):**
- `canonical_holdings` at 2026-04-30: confirmed to contain BFIX3-rescued accounts (AE 0.7 B_00 Step 11)
- `account_performance` at 2026-04-30: 6,106 accounts (delta of 58 vs canonical_holdings)
- `out_of_scope_accounts.json`: `excluded_c1_count=58`, `excluded_c1_aua=$56,801,374`
- `c1_recovered_accounts.json`: `total_recovered_count=0` (sidecar incorrect)

---

## Fix: Code Diff (D_04 `build_c1_recovered_accounts()`)

### Before (lines 3481–3541 pre-edit)

**Block 1 — account_performance load (lines 3481–3500):**
```python
# Load gold account_performance for recovered-account set
try:
    perf_df = _read_parquet(ACCOUNT_PERFORMANCE, columns=['date', 'account_id'])
    perf_df['account_id'] = perf_df['account_id'].astype(str).str.strip()
    perf_df['date'] = pd.to_datetime(perf_df['date'], errors='coerce')
    perf_at_date = perf_df[perf_df['date'] == latest_gold_date]
    gold_account_ids = set(perf_at_date['account_id'].unique())
    print(f'  account_performance @ {snapshot_date}: {len(gold_account_ids):,} accounts')
    # Accounts first appearing in gold on/after fix date are C1 recovery candidates.
    # Accounts always in gold have earlier first-seen dates and are excluded.
    first_seen_df = (perf_df.dropna(subset=['date'])
                     .groupby('account_id')['date'].min()
                     .reset_index(name='first_seen_gold'))
    recently_added_ids = set(
        first_seen_df[first_seen_df['first_seen_gold'] >= _C1_FIX_DATE]['account_id']
    )
    print(f'  accounts first seen in gold >= {_C1_FIX_DATE.date()}: {len(recently_added_ids):,}')
except Exception as e:
    print(f'  ERROR: failed to load account_performance: {e}')
    return None
```

**Block 2 — c1_recovered filter (lines 3533–3546):**
```python
# C1 recovered = C1 universe accounts that are in gold AND first appeared in gold
# on/after the fix date (2026-05-01 when BFIX3 + A_03 Option B landed).
c1_recovered = c1_universe[
    c1_universe['account_id'].isin(gold_account_ids)
    & c1_universe['account_id'].isin(recently_added_ids)
].copy()
```

**Block 3 — mechanism detection (lines 3554–3577):** loaded `ch_df` from S3 inline.

---

### After (current local edit)

**Block 1 — account_performance load (trimmed) + canonical_holdings early load (added):**
```python
# Load gold account_performance for gold-membership baseline
try:
    perf_df = _read_parquet(ACCOUNT_PERFORMANCE, columns=['date', 'account_id'])
    perf_df['account_id'] = perf_df['account_id'].astype(str).str.strip()
    perf_df['date'] = pd.to_datetime(perf_df['date'], errors='coerce')
    perf_at_date = perf_df[perf_df['date'] == latest_gold_date]
    gold_account_ids = set(perf_at_date['account_id'].unique())
    print(f'  account_performance @ {snapshot_date}: {len(gold_account_ids):,} accounts')
except Exception as e:
    print(f'  ERROR: failed to load account_performance: {e}')
    return None

# Load canonical_holdings for recovery detection.
# BFIX3/Option B rescues appear in canonical_holdings (B_00 output) but NOT in
# account_performance (C_03 propagation gap: cannot build timeseries for all-stale
# accounts without prior gains history from B_03). Detection signal:
#   in canonical_holdings AND NOT in account_performance at snapshot_date.
# ch_df kept in scope for mechanism detection below (avoids double S3 read).
ch_df: pd.DataFrame | None = None
ch_account_ids: set[str] = set()
try:
    ch_key = canonical_holdings_key(snapshot_date)
    resp = s3.get_object(Bucket=BUCKET, Key=ch_key)
    ch_df = pd.read_parquet(BytesIO(resp['Body'].read()))
    ch_df['account_id'] = ch_df['account_id'].astype(str).str.strip()
    ch_account_ids = set(ch_df['account_id'].unique())
    print(f'  canonical_holdings @ {snapshot_date}: {len(ch_account_ids):,} accounts')
except Exception as e:
    print(f'  WARN: canonical_holdings load failed ({e}) -- falling back to first_seen heuristic')
```

**Block 2 — c1_recovered filter (canonical_holdings primary, first_seen fallback):**
```python
# C1 recovered = C1 universe accounts present in canonical_holdings (BFIX3/Option B
# rescued) but absent from account_performance (C_03 propagation gap).
if ch_account_ids:
    c1_recovered = c1_universe[
        c1_universe['account_id'].isin(ch_account_ids)
        & ~c1_universe['account_id'].isin(gold_account_ids)
    ].copy()
    print(f'  C1 recovered (in canonical, not in perf): {len(c1_recovered):,} accounts, '
          f'${c1_recovered["allocation_aua"].sum():,.2f} AUA')
else:
    # Fallback: first-seen-in-gold heuristic (used if canonical_holdings unavailable)
    first_seen_df = (perf_df.dropna(subset=['date'])
                     .groupby('account_id')['date'].min()
                     .reset_index(name='first_seen_gold'))
    recently_added_ids = set(
        first_seen_df[first_seen_df['first_seen_gold'] >= _C1_FIX_DATE]['account_id']
    )
    c1_recovered = c1_universe[
        c1_universe['account_id'].isin(gold_account_ids)
        & c1_universe['account_id'].isin(recently_added_ids)
    ].copy()
    print(f'  WARN: canonical_holdings unavailable -- first_seen fallback: '
          f'{len(c1_recovered):,} accounts')
```

**Block 3 — mechanism detection (reuses ch_df; eliminates duplicate S3 read):**
- `ch_df is not None` guard replaces unconditional S3 load
- Mechanism assignment logic unchanged

---

## Expected Count Post-Fix (REVISED 20260504T172601Z per DS~B empirical brief)

| Ship state | Expected count | AUA | Explanation |
|------------|---------------|-----|-------------|
| Post-A only (99664e778) | **0** | $0 | HONEST — BFIX3 confirmed did NOT rescue accounts; they hit `bd_df units>0` pre-filter in B_00 and never entered canonical_holdings. `C1 ∩ canonical_holdings − account_performance = empty`. |
| Post-A + B2 (A_03 epsilon guard) | 58–73 | ~$56.8M–$71.4M | B2 rescues the accounts into canonical_holdings; A correctly detects them via the new delta. |
| Post-A + B1 + B2 (full architectural fix) | 58–73 | ~$56.8M–$71.4M | Same as above. |

**Key finding (DS~B brief, 20260504T172601Z):**
BFIX3 log events fired in B_00 (chain run cc09f9a8 confirmed), but the 40 RECONCILE_DROP
Schwab-custodied accounts hit the `bd_df units>0` pre-filter BEFORE BFIX3's injection path.
They were filtered out upstream and never entered canonical_holdings. The 58 accounts confirmed
by `excluded_c1_count` are therefore NOT in canonical_holdings at 2026-04-30.

**Why Option A is still correct:**
The new detection `C1 ∩ canonical_holdings − account_performance` is the honest metric.
Post-A-only-ship, count=0 is the accurate answer (no rescues landed). The prior heuristic
would have reported a false non-zero by using `first_seen_gold >= 2026-05-01` even when
nothing was actually rescued. Option A is the truth-telling fix; B2 is the rescue fix.

---

## Validation Strategy

On next chain re-run (after this fix ships + chain re-dispatched from B_00):

1. **canonical_holdings count check:**
   D_04 will print `canonical_holdings @ 2026-04-30: {N} accounts` — expect N = 6,106 + 58 = 6,164.

2. **sidecar count check:**
   D_04 prints `C1 recovered (in canonical, not in perf): {count} accounts`.
   Post-A-only ship: expect **0** (BFIX3 accounts not in canonical_holdings per DS~B empirical brief).
   Post-A+B2 ship: expect 58–73.
   count=0 from current QA run (SSM 6f75bf31) is the CORRECT HONEST result.

3. **out_of_scope check:**
   `excluded_c1_count` remains 58 until Option B ships (sidecar tracks recovery; the AUA gap
   persists in the firm roll-up until C_03 propagation is fixed).

4. **ETag capture:**
   `aws s3api head-object --bucket opal-data-bd --key gold/artifacts/49f/c1_recovered_accounts.json --query ETag`
   — for RAVC4 evidence.

---

## Side-Effect Audit

**Q: Does this affect any other consumer of `c1_recovered_accounts.json`?**

From `comp-platinum reverse c1_recovered_accounts.json` (Phase 1 mandate, session log):
- Result: **Zero downstream consumers** — forensic-only initial state.
- No FE component reads this artifact. No portal tab wired to it.
- No other D_04 step reads the sidecar (it's write-only in D_04's main() chain).

**Q: Does loading canonical_holdings early change D_04 behavior anywhere else?**

No. `ch_df` was previously local to the `if not c1_recovered.empty:` block and was only
used for mechanism detection. The early load simply hoists it outside that guard. The
mechanism detection block now uses the pre-loaded `ch_df` via `ch_df is not None` guard
rather than re-fetching from S3. Net effect: one fewer S3 read when c1_recovered is non-empty;
same result.

**Q: What happens when Option B (propagation gap fix) ships and C_03 includes BFIX3 accounts?**

After Option B:
- BFIX3 accounts will be in BOTH canonical_holdings AND account_performance.
- New filter: `in ch_account_ids AND NOT in gold_account_ids` → ZERO for these accounts.
- Sidecar `total_recovered_count = 0` after full fix — correct. The sidecar's purpose was
  forensic tracking of the recovery event during the propagation gap window.
- If persistent forensic tracking is wanted post-Option-B, the detection signal should change
  to `in ch_account_ids` (unconditional) — but that is a separate scope decision for CTO.

---

## Pre-Commit Gate Result (local validation)

```
py_compile:          PASS
ds-precommit-check:  PASS (exit 0)
ruff:                All checks passed!
```

**Draft is ready to commit on CTO ratify GO from COO.**
