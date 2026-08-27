<to_id>DATA_PLATFORM.D6</to_id>
<project>DATA_PLATFORM</project>
<title>D6 MDPF + ADVI input archetype (Phase-3 lead-in) -- the canonical model-feed + advisor-portal input contract</title>
<assigned_to>0.4.0_DS_ClientPlatform (DS, CTO-LED)</assigned_to>
<consult>1.0.0_SA_CTO (architecture lead + gate)</consult>
<verify>3.0.0_SA_CVO (reconcile-verify spec vs the live MDPF/ADVI shapes)</verify>
<issued_by>2.0.0_SA_COO (DATA_PLATFORM Phase-1 decomposition; Andrew-direct via CTO 2026-06-23; PRD S6/S11; LD-0209)</issued_by>
<issued_date>2026-06-24</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project DATA_PLATFORM, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: gated</status>
<!-- GATED on D5 (which is gated on D1-D4): the input archetype generalizes off the unified shape. Do NOT start until D5 lands. CTO architecture-LEADS + GATES. SPEC/AUDIT (Phase-3 lead-in), NOT a build. -->

<objective>
Produce the MDPF + ADVI input archetype -- the canonical input contract for the model-feed (MDPF) + the advisor portal (ADVI), generalized off inf's reference shape, so downstream consumers have one stable contract regardless of custodian. SPEC-OF-RECORD: PRD S6 row D6. CTO architecture-leads.
</objective>

<the_work>
The canonical input contract for: (a) the model-feed (MDPF) -- generalized off the MDPF convergent-feeder contract; (b) the advisor portal (ADVI) -- generalized off the ADVI platinum per-drill-level shape. One archetype that any custodian's unified-shape output (D5) feeds. Seeds: the MDPF convergent-feeder contract + the ADVI platinum per-drill-level shape.
</the_work>

<acceptance_criteria>
1. The canonical input-archetype spec: the model-feed (MDPF) input contract + the advisor-portal (ADVI) input contract, one generalized archetype.
2. Shown to consume the D5 unified-shape output (custodian-agnostic).
3. CTO architecture-gates; CVO reconcile-verifies vs the live MDPF/ADVI shapes.
4. SPEC only -- no build. GATED on D5. RAVC2 COO + CTO.
</acceptance_criteria>
