This is an ADVI_NNAVAR-001 gap decomposition alignment thread between DS and DT.

Context: The ACAT param grid v2 (24 combos, ONBOARDING_DAYS x BURST_THRESHOLD) was executed on 2026-03-05. Critical finding: ALL ACAT combos return Pearson r = 0.175 -- identical to the no-ACAT baseline. ACAT adds $12-22M gap closure but does NOT improve correlation. The remaining -$119.8M 13-month gap vs Schwab is driven by factors OUTSIDE the ACAT scope.

The NNAVAR PRD identifies candidate explanatory variables: JNL/sweep exclusion calibration, velocity cap tuning (90-day/1.0x AUA), AUA-based outflow cap, transaction deduplication aggressiveness, account coverage gaps (43 accounts = $9.1M), timing misalignment.

Note: The JNL/sweep exclusion fix was ALREADY committed to script 05 + 05b (canonical_nna_logic.md session, 2026-03-05). It is committed but NOT yet rebuilt into gold layer (awaiting CEO go/no-go). This is NOT in the NNAVAR PRD prior art table -- DS should be aware of it.

DS is the knowledge source: they know the script logic, the filter parameters, and what diagnostic framework is needed. DT is the execution source: they know EC2 feasibility, runtime estimates, and S3 artifact management.

Purpose of this thread:
1. DS proposes the gap decomposition diagnostic framework (which filters to test, in what order)
2. DS recommends optimal ACAT params from the v2 grid (even though ACAT alone doesn't move r)
3. DT confirms EC2 feasibility and execution sequence for each proposed diagnostic
4. Thread receipt = agreed diagnostic plan that COO will convert to DS+DT task orders

Deliverable: DS closes with a concrete decomposition plan block: which diagnostics to run, what each measures, expected EC2 runtime, and the recommended ACAT params. DT confirms or adjusts the execution plan.
