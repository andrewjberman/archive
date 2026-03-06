This is an ADVI_AUAVAR-001 AUA gap segment decomposition alignment thread between DS and DT.

Context: As of 2026-03-02, our BD gold layer reports ~$1.545B non-cash AUA while BD's own allocation snapshot shows ~$1.605B. The gap is ~$55M (3.4%). 49Financial leadership uses BD numbers as their source of truth, so understanding where this gap lives is a business priority.

Prior DS investigation (2026-03-05) established:
- Root cause: fundamental data source difference (BD = point-in-time allocation snapshot; our model = reconstructed from transactions + positions + canonical_prices)
- Known account coverage gap: 43 accounts in BD but missing from accounts_dimension = $9.1M
- Deduplication: $0 impact. Settlement/pending trades: $0 impact.
- Pricing variance: INCONCLUSIVE (BD allocations lack symbol-level data for direct comparison)
- CRITICAL: The DS Phase 1 investigation showed our model at $1.236B (2026-03-02) vs Andrew's $1.545B. This discrepancy -- $309M difference -- must be explained before any gap decomposition is meaningful. It likely reflects a different date (2026-03-02 vs a later date) or a different AUA definition (non-cash filter, relationship aggregation vs account-level, etc.).

DS is the knowledge source: they know the script logic, prior investigation findings, and what segment decomposition approach will work. DT is the execution source: they know EC2 data availability (are BD allocation snapshots for matching dates on S3?), runtime feasibility, and S3 artifact management.

Purpose of this thread:
1. DS resolves the $1.236B vs $1.545B discrepancy (by reading script 05 and phase1 script)
2. DS proposes the segment decomposition approach for the ~$55M gap (once metric is reconciled)
3. DT confirms data availability: are BD allocation snapshots available at matching dates? What parquets are accessible?
4. Thread receipt = agreed decomposition plan that COO converts to DS+DT task orders

Deliverable: DS closes with a structured block: reconciled AUA definition, segment list with proposed measurement approach, data requirements per segment, which are addressable vs explainable. DT confirms data availability and EC2 execution path.
