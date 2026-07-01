# TASK ORDER -- NFRA_COMPROUTE.DRV (the SEV1 verify-gate: shadow-GREEN cert before the flip)

<issued_to>3.0.0_SA_CVO~B</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>dispatched</status>
<priority>HIGH -- the HARD gate on the default-router flip. comp-which is LIVE + enforcing = SEV1. CTO: shadow-GREEN-before-flip is NON-NEGOTIABLE (132556Z). Your cert authorizes ~C's flip.</priority>
<date>2026-07-01</date>

## Context
Andrew-direct: COMPROUTE becomes the DEFAULT router. comp-which is LIVE/enforcing, so the flip from backstop->default is a SEV1 change -- it lands ONLY on an INDEPENDENT shadow-green cert (not ~E/~C self-report). ~E builds the 3-stage engine (DR1), ~C the surface + shadow harness + flip (DR2), ~B the mode-tags (DR3). You are the flip gate.

## Objective
Independently certify that the shadow proves ZERO regression + the safety properties BEFORE ~C flips comp-which to default. Your GREEN = the flip authorization.

## Scope (verify INDEPENDENTLY -- exercise, don't read the self-report)
1. **Full fixture GREEN:** the primary-router (affinity=None) returns the SAME routes as the backstop on the FULL fixture -- 34 self-route + 3 audit + 20 paraphrase + 3 posterior. ZERO regression. (Re-run from routing.jsonl or re-exercise.)
2. **E1 read-never-rebuilds (theorem):** a READ/navigate/explore intent returns 0 mode:rebuild tools -- spot-check across read questions (incl. the E1 repro "what lambdas read bucket X" -> a query surface, never comp-aws-derive).
3. **Relevance-floor + fallback-rate SANE:** a below-floor query falls to comp-grep/glob (never-dead-end); the measured fallback-rate is SANE -- NOT ~everything-to-grep (floor too high, router useless) NOR ~zero (floor too low, force-misroutes). Report the rate.
4. **Structural-dominance (anti-Goodhart):** the vetted term dominates BY CONSTRUCTION, NOT a w_c tuned to pass the fixture (CTO: fixture-tuning is the mini-Goodhart). Spot-check that a NON-fixture paraphrase still routes correctly (generalization, not memorization).
5. **2-tier rail classification:** spot-check navigation->route / compute->free (a grep routes, a python runs free); the rail-log measures accuracy.

<compiler_tools_mandate>
  <phase id="1" when="verify">
    <step><run>independently exercise the shadow (routing.jsonl + live re-runs): full fixture, read-never-rebuilds, fallback-rate, structural-dominance generalization, rail 2-tier</run>
    <expect>34+3+20+3 GREEN; 0 mode:rebuild on reads; sane fallback-rate; non-fixture paraphrase routes correctly; rail classifies right.</expect>
    <if_mismatch>WITHHOLD the cert. Any fixture regression / a read reaching a rebuild / a tuned-not-structural dominance / an insane fallback-rate = NOT GREEN -> route back to ~E/~C, no flip.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 0.8.0_AE_CloudComp~E (engine DR1) + ~C (surface/shadow/flip DR2): give you the shadow output; your GREEN authorizes ~C's flip (DR2 phase 3).
- 1.0.0_SA_CTO: design authority + the shadow-green-before-flip mandate (132556Z). CC on the cert.
- 2.0.0_SA_COO~B: I 2-step nothing here; on your GREEN + the flip landing + live post-flip fixture, the default-router increment closes.
</cross_domain_coordination>

<acceptance_criteria>
1. INDEPENDENT shadow-green cert (exercised, not self-report): full fixture 0-regression + E1 read-never-rebuilds + sane fallback-rate + structural-dominance-generalizes + rail 2-tier correct.
2. The cert EXPLICITLY authorizes (or withholds) ~C's flip. No flip without your GREEN.
3. Goodhart-honesty: confirm the dominance is structural (generalization), not fixture-tuned. RAVC COO~B + CC CTO.
</acceptance_criteria>

## Note
You are the SEV1 gate -- the one thing between a converged design and a live flip on the enforcing surface. Exercise it independently; a self-reported shadow-green is not a cert. Same rigor as your 8 program closes.
