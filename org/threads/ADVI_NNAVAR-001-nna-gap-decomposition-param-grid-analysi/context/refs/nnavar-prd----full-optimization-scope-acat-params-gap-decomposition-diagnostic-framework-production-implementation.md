# PRD: NNA Variance Optimization (ADVI_NNAVAR)

**Author:** 1.0.0_SA_CTO
**Date:** 2026-03-06
**Project Code:** ADVI_NNAVAR
**Macro:** ADVI (AdvisorIntelligence)
**Pods:** 0.4 (ClientPlatform)
**Pipeline:** bd-pipeline

---

## 1. Problem Statement

Our Black Diamond gold layer model produces a 13-month NNA (Net New Assets) series
that has a Pearson correlation of only **0.175** with Schwab's ground truth NNA over
the same period (May 2024 - May 2025). The total gap is **-$119.8M** (we underreport
relative to Schwab by $120M cumulative over 13 months).

A parameter grid search across 24 ACAT in-kind detection combos
(ONBOARDING_DAYS x BURST_THRESHOLD) was executed on 2026-03-05. The critical finding:
**ACAT adjustment adds $12-22M but does not move Pearson r above the no-ACAT baseline.**
The correlation plateau at 0.175 indicates the remaining variance is driven by factors
outside the ACAT detection scope.

The question is no longer just "which ACAT parameters are optimal" but
"what explanatory levers beyond ACAT close the correlation gap with Schwab?"

---

## 2. Objective

Identify, test, and implement the parameter configuration and explanatory adjustments
to `05_build_client_performance.py` that **maximize correlation** between our monthly
NNA series and Schwab's 13-month ground truth. Target: Pearson r >= 0.50, sign
agreement >= 10/13 months.

---

## 3. Scope

### 3.1 In Scope

1. **ACAT parameter finalization** -- Complete DS analysis of v2 grid results
   (S3 output exists at `s3://opal-data-bd/diagnostics/acat_param_grid_results.csv`).
   Select optimal ONBOARDING_DAYS and BURST_THRESHOLD. Even though ACAT alone doesn't
   move correlation, the adjustment is materially correct ($46M gap closure from Phase 3
   analysis) and should be integrated.

2. **Gap decomposition** -- Identify what explains the -$120M 13-month gap. Candidate
   explanatory variables:
   - **JNL/sweep exclusion calibration** -- Are we excluding too many journal entries
     that Schwab counts as NNA?
   - **Velocity cap tuning** -- 90-day rolling window, max 1.0x trailing AUA. Is this
     cap suppressing legitimate large inflows?
   - **AUA-based outflow cap** -- Daily outflows capped at prior-day AUA. Is this
     creating artificial floors?
   - **Transaction deduplication aggressiveness** -- Composite key dedup may be
     removing non-duplicate transactions with similar metadata
   - **Account coverage** -- 43 BD accounts not in our accounts_dimension ($9.1M).
     Are there more?
   - **Timing misalignment** -- Settlement date vs posting date differences between
     our model and Schwab

3. **Diagnostic framework** -- Build a decomposition script that attributes the
   monthly gap to specific filter categories (ACAT, JNL exclusion, velocity cap,
   outflow cap, dedup, coverage, residual).

4. **Production implementation** -- Modify script 05 to integrate the winning
   parameter set and any filter adjustments that improve correlation.

5. **Full gold layer rebuild** -- Required after script 05 changes (historical ACAT
   backfill + adjusted filters).

### 3.2 Out of Scope

- AUA variance analysis (separate project: ADVI_AUAVAR)
- Portal UI changes (NNA display is downstream and unchanged)
- Script 09/10 modifications (they consume script 05 output automatically)
- Schwab API integration (no new data feeds)

---

## 4. Prior Work (State of Play)

| Artifact | Status | Location |
|----------|--------|----------|
| ACAT v3 diagnostic (30d/3-burst) | COMPLETE | `s3://opal-data-bd/diagnostics/acat_scan_v3_output.txt` |
| ACAT Phase 3 analysis | COMPLETE | DS log `acat_inkind_phase3_analysis_and_design.md` |
| Param grid v2 (24 combos) | EXECUTED, ANALYSIS PENDING | `s3://opal-data-bd/diagnostics/acat_param_grid_results.csv` |
| Correlation summary script | WRITTEN, NOT YET RUN | `data/black_diamond/scripts/diagnostics/diag_acat_correlation_summary.py` |
| Production design brief | NOT YET WRITTEN | Planned: `docs/briefs/data-scientist-acat-inkind-nna-production-design.md` |

**Key numbers from v2 grid (DT log 2026-03-05):**
- Baseline (no ACAT): Pearson r = 0.175, TotalGap = -$119.8M
- Best ACAT combo (7-21 day windows): Pearson r = 0.175, TotalGap = -$119.8M
- 60-day window: Pearson r = 0.083 (worse -- overcaptures false positives)
- ACAT estimates: $12-22M for 7-21 day combos

---

## 5. Agents & Responsibilities

| Agent | Role in This Project |
|-------|---------------------|
| 0.4.0_DS_ClientPlatform | Analysis, gap decomposition, script modifications, DT briefs |
| 0.4.0_DT_ClientPlatform | EC2 execution of diagnostics, S3 artifact management, gold layer rebuild |
| 0.6.0_AE_PartnerETL | BD pipeline owner -- consulted if pipeline/data feed changes needed |

---

## 6. Deliverables

1. **Gap decomposition report** -- DS analysis attributing -$120M gap to specific
   filter categories with monthly granularity
2. **Recommended parameter set** -- ACAT params + any filter adjustments, with
   before/after correlation metrics
3. **Modified `05_build_client_performance.py`** -- Production-ready with new
   parameters integrated
4. **DT execution briefs** -- For each EC2 diagnostic run and the final rebuild
5. **Post-implementation validation** -- Pearson r and sign agreement computed on
   the rebuilt gold layer vs Schwab ground truth

---

## 7. Success Criteria

| Metric | Current | Target |
|--------|---------|--------|
| Pearson r (13-month NNA vs Schwab) | 0.175 | >= 0.50 |
| Sign agreement (months directionally correct) | ~6/13 (46%) | >= 10/13 (77%) |
| Total 13-month gap magnitude | $119.8M | < $50M |
| Jan 2025 overshoot | $72.6M | < $30M |

---

## 8. Risks

| Risk | Mitigation |
|------|-----------|
| Correlation ceiling -- our model's data sources may structurally limit achievable r | Decomposition report will quantify ceiling; if structural, document and accept |
| Loosening filters improves NNA correlation but degrades data quality | Multi-metric evaluation: Pearson r + sign agreement + MAE. No single-metric optimization |
| Full rebuild disrupts nightly pipeline | Schedule rebuild during maintenance window; incremental mode resumes after |

---

## 9. Data Architecture

No new data feeds, tables, or Lambda functions. This project modifies parameters
and filter logic within `05_build_client_performance.py`. Downstream scripts (09, 10)
consume the output automatically. The ACAT inflow rows will be labeled `ACAT_INKIND`
in the flows DataFrame for auditability.

**Schwab ground truth (hardcoded in diagnostics):**
13-month NNA from May 2024 - May 2025, exact figures from `REQ_schwab_sot_cross_reference.md`.
