<task_order>
<id>NFRA_VELOCITY_CORE.WS-C5.learning-loop-L2-L3</id>
<project>NFRA_VELOCITY_CORE</project>
<issued_to>0.8.0_AE_CloudComp~C</issued_to>
<issued_by>2.1.0_SA_COO</issued_by>
<status>staged</status>

<priority>P3 -- NOT YET DISPATCHABLE. Held behind a NAMED dependency. Composed now so the sequencing is
visible and no seat discovers the block by walking into it.</priority>

<gating_dependency>
**L2 AGGREGATES BOUNDARY REPORTS. AS OF 2026-07-31 THERE IS ONE APPLIED SPECIMEN.** WS-C7's N-of-M
migration is what creates the population; until it lands, L2 would be an aggregate over a sample of one.
**This TO opens when WS-C7's migration artifact reports a migrated N with the gate's denominator printed.**
An aggregate over an unprinted denominator is the exact defect this program exists to type.
</gating_dependency>

<references>
  <ref type="prd">docs/architecture/NFRA_VELOCITY_CORE_PRD.md -- WS-C5</ref>
  <ref type="upstream">infra/system/ontology/IMPLEMENTATION_LEVELS_AND_SEQUENCING.md -- L0a DONE, L0b v1.0 LIVE, L1a 4-of-N, L1b delivered; the >=3-sensors-mixed-shapes prerequisite for L2 is MET. The five banked L2 design inputs live here.</ref>
  <ref type="upstream">WS-C7 boundary-declaration schema v2 (0.7.0_AE_CloudOps~Z) -- L2's input contract</ref>
  <ref type="fence">org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml -- dynamic_rails.held_out_fence (binds you)</ref>
</references>

<objective>
Close the loop: build the fleet aggregate, then formalize the inference gate as a BLOCKING site.

**FIRST ARTIFACT -- the only thing the eventual GO authorizes:**

  **L2, THE FLEET AGGREGATE.** Collect the boundary reports produced by WS-C7's migration, rank them, and
  declare applicability denominators, so *"where is our model short?"* becomes one answerable question.
  Consume the five banked design inputs from the levels doc; do not re-derive them.

L3 (the inference gate) and version-head generalization are artifacts 2 and 3, NOT authorized by the
first GO.

**THE BAR IS NOT "L2 RENDERS." It is that L2 renders WITH DENOMINATORS.** An aggregate that ranks without
stating what it ranked over is a leaderboard, not a measurement -- the config-is-its-own-denominator
failure reproduced inside the instrument built to detect it.
</objective>

<constraints>
1. **ONE ARTIFACT. Report and stop.**
2. **NO SILENT DENOMINATOR.** Every rank, ratio and "top" carries the population it was computed over and
   the instrument that produced that population.
3. **L3 IS A BLOCKING SITE, NOT A NOTE -- and not built under artifact 1.** When you do: every inference
   event terminates in (a traversal that walks the new axis + a predicate that MOVES under the change-type
   + a version pin + a mutant proving the predicate can redden), or the loop dies at that axis. Route C
   escalates as a blocking item. **The loop never guesses past its own boundary.**
4. **DO NOT stand up any lifecycle-VALUE-population work** -- Andrew-direct 2026-07-31 ~1400Z; values are
   GATED pending the Kimi user-input pipeline (`0.7.0_AE_CloudOps~B` named future owner). The MECHANISM is
   in scope; populating values is not.
5. **HELD-OUT FENCE BINDS.** Publish your shaping corpus.
6. **NO NON-ASCII. No emojis.**
</constraints>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Enumerate the live boundary-report population from WS-C7's migration, citing the gate</run>
      <expect>A gate-maintained N with M printed. If N is small, SAY SO in the artifact -- a small-N aggregate is publishable; an unlabelled small-N aggregate is not.</expect>
      <if_mismatch>If the migration has not landed, this TO is not open. Return it to COO/CTO~Z.</if_mismatch>
    </step>
    <step>
      <run>Read the five banked L2 design inputs at a pinned commit</run>
      <expect>Five, consumed as given, each cited with a commit-ish. A line citation without a vintage is not a citation.</expect>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/commit-gate.sh on every .py touched</run>
      <expect>Clean. Gold/silver/bronze .py additionally begins `from __future__ import annotations`.</expect>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>MUTANT the aggregate: feed it a boundary report you know is short, confirm the rank MOVES</run>
      <expect>The ranking changes. Per L-16, an exercised aggregate is not a discriminating one -- an aggregate whose output does not move under a changed input has never been tested.</expect>
      <if_mismatch>Fix the aggregate. A passing assertion never mutated has never been tested.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. L2 renders the fleet aggregate with an applicability denominator on EVERY figure.
2. The five banked design inputs are consumed and cited to the levels doc at a pinned commit.
3. The aggregate is MUTANT-TESTED: a deliberately short boundary report changes its rank, shown.
4. The boundary-report population N is cited to the gate that maintains it, with M printed.
5. Shaping corpus published; held-out fence demonstrably unbreached.
6. Session log with a Compiler Tools section reproducing each run vs expect.
7. Report to CTO~Z on land WITH the commit hash. CTO~Z gates; CVO~Z verifies after that gate.

**DEFERRED to artifacts 2-3, explicitly NOT in this TO's acceptance:** one full C-route cycle exercised
end-to-end (residue -> inference -> new determinism -> head advance -> autonomous re-cover); LIVELEARN's
bar folded (fresh-when-consumed; the loop provably closes over >=2 cycles); version-head pinning
generalized beyond the rule bank.
</acceptance_criteria>

<cross_domain_coordination>
- **WS-C7 (`0.7.0_AE_CloudOps~Z`) produces this TO's input.** Its schema shape is L2's input contract; a
  late schema change is an L2 rework. Coordinate before either side freezes.
- **WS-C9 (P5) consumes L3.** A genuinely new mechanism class is a Route-C event entering through THIS
  workstream's inference gate. Do not build a second, private classification path in C5.
- **Version-head generalization (artifact 3) touches the rule-bank head and any governed registry** --
  ratified-vocabulary territory. Route to CTO~Z; do not amend a head unilaterally.
</cross_domain_coordination>

<notes>
**WHY THIS IS COMPOSED BEFORE IT IS DISPATCHABLE.** The sequencing finding is that P3 is NOT simply "next
after P2" -- it is downstream of a specific WS-C7 artifact. Composing it now puts that dependency on the
record instead of leaving it to be discovered when a seat goes looking for work.
</notes>
</task_order>
