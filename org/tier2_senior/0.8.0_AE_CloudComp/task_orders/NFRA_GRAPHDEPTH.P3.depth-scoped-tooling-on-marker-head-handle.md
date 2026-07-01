# TASK ORDER — NFRA_GRAPHDEPTH.P3 (depth-scoped tooling)

<issued_to>0.8.0_AE_CloudComp~C</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>pending</status>
<priority>HIGH — Andrew-direct 2026-07-01: "GRAPHUNI and GRAPHDEPTH need to be finished." The LAST GRAPHDEPTH phase. UNBLOCKED: P1 (populate) done (Phase-B derive, CVO~B L3 GREEN 5fc0bce73); P2 (calibration = COMPUNIFY S4 grain_contract) done; ~D's marker-head read-handle (comp_marker_read.py dfad285bf) is BUILT + you grain-co-verified it GREEN (all 4 governor conditions, D4 one-head works). You're the grain governor -- natural owner.</priority>
<date>2026-07-01</date>

## Context
NFRA_GRAPHDEPTH: every investigation needs TWO coordinates -- BREADTH (where on the surface) + DEPTH (what grain). PRD: `docs/architecture/NFRA_GRAPHDEPTH_PRD.md` (§9, 5 rulings). Map: `org/projects/NFRA_GRAPHUNI/SUBSTRATE-CLOSEOUT-MAP.md`. The substrate is populated + depth-typed (declared `level` on a stable CONTAINS ladder: Pipeline>Script>Function, Bucket>Key; EC2-RUNS-Script). P3 = make tools SCOPE by that depth. Your grain co-verify (GREEN on comp_marker_read.py: .grains from node_type_grain 52/52, drill/rollup directions, .level=None for 1442 resources, rollup_defects delegation) confirms the composition works -- P3 exposes it as a usable capability.

## Objective
Expose DEPTH-SCOPED querying on the marker-head read-handle (comp_marker_read.py): scope an investigation to a declared `level` on the CONTAINS ladder (resource-grain vs function-grain vs pipeline-grain), calibrated by the grain_contract you govern. Tools can ask "the function-grain subgraph of X" or "roll X up to resource-grain." This is the DEPTH coordinate that composes with BREADTH (GRAPHUNI/COMPUNIFY).

## Scope — P3 (5 CTO rulings, PRD §9)
1. **Depth-scoped read surface** on comp_marker_read.py: level-scoped queries (drill to a finer grain / rollup to a coarser grain on the CONTAINS ladder), grain-calibrated via the grain_contract (node_type_grain + drilldown_seams + strata). Size-invariant: ONE type-system + toolset serves every grain (declared `level`, never a type fork).
2. **Fold the refinement you flagged to ~D**: derive the drilldown edge-type set from `grain_contract.drilldown_seams` (NOT hardcoded) -- so a future 4th stratum-stitcher doesn't drift. Coordinate with ~D (handle owner) -- fold before/with the re-point, per your flag.
3. **Compose with GRAPHUNI P2**: the depth-scoping reads through the SAME marker-head handle the re-pointed tools use (one-head; provenance current). Coordinate the read-API shape with ~D so depth + breadth compose on one surface.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>re-confirm your grain co-verify on comp_marker_read.py (dfad285bf) + read grain_contract.drilldown_seams + strata (the depth calibration source)</run>
      <expect>The 4 governor conditions hold (grains/drill-rollup/level/rollup_defects); drilldown_seams is the authoritative edge-type source (not a hardcode). Marker provenance current (5434137157015633165).</expect>
      <if_mismatch>STOP. If the grain_contract drift-source is ambiguous, resolve it (you govern it) before building the scoping on top.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>depth-scoped query self-test (drill EC2->function-grain; rollup function->resource-grain) + drilldown-seams-derived (not hardcoded) check + ds-commit-gate + non-ASCII</run>
      <expect>Level-scoped queries return the correct grain subset/rollup (resource-grain vs function-grain distinct + correct); drilldown edge-types derived from grain_contract; ds-gate clean.</expect>
      <if_mismatch>STOP. A wrong-grain result or a hardcoded seam-set is the defect this closes.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>a real depth-scoped investigation end-to-end (scope a Lambda's blast radius to function-grain vs resource-grain) on the live marker head</run>
      <expect>Depth-scoping is usable + composes with breadth on the one marker head; provenance current; size-invariant (same toolset, declared level).</expect>
      <if_mismatch>Fix before RAVC. Depth-scoping that doesn't compose with the unified head = incomplete.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 0.8.0_AE_CloudComp~D: owns comp_marker_read.py (the handle) + GRAPHUNI P2 re-point. Coordinate the read-API shape so depth + breadth compose on ONE head; fold the drilldown_seams-derivation refinement with the re-point.
- 3.0.0_SA_CVO~B: certifies the depth-scoped tooling (correct grain, size-invariant, on the marker head). GRAPHDEPTH close-verify.
- 1.0.0_SA_CTO: PRD §9 rulings (depth-first-class / type-set-grows-by-semantic-not-depth / size-invariant-bounded-materialization / type-specific-drilldown-depth). RAVC.
- NFRA_GRAPHUNI: GRAPHDEPTH P3 + GRAPHUNI P2/P3 close TOGETHER (the unified depth+breadth substrate).
</cross_domain_coordination>

<acceptance_criteria>
1. Depth-scoped querying live on comp_marker_read.py: level-scoped drill/rollup on the CONTAINS ladder, grain-calibrated via grain_contract (drilldown edge-types DERIVED from drilldown_seams, not hardcoded); size-invariant.
2. Composes with GRAPHUNI P2's breadth on ONE marker head (provenance current); a real depth-scoped investigation works end-to-end.
3. Session log Compiler Tools section reproduces every run. RAVC COO~B + CC CTO + ~D + CVO~B -- CVO~B's cert + GRAPHUNI P2/P3 close GRAPHDEPTH + GRAPHUNI together.
</acceptance_criteria>

## Note
The final GRAPHDEPTH phase. Builds on the handle you already grain-verified GREEN (no re-derive). Coordinate tightly with ~D (handle + re-point) so depth composes with breadth on the one head. On this + GRAPHUNI P2/P3 + CVO~B GREEN, both close -- the last two of the NFRA_COMP*/GRAPH* group.
