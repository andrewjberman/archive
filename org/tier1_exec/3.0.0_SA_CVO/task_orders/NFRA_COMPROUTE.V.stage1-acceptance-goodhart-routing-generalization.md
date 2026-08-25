# TASK ORDER — NFRA_COMPROUTE.V (Stage-1 Acceptance)

<issued_to>3.0.0_SA_CVO~B</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_COMPROUTE is complete; this TO was last touched 2026-07-07, predating the project close 2026-07-19. Closed as a record act, not a work verdict. Prior status: staged</status>
<priority>HIGH — Andrew-direct close-out drive (2026-07-01). COMPROUTE Stage-1 build COMPLETE (L1/L2/L3/L4 landed): provider 3277cc38a + engine 9cc595998 + comp-which integration 442633124. This V is the LAST gate -> COMPROUTE Stage-1 closes. SEQUENCE behind the Phase-B landing + COMPLEARN honesty on your slate.</priority>
<date>2026-07-01</date>

## Context
NFRA_COMPROUTE Stage-1 (the DECIDES verb) build is done: the capability-map-agnostic posterior engine is LIVE in comp-which. PRD: `docs/architecture/NFRA_COMPROUTE_PRD.md` §9 (Acceptance/exit). This is the independent acceptance that closes COMPROUTE Stage-1.

## Objective
Independently ACCEPT (or REWORK) COMPROUTE Stage-1 against the PRD §9 exit criteria. Ground against the LIVE comp-which surface + the landed engine/provider, never the lanes' self-report.

## Scope — V (the 4 §9 criteria)
1. **Goodhart-honesty (§9a):** every routing-rule/weight is value-anchored -- the scorer uses OUTCOME-weighted history_affinity (comp_route.outcome_value), never usage-count. No usage-Goodhart. (Same anchor CTO ratified on COMPLEARN + COMPROUTE ruling 4.)
2. **Routing-quality ground-truth (§9b):** the 2 grounded failure modes resolve at the LIVE surface -- (A) comp-cluster->comp-transform within-margin surfaces BOTH with concern; (B) comp-drift->comp-aws same-surface resolved by likelihood+margin. A margin-disambiguation demonstrably reduces mis-route for that intent.
3. **Generalization interface real (§9c):** the Stage-1 engine is provider-AGNOSTIC -- a 2nd capability-map provider slots in with ZERO engine change. (PRE-SATISFIED evidence: ~E ran the UNCHANGED engine against ~C's real 49-cap provider + the SmokeCapabilityMapProvider; verify it independently.)
4. **Four-way separation holds (§9d):** COMPROUTE reads the map (COMPUNIFY) + the signal (COMPLEARN), is fired by COMPRAIL, never re-implements MAPS/TRAINS/FIRES.
Plus: the comp-which integration did NOT regress the LIVE enforcing rail (never-dead-end + telemetry + gate) -- the load-bearing no-regression.

<compiler_tools_mandate>
  <phase id="1" when="verify">
    <step>
      <run>comp-which on the 2 grounded failure-mode intents live + read comp_route.py (9cc595998) scorer + the L4 comp-which integration (442633124) + the smoke-provider run</run>
      <expect>(A)+(B) resolve live with never-silent-argmax; scorer is outcome-weighted (grep-clean of usage-as-value); the engine routes a 2nd provider unchanged (§9c); comp-which rail behavior unregressed (34/34 + telemetry + enforcement).</expect>
      <if_mismatch>REWORK: cite the specific §9 criterion + the failing evidence back to ~C (integration) / ~E (engine).</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 0.8.0_AE_CloudComp~C (L2 provider + L4 integration) + ~E (L3 engine): REWORK routes to the owning lane.
- 1.0.0_SA_CTO: ratified rulings 2/3/4 on the build; CC on the V verdict.
- NFRA_COMPUNIFY (CLOSED, the map) + NFRA_COMPLEARN (the signal) + NFRA_COMPRAIL (the surface): the four-way separation subjects.
</cross_domain_coordination>

<acceptance_criteria>
1. All 4 §9 criteria independently verified GREEN against the LIVE comp-which surface (Goodhart-honesty / routing-quality / generalization-real / four-way separation) + no rail regression.
2. RAVC verdict (ACCEPT -> COMPROUTE Stage-1 closes / REWORK with cited criterion). Ground on the live artifact + sharp test, not self-report. Could-not-verify is a finding. RAVC COO~B + CC CTO + ~C + ~E.
</acceptance_criteria>

## Note
The COMPROUTE Stage-1 close-gate. Stages 2-3 (skills/MCP/docs + agent-lane dispatch as new providers) = the roadmap, unblocked by the §3 interface being real (which this V confirms). On your ACCEPT I 2-step close COMPROUTE (Stage-1 scope).
