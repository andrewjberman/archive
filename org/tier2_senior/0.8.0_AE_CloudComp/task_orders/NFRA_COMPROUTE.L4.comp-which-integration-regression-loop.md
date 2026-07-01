# TASK ORDER — NFRA_COMPROUTE.L4

<issued_to>0.8.0_AE_CloudComp~C</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>complete</status>  <!-- LANDED 442633124 (pushed CLOUD): posterior wired LIVE into comp-which as a fail-safe grep-tail backstop; regression 34/34+3/3+20/20+3/3 (ZERO rail regression); never-silent-argmax verified live; flywheel emits to comproute-routing.jsonl. All 4 acceptance criteria met; RAVC'd COO~B + CC CTO/~E/CVO~B. Ready for CVO~B COMPROUTE-V. ~C 2026-07-01T0424Z -->

<priority>HIGH — Andrew-direct close-out drive (2026-07-01). The COMPROUTE Stage-1 EXIT. L2 (your provider 3277cc38a) + L3 (~E engine 9cc595998) are landed + cross-validated (~E ran the unchanged engine against your real 49-cap provider). Integration is de-risked. Coordinate engine specifics with ~E (on-call).</priority>
<date>2026-07-01</date>

## Context
NFRA_COMPROUTE Stage-1: L1 (comp-dispatch/comp-symbols, DONE) + L2 (capability-map provider, your 3277cc38a) + L3 (posterior engine comp_route.py, ~E 9cc595998) all landed. L4 is the EXIT: put the posterior LIVE in the first surface (comp-which) + unify the routing regression test with the self-improving loop. PRD: `docs/architecture/NFRA_COMPROUTE_PRD.md` §7/§9 (Stage-1 exit) + DECOMP-MAP.md.

## Objective
Wire ~E's posterior engine (`org/modules/graph/comp_route.py`) into the `comp-which` surface as the routing decision, backed by your real capability-map provider (`comp_capability_provider.py`), and UNIFY the routing regression test with the loop (33/35 -> 34/35; each disambiguation = a new test case + a `tool_activity` training row). This makes the router LIVE on the highest-frequency junction.

## Scope — L4
1. **Integrate:** call `comp_route.route(intent, ctx, provider)` from `comp-which`, using your real COMPUNIFY provider (the 49-cap live map). comp-which becomes the first live SURFACE for the posterior (PRD §1: comp-which is the surface, COMPROUTE decides).
2. **Regression test unified with the loop:** extend the existing comp-which routing regression (PRD §7: 33/35 -> 34/35). Each margin-disambiguation the engine surfaces = a NEW regression test case + a `tool_activity` training row (the self-feeding flywheel, PRD §2). The test IS the loop.
3. **Preserve the surface invariants (LOAD-BEARING):** at the comp-which surface, PRIOR-not-FILTER + NEVER-silent-argmax must hold (within-margin -> surface BOTH candidates with `concern`, per L3). And NO-REGRESSION on comp-which's existing COMPRAIL behavior: never-dead-end + the rail telemetry (`org/mcp/comp-which-rail.log`) + the gate enforcement stay intact (comp-which is LIVE + enforcing fabric-wide -- do not break the rail).

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-which on a set of known intents (baseline) + read the existing comp-which routing regression fixtures (the 33/35 set)</run>
      <expect>Baseline captured: current route-or-run behavior on the high-traffic intents + the 12/12 non-dead-end + gold-id no-regression set (COMPRAIL TO-2). The regression fixture set located.</expect>
      <if_mismatch>STOP. If the regression fixtures aren't locatable, coordinate with ~E (who unified the disambiguation->test flywheel) before wiring.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-which on the SAME baseline intents post-integration + the routing regression suite + ds-commit-gate + non-ASCII grep</run>
      <expect>Regression 34/35 (the target improvement); ZERO regression on the existing rail behavior (never-dead-end, rail telemetry, enforcement); within-margin cases surface BOTH candidates (no silent-argmax); ds-commit-gate clean; ASCII-only.</expect>
      <if_mismatch>STOP. A rail regression (dead-end, lost telemetry, broken enforcement) or a silent-argmax is a blocker -- comp-which is LIVE fabric-wide. Fix before commit.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>the 2 grounded failure modes at the surface (comp-cluster->comp-transform within-margin; comp-drift->comp-aws same-surface) via comp-which live</run>
      <expect>(A) surfaces both with concern; (B) prior-necessary-not-sufficient resolved by likelihood+margin -- the routing improvement is real at the live surface, not just in-engine.</expect>
      <if_mismatch>Fix before RAVC. The engine passed these in-unit; a surface-level failure = an integration seam bug.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 0.8.0_AE_CloudComp~E: engine owner (comp_route.py 9cc595998). Coordinate the route() call signature + the disambiguation->tool_activity emission (the flywheel ~E built). ~E on-call for engine specifics.
- NFRA_COMPRAIL (comp-which is its enforced surface): NO-REGRESSION on never-dead-end + rail telemetry + gate enforcement. comp-which stays LIVE + enforcing.
- 1.0.0_SA_CTO: PRD/arch-gate. RAVC the Stage-1 exit.
- 3.0.0_SA_CVO~B: COMPROUTE-V acceptance (PRD §9) follows L4 -- Goodhart-honesty + routing-quality + generalization-real (§9c pre-satisfied by ~E's real-provider run) + four-way separation. Your L4 + ~E's L3 evidence feed it.
</cross_domain_coordination>

<acceptance_criteria>
1. `comp_route.route()` is LIVE in comp-which backed by the real COMPUNIFY provider; the posterior is the routing decision on the first surface.
2. Routing regression 34/35 achieved AND unified with the loop (each disambiguation emits a test case + a tool_activity row). Zero regression on comp-which's existing rail behavior (never-dead-end + telemetry + enforcement).
3. PRIOR-not-FILTER + never-silent-argmax hold at the surface; the 2 grounded failure modes resolve live.
4. Session log Compiler Tools section reproduces every `<run>` + observed output + pass/fail. RAVC COO~B + CC CTO + ~E + CVO~B -- this completes COMPROUTE Stage-1; CVO~B's COMPROUTE-V then closes it.
</acceptance_criteria>

## Note
The Stage-1 exit -- landing this + CVO~B's V closes COMPROUTE Stage-1 (Stages 2-3 = the roadmap, unblocked by the §3 interface). comp-which is LIVE + enforcing fabric-wide: the posterior AUGMENTS routing, it must NOT break the rail. Coordinate with ~E; hold your Phase-B co-sign + V1-support interrupts. Do not self-wind -- start now.
