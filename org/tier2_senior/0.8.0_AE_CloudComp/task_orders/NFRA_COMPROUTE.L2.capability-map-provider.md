# TASK ORDER — NFRA_COMPROUTE.L2

<issued_to>0.8.0_AE_CloudComp~C</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>complete</status>  <!-- LANDED 3277cc38a (pushed CLOUD); provider comp_capability_provider.py + role_surface_affinity governor ADD; all 4 acceptance criteria met; mandate triad reproduced; RAVC'd COO~B + CC CTO/~E. ~C 2026-07-01T0345Z -->

<priority>HIGH — Andrew-direct DRIVE-NOW (2026-07-01). Stage-1 is NOT gate-lift-gated: reads the already-live COMPUNIFY map. Start now; your Phase-B derive co-sign priority-interrupt still stands (yield to the ~B-fired derive if the gate lifts mid-build, then resume).</priority>
<date>2026-07-01</date>

## Context
NFRA_COMPROUTE = the fabric's intent->capability ROUTER (the DECIDES verb). PRD: `docs/architecture/NFRA_COMPROUTE_PRD.md`. Decomp map: `org/projects/NFRA_COMPROUTE/DECOMP-MAP.md`. You are the COMPUNIFY governor, so you own the PRIOR: the capability map. L2 exposes that map as the pluggable **capability-map PROVIDER** the posterior engine (L3, ~E) consumes.

## Objective
Build the **capability-map provider** conforming to the PRD §3 interface, sourced from the LIVE COMPUNIFY map, PLUS the `role->surface_affinity` table hook (the surface_prior's context input). Registration stays YOUR governor act (PRD §5) — read-side logic is lane-portable (`org/modules/graph/`, shell to `comp-kuzu --json`), the map REGISTRATION is the governor's.

## THE INTERFACE CONTRACT (PRD §3 — binding, shared with L3/~E)
`route(intent, ctx, capability_map_provider) -> decision | disambiguation`. Your provider exposes, per capability:
`{id, keywords, surface, grain, concern, affinity-key}`
sourced from COMPUNIFY: `surfaces[]` + `tools[].surface` + `tool_grain_calibration` + the `role->surface_affinity` table. The provider is a clean interface object — L3's engine must run against it with ZERO knowledge that it is "comp-tools" (so a Stage-2 provider slots in unchanged).

## Scope — L2
1. **The provider** — expose the full comp-tool capability set from the live COMPUNIFY map as `{id, keywords, surface, grain, concern, affinity-key}` records, behind the §3 `capability_map_provider` interface. Lane-portable home (`org/modules/graph/`), shells to `comp-kuzu --json` for the map data.
2. **The `role->surface_affinity` table hook** — the context-prior input: `surface_prior(cap.surface, ctx)` reads it. If the table is absent from the current COMPUNIFY map, ADD it (governor's act) with the initial role->surface priors (seed from the DE's LD-0231 curated rules as cold-start priors, PRD §4).
3. **Registration** — register the provider + affinity table as the governor (one-home; COMPUNIFY owns the map, COMPROUTE only reads it — never edit the map from the router side, PRD §8).

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-kuzu "MATCH (t) WHERE t.node_type = 'tool' RETURN t.id, t.surface, t.grain LIMIT 5"  (or read the live COMPUNIFY map artifact ~C governs)</run>
      <expect>Every comp-tool capability carries surface + grain + a mappable concern; enumerate the full set. Confirm the map is the S4-AUDIT-GREEN vintage.</expect>
      <if_mismatch>STOP. If any §3 field ({id,keywords,surface,grain,concern,affinity-key}) is unmappable from the live map, flag COO~B BEFORE coding the provider — do not invent a field the map does not carry.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>`from __future__ import annotations` (if py); `.tools/ds-commit-gate.sh`; grep the provider for non-ASCII</run>
      <expect>ds-commit-gate clean (py_compile + ruff py39); zero non-ASCII (CloudWatch/charmap-safe); lane-portable (no AE-infra/exec-manifest ownership needed).</expect>
      <if_mismatch>STOP. Do not commit until clean.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>a smoke-consumer calls the provider -> returns the full capability set with all six §3 fields populated</run>
      <expect>Conformance: every record has {id,keywords,surface,grain,concern,affinity-key}; role->surface_affinity table present + queryable.</expect>
      <if_mismatch>Fix before RAVC. A missing field = L3's engine gets an undefined -> silent mis-route.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 0.8.0_AE_CloudComp~E (L3): CONSUMES your provider via the §3 interface. The `{id,keywords,surface,grain,concern,affinity-key}` shape + `role->surface_affinity` are the binding contract between L2 and L3 — coordinate any field-shape change with ~E BEFORE committing. ~E can start against a smoke-provider in parallel; your real provider integrates at L4.
- 1.0.0_SA_CTO: PRD/arch-gate owner. The provider interface = §3 (his ruling 2). RAVC the L2 build.
- 3.0.0_SA_CVO~B: verifies "the generalization interface is real" (§9c) — your provider + ~E's engine must let a 2nd (smoke) provider slot in unchanged.
- COMPUNIFY map = read-only from the router side (PRD §8) — never edit the map to serve the router; the affinity-table ADD is a governor registration, not a map mutation.
</cross_domain_coordination>

<acceptance_criteria>
1. The capability-map provider exposes the full comp-tool set as `{id,keywords,surface,grain,concern,affinity-key}` records behind the §3 `capability_map_provider` interface; lane-portable (`org/modules/graph/`, shells to `comp-kuzu --json`). No "comp-tool"-specific coupling leaks into the interface shape.
2. The `role->surface_affinity` table hook is present + queryable (seeded from the LD-0231 curated rules as cold-start priors); registered as the governor's act.
3. A smoke-consumer / ~E's engine calls `route(...)` against the provider and receives the full capability set (Phase-3 conformance run passes).
4. Session log Compiler Tools section reproduces every `<run>` from the mandate with observed output + pass/fail vs `<expect>`. RAVC COO~B + CC CTO + ~E (so ~E integrates against the real provider).
</acceptance_criteria>

## Note
DRIVE-NOW, not gate-held. Build against the live COMPUNIFY map (S4-AUDIT GREEN); COMPUNIFY V1 acceptance (CVO~B, on gate-lift) is ADDITIVE — if V1 surfaces any map delta, flag COO~B and I re-sequence. Do not self-wind to "tonight" — start now.
