# ADVI_49FNV3.008 — COO Briefing: Gold-Silver AUA Validation Pipeline

**From:** 1.0.0_SA_CTO
**Date:** 2026-03-12
**Project:** ADVI_49FNV3
**Task order:** `org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/ADVI_49FNV3.008.gold-silver-aua-validation.md`

---

## Context: .007 Closed, .008 Remains

ADVI_PSCFIX (completed 2026-03-12) resolved the **display** side of the AUA discrepancy:
- `05d_write_aua_certification.py` now runs daily, compares gold vs silver, writes a certification JSON
- `bd-portal-publisher` (bd-v2.18.3) applies certified_aua from silver to all total_aua displays
- `09_generate_partner_analytics.py` applies certified_aua to current-period donut totals
- All portal AUA displays converge on the BD-official silver number

This fully resolves **.007** (timeseries vs snapshot consistency). That task order is now marked complete.

**.008 remains** because it addresses a different concern: **pipeline observability and root cause investigation**. The display is correct, but the gold layer still silently diverges from silver by ~0.36% ($5.7M) due to two independent errors that cancel each other. Without .008, we have no structured alerting, no trend history, and no understanding of whether the gap is stable or drifting.

---

## What .008 Asks For (Unchanged)

The existing task order at `0.6.0_AE_PartnerETL` is well-specified and still valid. Summary:

| # | Deliverable | Status |
|---|------------|--------|
| 1 | Create `05c_validate_aua_vs_silver.py` — structured validation with PASS/WARN/FAIL thresholds and account-level gap decomposition | **Not started** |
| 2 | Wire 05c into pipeline (runs after 05_build_client_performance, before 09) | **Not started** |
| 3 | Backfill 35 dates (2026-01-16 through 2026-03-09) to `gold/validation/` | **Not started** |
| 4a | Investigate 83 accounts in silver not in gold accounts_dimension | **Not started** |
| 4b | Document canonical price divergence methodology (~$20.5M hot vs BD prices) | **Not started** |

### What PSCFIX Already Provides (Reduces Scope Slightly)

- `05d_write_aua_certification.py` already loads silver allocations and computes `certified_aua`, `gold_aua`, `gap_abs`, `gap_pct`, and `liability_types_excluded`. The 05c script can reuse this foundation but adds: PASS/WARN/FAIL thresholds, account-level decomposition (missing accounts + price divergence estimate), and writes to `gold/validation/` instead of `gold/aua_certification/`.
- The 6 liability account types to exclude are already codified in 05d: CreditCard, Mortgage, Loans, Insurance, TermLife, Annuity.

### Known Baseline (From DE investigation 2026-03-11)

```
Gold AUA:                    $1,604,943,633
Silver AUA:                  $1,599,225,407
Gap:                         +$5,718,227  (0.36%)
Accounts in silver not gold: 83 accounts, $14.8M MV
Price divergence estimate:   ~$20.5M (canonical prices run hot vs BD)
```

These two errors (-$14.8M missing accounts + $20.5M hot prices) partially cancel, producing a deceptively small net gap.

---

## Routing

**Assigned to:** `0.6.0_AE_PartnerETL` (task order already in their queue)
**Priority:** Low-medium. Not feature-blocking — the portal displays correct numbers via PSCFIX. This is engineering quality / observability.
**Dependencies:** None. Silver allocations exist daily from 2026-01-16. Gold client_performance and accounts_dimension are available in S3.
**Deployment:** EC2 gold layer script + wiring into `run_gold_layer.sh`. No Lambda changes needed.

---

## Action Required from COO

1. Confirm `0.6.0_AE_PartnerETL` has bandwidth (check against DRFR_PTMCH P5 orchestrator work and any other pending task orders)
2. If bandwidth exists, activate the existing .008 task order — no changes needed to the spec
3. If bandwidth is tight, .008 can be deferred — the display correctness is already handled by PSCFIX
