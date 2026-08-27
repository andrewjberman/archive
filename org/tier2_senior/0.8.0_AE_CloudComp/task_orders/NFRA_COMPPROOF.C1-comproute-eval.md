# TASK ORDER -- NFRA_COMPPROOF.C1 (COMPROUTE efficacy eval: does DECIDES route well?)

<issued_to>0.8.0_AE_CloudComp~E</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_COMPPROOF is complete; this TO was last touched 2026-07-01, predating the project close 2026-07-07. Closed as a record act, not a work verdict. Prior status: HELD -- sequenced AFTER the default-router SHADOW-FLIP (else C evals a superseded backstop). Do NOT start until comp-which flips to the DEFAULT router (DR2 flip on CVO~B's cert).</status>
<priority>MEDIUM-HIGH -- C is a program workstream; sequences after the default-router lands. PRD SS2-C/SS6.</priority>
<date>2026-07-01</date>

## Context
COMPPROOF-C: does the DECIDES peer (COMPROUTE) actually route well? You own the posterior; you build the eval. CRITICAL SEQUENCING: C evaluates the just-shipped DEFAULT router (the DR1-DRV increment), so it runs AFTER the shadow-flip -- evaluating the superseded grep-tail backstop would measure the wrong thing. HELD until the flip lands.

## Objective
An efficacy verdict -- routes-well / needs-tuning / structurally-short -- with precision@1 + recall on a labeled intent-set, under a CVO honesty-gate.

## Scope
1. **Labeled intent-set:** from B's incidents (TO-B1 symptoms -> the correct lens/tool) + LIVE `comp-which-rail.log` + `agent_telemetry/*.jsonl`. Label the correct capability per intent.
2. **Metrics:** precision@1 + recall of the top pick vs the correct lens; margin-gate calibration (does it abstain/disambiguate when it should?); cold-start behavior; the 2 named PRD failure modes.
3. **CVO HONESTY-GATE (the Goodhart guard):** the eval must NOT be graded on data the router was FIT on (the fixture/curated set). CVO signs that the labeled set is held-out / independent. A precision number on training data is void.
4. **Verdict:** routes-well / needs-tuning / structurally-short, grounded.

<compiler_tools_mandate>
  <phase id="1" when="before build">
    <step><run>confirm the default-router is FLIPPED (comp-which default = comp_route, not the backstop) + the labeled set is HELD-OUT from the router's fit data (CVO honesty-gate pre-check)</run>
    <expect>The eval targets the LIVE default router; the labeled intent-set is independent of the fixture/curated fit.</expect>
    <if_mismatch>STOP. If the flip hasn't landed, HOLD (don't eval the backstop). If the label set overlaps the fit data, re-draw it (CVO gate).</if_mismatch></step>
  </phase>
  <phase id="2" when="eval">
    <step><run>precision@1 + recall + margin-gate + cold-start + 2 failure-modes on the held-out labeled set; CVO honesty-gate sign-off</run>
    <expect>Metrics on independent data; CVO signs the honesty-gate; explicit verdict.</expect>
    <if_mismatch>An un-signed honesty-gate = the eval is not accepted (could be Goodhart-fit).</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 3.0.0_SA_CVO / CVO~B: the HONESTY-GATE (held-out data, not fit-on). Their sign-off is required.
- TO-B1 (~D): B's incidents seed the labeled intent-set.
- 2.0.0_SA_COO~B: I signal you the moment the default-router flips (unblocks C).
- 1.0.0_SA_CTO: PRD failure-modes + CC.
</cross_domain_coordination>

<acceptance_criteria>
1. precision@1 + recall on a HELD-OUT labeled set (CVO honesty-gate signed -- NOT graded on fit data); margin-gate + cold-start + 2 failure-modes characterized.
2. Evaluates the LIVE DEFAULT router (post-flip), not the backstop.
3. Explicit verdict (routes-well / needs-tuning / structurally-short). RAVC COO~B + CC CTO + CVO.
</acceptance_criteria>

## Note
HELD until the default-router flip. The CVO honesty-gate (held-out, not fit-on) is the whole validity of C -- a precision number on training data proves nothing.
