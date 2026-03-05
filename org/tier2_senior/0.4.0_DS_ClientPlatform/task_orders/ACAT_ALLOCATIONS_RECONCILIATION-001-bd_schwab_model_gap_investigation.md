# TASK ORDER: BD/Schwab/Model Allocation Gap Investigation

**Issue Code:** `ACAT_ALLOCATIONS_RECONCILIATION-001`
**Date Issued:** 2026-03-05
**Owner:** 0.4.0_DS_ClientPlatform
**Assigned to:** Data Scientist (DS)
**Status:** READY FOR EXECUTION

---

## Executive Summary

On 2026-03-04, three data sources show different total AUA for 49 Financial:

| Source | Total AUA | vs Schwab |
|--------|-----------|-----------|
| **Schwab** | $1,510,000,000 | baseline |
| **Our Model** | $1,545,000,000 | +$35M (+2.3%) |
| **BD Allocations** | $1,627,000,000 | +$117M (+7.7%) |

**Gap to explain:** $82M between BD and our model.

**Objective:** Identify sources of the $82M gap and determine if our model is correctly filtering data or if issues exist in the underlying data.

---

## Investigation Scope

### In Scope
- Compare BD allocations file (2026-03-03.parquet) vs our gold layer (client_performance 2026-03-04)
- Compare our model vs Schwab reported figure
- Hypothesis testing: pricing, deduplication, settlement, account filtering
- Document source of all material gaps

### Out of Scope
- Fixing any issues found (separate implementation tasks)
- Comparing to historical data (focus on 3/4/2026 only)
- Reprocessing source data

---

## Investigation Methodology

### Phase 1: Data Collection (DURATION: 30 min)
**Objective:** Confirm the three numbers and document metadata

**Tasks:**
1. Load BD allocations for 3/4/2026 (file: `silver/allocations/2026-03-03.parquet`)
   - Count total rows
   - Identify total AUA column
   - Count unique accounts
   - Check for duplicates on account_id
   - Identify cash positions

2. Load our gold layer for 3/4/2026 (file: `gold/client_performance.parquet`)
   - Filter to 2026-03-04
   - Count total rows
   - Identify total AUA column
   - Count unique relationships
   - Sum total AUA

3. Document Schwab figure (known: $1,510,000,000)

4. Calculate exact gaps:
   - BD to Schwab
   - Our Model to Schwab
   - BD to Our Model

**Success Criteria:** Confirm all three numbers ±$1M

---

### Phase 2: Hypothesis Testing (DURATION: 60 min, parallel execution)

#### **Track A: Pricing Differences (20 min)**
**Hypothesis:** BD uses different prices than our canonical_prices

**Tasks:**
1. Extract top 20 holdings from BD allocations (by market value)
2. For each holding:
   - Get BD price, units, market_value
   - Get our canonical price for same security
   - Calculate price delta per unit
   - Calculate total value impact

3. Sum value impacts across top 20 holdings
4. Extrapolate to full portfolio (if needed)

**Success Criteria:** Identify if pricing explains ≥$50M of the $82M gap

---

#### **Track B: Deduplication Completeness (20 min)**
**Hypothesis:** BD allocations file has duplicate account records not fully removed

**Tasks:**
1. Count BD allocations rows vs unique account_ids
2. If duplicates exist:
   - Identify which accounts have multiple rows
   - Sum market_value for duplicate rows
   - Measure total impact

3. Test: Re-deduplicate on (account_id, as_of_date) vs account_id alone
4. Measure value difference

**Success Criteria:** Identify if deduplication issues explain ≥$20M of the gap

---

#### **Track C: Settlement/Pending Trades (20 min)**
**Hypothesis:** BD includes pending/unsettled trades; our model excludes them

**Tasks:**
1. Identify settlement-related positions in BD allocations:
   - Check for `settlement_date > as_of_date` rows
   - Check for security names containing "settlement", "pending", "cash", "sweep"

2. Sum market value of identified pending positions

3. Check script 05 logic:
   - Does it exclude unsettled trades?
   - Does it apply settlement date filters?

4. If script 05 excludes pending: gap = pending trade total

**Success Criteria:** Identify if settlement/pending explains ≥$20M of the gap

---

### Phase 3: Account-Level Drill-Down (DURATION: 30 min)
**Objective:** Understand account structure differences

**Tasks:**
1. Account status analysis in BD:
   - Distribution by account_status (Open, Closed, Inactive, etc.)
   - Market value by status

2. Filter test:
   - Re-total BD allocations for "Open" accounts only
   - Compare to full total
   - Measure value of closed/inactive accounts

3. Cross-reference with our model:
   - Does our gold layer include closed accounts?
   - Are we explicitly filtering by account status?

**Success Criteria:** Quantify account status impact (target: <$20M)

---

### Phase 4: Model Source Verification (DURATION: 30 min)
**Objective:** Understand what data our model uses and how

**Tasks:**
1. Inspect `data/black_diamond/scripts/gold/05_build_client_performance.py`:
   - Primary data source: allocations, transactions, or hybrid?
   - AUA computation method
   - Any exclusion filters applied
   - Settlement date handling

2. Cross-reference with BD allocation logic:
   - Does script 05 use same allocations file?
   - Are there intentional adjustments/filters?

3. Document findings:
   - Source of our $1.545B figure
   - List all filters/adjustments applied

**Success Criteria:** Clear documentation of our model's data lineage

---

### Phase 5: Final Reconciliation (DURATION: 30 min)
**Objective:** Build complete reconciliation explaining the $82M gap

**Tasks:**
1. Build reconciliation table:
   ```
   BD allocations:      $1.627B
   Less: [Reason 1]     -$[X]
   Less: [Reason 2]     -$[Y]
   Less: [Reason 3]     -$[Z]
   ...
   Our model:           $1.545B
   Unexplained:         $[remaining]
   ```

2. Validate logic:
   - Sum of adjustments = $82M ±$5M?
   - Does each adjustment have documented evidence?

3. Cross-validate against Schwab:
   - Our model: $1.545B
   - Less: [items Schwab excludes]
   - Expected Schwab: ≈$1.510B ±$20M?

4. Produce final report with:
   - Reconciliation table
   - Evidence for each adjustment
   - Confidence level (low/medium/high) for each

**Success Criteria:** Account for ≥$70M of the $82M gap with documented evidence

---

## Success Criteria (Overall)

Investigation is **SUCCESSFUL** if:
- ✅ All three numbers confirmed ±$1M
- ✅ ≥$70M of the $82M gap is explained
- ✅ Each explanation has documented evidence
- ✅ Final reconciliation sums to within $5M
- ✅ Clear next steps identified

Investigation is **COMPLETE** when reconciliation explains the gap or identifies that further investigation is needed.

---

## Deliverables

| Deliverable | Format | Owner | Due |
|---|---|---|---|
| Phase 1 Output (confirmed numbers) | Console log + markdown | DS | +30 min |
| Phase 2A Output (pricing analysis) | CSV + analysis | DS | +90 min |
| Phase 2B Output (dedup analysis) | CSV + analysis | DS | +90 min |
| Phase 2C Output (settlement analysis) | CSV + analysis | DS | +90 min |
| Phase 3 Output (account drill-down) | CSV + summary | DS | +120 min |
| Phase 4 Output (script inspection) | Code notes + summary | DS | +150 min |
| Final Report | Markdown + reconciliation table | DS | +180 min |
| Session Log | Markdown | DS | +180 min |

---

## Timeline

| Phase | Task | Start | Duration | End |
|-------|------|-------|----------|-----|
| 1 | Data Collection | 0:00 | 30 min | 0:30 |
| 2A | Pricing (parallel) | 0:30 | 20 min | 0:50 |
| 2B | Dedup (parallel) | 0:30 | 20 min | 0:50 |
| 2C | Settlement (parallel) | 0:30 | 20 min | 0:50 |
| 3 | Account Drill-Down | 0:50 | 30 min | 1:20 |
| 4 | Script Inspection | 1:20 | 30 min | 1:50 |
| 5 | Reconciliation | 1:50 | 30 min | 2:20 |

**Total Duration:** ~2 hours 20 minutes

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Data files not available for 3/4/2026 | LOW | HIGH | Use closest available date; document timing difference |
| Python environment not available | LOW | MEDIUM | Use shell scripts with AWS CLI to extract basic numbers |
| Gaps cannot be explained | MEDIUM | MEDIUM | Document as "requires further investigation"; escalate |
| Script 05 logic is complex/undocumented | MEDIUM | MEDIUM | Read code directly; add comments for clarity |

---

## Resources Required

- **AWS credentials** (S3 access)
- **Python 3.x** with pandas, boto3, pyarrow
- **Text editor** for documentation
- **Spreadsheet tool** (Excel/sheets) for reconciliation table

---

## References

| Document | Purpose |
|----------|---------|
| `data/black_diamond/scripts/diagnostics/phase1_data_collection_20260304.py` | Phase 1 executable |
| `data/black_diamond/scripts/gold/05_build_client_performance.py` | Source code to inspect |
| `silver/allocations/2026-03-03.parquet` | BD allocations data |
| `gold/client_performance.parquet` | Our model data |

---

## Sign-Off

**Issued by:** 0.4.0_DS_ClientPlatform
**Date:** 2026-03-05
**Status:** READY FOR EXECUTION

**Next Action:** Execute Phase 1 data collection
