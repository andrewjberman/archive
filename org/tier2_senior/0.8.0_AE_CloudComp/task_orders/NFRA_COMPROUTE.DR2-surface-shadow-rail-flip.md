# TASK ORDER -- NFRA_COMPROUTE.DR2 (SURFACE restructure + SHADOW harness + 2-tier RAIL + the FLIP)

<issued_to>0.8.0_AE_CloudComp~C</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>dispatched</status>
<priority>HIGH -- Andrew-direct default-router promotion. CTO design BLESSED (132556Z). You own the surface + the shadow harness + the flip -- the SEV1 gate lives here.</priority>
<date>2026-07-01</date>

## Context
Making comp_route the DEFAULT router (Andrew-direct). comp-which is LIVE + enforcing = SEV1 -- the flip from backstop->default must be shadow-proven zero-regression first. You own the comp-which surface, the shadow harness, and (per your design input, ACCEPTED) execute the flip on CVO~B's shadow-green cert. Design authority: CTO 132556Z. Your DR2 pairs with ~E's engine (DR1) + ~B's mode-tags (DR3).

## Objective
Restructure comp-which to feed the default router, build the shadow harness that proves zero-regression, add the 2-tier intent rail, and execute the flip ONLY on CVO~B's shadow-green cert.

## Scope (CTO-blessed)
1. **Surface restructure:** the vetted curated / surface-first / fuzzy layers become SignalExtractors {cap_id, confidence, vetted} FEEDING comp_route (Stage B), NOT returning gates. comp-which's default path becomes comp_route (the 3-stage engine), with the confidence/fallback threshold surfaced. Interface LOCKED with ~E (DR1).
2. **SHADOW harness (the SEV1 safety):** run the new primary-router in PARALLEL with today's backstop; log BOTH to the routing.jsonl flywheel sink; prove ZERO regression on the FULL fixture (34 self + 3 audit + 20 paraphrase + 3 posterior) + the E1 read-never-rebuilds property + a measured fallback-rate. Same discipline as ~E's affinity shadow. NO flip before shadow-GREEN.
3. **2-TIER intent rail (COMPRAIL rescope):** Tier-1 = cheap syntactic at the PreToolUse hook (~90%): repo grep/find/rg + aws describe|list|get-INSPECTION = NAVIGATE -> route; python/terraform/git/pytest/npm/bun/docker/make = COMPUTE -> FREE. Tier-2 = ambiguous tail (cat|grep pipes, novel verbs) -> defer to the router to classify (bounded). The rail-log (yours) MEASURES classification accuracy (navigation-classified -> useful route? compute-classified -> actually ran?) for OUTCOME-anchored (Goodhart-safe) tuning.
4. **THE FLIP (HARD-gated):** flip comp-which backstop->DEFAULT ONLY on CVO~B's shadow-green cert (DRV). This TO's flip phase does NOT land until that cert exists. shadow-GREEN-before-flip is the HARD acceptance gate (CTO: non-negotiable, SEV1).

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>comp-surface-check (comp-which is a critical surface) + confirm the routing.jsonl flywheel sink + the frozen fixture + LOCK the SignalExtractor interface with ~E</run>
    <expect>Surface baseline captured; the flywheel sink + fixture exist; interface locked.</expect>
    <if_mismatch>STOP. If the interface isn't locked with ~E, resolve before building (the engine + surface must agree on the score-signature).</if_mismatch></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>shadow run: primary-router vs backstop over the full fixture -> routing.jsonl; assert ZERO regression + read-never-rebuilds + fallback-rate; rail 2-tier classification self-test (a grep -> route, a python -> free); comp-surface-check + ds-gate + non-ASCII</run>
    <expect>Shadow logs both; 0 regression on 34+3+20+3; read-never-rebuilds holds; rail classifies navigation vs compute correctly; surface-check clean.</expect>
    <if_mismatch>STOP. Any shadow regression = do NOT proceed to the flip; reconcile with ~E + CVO~B.</if_mismatch></step>
  </phase>
  <phase id="3" when="after commit / FLIP">
    <step><run>on CVO~B's shadow-green cert (DRV): flip comp-which default->comp_route; re-run the fixture LIVE post-flip; comp-surface-check</run>
    <expect>Flip lands ONLY post-cert; live post-flip fixture GREEN; surface-check clean; the router is now DEFAULT.</expect>
    <if_mismatch>ROLL BACK the flip immediately + escalate to COO~B/CVO~B. A live regression on the SEV1 surface is a rollback, not a fix-forward.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 0.8.0_AE_CloudComp~E: owns the engine (DR1); LOCK the SignalExtractor/score interface.
- 0.8.0_AE_CloudComp~B: provides mode:query|rebuild tags (DR3); coordinate the comp-which mode-tag integration.
- 3.0.0_SA_CVO~B: the shadow-green CERT (DRV) HARD-gates your flip. Give her the shadow output (fixture-result + read-never-rebuilds + fallback-rate) for her independent verify. Her GREEN authorizes the flip.
- 1.0.0_SA_CTO: design authority (132556Z). RAVC.
</cross_domain_coordination>

<acceptance_criteria>
1. comp-which restructured: vetted layers -> SignalExtractors feeding comp_route; confidence/fallback threshold surfaced; interface locked with ~E.
2. Shadow harness proves ZERO regression on the full fixture (34+3+20+3) + read-never-rebuilds + measured fallback-rate, logged to routing.jsonl.
3. 2-tier rail live: Tier-1 syntactic (navigation->route, compute->free) + Tier-2 router tail; rail-log measures classification accuracy.
4. THE FLIP lands ONLY on CVO~B's shadow-green cert (DRV); live post-flip fixture GREEN; comp-surface-check clean. RAVC COO~B + CC CTO + ~E + CVO~B.
</acceptance_criteria>

## Note
You hold the SEV1 gate. Shadow-GREEN-before-flip is HARD -- never flip comp-which on a self-report; CVO~B's independent cert is the authorization. Andrew's "shell/compute free, navigation/read routed" IS the 2-tier rail.
