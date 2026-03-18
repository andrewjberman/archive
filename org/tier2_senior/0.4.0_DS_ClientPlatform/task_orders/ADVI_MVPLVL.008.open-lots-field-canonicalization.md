# Task Order: ADVI_MVPLVL.008 — Open Lots Field Canonicalization

**To:** `0.4.0_DS_ClientPlatform`
**From:** `0.4.0_DE_ClientPlatform`
**Project:** `ADVI_MVPLVL`
**Date:** 2026-03-18

---

## Context

The Books tab L3 view now has an expandable grouped open lots table. Each unique
asset is collapsed into a single row with an expand toggle; clicking reveals individual
lot sub-rows. The aggregate row computes:

- **Qty**: total units across all lots for the asset
- **Avg Cost**: total cost basis / total units (cost basis per unit)
- **Mkt Value**: sum of market values
- **Gain**: sum of unrealized gains
- **Term**: Short / Long / Hybrid (mixed)
- **Acq. Date**: most recent acquisition date across all lots

Two field name mismatches between the Lambda output and the frontend interface are
currently silently broken. Additionally, two fields already fetched by the Lambda are
not being forwarded to the API response.

---

## Field Mismatches (broken, silent)

The Lambda (`bd-portal-advisor-publisher`) builds `open_lots` using `lot_cols` (line 701):

| Lambda key | Frontend expects | Current state |
|---|---|---|
| `current_units` | `quantity` | **Broken** — `quantity` is always `undefined` on the frontend; displays `--` |
| `accrued_gain` | `unrealized_gain` | **Broken** — `unrealized_gain` is always `undefined`; gain displays as `$0.00` |

---

## Fields Available but Not Forwarded

These columns are already in `lot_cols` and fetched from source data but the
frontend `OpenLot` interface didn't previously consume them. They are now in the
interface as optional fields. Confirm they are in the Lambda output:

| Lambda key | Frontend field | Usage |
|---|---|---|
| `cost_per_unit` | `cost_per_unit?` | Shown in per-lot expanded rows as "Avg Cost" fallback |
| `current_price` | `current_price?` | Available for future use (current market price per unit) |

---

## Requested Lambda Change

In `build_tax_detail()` in `bd-portal-advisor-publisher/lambda_function.py`, update the
`open_lots` output block (around line 711-723) to rename the two mismatched fields:

```python
# In the lot dict construction loop, add canonical aliases:
if 'current_units' in lot:
    lot['quantity'] = lot.pop('current_units')   # rename to canonical
if 'accrued_gain' in lot:
    lot['unrealized_gain'] = lot.pop('accrued_gain')  # rename to canonical
```

OR equivalently, update `lot_cols` to output `quantity` and `unrealized_gain` directly
by renaming the source columns before iterating:

```python
taxable_open = taxable_open.rename(columns={
    'current_units': 'quantity',
    'accrued_gain': 'unrealized_gain',
})
```

**Also confirm** `cost_per_unit` and `current_price` are included in the available
columns (they are already in `lot_cols` at lines 705-706).

---

## Acceptance Criteria

1. `open_lots[*].quantity` is a non-zero number for positions with units
2. `open_lots[*].unrealized_gain` matches `market_value - cost_basis` for each lot
3. `open_lots[*].cost_per_unit` present and equal to `cost_basis / quantity`
4. `open_lots[*].current_price` present
5. In the portal Books L3 view: Qty column shows real unit counts; Gain column shows
   real gain values; lot expand rows show per-lot Avg Cost from `cost_per_unit`
6. A re-publish run is required after the Lambda fix to regenerate all client JSON files

---

## Deploy path

Lambda fix → `terraform apply` (bd-pipeline) → re-run `bd-portal-advisor-publisher`
for all relationships → verify spot-check a known relationship JSON in S3.
