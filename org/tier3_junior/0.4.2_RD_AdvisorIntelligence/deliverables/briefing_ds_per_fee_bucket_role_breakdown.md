# Briefing: Per-Fee-Bucket Per-Role Breakdown in Platinum Leaderboard

**From:** 0.4.2_RD_AdvisorIntelligence
**For:** 0.4.0_DS_ClientPlatform (routed by Andrew)
**Date:** 2026-04-10
**Page affected:** `portal/src/pages/AdvisorIntelligence/AdvisorPublicProfile.tsx` (RoleDonut)
**Source script:** `data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py`
**Source artifact:** `s3://opal-data-bd/platinum/firm/leaderboard.json`

---

## What we want

The Role Composition donut on the advisor drilldown page should respond to the Fee toggle (All / Fee-Paying / No-Fee). Today the donut and per-role tiles are static no matter which fee bucket is selected because the JSON does not carry per-fee-bucket per-role aggregations.

## Why it matters

Andrew specifically called this out as misleading. When a user selects "Fee-Paying" they reasonably expect every panel on the page -- summary tiles, time series, **and** role donut -- to reflect the fee bucket. Right now the SummaryCard and TimeSeries respect the toggle (because `applyFeeBucket()` swaps the entry-level fields) but the RoleDonut silently keeps showing the all-fee total. I previously had a "Fee filter not applied -- role split available at tagged-total grain only" footnote on the donut to warn users; Andrew asked me to remove it because the wording was confusing, so now the misalignment is invisible.

The cleanest fix is to publish per-fee-bucket per-role data in the platinum leaderboard JSON. The source data (silver/transactions joined with advisor_assignments_history and the fee schedule from A_01) already has everything required.

## Current state of the JSON

I read a sample entry from `s3://opal-data-bd/platinum/firm/leaderboard.json` (49financial, QTD window, 153 entries):

```json
{
  "name": "...",
  "advisor_id": "...",
  "roles": ["architect", "implementor", "consultant", "local_ops"],
  "total_aua": ...,
  "fee_breakdown": {
    "fee_paying": {
      "aua": 88937234.5,
      "account_count": 401,
      "client_count": 0,
      "nna": 657294.68,
      "inflows": 660994.54,
      "outflows": 3699.87,
      "period_start_aua": 85892053.42,
      "aua_growth_pct": 3.55
    },
    "no_fee": { ... same shape ... }
  },
  "role_breakdown": {
    "architect": {
      "aua": 78245.89,
      "nna": 0.0,
      "inflows": 0.0,
      "outflows": 0.0,
      "account_count": 2,
      "client_count": 2
    },
    "implementor": { ... },
    "consultant": { ... },
    "local_ops": { ... }
  }
}
```

`fee_breakdown` and `role_breakdown` exist as siblings but never intersect.

## Proposed shape

Two viable options. I'd lean toward Option 1 because it mirrors the existing `fee_breakdown` pattern and keeps the role data grouped under each role (which is how the frontend iterates).

### Option 1 (preferred): nest fee buckets inside each role

```json
"role_breakdown": {
  "architect": {
    "aua": 78245.89,
    "nna": 0.0,
    "inflows": 0.0,
    "outflows": 0.0,
    "account_count": 2,
    "client_count": 2,
    "fee_paying": {
      "aua": 78245.89,
      "nna": 0.0,
      "inflows": 0.0,
      "outflows": 0.0,
      "account_count": 2,
      "client_count": 2
    },
    "no_fee": {
      "aua": 0.0,
      "nna": 0.0,
      "inflows": 0.0,
      "outflows": 0.0,
      "account_count": 0,
      "client_count": 0
    }
  },
  ...
}
```

Top-level fields stay (the "all" view) so existing consumers don't break. New `fee_paying` / `no_fee` sub-objects let the frontend pick the right slice based on `feeView`.

### Option 2: nest role breakdown inside each fee bucket

```json
"fee_breakdown": {
  "fee_paying": {
    "aua": 88937234.5,
    ...,
    "role_breakdown": {
      "architect": { "aua": ..., "nna": ..., ... },
      "implementor": { ... },
      ...
    }
  },
  "no_fee": { ..., "role_breakdown": { ... } }
}
```

Cleaner conceptually but the frontend already iterates `entry.role_breakdown` keys, so Option 1 is a smaller delta on the consumer side.

Both options preserve backward compat for the all-fee view.

## Implementation sketch (D_00c.portal_leaderboard.py)

Today `role_breakdown_by_advisor` is built around `role_detail = window.groupby(['advisor', 'role']).agg(...)` (line 266). The fields `aua, account_count, client_count` get overridden from `at_role_breakdown` (the all-tagged view) at lines 298-301, while `nna, inflows, outflows` stay from the fee-paying-only `window` aggregation. So the current `role_breakdown[role]` is already a hybrid (tagged AUA + fee-paying flows), which is part of why the per-fee-bucket version is murky.

The fix is two new aggregations -- one over fee-paying transactions only, one over no-fee transactions only -- both grouped by `(advisor, role)`. The fee-paying view is essentially what `window.groupby(['advisor','role']).agg(...)` already does (since `detail` from C_08 is fee-paying scoped); the no-fee view needs a parallel pass over the no-fee slice. The `at_role_breakdown` melt at line 502 already walks `account_team` with `total_aua` and the role columns; that loop can be split by fee status to produce both buckets in one pass.

Pseudocode:

```python
# After computing the existing role_detail (fee-paying-only via window)
# and at_role_breakdown (all-tagged via account_team melt), add:

at_role_breakdown_fee_paying = {}  # advisor -> role -> {aua, accts, clients}
at_role_breakdown_no_fee     = {}

if account_team is not None and 'is_fee_paying' in account_team.columns:
    fee_at = account_team[account_team['is_fee_paying']]
    nofee_at = account_team[~account_team['is_fee_paying']]
    # Repeat the existing melt+groupby pattern (lines 502-528) on each slice,
    # writing into the two new dicts.

# Then in the per-advisor entry build (line 290+), populate:
breakdown[role_str] = {
    'aua':           ...,  # all-tagged (current)
    'nna':           ...,  # current
    'inflows':       ...,  # current
    'outflows':      ...,  # current
    'account_count': ...,  # current
    'client_count':  ...,  # current
    'fee_paying': {
        'aua':           at_role_breakdown_fee_paying.get(adv, {}).get(role_str, {}).get('aua', 0),
        'nna':           ...,  # from fee-paying scoped role_detail
        'inflows':       ...,
        'outflows':      ...,
        'account_count': ...,
        'client_count':  ...,
    },
    'no_fee': {
        'aua':           at_role_breakdown_no_fee.get(adv, {}).get(role_str, {}).get('aua', 0),
        'nna':           ...,  # tagged_role - fee_paying_role
        'inflows':       ...,
        'outflows':      ...,
        'account_count': ...,
        'client_count':  ...,
    },
}
```

For NNA / inflows / outflows in the no-fee bucket, the existing pattern at line 386-393 (no_fee = tagged - fee_paying at the entry level) should generalize cleanly to per-role: `no_fee_role_nna = tagged_role_nna - fee_paying_role_nna`, where `tagged_role_nna` would need a new tagged-window-metrics-by-role computation (currently `_compute_tagged_window_metrics` only aggregates per-advisor, not per-(advisor, role)).

The role-overlap multi-counting note is still relevant here -- whatever rule D_00c eventually applies for the all-AUA-divided-evenly fix Andrew has flagged should apply identically to the per-fee-bucket sub-aggregations so the ratios stay consistent.

## Validation checklist

When the change ships, the frontend should be able to verify:

1. **Sum invariant per advisor:** for every role `r`, `role_breakdown[r].fee_paying.aua + role_breakdown[r].no_fee.aua == role_breakdown[r].aua` (within rounding).
2. **Sum invariant per fee bucket:** sum over roles of `role_breakdown[r].fee_paying.aua` should equal `fee_breakdown.fee_paying.aua` (modulo the multi-role overlap factor; same caveat as today).
3. **No regressions on existing fields:** the top-level `role_breakdown[r].{aua, nna, inflows, outflows, account_count, client_count}` stay numerically identical to today.
4. **NNA sign preserved:** `no_fee.nna` can be negative; do not clamp.
5. **Spot check on 49financial:** run the audit script `data/analysis/role_overlap_audit.py` post-change to confirm the per-role sums roll up correctly. Andrew has the previous role-overlap audit results (372 accounts, ~3.74%) for cross-reference.

## Frontend impact (after DS ships)

Once the new shape lands, I will:

1. Update `PlatinumRoleBreakdown` in `portal/src/pages/AdvisorIntelligence/types.ts` to add the optional `fee_paying` / `no_fee` sub-objects.
2. In `RoleDonut`, look up `entry.role_breakdown[role][feeView]` when `feeView !== 'all'`, falling back to the top-level fields for backward compat.
3. Pass `feeView` back into `RoleDonut` (I dropped it from the props in the last commit since the data wasn't there to use).
4. Verify that summing the per-role per-fee-bucket AUA matches the entry-level `fee_breakdown[feeView].aua` to within the multi-role tolerance.

Total frontend delta is ~30 lines.

## Coordination notes

- **No urgent deadline.** The donut works correctly for the All view today. Fee-Paying / No-Fee viewers see the all-fee role breakdown silently, which is the same behavior they had before I removed the warning.
- **Coordinate with the role-overlap divide-evenly fix** Andrew already flagged for D_00c (the 372-accounts-with-multi-role briefing). Both touch the same role aggregation code, so it's cheaper to land them together than back-to-back.
- **No type-system change required for the wire format.** The TS interface change is additive and the Lambda router doesn't validate the JSON shape -- the new fields just pass through.
