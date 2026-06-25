<to_id>ETFS_AVGCAP.W1</to_id>
<project>ETFS_AVGCAP</project>
<title>ETFS_AVGCAP W1 (P1, DS) -- averaging methodology + Inflection leg (provable-now) + bd<->Schwab-RPS account-level recon</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<consult>0.7.0_AE_CloudOps (ETFS_SETUP-W1 daily-slice contract -- AVGCAP reads it)</consult>
<verify>3.0.0_SA_CVO</verify>
<issued_by>2.0.0_SA_COO (ETFS_AVGCAP decomposition; CTO-GO + Andrew-direct 2026-06-23; PRD docs/architecture/ETFS_AVGCAP.md, 8 Andrew-decisions resolved)</issued_by>
<issued_date>2026-06-23</issued_date>
<status>complete</status>
<!-- GATED on ETFS_SETUP-W1's Inflection producer (daily slice live + daily-artifact contract). DATA-ONLY (no DE/portal, D8). DS-compute lane; CVO verifies. P2 (49F)/P3 (Cottonwood) = phased follow-ons gated on their blockers (below) -- charter'd when those clear. No-rush (full 3-partner June ~early-July); methodology + Inflection leg start as soon as SETUP-W1's slice is live. -->
<!-- COMPLETE 2026-06-25 (COO flip, ETFS TO-status convention; CVO cert-PASS + DS served-artifact RAVC2): AC#1 methodology (avgcap_monthly_average.py 116c84ed7, cert) + AC#2 served (opal-data-etfs/monthly/2026-05.json $24.29M + 2026-06.json $76.21M, inflection-only, CVO-cert-matched-to-cent, scope-corrected off auto-discovery widen) + AC#3 bd<->RPS recon (daeddb41a, reproduces PRD anchor $529.9M/$508.6M/-4.02% exactly). Served = real completion gate met. FOLLOW-ONS (separate, NOT this W1): Cottonwood AVGCAP rollup (cot June-only, needs own cert) + inf-gold reprice (queued DS, window 06-18..06-23). -->

<objective>
Build the ETFS_AVGCAP averaging methodology + the FIRST partner leg (Inflection, provable-now) per the PRD (docs/architecture/ETFS_AVGCAP.md, all 8 Andrew-decisions resolved). DATA-ONLY (ETF business, no model-portfolio/DE lane). Reads the ETFS_SETUP daily ETF-ownership slices (opal-data-etfs/{partner}/{date}.json), computes monthly-average ETF ownership per partner + the bd<->Schwab-RPS account-level reconciliation.
</objective>

<the_work>
P1 (THIS TO):
1. AVERAGING METHODOLOGY: monthly-average ETF ownership per the PRD (avg of the daily slices over the month, per ETF per partner). Implement on the SETUP-W1 daily contract. Clock 05-15 (per SETUP-W1) -> May = partial-month, June = MTD.
2. INFLECTION LEG: compute Inflection's monthly-avg from its live daily slice (opal-data-etfs/inflection/{date}.json). Provable-NOW (Inflection live-daily). May-partial (05-15..) + June-MTD = the acceptance artifacts.
3. bd<->Schwab-RPS ACCOUNT-LEVEL RECON per the PRD (reconcile account-level ETF ownership bd-vs-Schwab-RPS at account grain).
DATA-ONLY: gold/etfs compute; no portal/DE. CVO verifies methodology + Inflection-leg numbers + recon.
</the_work>

<dependencies_blockers>
- GATE: ETFS_SETUP-W1's Inflection daily producer LIVE + writing the slice (the substrate). Don't start the compute until the slice is live (AE signals). [SETUP-W1 is now active, scope-corrected to REUSE the existing opal-data-etfs bucket.]
- P2 (49F via silver/RPS) = phased follow-on (ETFS_AVGCAP.W2), BLOCKED on B1 (49F silver/RPS EMPTY -> needs /49-schwab-conv = ETFS_SETUP-W2) + B2 (49F Schwab = manual monthly batch, latest raw 06-09, next ~early-July). Charter'd when SETUP-W2 lands + the next Schwab batch arrives.
- P3 (Cottonwood) = phased follow-on (ETFS_AVGCAP.W3), post-COTETL (B3: COTETL freeze fixed 06-22, now unblocked). Charter'd post-COTETL-stable.
- CRITICAL PATH: SETUP-W1 (Inflection producer) -> THIS (AVGCAP-W1). Full 3-partner June converges ~early-July (no rush).
</dependencies_blockers>

<compiler_tools_mandate>
comp-which-first for every search/inspection; ds-commit-gate (py_compile + ds-precommit-check + ruff FA; from __future__ import annotations); firm-sep (etfs compute reads opal-data-etfs ONLY per the SETUP-W1 write-out model -- zero firm-bucket grants). verify-on-served.
</compiler_tools_mandate>

<acceptance_criteria>
1. Averaging methodology implemented + documented (monthly-avg per ETF per partner, on the SETUP-W1 daily contract).
2. Inflection leg: monthly-avg from the live daily slice; May-partial (05-15..) + June-MTD artifacts; numbers sane (Inflection ~$82M-area ETF ownership); CVO-verified.
3. bd<->Schwab-RPS account-level recon per the PRD; CVO-verified.
4. DATA-ONLY (no DE/portal); firm-sep (opal-data-etfs read-only); ds-commit-gate PASS.
5. RAVC2 COO + CVO; CVO verifies each piece. P2/P3 remain phased-gated (B1/B2 + B3) -- not started under this TO.
</acceptance_criteria>
