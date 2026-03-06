# PRD: AUA Variance Analysis (ADVI_AUAVAR)

**Author:** 1.0.0_SA_CTO
**Date:** 2026-03-06
**Project Code:** ADVI_AUAVAR
**Macro:** ADVI (AdvisorIntelligence)
**Pods:** 0.4 (ClientPlatform)
**Pipeline:** bd-pipeline

---

## 1. Problem Statement

As of 2026-03-02, our Black Diamond gold layer reports **~$1.545B non-cash AUA**,
while Black Diamond's own allocation snapshot shows **~$1.60B non-cash AUA**.
The 49Financial data team confirmed that their leadership relies primarily on
Black Diamond numbers. The gap is approximately **$55M** (3.4%).

Prior DS investigation (2026-03-05) established that the gap is a **fundamental data
source difference**: BD provides a point-in-time allocation snapshot, while our model
reconstructs AUA from transaction history + daily positions + price feeds. The DS found
our model is actually closer to Schwab ($1.51B) than BD is, validating our filters.

However, the business question has shifted. Since leadership uses BD as their source
of truth, we need to understand at a **segment level** what accounts or categories
we are undervaluing. This is not about fixing our model to match BD -- it is about
understanding where the variance lives so we can explain it or address it.

---

## 2. Objective

Produce a segment-level decomposition of the ~$55M AUA gap between our gold layer
model ($1.545B) and Black Diamond allocations ($1.60B) as of a matching date.
Identify which account segments, asset classes, or pricing differences explain
the variance, and determine which (if any) should be incorporated into our model.

---

## 3. Scope

### 3.1 In Scope

1. **Date-aligned comparison** -- Run both BD allocations and our gold layer model
   for the same date (ideally 2026-03-03 or later) to eliminate date-shift noise.
   Prior comparison used mismatched dates (BD 2026-03-03 vs model 2026-03-02).

2. **Segment decomposition** -- Break the gap into explanatory segments:
   - **Account coverage gap** -- Accounts present in BD but absent from our
     accounts_dimension (known: 43 accounts = $9.1M from prior investigation)
   - **Asset class variance** -- Which asset classes (equities, fixed income,
     alternatives, cash equivalents) contribute most to the gap?
   - **Pricing variance** -- BD uses their own pricing engine; we use canonical_prices.
     Quantify the pricing contribution where symbol-level matching is possible.
   - **Household aggregation** -- Our model aggregates to relationship level via
     accounts_dimension. Does the aggregation lose or double-count anything?
   - **Cash treatment** -- BD may include cash positions our model filters as
     "non-investable." Quantify the cash/sweep delta.
   - **Closed/pending accounts** -- BD shows only open accounts (6,334). Confirm
     our model also filters to open-only.

3. **Waterfall chart data** -- Produce a reconciliation waterfall:
   `BD Total -> -Account Coverage -> -Pricing -> -Cash Treatment -> ... -> Our Total`
   Each segment quantified in dollars.

4. **Recommendation memo** -- For each segment, classify as:
   - **Addressable** -- We should incorporate this into our model (e.g., missing accounts)
   - **Explainable** -- Legitimate difference we can document (e.g., pricing methodology)
   - **Investigate further** -- Needs more data (e.g., symbol-level pricing match)

### 3.2 Out of Scope

- NNA correlation optimization (separate project: ADVI_NNAVAR)
- Modifying BD pipeline data ingestion
- Portal UI changes
- Reconciling with Schwab's separate $1.51B figure (use BD as the reference)

---

## 4. Prior Work (State of Play)

| Artifact | Status | Location |
|----------|--------|----------|
| Phase 1 data collection | COMPLETE | DS log `bd_model_schwab_reconciliation_investigation.md` |
| Phase 2 hypothesis testing | COMPLETE | 4 hypotheses tested: pricing (INCONCLUSIVE), dedup ($0), settlement ($0), account filtering ($9.1M) |
| Phase 5 reconciliation | COMPLETE | Root cause: fundamental data source difference |
| Diagnostic scripts | COMMITTED | `data/black_diamond/scripts/diagnostics/phase1_data_collection_20260304.py` + phase2a/2b/2c + phase5 |

**Key numbers from prior investigation:**
- BD allocations (2026-03-03): $1.605B (6,334 accounts, all open)
- Our model (2026-03-02): $1.236B (2,770 relationship rows) -- NOTE: this was an
  earlier date and may use a different AUA definition than the $1.545B Andrew cites
- Known account coverage gap: 43 accounts = $9.1M (0.6% of total gap)
- Pricing: INCONCLUSIVE (BD allocations lack symbol/price data for direct comparison)

**Important:** The $1.236B figure from DS Phase 1 appears to use a different metric
or date than Andrew's $1.545B. First action is to reconcile these two numbers on a
matching date with a consistent non-cash AUA definition.

---

## 5. Agents & Responsibilities

| Agent | Role in This Project |
|-------|---------------------|
| 0.4.0_DS_ClientPlatform | Analysis scripts, segment decomposition, recommendation memo |
| 0.4.0_DT_ClientPlatform | EC2 execution of comparison scripts, S3 artifact management |
| 0.6.0_AE_PartnerETL | BD pipeline owner -- consulted if BD allocation data needs enrichment (e.g., symbol-level pricing) |

---

## 6. Deliverables

1. **Date-aligned comparison dataset** -- BD allocations and gold layer model AUA
   for the same date, both filtered to non-cash only
2. **Segment decomposition table** -- Each segment quantified in dollars with
   percentage of total gap
3. **Waterfall reconciliation** -- Visual data structure showing BD -> Our Model
   with each adjustment step
4. **Recommendation memo** -- Addressable / Explainable / Investigate classification
   for each variance segment
5. **Action items** -- If addressable segments exist, specific changes needed
   (with task order stubs for DS/DT)

---

## 7. Success Criteria

| Criterion | Target |
|-----------|--------|
| Gap decomposition coverage | >= 80% of $55M gap attributed to named segments |
| Date alignment | Both sources sampled on identical date |
| Non-cash AUA definition | Consistent between BD and our model (documented) |
| Recommendation coverage | Every segment classified as Addressable / Explainable / Investigate |

---

## 8. Risks

| Risk | Mitigation |
|------|-----------|
| BD allocations lack symbol-level data for pricing comparison | AE may need to check if richer allocation exports are available from BD API |
| $1.236B vs $1.545B discrepancy suggests metric definition mismatch | First task: reconcile the two numbers before any decomposition work |
| Gap may be fully explainable with no addressable action | That is a valid outcome -- the deliverable is the explanation, not necessarily a code change |

---

## 9. Data Architecture

No new Lambda functions or pipeline changes. This project produces diagnostic outputs
and a recommendation memo. If addressable segments are found, implementation changes
to script 05 or the BD ingestion pipeline would be scoped as follow-on work items.

**Data sources:**
- BD allocations: `s3://opal-data-bd/allocations/` (daily snapshots from BD API)
- Gold layer model: `s3://opal-data-bd/gold/client_performance.parquet`
- Accounts dimension: `s3://opal-data-bd/gold/accounts_dimension.parquet`
- Canonical prices: `s3://opal-data-bd/gold/canonical_prices.parquet`
