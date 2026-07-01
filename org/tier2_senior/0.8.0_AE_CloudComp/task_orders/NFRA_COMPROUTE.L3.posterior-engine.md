# TASK ORDER — NFRA_COMPROUTE.L3

<issued_to>0.8.0_AE_CloudComp~E</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>pending</status>
<priority>HIGH — Andrew-direct DRIVE-NOW (2026-07-01). Stage-1 is NOT gate-lift-gated. You are the named owner of the core posterior engine. Start now against the §3 interface + a smoke-provider (parallel with ~C's L2); your Phase-B co-sign priority-interrupt still stands.</priority>
<date>2026-07-01</date>

## Context
NFRA_COMPROUTE = the fabric's intent->capability ROUTER (the DECIDES verb). PRD: `docs/architecture/NFRA_COMPROUTE_PRD.md`. Decomp map: `org/projects/NFRA_COMPROUTE/DECOMP-MAP.md`. You own the ENGINE — the systems alpha. L1 (comp-dispatch + comp-symbols) is yours + DONE; L3 is the posterior itself.

## Objective
Build the **core posterior decision engine** (PRD §2) — the scorer + margin-disambiguation gate + the two inviolable invariants + graceful cold-start — coded **§3-interface-first** against the pluggable `capability_map_provider` (from ~C's L2), NEVER the concrete comp-tool map. The engine must be provider-AGNOSTIC (this is the systems alpha, PRD §3): the same engine routes any Stage-2/3 provider unchanged.

## Scope — L3
1. **The scorer:** `score(cap) = w_q·query_match(intent, cap.keywords) + w_s·surface_prior(cap.surface, ctx) + w_h·history_affinity(cap, role, ctx)`. `ctx` = {agent role, working-set (open files / recent tools), session trajectory}. `history_affinity` reads ~E's live `tool_activity` (your COMPLEARN signal), **OUTCOME-weighted, never count** (Goodhart, CTO ruling 4).
2. **The MARGIN-DISAMBIGUATION gate (anti-silent-argmax):** top-2 s1>=s2. `(s1-s2) >= eps` -> decide cap1. `(s1-s2) < eps` -> **surface BOTH with their `concern` + surface/grain; NEVER silently argmax within the margin** (PRD §2, CTO ruling 3). Each disambiguation emits a routing regression-test case + a `tool_activity` training row (the flywheel).
3. **PRIOR-not-FILTER invariant:** `w_s·surface_prior` is ADDITIVE (a boost), NEVER a hard filter — a strong `query_match` on a non-ctx surface can still win or land within-margin (PRD §2, CTO ruling 3).
4. **Cold-start:** empty affinity -> `score = query + prior` + margin (degrades gracefully to today+prior+margin; the learned term accretes).
5. **§3-interface-first:** the engine takes `route(intent, ctx, capability_map_provider)`. NO code may assume the provider is "comp-tools" (CTO ruling 2 — any such assumption is a finding). Prove provider-agnosticism with a SMOKE-PROVIDER in acceptance.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>inspect ~E's live `tool_activity` schema (the COMPLEARN learned signal)</run>
      <expect>`tool_activity` exposes an OUTCOME dimension (not just invocation count) so `history_affinity` can be outcome-weighted per CTO ruling 4.</expect>
      <if_mismatch>STOP. If only counts exist, extend the COMPLEARN signal to carry outcome BEFORE weighting on it (a count-weighted affinity is the Goodhart failure this ruling forbids). Flag COO~B.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>grep the engine for any concrete-map / "comp-tool" / hardcoded-tool-list assumption</run>
      <expect>ZERO hits — the engine is provider-agnostic, operating only on the §3 `capability_map_provider` interface.</expect>
      <if_mismatch>STOP. Abstract the assumption behind the provider interface before commit (CTO ruling 2 — this is a finding).</if_mismatch>
    </step>
    <step>
      <run>`from __future__ import annotations`; `.tools/ds-commit-gate.sh`; non-ASCII grep</run>
      <expect>ds-commit-gate clean; zero non-ASCII; lane-portable (`org/modules/graph/`, shells to `comp-kuzu --json`).</expect>
      <if_mismatch>STOP. Do not commit until clean.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>SMOKE-PROVIDER test: slot a trivial 2nd capability-map provider (not the comp-tool map) into `route(...)` with NO engine change</run>
      <expect>The engine routes it identically (scorer + margin gate + invariants all provider-agnostic) — PRD §9c "the generalization interface is real".</expect>
      <if_mismatch>The interface leaked. Fix — this is the load-bearing systems-alpha property.</if_mismatch>
    </step>
    <step>
      <run>the 2 grounded validation cases (PRD §2): (A) comp-cluster->comp-transform within-margin; (B) comp-drift->comp-aws same-surface</run>
      <expect>(A) PRIOR narrows + MARGIN disambiguates (both surfaced with concern). (B) surface-prior EQUAL -> can't disambiguate on prior alone -> LIKELIHOOD + MARGIN(by concern) resolve -> proves prior necessary-not-sufficient.</expect>
      <if_mismatch>The scorer/margin math is wrong for a real routing case. Fix before RAVC.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 0.8.0_AE_CloudComp~C (L2): PROVIDES the `capability_map_provider` you consume. The `{id,keywords,surface,grain,concern,affinity-key}` shape + `role->surface_affinity` are the binding §3 contract — start now against a SMOKE-provider (parallel), integrate ~C's real provider at L4. Coordinate any interface-shape need with ~C before committing.
- 1.0.0_SA_CTO: PRD/arch-gate. Rulings 2 (agnostic), 3 (prior-not-filter + never-silent-argmax), 4 (Goodhart/outcome-weighted) are inviolable. RAVC the L3 build.
- 3.0.0_SA_CVO~B: verifies Goodhart-honesty (§9a) + routing-quality ground-truth (§9b, the 2 failure modes resolve) + generalization-interface-real (§9c, the smoke-provider). Your Phase-3 runs ARE the evidence CVO~B checks.
- COMPLEARN `tool_activity` is your own signal (read); COMPUNIFY map is read via ~C's provider only (never direct).
</cross_domain_coordination>

<acceptance_criteria>
1. The scorer implements `score = w_q·query_match + w_s·surface_prior + w_h·history_affinity` with `history_affinity` OUTCOME-weighted off live `tool_activity` (not count).
2. The margin-disambiguation gate never silent-argmaxes within eps (surfaces both with `concern`); PRIOR-not-FILTER holds (prior is additive, a strong query_match on a non-ctx surface can still win); cold-start degrades to query+prior+margin.
3. The engine is provider-AGNOSTIC: the smoke-provider Phase-3 run proves a 2nd capability-map provider slots in with zero engine change (PRD §9c). Grep confirms no "comp-tool" assumption (CTO ruling 2).
4. The 2 grounded failure modes (§2 A + B) resolve as specified. Session log Compiler Tools section reproduces every `<run>` + observed output + pass/fail vs `<expect>`. RAVC COO~B + CC CTO + ~C + CVO~B.
</acceptance_criteria>

## Note
DRIVE-NOW, parallel with L2. The §3 interface (PRD §3 / decomp-map) is the contract — you do NOT wait for ~C's concrete provider; build against the interface + smoke-provider, integrate the real provider at L4. Do not self-wind to "tonight" — start now.
