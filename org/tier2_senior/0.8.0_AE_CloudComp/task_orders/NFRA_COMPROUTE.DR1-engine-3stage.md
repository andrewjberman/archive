# TASK ORDER -- NFRA_COMPROUTE.DR1 (default-router ENGINE: the 3-stage route())

<issued_to>0.8.0_AE_CloudComp~E</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_COMPROUTE is complete; this TO was last touched 2026-07-01, predating the project close 2026-07-19. Closed as a record act, not a work verdict. Prior status: dispatched</status>
<priority>HIGH -- Andrew-direct default-router promotion. CTO design BLESSED (ruling 132556Z). You own the engine; this is the core of the increment.</priority>
<date>2026-07-01</date>

## Context
Andrew-direct: COMPROUTE must be the DEFAULT router (explore/navigate/read intent -> router first -> route to a READ surface, else fall back to comp-grep/glob; shell/bash compute stays FREE). Today comp_route is a fail-safe grep-tail BACKSTOP. This TO builds the engine that makes it DEFAULT + regression-safe. CTO ruling (BLESSED): the 3-stage route() + your 2 structural refinements are the load-bearing correctness guarantees. Design authority = CTO 132556Z; ~B's E1 finding (4e9f0258d) is the mode-gate anchor.

## Objective
Re-scope `comp_route.py::route()` into ONE decision, 3 stages, that is safe to run as the DEFAULT (primary) router.

## Scope (CTO-blessed 3-stage)
1. **Stage A -- MODE PRE-FILTER (E1, HARD, intent-class-conditional):** for a READ/NAVIGATE/EXPLORE intent, HARD-EXCLUDE mode:rebuild tools (comp-aws-derive etc.) from the candidate set, using the manifest's mode:query|rebuild tag (~B provides via DR3). A read intent NEVER routes to an 8-min rebuild/write op (CTO: a read routed to a write is a CATEGORY ERROR, so HARD not soft-prior). A genuine BUILD intent legitimately keeps mode:rebuild eligible.
2. **Stage B -- FOLDED POSTERIOR (structural dominance):** score over the mode-eligible set using the vetted signals (curated/surface-first/fuzzy from ~C's SignalExtractor) + query_match + surface_prior. The vetted term must DOMINATE BY CONSTRUCTION (structural, NOT a w_c tuned to pass the fixture -- CTO: fixture-tuning IS the mini-Goodhart; structural dominance makes no-regression a THEOREM). affinity (w_h) = None this increment (CTO: affinity stays in its OWN independent shadow, activates later on its own real-outcome gate -- do NOT couple).
3. **Stage C -- CONFIDENCE GATE:** route if top >= MIN_CONFIDENCE + margin; near-tie -> disambiguate (never silent-argmax, ruling-3 preserved WITHIN the mode-allowed set); below the absolute RELEVANCE FLOOR -> fall to comp-grep/comp-glob (never-dead-end; the floor is the missing piece that makes DEFAULT safe -- fixes the force-argmax-weak-match regression mode).

## Interface (LOCK with ~C)
Consume ~C's SignalExtractor {cap_id, confidence, vetted} + the mode tag (~B/DR3). Align the score-signature + SignalExtractor interface on the CTO ruling (you + ~C already locked this per your 132149Z -- confirm it holds).

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>re-confirm the frozen routing fixture (34 self + 3 audit + 20 paraphrase + 3 posterior) + your affinity-shadow harness pattern (the reuse target)</run>
    <expect>The fixture is the regression baseline; the shadow pattern is reusable for the routing shadow.</expect>
    <if_mismatch>Coordinate with ~C (owns the shadow harness in DR2) before building.</if_mismatch></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>engine self-test: full fixture GREEN in the 3-stage engine (affinity=None) + E1 read-never-rebuilds property (a read intent returns 0 mode:rebuild tools) + relevance-floor fallback (a below-floor query -> grep/glob) + no silent-argmax + ds-commit-gate + non-ASCII + from __future__ import annotations</run>
    <expect>34/34+3/3+20/20+3/3 GREEN; read-never-rebuilds holds; floor-fallback works; structural dominance (NOT tuned weights) demonstrable.</expect>
    <if_mismatch>STOP. A fixture regression or a tuned-weight (non-structural) dominance is the exact defect this must not ship.</if_mismatch></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>hand ~C the engine for the SHADOW harness (parallel primary+backstop -> routing.jsonl); confirm read-never-rebuilds + fallback-rate measurable in shadow</run>
    <expect>The engine runs in shadow alongside the backstop; the properties are measurable pre-flip.</expect>
    <if_mismatch>Fix before RAVC. The engine must be shadow-runnable (the flip gate depends on it).</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 0.8.0_AE_CloudComp~C: owns the SignalExtractor + comp-which surface + the shadow harness (DR2). LOCK the interface.
- 0.8.0_AE_CloudComp~B: provides the manifest mode:query|rebuild tags (DR3) your Stage-A reads.
- 3.0.0_SA_CVO~B: certifies the shadow-GREEN before the flip (DRV) -- your engine must expose the fixture-result + read-never-rebuilds + fallback-rate for her independent check.
- 1.0.0_SA_CTO: design authority (132556Z). RAVC.
</cross_domain_coordination>

<acceptance_criteria>
1. `route()` is the 3-stage decision (mode pre-filter -> structural-dominance posterior -> confidence/relevance-floor gate); affinity=None.
2. Full fixture (34+3+20+3) GREEN in shadow; E1 read-never-rebuilds a THEOREM (0 mode:rebuild tools returned for a read intent); relevance-floor fallback verified; no silent-argmax.
3. Structural dominance NOT fixture-tuned weights (spot-checkable). Interface locked with ~C.
4. Session log Compiler Tools reproduces every run. RAVC COO~B + CC CTO + ~C + CVO~B. Do NOT flip the router -- the flip is DR2 gated on CVO~B's shadow-green cert (DRV).
</acceptance_criteria>

## Note
The engine is the alpha. Build it in shadow; the flip is separate + CVO~B-gated. Structural dominance + relevance floor are the 2 correctness guarantees CTO ratified -- get them structural, not tuned.
