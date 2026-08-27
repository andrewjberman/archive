<to_id>DATA_PLATFORM.D5</to_id>
<project>DATA_PLATFORM</project>
<title>D5 Unified data-shape / bucketing architecture (Phase-2 lead-in) -- the seam: one parameterized engine + per-custodian adapters</title>
<assigned_to>0.4.0_DS_ClientPlatform (DS, CTO-LED)</assigned_to>
<consult>1.0.0_SA_CTO (architecture lead + gate)</consult>
<verify>3.0.0_SA_CVO (reconcile-verify spec vs the 3 live firm gold trees)</verify>
<issued_by>2.0.0_SA_COO (DATA_PLATFORM Phase-1 decomposition; Andrew-direct via CTO 2026-06-23; PRD S6/S11; LD-0209)</issued_by>
<issued_date>2026-06-24</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project DATA_PLATFORM, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: gated</status>
<!-- GATED on D1-D4: the unification CONSUMES the per-custodian audits (D1 Schwab + D2 BD + D3 Orion/Eclipse + D4 SmartX). Do NOT start until D1-D4 land. CTO architecture-LEADS + GATES this leg. SPEC/AUDIT (Phase-2 lead-in), NOT a build. -->

<objective>
Produce the unified data-shape / bucketing architecture spec -- THE SEAM that lets one platform serve every custodian: one parameterized silver/gold engine downstream of silver, per-custodian bronze adapters, the platinum/firm contract promoted to first-class. SPEC-OF-RECORD: PRD S6 row D5. CTO architecture-leads.
</objective>

<the_work>
The seam, designed off the D1-D4 findings: ONE parameterized silver/gold engine downstream of silver; per-custodian BRONZE ADAPTERS (Schwab/BD/Orion/SmartX -> common shape); the platinum/firm de-facto contract promoted to a FIRST-CLASS spec; per-firm-capability declaration (OPTIONAL_INPUTS keyed off FIRM_ID). Seeds: the 3 firm gold trees + the platinum/firm de-facto contract. CONSUMES D1-D4.
</the_work>

<acceptance_criteria>
1. Unified-shape arch-spec: the parameterized engine design + the per-custodian bronze-adapter pattern.
2. The platinum/firm contract promoted to a first-class spec; per-firm-capability (OPTIONAL_INPUTS keyed off FIRM_ID) declared.
3. CTO architecture-gates the design; CVO reconcile-verifies vs the 3 live firm gold trees.
4. SPEC only -- no build. GATED on D1-D4 landing. RAVC2 COO + CTO.
</acceptance_criteria>
