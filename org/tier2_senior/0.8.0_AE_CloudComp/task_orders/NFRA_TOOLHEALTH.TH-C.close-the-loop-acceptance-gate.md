# TASK ORDER -- NFRA_TOOLHEALTH.TH-C (close the inert loop: make the health view ACT, not display)

<issued_to>0.8.0_AE_CloudComp</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_TOOLHEALTH, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>

<priority>HIGH -- the load-bearing part (deliverable c). Today the loop is ACCUMULATES-BUT-INERT (COMPLEARN D1); TH-C makes it DRIVE decisions. GATED on TH-A + TH-B + COMPPROOF-D1. PRD SS4 + acceptance SS6.4.</priority>
<date>2026-07-02</date>

## Context
Today the learning loop is `ACCUMULATES-BUT-INERT` (COMPLEARN D1): data collected + queryable, not autonomously consumed-and-improved. A health view that merely DISPLAYS verdicts changes nothing. TH-C's job is to make the fused health verdict DRIVE the retire/fix/promote/surface decisions into COMPLEARN's consume side + the CTO commission path -- and to be VERIFIABLE as acting (COMPPROOF-D1 cross-check that a health-verdict-driven change demonstrably altered behavior on a later cycle). If the loop stays inert, TOOLHEALTH's acceptance is NOT met.

## Objective
Wire the TH-B health verdict into action: FIX -> a fix TO candidate; PROMOTE -> a COMPROUTE routing-rule/HUD change candidate; RETIRE -> a deprecation candidate the CTO ratifies. Prove the loop ACTS via the COMPPROOF-D1 autonomy cross-check.

## Scope
1. **Verdict -> action wiring (advisory, CTO-ratified -- SS5.3):** each verdict class maps to a candidate action fed into COMPLEARN's worklist consume side + the CTO commission path. NEVER a self-rewriting toolset (mirror COMPLEARN + NFRA_DEBTSCAN never-auto-delete). The health view PROPOSES; the CTO ratifies retire/fix/promote.
2. **Close-loop proof (the acceptance gate -- SS6.4):** dispatch >=1 real health-verdict-driven action (fix/promote/retire) AND have COMPPROOF-D1 (the autonomy audit) confirm it demonstrably changed routing/agent behavior on a LATER cycle. Inert = acceptance NOT met.
3. **PROMOTE -> COMPROUTE handoff:** an effective-but-ignored tool (PROMOTE) becomes a concrete COMPROUTE routing-rule/weight/HUD change proposal (not just a flag).
4. **Ground on LIVE (Rule 22):** "the loop acted" is proven by an observed behavior delta on a later cycle (D1 evidence), never asserted.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>comp-which "where is the COMPLEARN worklist consume side + the CTO commission path"; read the COMPLEARN SS3 worklist + SS4/SS5 close mechanics + the COMPPROOF-D1 autonomy-audit TO (NFRA_COMPPROOF.D1); confirm the advisory-not-auto-mutating boundary</run>
    <expect>The worklist consume surface + CTO commission path + the D1 cross-check identified; the advisory boundary (propose, never auto-mutate) confirmed.</expect>
    <if_mismatch>STOP. If the only wiring path auto-mutates the toolset, redesign to advisory-only before writing -- auto-mutation violates SS5.3.</if_mismatch></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>self-test the verdict->action wiring on >=1 verdict of each actionable class (FIX/PROMOTE/RETIRE): the health view emits a candidate action into the worklist/commission path (advisory); assert NO auto-mutation of the toolset; ds-commit-gate + non-ASCII + `from __future__ import annotations`</run>
    <expect>Each verdict class produces a candidate action routed to the correct consumer (COMPLEARN worklist / CTO commission / COMPROUTE); zero auto-mutation.</expect>
    <if_mismatch>STOP. A verdict that mutates the toolset without CTO ratification violates the advisory gate.</if_mismatch></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>dispatch >=1 real health-verdict-driven action; on a LATER cycle, have COMPPROOF-D1 confirm the action demonstrably changed routing/agent behavior (the loop ACTED)</run>
    <expect>D1 autonomy audit records a real behavior delta attributable to the health-verdict-driven action -- the loop ACTS, not merely displays. Grounded on live D1 artifacts (Rule 22).</expect>
    <if_mismatch>If D1 shows no behavior delta, the loop is still inert -- TH-C acceptance is NOT met; iterate the wiring, do NOT close.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- COMPLEARN owner: the worklist consume side is COMPLEARN's. TH-C FEEDS it advisory candidates; it does not fork the worklist or auto-mutate.
- 1.0.0_SA_CTO: owns the commission path (ratifies retire/fix/promote). Every actionable verdict routes to CTO ratification -- advisory-only.
- NFRA_COMPPROOF-D1 (autonomy audit): the cross-check that the loop ACTED. TH-C's close-loop proof DEPENDS on D1 confirming a behavior delta. Coordinate the D1 evidence handshake.
- NFRA_COMPROUTE: receives PROMOTE-verdict routing/HUD change proposals.
- 3.0.0_SA_CVO~B (TH-V): verifies the close-loop proof is real (a genuine behavior delta, not a claimed one).
</cross_domain_coordination>

<acceptance_criteria>
1. Each verdict class (FIX/PROMOTE/RETIRE) wires to a candidate action in COMPLEARN's worklist consume side + the CTO commission path -- advisory, never auto-mutating (grep-proof: no toolset self-rewrite).
2. >=1 health-verdict-driven action is dispatched AND COMPPROOF-D1 confirms it demonstrably changed routing/agent behavior on a later cycle (PRD SS6.4 close-loop proven).
3. PROMOTE verdicts produce concrete COMPROUTE routing-rule/HUD change proposals (not bare flags).
4. Ground on LIVE D1 evidence (Rule 22). Session-log Compiler Tools reproduces every `<run>`. RAVC COO~B + CC CTO + CVO~B.
</acceptance_criteria>

## Note
This is the deliverable that separates "a dashboard" from "a closed learning loop." The acceptance bar is BEHAVIORAL (D1 confirms a real delta), not display. Advisory-only: the health view proposes, the CTO ratifies -- never a self-rewriting toolset. GATED on TH-A + TH-B + COMPPROOF-D1; do NOT start until COO~B fires the GO.
