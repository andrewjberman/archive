<to_id>DATA_PLATFORM.DC-CHAR</to_id>
<project>DATA_PLATFORM</project>
<title>Phase-1-DEEP DC-CHAR -- own-account API-quality characterization (the partner-quality signal; Option-B)</title>
<assigned_to>per-vendor: 0.4.0_DS_ClientPlatform (BD/Orion/Eclipse, supplant-side) + 0.6.0_AE_PartnerETL (SmartX, leverage-side)</assigned_to>
<verify>3.0.0_SA_CVO (ROE-compliance + the evidence-schema grounding)</verify>
<arch_gate>1.0.0_SA_CTO (folds into PRD S6b; partner-scoring synthesis)</arch_gate>
<issued_by>2.0.0_SA_COO (CTO methodology-expansion routing 145443Z; Andrew-ratified Recon ROE)</issued_by>
<issued_date>2026-06-24</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project DATA_PLATFORM, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: queued</status>
<!-- QUEUED behind the critical path (DC0 + DC-REV anchor + the per-vendor crawls). Rides own-account access; per-vendor owners pick up alongside their crawl/leverage work. -->
<roe>MANDATORY: complies with docs/architecture/DATA_PLATFORM_RECON_ROE.md -- OPTION-B (active own-account, within the 4 constraints: our data only / available+authorized endpoints only / read never scan / POLITE conservative-rate-limit + back-off). The forbidden tier (fuzzing/brute-force/auth-testing/out-of-account) is HARD-EXCLUDED.</roe>

<objective>
Characterize each vendor's API QUALITY via OWN-ACCOUNT behavior -- the partner-quality signal feeding the 6-dim partner-scoring (API-maturity + operational-maturity dims). For SUPPLANT vendors = "how-expensive-to-work-around"; for the SmartX LEVERAGE = the integration-depth signal.
</objective>

<the_work>
Per-vendor own-account characterization (within the ROE): pagination/cursor semantics, rate-limit behavior (observed, polite), schema-consistency, data-lag/freshness, export-completeness, UI-vs-export parity, identifier-stability. Apply the RECON-RIGOR evidence-schema (Observation/Evidence/Inference/CONFIDENCE/ALTERNATIVE/Business-significance). Rides the existing authenticated own-account sessions (no new scopes).
</the_work>

<acceptance_criteria>
1. Per-vendor API-quality characterization (BD/Orion/Eclipse via DS; SmartX via 0.6.0), evidence-schema-grounded.
2. Feeds the 6-dim partner-scoring (API-maturity + operational-maturity) -> the LEVERAGE headline + the SUPPLANT cost-to-work-around.
3. ROE-compliant: Option-B within the 4 constraints (CVO verifies -- our-data-only, authorized-endpoints, read-not-scan, polite).
4. RAVC2 COO + CTO; folds into the DC-REV/DC-LEV synthesis.
</acceptance_criteria>
